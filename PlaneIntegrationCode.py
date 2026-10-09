## This file will consolidate all exercises from Chapter 5
## of Computational Physics into this program.
## This section here is for Python Implementation.

## Importations:
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

## Step 2: Start by writing some code to compute the position at any time
## assuming v_t=54.0  m⁄s, i.e. have it calculate the integral of
## ∫_h^x dx=-v_t∫_h^x ((1-e^((-2gt)⁄v_t ))/(1+e^((-2gt)⁄v_t ) ))dt
## -> x = h-v_t ∫_0^t ((1-e^((-2gt)⁄v_t ))/(1+e^((-2gt)⁄v_t)))dt
## So, our integral gives us the distance that we have fallen
## which we then subtract from the initial height. If you assume
## an initial height of 1400 m, you should find that it takes
## about 29.74519 seconds to reach the ground (x = 0.0001225)
## assuming that no parachute is opened. Use this to check that
## your code is working at this point meaning that you have entered
## the equation properly and have it properly evaluating the integral.
## For the integration, I’d recommend using a library function.

# Constants
G = 9.8         # Acceleration due to gravity (m/s^2)
VT = 54.0       # Terminal velocity (m/s)

def integrand(t):
    """The velocity equation to be integrated."""
    return (1 - np.exp(-2 * G * t / VT)) / (1 + np.exp(-2 * G * t / VT))

def get_position(t, h_initial):
    """Calculates the position x at time t given an initial height."""
    # quad returns a tuple: (integral value, absolute error estimate)
    integral, _ = quad(integrand, 0, t)
    return h_initial - VT * integral

# --- Step 1: Validation Check ---
h_val = 1400.0
t_val = 29.74519
x_val = get_position(t_val, h_val)
print("--- Validation Check ---")
print(f"At t = {t_val} s, position x = {x_val:.7f} m")
print(f"Target x was approx 0.0001225 m. Diff: {abs(x_val - 0.0001225):.7f} m\n")

## Once that is working, modify your code to generate a list of positions versus times
##(use two arrays, one for position, one for time). Create a loop that will compute these
##positions and times until you hit the ground assuming that you didn’t open your parachute.
##Use a starting height of 4000 m. Create a plot of this data. You may also want to output the#
## data to a file for later use.

# --- Step 2: Loop from 4000 m until hitting the ground ---
h_start = 4000.0
dt = 0.5  # Time step in seconds
t_current = 0.0
x_current = h_start

# Arrays to store positions and times
times = []
positions = []

while x_current > 0:
    times.append(t_current)
    positions.append(x_current)
    
    t_current += dt
    x_current = get_position(t_current, h_start)

# Append the final boundary point where it hits the ground
if positions[-1] > 0:
    # Fine-tune the last time step to hit exactly 0 (using a simple approximation)
    t_final = times[-1] + (positions[-1] / VT)
    times.append(t_final)
    positions.append(0.0)

# Convert to numpy arrays
times = np.array(times)
positions = np.array(positions)

print("--- Simulation Run ---")
print(f"Total time to hit the ground from {h_start}m: {times[-1]:.4f} seconds.")

# --- Step 3: Output data to a file ---
output_filename = "skydive_trajectory.txt"
# Stack data columns horizontally and save
data_to_save = np.column_stack((times, positions))
np.savetxt(output_filename, data_to_save, fmt="%.4f", header="Time(s) Position(m)")
print(f"Trajectory data successfully saved to '{output_filename}'")

# --- Step 4: Plotting the data ---
plt.figure(figsize=(8, 5))
plt.plot(times, positions, label="Altitude (No Parachute)", color="blue", linewidth=2)
plt.title("Skydiver Position vs. Time (Initial Height = 4000m)")
plt.xlabel("Time (seconds)")
plt.ylabel("Position / Altitude (meters)")
plt.grid(True)
plt.axhline(0, color='red', linestyle='--', label='Ground Level')
plt.legend()
plt.savefig("Gravity_One_graph.pdf")

plt.clf() ## This helps clears the previous graph and make room for the second graph



## Now, lets assume that you do deploy your parachute at a height of 1200 m. It takes a few seconds
## for the chute to fully deploy, and during that time your terminal velocity will be changing.
## This would create a problem that would be much more difficult to solve analytically as we would
## have two variables changing in time. However, we can solve this numerically by making a simple assumption:
## for a small time interval, the terminal velocity will be constant. This is similar to what we did with the
## projectile, where we said that if we keep our time step small enough, then the acceleration of the projectile
## will be close to constant and we could then use constant acceleration kinematics to describe the changes in position
## and velocity over that small time interval.

## Once the chute is fully deployed you will be falling at a far gentler 7.6  m⁄s instead of 54.0  m⁄s. If it takes 3 seconds
## to full open, and we assume that the rate of change in terminal velocity is constant over that time, compute what this rate will
## be. Compute a time step that will keep the change in terminal velocity to about 10^(-6) during that step.


