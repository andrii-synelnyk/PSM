import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants for pendulum motion
l = 1.0  # length of the pendulum (m) (Changed 'r' to 'l' to match the Excel template)
g = 9.81  # acceleration due to gravity (m/s^2)
a = 1  # initial angle (radians) (Changed 'alpha0' to 'a')
w = 0.0  # initial angular velocity (rad/s) (Changed 'omega0' to 'w')
dt = 0.01  # time step (s)
duration = 10  # duration of simulation (s)
m = 1  # mass


def improved_euler_method(a, w, dt, l, g):
    results = [(0, a, w, 0, 0, 0)]
    time = 0
    while time < duration:
        k1a = w
        k1w = -g / l * np.sin(a)

        a_mid = a + k1a * dt / 2
        w_mid = w + k1w * dt / 2

        k2a = w_mid
        k2w = -g / l * np.sin(a_mid)

        a += k2a * dt
        w += k2w * dt

        PE, KE, TE = calculate_energies(a, w, l, m, g)
        results.append((time, a, w, PE, KE, TE))
        time += dt
    return results



def rk4_method(a, w, dt, l, g):
    results = [(0, a, w, 0, 0, 0)]
    time = 0
    while time < duration:
        k1a = w
        k1w = -g / l * np.sin(a)

        a2 = a + k1a * dt / 2
        w2 = w + k1w * dt / 2
        k2a = w2
        k2w = -g / l * np.sin(a2)

        a3 = a + k2a * dt / 2
        w3 = w + k2w * dt / 2
        k3a = w3
        k3w = -g / l * np.sin(a3)

        a4 = a + k3a * dt
        w4 = w + k3w * dt
        k4a = w4
        k4w = -g / l * np.sin(a4)

        a += (k1a + 2*k2a + 2*k3a + k4a) / 6 * dt
        w += (k1w + 2*k2w + 2*k3w + k4w) / 6 * dt

        PE, KE, TE = calculate_energies(a, w, l, m, g)
        results.append((time, a, w, PE, KE, TE))
        time += dt
    return results


# Energy calculations
def calculate_energies(a, w, l, m, g):
    h = l * (1 - np.cos(a))
    V = l * w
    PE = m * g * h  # Potential energy =ABS(mass*g*L5)
    KE = 0.5 * m * V**2  # Kinetic energy =mass*M5^2/2
    TE = PE + KE  # Total energy
    return PE, KE, TE


# Running the simulations
euler_results = improved_euler_method(a, w, dt, l, g)
rk4_results = rk4_method(a, w, dt, l, g)

# Convert results to DataFrame for easy handling, adjusting the column names to match the Excel templates
euler_df = pd.DataFrame(euler_results, columns=['time', 'a', 'w', 'PE', 'KE', 'TE'])
rk4_df = pd.DataFrame(rk4_results, columns=['time', 'a', 'w', 'PE', 'KE', 'TE'])

# Display the DataFrame
print("Improved Euler's Method")
print(euler_df.head())
print("\nRK4 Method")
print(rk4_df.head())

# Plotting Improved Euler Method
plt.figure(figsize=(12, 6))
plt.plot(euler_df['time'], euler_df['PE'], label='Potential Energy')
plt.plot(euler_df['time'], euler_df['KE'], label='Kinetic Energy')
plt.plot(euler_df['time'], euler_df['TE'], label='Total Energy')
plt.xlabel('Time (s)')
plt.ylabel('Energy (Joules)')
plt.title('Energy vs Time for Improved Euler Method')
plt.legend()
plt.grid(True)
plt.show()

# Plotting RK4 Method
plt.figure(figsize=(12, 6))
plt.plot(rk4_df['time'], rk4_df['PE'], label='Potential Energy')
plt.plot(rk4_df['time'], rk4_df['KE'], label='Kinetic Energy')
plt.plot(rk4_df['time'], rk4_df['TE'], label='Total Energy')
plt.xlabel('Time (s)')
plt.ylabel('Energy (Joules)')
plt.title('Energy vs Time for RK4 Method')
plt.legend()
plt.grid(True)
plt.show()

