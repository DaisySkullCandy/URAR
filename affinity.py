import psutil
import time
import math
from file_manager import open_config
from colorizer import clr,resetclr

roblox = "RobloxPLayerBeta.exe"  # Example target application
num_threads = open_config("cores_per_instance") # Number of threads or processes you want to assign cores to

def calculate_available_cores(num_cores, excluded_cores=[0, 5]):
    # Dynamically adjust the excluded cores based on available cores
    if num_cores < 8:
        excluded_cores = []  # Don't exclude any cores if there are fewer than 8
    elif num_cores == 8:
        excluded_cores = [0, 5]  # Exclude cores 0 and 5 for 8 cores
    elif num_cores > 8:
        # Exclude 0, 1 for lower cores and distribute accordingly
        excluded_cores = [0, 1] if num_cores <= 16 else [0, 1, num_cores // 2 - 1, num_cores // 2]

    # Get the list of available cores excluding the specified ones
    available_cores = [i for i in range(num_cores) if i not in excluded_cores]
    return available_cores


# List to store previously found PIDs
found_pids = []


def get_pids_by_name(app_name):
    """Find all PIDs for the app with the given name."""
    pids = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name matches and if the PID is not already in the found_pids list
            if app_name.lower() in proc.info['name'].lower() and proc.info['pid'] not in found_pids:
                pids.append(proc.info['pid'])
                found_pids.append(proc.info['pid'])  # Add the PID to the dynamic list
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return pids


def assign_cores_to_threads(available_cores, num_threads):
    """
    Assign available cores to threads, divide them as evenly as possible
    """
    cores_per_thread = math.floor(len(available_cores) / num_threads)  # Minimum cores per thread
    remainder = len(available_cores) % num_threads  # Any leftover cores

    # List to store the core assignments
    assignments = []
    start = 0
    for i in range(num_threads):
        # Add one extra core to the first 'remainder' threads
        end = start + cores_per_thread + (1 if i < remainder else 0)
        assignments.append(available_cores[start:end])
        start = end
    return assignments


def set_affinity_for_process(pid, assigned_cores):
    try:
        if assigned_cores:
            # Set CPU affinity for the process using the assigned cores
            psutil.Process(pid).cpu_affinity(assigned_cores)
            print(f"Process {pid} affinity set to: {assigned_cores}")
        else:
            print("No available CPU cores to assign.")
    except Exception as e:
        print(f"Error setting CPU affinity: {e}")


def get_pid_from_application_name(target_application, num_threads):
    try:
        # Get the number of available cores
        num_cores = psutil.cpu_count()

        # Calculate available cores for the process
        available_cores = calculate_available_cores(num_cores)

        # Assign cores to the threads
        assigned_cores = assign_cores_to_threads(available_cores, num_threads)

        # Loop through all running processes to find matching application instances
        for process in psutil.process_iter(['pid', 'name']):
            if target_application.lower() in process.info['name'].lower():
                pid = process.info['pid']
                print(f"Found {target_application} with PID: {pid}")

                # Set CPU affinity for the current process
                for i in range(min(num_threads, len(assigned_cores))):
                    set_affinity_for_process(pid, assigned_cores[i])

                # Add a small delay before moving to the next process
                time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")




