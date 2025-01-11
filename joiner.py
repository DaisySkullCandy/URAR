import requests
from file_manager import open_config, get_vip
from colorizer import resetclr, clr


# Function to launch an account using the API
def launch_account(account_name, place_id, password, port=open_config("RAM_port"), vip=False):
    # API endpoint to launch the account
    url = f"http://localhost:{port}/LaunchAccount?Account={account_name}&PlaceId={place_id}&Password={password}"
    vip_link = get_vip(place_id)
    vip_url =  f"http://localhost:{port}/LaunchAccount?Account={account_name}&PlaceId={place_id}&JobId={vip_link}&JoinVip={1}&Password={password}"
    # Make the request to launch the account
    try:
        if vip:
            response = requests.get(vip_url)
            if response.status_code == 200 or 400:
                print(clr("G") + f"\nSuccessfully launched {account_name} to place {place_id}" + resetclr())
                return 1
            else:
                print(clr("R") + f"\nFailed to launch account. Status code: {response.status_code}" + resetclr())
                print(response.text)
                return 0
        else:
            response = requests.get(url)
            if response.status_code == 200 or 400:
                print(clr("G") + f"\nSuccessfully launched {account_name} to place {place_id}" + resetclr())
                return 1
            else:
                print(clr("R") + f"\nFailed to launch account. Status code: {response.status_code}" + resetclr())
                print(response.text)
                return 0

    except requests.exceptions.RequestException as e:
        print(clr("R") + f"\nError while launching account: {e}" + resetclr())


def get_accounts(password, port, group="bots"):
    # URL for the GetAccounts API
    url = f"http://localhost:{port}/GetAccounts?Password={password}&Group={group}"

    try:
        # Send GET request to the API
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            # Successfully received account data, parse it
            accounts = response.text.strip()
            return accounts
        elif response.status_code == 401:
            print("Invalid Password or Method Not Allowed")
        elif response.status_code == 400:
            print("Bad Request or Invalid Account")
        else:
            print(f"Unexpected error: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    return "error"


def count_accounts(password, port, group="bots"):
    accounts = get_accounts(password, port)
    # Assuming the response is a comma-separated list of accounts
    account_list = accounts.split(",")
    print(account_list)
    account_count = len(account_list)
    return account_count

