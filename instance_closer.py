import ctypes
import psutil
from colorizer import resetclr, clr

# will close any program with RAM over the specified threshold
def close_on_RAM(process_dict, threshold_mb):
    for instances, pid in process_dict.items():
        try:
            # Check if the process exists
            if not psutil.pid_exists(pid):
                print(clr("R") + f"PID {pid} does not exist." + resetclr())
                continue
            # Get process memory info
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            memory_usage_mb = memory_info.rss / (1024 * 1024)  # Convert bytes to MB
            if memory_usage_mb > threshold_mb:
                print(
                    clr("Y")
                    + f"PID {pid} exceeds {threshold_mb} MB ({memory_usage_mb:.2f} MB). Terminating..."
                    + resetclr()
                )
                # Open the process with PROCESS_TERMINATE access
                PROCESS_TERMINATE = 0x0001
                handle = ctypes.windll.kernel32.OpenProcess(
                    PROCESS_TERMINATE, False, pid
                )
                if not handle:
                    print(
                        clr("R")
                        + f"Unable to open process with PID {pid}. Error code: {ctypes.windll.kernel32.GetLastError()}"
                        + resetclr()
                    )
                    continue
                # Terminate the process
                result = ctypes.windll.kernel32.TerminateProcess(handle, 0)
                if result:
                    print(
                        clr("G")
                        + f"Process with PID {pid} terminated successfully."
                        + resetclr()
                    )
                    return pid
                else:
                    print(
                        clr("R")
                        + f"Failed to terminate process with PID {pid}. Error code: {ctypes.windll.kernel32.GetLastError()}"
                        + resetclr()
                    )
                    return 1
                # Close the handle
                ctypes.windll.kernel32.CloseHandle(handle)
        except psutil.NoSuchProcess:
            print(clr("Y") + f"PID {pid} no longer exists." + resetclr())
            return 1
        except Exception as e:
            print(clr("R") + f"An error occurred for PID {pid}: {e}" + resetclr())
            return 1


def close_finished(PID):
    try:
        # Open the process with PROCESS_TERMINATE access
        PROCESS_TERMINATE = 0x0001
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, PID)
        if not handle:
            print(
                clr("R")
                + f"Unable to open process with PID {PID}. Error code: {ctypes.windll.kernel32.GetLastError()}"
                + resetclr()
            )
            return
        # Terminate the process
        result = ctypes.windll.kernel32.TerminateProcess(handle, 0)
        if result:
            print(
                clr("G")
                + f"Process with PID {PID} terminated successfully."
                + resetclr()
            )
        else:
            print(
                clr("R")
                + f"Failed to terminate process with PID {PID}. Error code: {ctypes.windll.kernel32.GetLastError()}"
                + resetclr()
            )
        # Close the handle
        ctypes.windll.kernel32.CloseHandle(handle)
    except Exception as e:
        print(clr("R") + f"An error occurred: {e}" + resetclr())
