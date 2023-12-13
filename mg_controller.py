"""
@author: Dr Soheil Mohseni

v1.0
"""

import matplotlib.pyplot as plt
import numpy as np

class SolarPV:
    def __init__(self, solar_power_output_vector):
        self.solar_power_output_vector = solar_power_output_vector
        self.current_hour = 0

    def get_solar_power_output(self):
        solar_power_output = self.solar_power_output_vector[self.current_hour]
        self.current_hour = (self.current_hour + 1) % 24
        return solar_power_output

class WindTurbine:
    def __init__(self, wind_power_output_vector):
        self.wind_power_output_vector = wind_power_output_vector
        self.current_hour = 0

    def get_wind_power_output(self):
        wind_power_output = self.wind_power_output_vector[self.current_hour]
        self.current_hour = (self.current_hour + 1) % 24
        return wind_power_output

class Battery:
    def __init__(self, capacity, charge_rate, discharge_rate, charge_threshold, discharge_threshold):
        self.capacity = capacity
        self.charge_rate = charge_rate
        self.discharge_rate = discharge_rate
        self.charge_threshold = charge_threshold
        self.discharge_threshold = discharge_threshold
        self.charge_level = 0

class Consumer:
    def __init__(self, power_demand_vector):
        self.power_demand_vector = power_demand_vector
        self.current_hour = 0

    def get_power_demand(self):
        power_demand = self.power_demand_vector[self.current_hour]
        self.current_hour = (self.current_hour + 1) % 24
        return power_demand

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0 

    def update(self, error):
        self.integral += error
        derivative = error - self.prev_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

class MainGrid:
    def __init__(self, min_power_output, max_power_output):
        self.min_power_output = min_power_output
        self.max_power_output = max_power_output
        self.power_output = np.random.uniform(min_power_output, max_power_output)

    def update_power_output(self):
        self.power_output = np.random.uniform(self.min_power_output, self.max_power_output)

