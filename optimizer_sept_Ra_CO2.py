import pandas as pd
import numpy as np
from scipy.optimize import minimize

def run_optimization():
    # --- Load full September data ---
    max_generation = pd.read_csv('processed/boosting_predictions2.csv')
    sept_consumption = pd.read_csv('processed/Consumo_sept.csv')

    # Get values and datetime
    S_all = np.array(max_generation['KWH_ENERGIA'])
    C_all = np.array(sept_consumption['TOTAL_KWH_ENERGIA'])
    datetime_all = pd.to_datetime(max_generation['Datetime'])

    hours_per_day = 24
    assert len(S_all) == len(C_all) == len(datetime_all)
    N = len(S_all)
    assert N % hours_per_day == 0

    days = N // hours_per_day
    max_battery_capacity = 100
    max_power = 100

    all_results = []

    for d in range(days):
        print(f"\nOptimizing day {d + 1}/{days}")
        start = d * hours_per_day
        end = (d + 1) * hours_per_day
        S = S_all[start:end]
        C = C_all[start:end]
        timestamps = datetime_all[start:end]

        surplus = np.maximum(S - C, 0)
        unmet_demand = np.maximum(C - S, 0)

        def objective(x):
            discharge = x[24:]
            return -np.sum(discharge)  # Maximize discharge (solar used later)

        def surplus_constraint(x):
            charge = x[:24]
            return surplus - charge

        def demand_constraint(x):
            discharge = x[24:]
            return unmet_demand - discharge

        def power_constraints(x):
            charge = x[:24]
            discharge = x[24:]
            return np.concatenate([
                max_power - charge,
                max_power - discharge
            ])

        def soc_constraints(x):
            charge = x[:24]
            discharge = x[24:]
            soc = np.zeros(24)
            soc[0] = charge[0] - discharge[0]
            for t in range(1, 24):
                soc[t] = soc[t-1] + charge[t] - discharge[t]
            return np.concatenate([
                soc,  # soc >= 0
                max_battery_capacity - soc  # soc <= capacity
            ])

        def daily_cycle_limit(x):
            charge = x[:24]
            discharge = x[24:]
            return [100 - np.sum(charge), 100 - np.sum(discharge)]

        constraints = [
            {'type': 'ineq', 'fun': surplus_constraint},
            {'type': 'ineq', 'fun': demand_constraint},
            {'type': 'ineq', 'fun': power_constraints},
            {'type': 'ineq', 'fun': soc_constraints},
            {'type': 'ineq', 'fun': daily_cycle_limit}
        ]

        x0 = np.zeros(48)
        x_bounds = [(0, max_power)] * 48

        solution = minimize(
            fun=objective,
            x0=x0,
            method='SLSQP',
            bounds=x_bounds,
            constraints=constraints,
            options={'maxiter': 1000, 'disp': False}
        )

        if not solution.success:
            print(f"⚠️ Day {d + 1} optimization failed:", solution.message)
            charge = [0.0] * 24
            discharge = [0.0] * 24
        else:
            charge = solution.x[:24]
            discharge = solution.x[24:]

        daily_df = pd.DataFrame({
            'Datetime': timestamps,
            'KWH_ENERGIA': S,
            'consumption': C,
            'battery_charge': charge,
            'battery_discharge': discharge,
            'surplus': surplus,
            'unmet_demand': unmet_demand,
            'day': d + 1
        })
        all_results.append(daily_df)

    final_df = pd.concat(all_results, ignore_index=True)
    

    # Load CO₂ intensity file
    co2_data = pd.read_csv("raw/ES_2024_hourly.csv")

    # Rename column for easier handling
    co2_data.rename(columns={"Datetime (UTC)": "Datetime_UTC"}, inplace=True)

    # Convert to datetime and localize as UTC
    co2_data["Datetime_UTC"] = pd.to_datetime(co2_data["Datetime_UTC"])
    co2_data["Datetime"] = co2_data["Datetime_UTC"].dt.tz_localize("UTC").dt.tz_convert("Europe/Madrid")

    # Drop the UTC version if you want
    co2_data.drop(columns=["Datetime_UTC"], inplace=True)
    final_df = final_df.merge(co2_data[['Datetime', 'Carbon Intensity gCO₂eq/kWh (LCA)']], on='Datetime', how='left')


    #Calculate avoided CO2
    final_df['grid_baseline'] = np.maximum(final_df['consumption'] - final_df['KWH_ENERGIA'], 0)
    final_df['grid_optimized'] = np.maximum(final_df['grid_baseline'] - final_df['battery_discharge'], 0)

    final_df['CO2_emitted'] = final_df['grid_baseline'] * final_df['Carbon Intensity gCO₂eq/kWh (LCA)']
    final_df['CO2_optimized'] = final_df['grid_optimized'] * final_df['Carbon Intensity gCO₂eq/kWh (LCA)']
    final_df['CO2_Avoided'] = final_df['CO2_emitted'] - final_df['CO2_optimized']

    co2_output = final_df[['Datetime', 'CO2_Avoided']]
    co2_output.to_csv('co2_avoided_max_Ra.csv', index=False)

    total_CO2_ev = co2_output['CO2_Avoided'].sum()
    
    print("\n✅ Optimization complete. Results saved to 'co2_avoided_max_Ra.csv'.")
    print(f"\n🌍 Total CO₂ emissions avoided: {total_CO2_ev:.4f} gCO₂ eq")

    
    # --- Ra Calculation ---
    direct_use = np.minimum(final_df['KWH_ENERGIA'], final_df['consumption']).sum()
    battery_use = final_df['battery_discharge'].sum()
    potential_solar = final_df['KWH_ENERGIA'].sum()

    Ra = (direct_use + battery_use) / potential_solar * 100

    print(f"\n🌞 Ra (Self-Consumption Ratio): {Ra:.4f}%")
        
    

if __name__ == "__main__":
    run_optimization()
