# pyMicrogridControl

## Version 1.0

## Overview

`pyMicrogridControl` is a Python framework for simulating the operation and control of a microgrid using a PID controller. The microgrid can include solar panels, wind turbines, a battery bank, and the main grid. The script models the exchange of power between these components over a simulated 24-hour period. Explore intelligent control mechanisms, renewable energy integration, and dynamic energy storage strategies. Efficiently manage local energy systems with this versatile microgrid simulation tool.

## Features

- **Renewable Energy Sources:**
  - Solar panels and wind turbines generate power based on randomly generated vectors.

- **Energy Storage:**
  - A battery is included with adjustable charge and discharge rates.

- **Intelligent Control:**
  - A PID controller dynamically adjusts charge and discharge thresholds to optimize power distribution.

- **Grid Interaction:**
  - The microgrid interacts with a main grid, which has a fluctuating power output.

- **Consumer Demand:**
  - A consumer with a randomly generated power demand vector.

## How to Use

1. **Requirements:**
   - Python (3.x recommended)

2. **Run the Simulation:**
   - Modify the script parameters (e.g., power vectors, controller parameters) as needed.
   - Run the script:
     ```bash
     python microgrid_simulation.py
     ```

3. **Results:**
   - The script will print hourly updates on power supply and demand.
   - Power flow plots will be displayed, showing the dynamics of the microgrid.

## Script Components

- **SolarPV:**
  - Represents solar power generation.

- **WindTurbine:**
  - Represents wind power generation.

- **Battery:**
  - Models energy storage with adjustable parameters.

- **Consumer:**
  - Represents the energy demand of the consumer.

- **PIDController:**
  - Implements a PID controller for intelligent charge and discharge adjustments.

- **MainGrid:**
  - Simulates interaction with the main grid.

- **MicrogridSimulation:**
  - Orchestrates the simulation by updating and interacting with the components.

## Adjusting Parameters

- Modify parameters in the script for different scenarios:
  - Adjust renewable power vectors, battery parameters, consumer demand, and PID controller gains.

## Dependencies

- `matplotlib`
- `numpy`
