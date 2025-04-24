#************************************* LIKWRAP *************************************************

#!/usr/bin/env python3

import subprocess  # For executing shell commands
import time  # For measuring time intervals
import argparse  # For handling command-line arguments
import os  # For interacting with the OS
import sys  # For system-related functionalities

#######################################################################
		#Likwid Parameters
#######################################################################

CORES = "0-55"  # Specify CPU cores to monitor
ENERGY_PMCS = "PWR_PKG_ENERGY:PWR0,PWR_DRAM_ENERGY:PWR3"  # Define energy monitoring counters

# List of output files to delete before running the script
OUTPUT_FILES = ["baseline_output.txt", "application_output.txt", "dynamic_energy_output.txt"]

#######################################################################
		# Function to Delete Previous Output Files
#######################################################################

def delete_previous_output_files():
    """Delete previously saved output files before running a new measurement"""
    print("\nDeleting previous output files...")
    for file in OUTPUT_FILES:
        if os.path.exists(file):
            print(f"Deleting {file}...")
            os.remove(file)
            print(f"{file} deleted successfully.")
    print("All old output files removed.\n")

#######################################################################
		# Function to Parse LIKWID Output
#######################################################################

def parse_likwid_output(output):
    """Parse LIKWID output to extract energy metrics"""
    print("\nRaw LIKWID output:")
    print("=" * 50)
    print(output)
    print("=" * 50)

    metrics = {}
    table_started = False
    header_found = False

    for line in output.split('\n'):
        if not line.strip():
            continue
        
        if '+-' in line and not table_started:
            table_started = True
            continue
        
        if 'Event' in line and 'Counter' in line:
            header_found = True
            continue
        
        if '+-' in line:
            continue
        
        if table_started and header_found:
            parts = [part.strip() for part in line.split('|') if part.strip()]
            
            if len(parts) >= 3:
                event_name = parts[0]
                try:
                    sum_value = float(parts[2])  # Extract "Sum" column
                    
                    if "PWR_PKG_ENERGY STAT" in event_name:
                        metrics['PKG_Energy'] = sum_value
                        print(f"Found Package Energy: {sum_value:.2f} Joules")
                    elif "PWR_DRAM_ENERGY STAT" in event_name:
                        metrics['DRAM_Energy'] = sum_value
                        print(f"Found DRAM Energy: {sum_value:.2f} Joules")
                except ValueError:
                    continue
    
    return metrics    

#######################################################################
		# Function to Measure Baseline Energy (Idle System)
#######################################################################

def measure_baseline():
    """Measure baseline energy using LIKWID"""
    print("\nMeasuring Baseline Energy (Idle System)")
    print("=" * 50)

    cmd = f"likwid-perfctr -c {CORES} -g {ENERGY_PMCS} sleep 60"
    print(f"Running command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        metrics = parse_likwid_output(result.stdout)

        if metrics:
            pkg_energy = metrics.get('PKG_Energy', 0)
            dram_energy = metrics.get('DRAM_Energy', 0)
            total_energy = pkg_energy + dram_energy

            # Calculate power (Energy/Time)
            pkg_power = pkg_energy / 60
            dram_power = dram_energy / 60
            total_power = total_energy / 60

            # Print Baseline Power Consumption
            print("\nBaseline Power Measurements:")
            print("=" * 40)
            print(f"Package Power: {pkg_power:.2f} W")
            print(f"DRAM Power: {dram_power:.2f} W")
            print(f"Total Power (Idle): {total_power:.2f} W")

            return {'pkg_power': pkg_power, 'dram_power': dram_power, 'total_power': total_power}
    
    except Exception as e:
        print(f"Error measuring baseline: {e}")
        return None

#######################################################################
		# Function to Measure Application Energy
#######################################################################

def measure_application_energy(app_type):
    """Measure energy consumption while running an application"""
    
    app_cmd = "./run_pmxm.sh" if app_type == 'parallel' else "./run_smxm.sh"

    print(f"\nMeasuring Energy Consumption for {app_type.upper()} Application")
    print("=" * 50)
    
    cmd = f"likwid-perfctr -c {CORES} -g {ENERGY_PMCS} {app_cmd}"
    print(f"Running command: {cmd}")

    try:
        start_time = time.time()
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        runtime = time.time() - start_time

        metrics = parse_likwid_output(result.stdout)

        if metrics:
            pkg_energy = metrics.get('PKG_Energy', 0)
            dram_energy = metrics.get('DRAM_Energy', 0)
            total_energy = pkg_energy + dram_energy

            avg_pkg_power = pkg_energy / runtime
            avg_dram_power = dram_energy / runtime
            avg_total_power = total_energy / runtime

            print("\nApplication Power and Energy Measurements:")
            print("=" * 40)
            print(f"Runtime: {runtime:.2f} seconds")
            print(f"Total Energy Consumed: {total_energy:.2f} J")
            print(f"Average Total Power: {avg_total_power:.2f} W")

            return {'runtime': runtime, 'pkg_energy': pkg_energy, 'dram_energy': dram_energy, 'total_energy': total_energy}
    
    except Exception as e:
        print(f"Error measuring application energy: {e}")
        return None

#######################################################################
		# Function to Calculate Dynamic Energy
#######################################################################

def calculate_dynamic_energy(baseline, app_metrics):
    """Calculate dynamic energy consumption"""
    print("\nDynamic Energy Calculation:")
    print("=" * 50)

    ET = app_metrics['total_energy']
    PS = baseline['total_power']
    TE = app_metrics['runtime']

    # Apply the formula: ED = ET - (PS × TE)
    ED = ET - (PS * TE)

    print(f"Total Energy Consumed (ET): {ET:.2f} J")
    print(f"Static Power Consumption (PS): {PS:.2f} W")
    print(f"Execution Time (TE): {TE:.2f} seconds")
    print(f"Calculated Dynamic Energy (ED): {ED:.2f} J")

    return ED

#######################################################################
			# Main Function
#######################################################################

def main():
    parser = argparse.ArgumentParser(description='Measure application energy consumption using LIKWID')
    parser.add_argument('--app-type', choices=['serial', 'parallel'], default='serial', help='Type of application to run (default: serial)')
    
    args = parser.parse_args()

    delete_previous_output_files()

    baseline = measure_baseline()
    if not baseline:
        return

    app_metrics = measure_application_energy(args.app_type)
    if not app_metrics:
        return

    dynamic_energy = calculate_dynamic_energy(baseline, app_metrics)
    print(f"\nFinal Dynamic Energy Consumption: {dynamic_energy:.2f} J")

if __name__ == "__main__":
    main()

