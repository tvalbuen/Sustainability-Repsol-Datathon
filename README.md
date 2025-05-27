# ⚡ Solar Optimization for CO₂ Emission Reduction in Industrial Plants

## 🏆 Project: Repsol – IE Sustainability Challenge (6th Edition)

This repository contains our solution to the **IE Sustainability Datathon 2025**, focused on optimizing the energy usage of an industrial plant through **solar energy generation modeling**, **battery storage optimization**, and **CO₂ emission impact analysis**.

---

## 🧠 Problem Statement

In Spain’s energy transition, integrating intermittent renewable energy into industrial systems is a critical challenge. The datathon simulates a real-world industrial facility with a 175kWp solar installation (no grid feed-in) and evaluates:

1. The **maximum potential solar generation**.
2. **Battery charge/discharge optimization** for maximizing solar use.
3. **Quantification of CO₂ emissions avoided** by optimized energy use.

---

## 🎯 Objectives

### ✅ Objective 1: Solar Generation Potential
- Forecast the **maximum possible solar generation** (kWh) in September 2024 using historical weather data.
- Compare with actual plant usage to calculate **underutilized solar energy**.

### ✅ Objective 2: Battery Optimization
- Simulate a 100 kWh battery with 100 kW max power, allowing **one full charge/discharge cycle per day**.
- Maximize **Ra (Self-Consumption Ratio)** to increase energy efficiency and grid independence.

### ✅ Objective 3: Environmental Impact
- Use Spanish electricity mix data to calculate hourly **CO₂ intensity**.
- Optimize battery discharge during high-emission hours to **maximize CO₂ avoided**.

---

## 🛠️ Technologies & Tools

| Tool / Library         | Description                                          |
|------------------------|------------------------------------------------------|
| `Python`               | Programming language                                 |
| `Pandas`, `NumPy`      | Data manipulation and numerical computing            |
| `SciPy (SLSQP)`        | Constrained optimization for battery usage           |
| `Matplotlib`           | Visualization of battery and emissions behavior      |
| `CSV`                  | Weather, solar, and grid data inputs                 |

---

## 📂 Repository Structure

- Final_Notebook_V3.ipynb # Final solution notebook with methodology & results
- optimizer_sept_CO2_vf.py # Battery optimization maximizing CO₂ avoided
- optimizer_sept_Ra_CO2.py # Battery optimization maximizing Ra (self-consumption)
- README.md # Project documentation
- /processed # Contains input CSVs (solar predictions, consumption)
- /raw # Carbon intensity datasets

---

## 📊 Key Metrics

| Metric                         | Description                                         |
|-------------------------------|-----------------------------------------------------|
| `MAE`                         | Forecast error of solar generation (Objective 1)    |
| `Underutilization (kWh)`      | Solar energy that could have been used but wasn't   |
| `Ra (%)`                      | Self-consumption ratio: used/generated energy       |
| `CO₂ev (gCO₂ eq)`             | Emissions avoided via battery optimization          |

---

## 📈 Optimization Highlights

- **Energy Forecasting**: Boosted model trained to estimate solar generation using historical weather patterns.
- **Battery Strategy**: Constrained optimization of battery cycles ensures:
  - No grid interaction
  - Discharge during peak CO₂ hours
  - Compliance with daily energy limits
- **Impact**:
  - Improved Ra (self-consumption) efficiency
  - Quantified reduction of carbon footprint (gCO₂ eq)

---

## 🌍 Business Value

- Demonstrates how renewable energy can be efficiently integrated into industrial operations.
- Helps industrial stakeholders **minimize grid reliance**, **reduce emissions**, and **maximize ROI** on solar installations.
- Scalable framework for any factory setup with PV and battery storage systems.

---

## 📢 Team Notes

This project was submitted for evaluation under the **IE Sustainability Challenge 2025**. The code is modularized into separate scripts for reproducibility, and the notebook contains detailed analysis and plots to communicate insights clearly.

---

## 📬 Contact

For inquiries or collaboration opportunities, please reach out via GitHub or LinkedIn.

---

## 📝 License

This project is for educational and non-commercial use only under the IE Sustainability Datathon guidelines.

