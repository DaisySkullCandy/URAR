import os
import threading
import time
import sys
import subprocess
import affinity
from elevate import elevate
from listener import app
from joiner import launch_account, count_accounts
from file_manager import (
    initial_check,
    open_config,
    open_accounts,
    revert_xml,
    setup_xml,
    setup_json,
    copy_scripts,
    delete_scripts
)
from colorizer import clr, resetclr
from instance_closer import close_on_RAM, close_finished

# admin privileges so it can close roblox,RAM
elevate()
# check if you have accounts.txt and create json if it's not there already
initial_check()
# setup custom XML if enabled
setup_xml()
# setup client app settings
setup_json(
    "content/ClientAppSettings.json",
    os.path.join(open_config("roblox_ver"), "ClientSettings"),
)
# copy scripts from scripts folder to autoexec folder
copy_scripts(
    "content/scripts",
    open_config("autoexecute_path"),
)
# yes ik this is stupid
linked = {}
# limit of 50 for joins per hour, could set up cool connection thingies to do even 400-500joins P/H,  but I don't want skids having my amount of rizz
# uh also it only works if u save PID cuz fk u 😊 ("close_on_finish": true)
LaunchCounter = 0
# number of current instances blablabla
instances = 0
# prevent my dumbass from accessing a billion same values at the same fucking time causing it to break
instances_lock = threading.Lock()
linked_lock = threading.Lock()

number_of_accounts = count_accounts(open_config("password"), open_config("RAM_port"))
if number_of_accounts == "error":
    input("Couldn't get number of accounts, please check your RAM accounts")
else:
    print(f"got {number_of_accounts} accounts from RAM")

#used to reset the counter that prevents getting your IP blocked by the 50 launches P/H limit
def timer():
    global LaunchCounter
    counter = 0  # Initialize the counter
    max_seconds = 3600  # Number of seconds in an hour (1 hour = 3600 seconds)

    while True:
        time.sleep(1)  # Wait for 1 second
        counter += 1  # Increment the counter

        if counter >= max_seconds:  # Check if the counter has reached an hour
            print(clr("Y")+"Resetting counter..."+resetclr())
            counter = 0  # Reset the counter
            LaunchCounter = 0
def quit():
    try:
        print(clr("Y") + f"Warning pressing [ENTER] WILL close RAM,Roblox,and Python" + resetclr())
        input(clr("G") + f"Press [ENTER] to stop URAR" + resetclr())
        # close all roblox instances & RAM if enabled
        subprocess.run("taskkill /f /im RobloxPlayerBeta.exe")
        if open_config("close_RAM"):
            subprocess.run("taskkill /f /im RobloxAccountManager.exe")
            os.remove(open_config("roblox_path") + "\\LocalStorage\\RobloxCookies.dat")
            print(clr("G") + "Deleted Roblox Cookies File" + resetclr())
            # Fix to normal
        os.remove(open_config("roblox_ver") + "\\ClientSettings\\ClientAppSettings.json")
        revert_xml()
        if not open_config("using_awp"):
            delete_scripts(
                "content/scripts",
            open_config("autoexecute_path"),
            )
        sys.exit(0)
    except Exception as e:
        print(clr("R") + f"Error in quit function: {e}" + resetclr())


# will close accounts with high ram or that have crashed/lagged etc
def close_accounts():
    global instances
    if not open_config("close_on_finish"):
        time.sleep(1)
        return
    current_key = set()
    while True:
        time.sleep(3)
        while not linked:
            time.sleep(0.2)
        ram_check =close_on_RAM(linked, open_config("ram_threshold"))
        with linked_lock:
            closed_instance = [key for key, value in linked.items() if value == ram_check  and key not in current_key]
        if closed_instance:
            for key in closed_instance:
                with linked_lock:
                    del linked[key]
                    print(linked)
                    with instances_lock:
                        instances -= 1
            time.sleep(1)
        else:
            time.sleep(0.5)

        time.sleep(3)


# Loop through each account and perform actions based on conditions
def autolaunch():
    global instances
    global linked
    global LaunchCounter
    if open_config("vpn"):
        limit = 40
    else:
        limit = 50
    while True:
        while instances < open_config("concurrent_usrs") and LaunchCounter < limit:
            for account in open_accounts():
                if not account["finished"] and instances < open_config("concurrent_usrs") and account["username"] not in linked.keys():
                    # add instance until it gets to limit blablabla
                    with instances_lock:
                        if account["vip"]:
                            result = launch_account(account["username"], account["placeid"], open_config("password"),
                                                    vip=True)
                            if result == 1:
                                instances += 1
                                LaunchCounter += 1
                        else:
                            result = launch_account(account["username"], account["placeid"], open_config("password"))
                            if result == 1:
                                instances += 1
                                LaunchCounter += 1

                    if open_config("close_on_finish"):
                        pid_result = []
                        #try around 15 times  to know if it failed or not
                        tries = 30
                        while tries > 0:  # Keep looping until the PID is found
                            pid_result = affinity.get_pids_by_name(affinity.roblox)
                            if pid_result:
                                break
                            time.sleep(0.5)# Wait for 0.5 seconds before retrying
                            tries -= 1
                        if  not pid_result:
                            print(clr("R")+"Couldn't find Launched Instance, are you being rate-limited?"+resetclr())
                            return
                        linked[account["username"]] = pid_result[0]
                    if not instances >= open_config("concurrent_usrs"):
                        # retard proofing so they don't kill their connection for an hour and cry
                        if open_config("launch_delay") <= 15 and open_config("concurrent_usrs") >= 8:
                            print(clr("G")+"Waiting 15 seconds"+resetclr())
                            time.sleep(15)
                        else:
                            print(clr("G")+f"Waiting {open_config("launch_delay")} seconds"+resetclr())
                            time.sleep(open_config("launch_delay"))
                    if instances >= open_config("concurrent_usrs"):
                        if open_config("close_on_finish"):
                            print(linked)
        time.sleep(0.2)


# will tell you how to close teh app or wtv
threading.Thread(
    target=quit,
).start()
# continue running shit without autolaunch being a little bitch
threading.Thread(target=autolaunch, daemon=True).start()
# make a thread to close accounts that are finished or are in the limit of ram, and remove them form the dictionary
threading.Thread(target=close_accounts, daemon=True).start()
threading.Thread(target=timer, daemon=True).start()