## Modify your code so that after the appropriate distance fallen, your chute deploys. Your terminal velocity starts to change at 
## the rate you just computed. Your code should now compute the change in position for each time step based on the estimated terminal
## velocity at that time. Make sure that your code goes to the purely constant terminal velocity of 7.6  m⁄s once that is reached,
## and back to a larger time step so that your code doesn’t take forever to finish. Make sure that you compute how long it takes to
## go from 54.0  m⁄s to 7.6  m⁄s and check that it agrees with our assumption of 3 seconds. How far did you fall while the chute was
## deploying?

## Make sure that your code still tracks the position versus time for the whole trip. 
## Plot this data once the ground is reached. You may also want to output this data to a file for later use.

# Constants
G = 9.8
V_T0 = 54.0       # Initial terminal velocity (m/s)
V_TF = 7.6        # Final terminal velocity with open chute (m/s)
T_DEPLOY = 3.0    # Deployment duration (s)
CHUTE_HEIGHT = 1200.0  # Height at which chute is pulled (m)

# 1. Calculate rate of change of terminal velocity
rate_vt = (V_TF - V_T0) / T_DEPLOY
print(f"Calculated rate of change of terminal velocity: {rate_vt:.4f} m/s^2")

# 2. Calculate requested theoretical time step
dt_theoretical = 1e-6 / abs(rate_vt)
print(f"Theoretical time step for 10^-6 vt change: {dt_theoretical:.4e} seconds\n")

# Simulation setup
t = 0.0
h = 4000.0   # Initial height (m)
v = 0.0      # Initial velocity (m/s)

# Lists to track the whole trip
times = []
positions = []
velocities = []

# Time step configurations
dt_normal = 0.1
dt_deploy = 0.001  # Used for efficient execution while preserving sub-millisecond accuracy

chute_triggered = False
chute_fully_open = False
t_chute_start = 0.0
h_chute_start = 0.0
h_chute_end = 0.0

# --- Simulation Loop ---
while h > 0:
    times.append(t)
    positions.append(h)
    velocities.append(v)
    
    # Determine the active terminal velocity and time step
    if h <= CHUTE_HEIGHT and not chute_triggered:
        chute_triggered = True
        t_chute_start = t
        h_chute_start = h
        print(f"--- Parachute Deployed at h = {h:.2f} m (t = {t:.2f} s) ---")

    if chute_triggered and not chute_fully_open:
        elapsed_deploy = t - t_chute_start
        if elapsed_deploy >= T_DEPLOY:
            chute_fully_open = True
            h_chute_end = h
            deployment_duration = t - t_chute_start
            print(f"--- Parachute Fully Open at h = {h:.2f} m (t = {t:.2f} s) ---")
            print(f"Verified deployment duration: {deployment_duration:.4f} seconds")
            print(f"Distance fallen during deployment: {h_chute_start - h_chute_end:.2f} meters\n")
            vt = V_TF
            dt = dt_normal  # Go back to a larger time step
        else:
            vt = V_T0 + rate_vt * elapsed_deploy
            dt = dt_deploy  # Drop to small time step for precision
    elif chute_fully_open:
        vt = V_TF
        dt = dt_normal
    else:
        vt = V_T0
        dt = dt_normal

    # Numerical integration using constant acceleration kinematics over dt
    # Acceleration equation: dv/dt = g * (1 - (v/v_t)^2)
    accel = G * (1.0 - (v / vt)**2)
    
    # Update velocity and position
    v += accel * dt
    h -= v * dt
    t += dt

# Ensure ground condition ends cleanly at exactly 0m
times.append(t)
positions.append(0.0)
velocities.append(v)

print(f"--- Ground Reached ---")
print(f"Total time for the entire descent: {t:.2f} seconds.")

# --- Save Data to File ---
output_filename = "parachute_descent_trajectory.txt"
data_to_save = np.column_stack((times, positions, velocities))
np.savetxt(output_filename, data_to_save, fmt="%.4f", 
           header="Time(s) Position(m) Velocity(m/s)")
print(f"Full trajectory data successfully saved to '{output_filename}'\n")

# --- Plot the Trajectory ---
plt.figure(figsize=(10, 6))
plt.plot(times, positions, color='blue', linewidth=2.5, label='Skydiver Altitude')
plt.axhline(CHUTE_HEIGHT, color='orange', linestyle=':', label='Chute Deployment Trigger (1200m)')
plt.axhline(0, color='red', linestyle='--', label='Ground Level')

# Visual markers for deployment phase
plt.plot(t_chute_start, h_chute_start, 'go', label='Chute Pull')
plt.plot(t_chute_start + T_DEPLOY, h_chute_end, 'ro', label='Fully Open')

plt.title("Full Skydiver Trajectory with Parachute Deployment")
plt.xlabel("Time (seconds)")
plt.ylabel("Altitude / Position (meters)")
plt.grid(True)
plt.legend()
plt.savefig("Gravity_Two_graph.pdf")