import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
m = 1.0   # mass (kg)
g = -9.81  # gravity (m/s^2)
k = 0.5  # drag coefficient
dt = 0.1  # time step (s)
duration = 5  # duration of simulation (s)

# Initial conditions
v0 = 20.0  # initial velocity (m/s)
angle = 45.0  # launch angle (degrees)

v0x = v0 * np.cos(np.radians(angle))  # initial horizontal velocity
v0y = v0 * np.sin(np.radians(angle))  # initial vertical velocity
s0 = np.array([0, 0])  # initial position (x, y)

time = 0


def euler_method(v0x, v0y, s0, dt, time, k, m, g):
    vx, vy = v0x, v0y
    sx, sy = s0
    results = [(0, s0[0], s0[1], v0x, v0y, 0, 0, -k*v0x, m*g-k*v0y, -k*v0x/m, (m*g-k*v0y)/m, 0, 0)]  # Initial conditions
    while time < duration:
        # Calculate the drag force in both x and y directions
        Fx = -k * vx
        Fy = m * g - k * vy

        # Compute the acceleration in both x and y directions
        ax = Fx / m
        ay = Fy / m

        # Calculate change in velocity for both x and y directions
        DVx = ax * dt
        DVy = ay * dt

        # Calculate change in position for both x and y directions
        DSx = vx * dt
        DSy = vy * dt

        # Update position and velocities for the next iteration
        sx += DSx
        sy += DSy
        vx += DVx
        vy += DVy

        results.append((time, sx, sy, vx, vy, DSx, DSy, Fx, Fy, ax, ay, DVx, DVy))
        time += dt
        if sy < 0:
            break
    return results


def midpoint_method(v0x, v0y, s0, dt, time, k, m, g):
    vx, vy = v0x, v0y
    sx, sy = s0
    results = [(0, s0[0], s0[1], v0x, v0y, 0, 0, -k * v0x, m * g - k * v0y, -k * v0x / m, (m * g - k * v0y) / m, 0, 0)]  # Initial conditions
    while time < duration:
        # Initial Euler step to estimate midpoint velocity
        Fx = -k * vx
        Fy = m * g - k * vy
        ax = Fx / m
        ay = Fy / m
        mid_vx = vx + ax * dt / 2
        mid_vy = vy + ay * dt / 2

        # Calculate forces, accelerations, and deltas at the midpoint
        mid_Fx = -k * mid_vx
        mid_Fy = m * g - k * mid_vy
        mid_ax = mid_Fx / m
        mid_ay = mid_Fy / m
        DVx = mid_ax * dt
        DVy = mid_ay * dt
        DSx = mid_vx * dt
        DSy = mid_vy * dt

        # Update position and velocity using midpoint values
        sx += DSx
        sy += DSy
        vx += DVx
        vy += DVy

        results.append((time, sx, sy, vx, vy, DSx, DSy, mid_Fx, mid_Fy, mid_ax, mid_ay, DVx, DVy))
        time += dt
        if sy < 0:
            break
    return results


# Perform the simulations
simulation_results = euler_method(v0x, v0y, s0, dt, time, k, m, g)
midpoint_simulation_results = midpoint_method(v0x, v0y, s0, dt, time, k, m, g)

# Convert results to a structured format
simulation_df = pd.DataFrame(simulation_results, columns=['t', 'Sx', 'Sy', 'Vx', 'Vy', 'DSx', 'DSy', 'Fx', 'Fy', 'ax', 'ay', 'DVx', 'DVy'])
midpoint_simulation_df = pd.DataFrame(midpoint_simulation_results, columns=['t', 'Sx', 'Sy', 'Vx', 'Vy', 'DSx', 'DSy', 'Fx', 'Fy', 'ax', 'ay', 'DVx', 'DVy'])

# Display the DataFrame
print("Euler's Method")
print(simulation_df)
print("\n")
print("Midpoint Method")
print(midpoint_simulation_df)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(simulation_df['Sx'], simulation_df['Sy'], label='Euler Method', marker='o')
plt.plot(midpoint_simulation_df['Sx'], midpoint_simulation_df['Sy'], label='Midpoint Method', marker='x')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion Simulation')
plt.legend()
plt.grid(True)
plt.show()
