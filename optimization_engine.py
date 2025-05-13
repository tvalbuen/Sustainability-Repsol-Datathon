import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def datathon_optimization_co2(S: np.array, C: np.array, CO2: np.array, max_battery_capacity=100):


    assert len(S) == len(C), 'Solar Generation and Consumption must be of the same length'
    assert len(S) == len(CO2), 'Solar Generation and CO2 must be of the same length'

    N = len(S)
    x_bounds = [(-100, 100)] * N
    surplus = np.maximum(0, S - C)
    x0 = np.sqrt(surplus)
    x0[-1] = -x0.max()

    print(f'The Naive Guess for this iteration is', x0)

    const=[]

    def objective(x):
        co2_unspent = 0
        for t in range(N):
            if x[t] < 0:
                co2_unspent = co2_unspent + (CO2[t] * x[t])
                
        return co2_unspent
    
    def surplus_constraint(x):
    # The charge amount must be smaller or equal than the surplus, if there is no surplus not greater than 0.   
        G = []
        for t in range(N):
            surplus = max(S[t] - C[t], 0)
            G.append( surplus - x[t] )
        return np.array(G)

    surplus_cons = {
        'type': 'ineq',
        'fun': surplus_constraint
    } 

    const.append(surplus_cons)

    def soc_constraint(x): 
        # State of Charge (soc) must be always greater or equal than 0, and can't be greater than the max battery capacity (100kwh) 
        soc = np.cumsum(x)  # SoC at each hour, assuming SoC starts at 0 for t=0
        G = []
        for t in range(N):
            G.append( soc[t] )
            G.append( max_battery_capacity - soc[t] )
        
        return np.array(G)
    
    soc_cons = {
        'type': 'ineq',
        'fun': soc_constraint
        }  
    
    const.append(soc_cons)

    def cycle_constraint(x):
        # Can't charge more than 100 kWh per day
        positive_x = np.array([i for i in x if i > 0 ])
        return 100 - np.sum(positive_x)

    cycle_cons = {
        'type': 'ineq',
        'fun': cycle_constraint
    }

    const.append(cycle_cons)

    print(const)

    solution = minimize(
        fun=objective,
        x0=x0,
        method='SLSQP',
        bounds=x_bounds,
        constraints=const,
        options={'maxiter': 1000, 'disp': True}
    )
    return solution

if __name__ == "__main__":
    S = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.84, 10.5, 33.45, 74.84, 100.45, 122.96, 125.41, 121.28, 85.13, 52.41, 61.22, 36.73, 12.54, 1.21, 0, 0])
    C = np.array([110.8558884, 107.3412018, 105.5503082, 106.8401031, 05.8797913, 106.0003967, 105.4976807, 101.1223373, 
        97.6912384, 64.41342926, 43.48149872, 40.48365021, 55.5661087, 47.57512665, 41.42887115, 47.5853653, 
        54.39416885, 55.62261963, 9.58168602, 26.94274521, 53.62102509, 73.34294128, 106.4267731,104.5549622
        ])
    
    CO2 = np.array([158.77, 164.81, 170.04, 175.13, 175.53, 174.22, 175.05, 170.19,
                     159.95, 123.35, 81.8, 66.29, 57.99, 55.83, 48.66, 47.05, 
                     47.9, 54.81, 68.23, 111.68, 154.65, 175, 175.76, 168.76])
    
    solution = datathon_optimization_co2(S=S, C=C, CO2=CO2)
    # The result
    print("Success:", solution.success)
    print("Objective (negative of solar used) =", solution.fun)
    print("x =", np.round(solution.x, decimals=4))  # first 50 hours to see a snippet
    type(solution.x)
    plt.plot(np.round(solution.x, decimals=4))