class MicrogridSimulation:
    def __init__(self, solar_pv, wind_turbine, battery, consumer, pid_controller, main_grid):
        self.solar_pv = solar_pv
        self.wind_turbine = wind_turbine
        self.battery = battery
        self.consumer = consumer
        self.pid_controller = pid_controller
        self.main_grid = main_grid
        self.prev_error = 0
        self.log = {'hour': [], 'total_available_power': [], 'deficit': [], 'battery_charge_level': [], 'controller_output': [], 'main_grid_power': []}

    def simulate(self, duration_hours):
        for hour in range(duration_hours):
            solar_power = self.solar_pv.get_solar_power_output()
            wind_power = self.wind_turbine.get_wind_power_output()

            total_renewable_power = solar_power + wind_power
            total_available_power = total_renewable_power + self.battery.charge_level + self.main_grid.power_output

            error = self.consumer.get_power_demand() - total_available_power

            # Use PID controller to adjust charge and discharge thresholds
            pid_output = self.pid_controller.update(error)
            self.battery.charge_threshold += pid_output
            self.battery.discharge_threshold += pid_output

            # Update main grid power output
            self.main_grid.update_power_output()

            self.log['hour'].append(hour)
            self.log['total_available_power'].append(total_available_power)
            self.log['deficit'].append(max(0, error))
            self.log['battery_charge_level'].append(self.battery.charge_level)
            self.log['controller_output'].append(pid_output)
            self.log['main_grid_power'].append(self.main_grid.power_output)

            if total_available_power >= self.consumer.get_power_demand():
                print(f"Hour {hour + 1}: Microgrid is supplying enough power from renewable sources and the main grid.")
            else:
                deficit = self.consumer.get_power_demand() - total_available_power
                print(f"Hour {hour + 1}: Microgrid is experiencing a power deficit of {deficit} units.")

                # Intelligent charge and discharge
                if total_renewable_power > self.battery.discharge_threshold * self.consumer.get_power_demand():
                    discharge_amount = min(
                        (total_renewable_power - self.consumer.get_power_demand()) * self.battery.discharge_rate,
                        self.battery.charge_level
                    )
                    self.battery.charge_level -= discharge_amount
                elif total_available_power < self.battery.charge_threshold * self.consumer.get_power_demand():
                    charge_amount = min(
                        (self.consumer.get_power_demand() - total_available_power) * self.battery.charge_rate,
                        self.battery.capacity - self.battery.charge_level
                    )
                    self.battery.charge_level += charge_amount

            # Update battery charge level
            self.battery.charge_level += (total_renewable_power - self.consumer.get_power_demand()) * self.battery.charge_rate
            self.battery.charge_level = min(self.battery.charge_level, self.battery.capacity)

            # Discharge battery if needed
            if total_renewable_power < self.consumer.get_power_demand():
                discharge_amount = (self.consumer.get_power_demand() - total_renewable_power) * self.battery.discharge_rate
                self.battery.charge_level -= discharge_amount
                self.battery.charge_level = max(self.battery.charge_level, 0)

            self.prev_error = error

    def plot_power_flows(self):
        plt.figure(figsize=(14, 12))

        # Plot the first set of subplots
        plt.subplot(2, 2, 1)
        plt.plot(self.log['hour'], self.log['total_available_power'], label='Total Available Power')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Power (kW)', fontsize=14) 
        plt.title('(a) Microgrid Power Flows Over Time', fontsize=14) 
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(self.log['hour'], self.log['deficit'], label='Power Deficit')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Power (kW)', fontsize=14) 
        plt.title('(b) Power Deficit Over Time', fontsize=14) 
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(self.log['hour'], self.log['battery_charge_level'], label='Battery Charge Level')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Power (kWh)', fontsize=14) 
        plt.title('(c) Battery Charge Level Over Time', fontsize=14) 
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(self.log['hour'], self.log['controller_output'], label='Controller Output', color='orange')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Controller Output', fontsize=14) 
        plt.title('(d) PID Controller Output Over Time', fontsize=14)
        plt.legend()
        plt.grid(True)

        # Plot the second set of subplots
        plt.figure(figsize=(14, 12))

        plt.subplot(3, 1, 1)
        plt.plot(self.log['hour'], self.solar_pv.solar_power_output_vector, label='Solar Power Output')
        plt.xlabel('Hour', fontsize =14)
        plt.ylabel('Power (kW)', fontsize =14)
        plt.title('(a) Solar Power Output Over Time (kW)', fontsize =14)
        plt.legend()
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(self.log['hour'], self.wind_turbine.wind_power_output_vector, label='Wind Power Output', color='green')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Power (kW)', fontsize=14) 
        plt.title('(b) Wind Power Output Over Time', fontsize=14) 
        plt.legend()
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.plot(self.log['hour'], self.consumer.power_demand_vector, label='Load Demand', color='red')
        plt.xlabel('Hour', fontsize=14) 
        plt.ylabel('Power (kW)', fontsize=14) 
        plt.title('(c) Load Demand Over Time', fontsize=14) 
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Test the updated microgrid simulation with dynamic grid exchange
    # create components with intelligent charge and discharge parameters
    solar_power_vector = np.random.uniform(20, 40, 24)  # Example solar power output vector for 24 hours
    wind_power_vector = np.random.uniform(10, 30, 24)  # Example wind power output vector for 24 hours
    load_demand_vector = np.random.uniform(30, 50, 24)  # Example random load demand vector for 24 hours

    solar_pv = SolarPV(solar_power_output_vector=solar_power_vector)
    wind_turbine = WindTurbine(wind_power_output_vector=wind_power_vector)
    battery = Battery(
        capacity=50,
        charge_rate=0.2,
        discharge_rate=0.1,
        charge_threshold=0.8,
        discharge_threshold=0.2
    )
    house_consumer = Consumer(power_demand_vector=load_demand_vector)  # Pass the load demand vector

    # create a PID controller
    pid_controller = PIDController(kp=0.1, ki=0.01, kd=0.05)

    # create a main grid with a power output fluctuating between 5 and 15
    main_grid = MainGrid(min_power_output=5, max_power_output=15)

    # create a microgrid simulation with PID controller and main grid
    simulation = MicrogridSimulation(
        solar_pv=solar_pv,
        wind_turbine=wind_turbine,
        battery=battery,
        consumer=house_consumer,
        pid_controller=pid_controller,
        main_grid=main_grid
    )

    # run the simulation for 24 hours
    simulation.simulate(duration_hours=24)

    # plot power flows
    simulation.plot_power_flows() 
