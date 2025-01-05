import os
from colorizer import clr, resetclr
import json
import shutil

# Path to the default JSON template
default_json_path = "settings/default.json"
# Path to the accounts JSON file
accounts_json_path = "settings/accounts.json"
# Path to the config JSON file
config_json_path = "settings/config.json"
# Path to the VIP JSON file
vip_json_path = "settings/vipservers.json"
# Prepare a list to hold all accounts
accounts_list = []

# create the acocunts.json files based on the accounts.txt
def auto_format(default_json_path, accounts_file_path, output_json_path):
    try:
        # Create a temporary copy of the default JSON file
        temp_file_path = "temp_default.json"
        shutil.copy(default_json_path, temp_file_path)

        # Read the account names from the text file
        with open(accounts_file_path, "r") as accounts_file:
            account_names = [line.strip() for line in accounts_file if line.strip()]

        accounts_list = []  # Initialize the accounts list

        # Read the default JSON data from the temporary file
        with open(temp_file_path, "r") as temp_file:
            default_data = json.load(temp_file)

        # Process each account name
        for account_name in account_names:
            # Create a copy of the default data and update the username field
            updated_data = default_data.copy()
            updated_data["username"] = account_name
            accounts_list.append(updated_data)

        # Write the entire list to the output JSON file
        with open(output_json_path, "w") as output_file:
            json.dump(accounts_list, output_file, indent=4)

        # Clean up the temporary file
        os.remove(temp_file_path)

        print(
            f"Generated JSON file at '{output_json_path}' with {len(accounts_list)} accounts."
        )

    except Exception as e:
        print(f"An error occurred: {e}")


def initial_check():
    if not os.path.isfile(accounts_json_path):
        if not os.path.isfile("accounts.txt"):
            print(
                clr("R")
                + "Please place the accounts.txt file inside the folder"
                + resetclr()
            )
            input(clr("Y") + "Press [ENTER] to exit the program..." + resetclr())
        else:
            print(
                clr("Y") + "Detected  fresh start, Generating JSON file " + resetclr()
            )
            auto_format(default_json_path,"accounts.txt",accounts_json_path)


def open_accounts():
    with open(accounts_json_path, "r") as file:
        accounts = json.load(file)
        return accounts  # This will be a list of the accounts


def get_vip(server):
    server = str(server)
    with open(vip_json_path, "r") as file:
        vip = json.load(file)  # servers
    return vip[server]


def open_config(action):
    with open(config_json_path, "r") as file:
        config = json.load(file)  # config
    return config[action]


def revert_xml():
    open(open_config("roblox_path") + r"\\GlobalBasicSettings_13.xml", "w").write(
        open("content//nm.xml", "r").read()
    )


def setup_xml():
    if open_config("optimised_xml"):
        open(open_config("roblox_path") + r"\\GlobalBasicSettings_13.xml", "w").write(
            open("content//ml.xml", "r").read()
        )
    print(clr("G") + f"Successfully Generated XML File" + resetclr())


def setup_json(source_file, destination_directory):
    # Construct the full destination path
    destination_file = os.path.join(destination_directory, "ClientAppSettings.json")

    # Read content from the source file
    with open(source_file, "r") as src:
        content = json.load(src)

    # Write the content to the destination file
    with open(destination_file, "w") as dest:
        json.dump(content, dest, indent=4)

    print(clr("G") + f"Successfully Generated JSON File" + resetclr())


# this will copy .txt and .lua files from the "scripts" folder into the desired autoexec folder
def copy_scripts(
    src_dir,
    dest_dir,
):
    extensions = ("lua", "txt")
    try:
        # Ensure source directory exists
        if not os.path.isdir(src_dir):
            print(
                clr("R") + f"Source directory '{src_dir}' does not exist." + resetclr()
            )
            return
        # Ensure destination directory exists
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
            print(
                clr("R") + f"Source directory '{dest_dir}' does not exist." + resetclr()
            )
        # Iterate through files in the source directory
        for file_name in os.listdir(src_dir):
            # Check if the file has one of the specified extensions
            if file_name.endswith(extensions):
                src_file = os.path.join(src_dir, file_name)
                dest_file = os.path.join(dest_dir, file_name)
                # Copy the file
                shutil.copy(src_file, dest_file)
        print(clr("G") + "Script files copied to AutoExec folder" + resetclr())

    except Exception as e:
        print(clr("R") + f"An error occurred: {e}" + resetclr())


def delete_scripts(src_dir, dest_dir, extensions):
    pass
