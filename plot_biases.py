import numpy as np
from scipy.interpolate import interp1d, UnivariateSpline
import matplotlib.pyplot as plt


def get_temperature_voltage_data():
    file_name = "data\Temperature_Sensor_Voltage_Temperature_dependence.txt"
    with open(file_name) as f:
        lines = f.readlines()
        V = []
        T = []
        lines = [line for line in lines if line.strip()]
        for i, line in enumerate(lines):
            if i > 0:
                if line[0] != ",":
                    values = line.split(",")
                    if float(values[0]) > 0:
                        T.append(float(values[0]))
                        V.append(float(values[1]))
        return np.array(V), np.array(T)


def get_vcal_vs_v_data():
    file_name = "data\VuncalVcal.txt"
    with open(file_name) as f:
        lines = f.readlines()
        V_cal = []
        V = []
        lines = [line for line in lines if line.strip()]
        for i, line in enumerate(lines):
            if i > 0:
                line = line.strip()
                values = line.split()
                V_cal.append(float(values[0]))
                V.append(float(values[1]))
        return np.array(V_cal), np.array(V)


def get_Tshown_Vuncal_data():
    filename = "data\T_shown_V_uncal.txt"
    with open(filename) as f:
        lines = f.readlines()
        T = []
        V = []
        lines = [line for line in lines if line.strip()]
        for i, line in enumerate(lines):
            values = line.split()
            T.append(float(values[0]))
            V.append(float(values[1]))
    return np.array(T), np.array(V)


calibrated_voltage, temperature = get_temperature_voltage_data()
T_wanted_V_cal = interp1d(temperature, calibrated_voltage)

V_cal, V_uncal = get_vcal_vs_v_data()
V_cal_V_uncal = UnivariateSpline(V_cal, V_uncal, s=0.0001)
T_shown, Vcal = get_Tshown_Vuncal_data()
Vinput = V_cal_V_uncal(Vcal)
T_shown_Vinput = UnivariateSpline(Vinput[::-1], T_shown[::-1], s=0.01)
x_smooth = np.linspace(Vinput.min(), Vinput.max(), 1000)
y_smooth = T_shown_Vinput(x_smooth)
plt.plot(x_smooth, y_smooth)
plt.scatter(Vinput, T_shown)
plt.show()
temperatures = np.linspace(12, 300, 293)

Vcal_attained = T_wanted_V_cal(temperatures)
T_shown_calibrated = T_shown_Vinput(Vcal_attained)
bias_calibrated = T_shown_calibrated - temperatures
V_uncal_attained = V_cal_V_uncal(Vcal_attained)
T_shown_uncalibrated = T_shown_Vinput(V_uncal_attained)
bias_uncalibrated = T_shown_uncalibrated - temperatures

plt.plot(temperatures, bias_calibrated, label="Calibrated bias")
plt.plot(temperatures, bias_uncalibrated, label="Uncalibrated bias")
plt.xlabel("Temperature (K)")
plt.ylabel("Bias (K)")
plt.xticks(np.arange(12, 301, 10))  # Smaller increments along x-axis
plt.legend()
plt.grid(True)  # Add grid
plt.show()
