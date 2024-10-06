import PIL
import requests
import json
import time
import random
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse
import os

# Initialize Colorama for terminal colors
init(autoreset=True)

url = "https://notpx.app/api/v1"
WAIT = 180 * 3
DELAY = 1
WIDTH = 1000
HEIGHT = 1000
MAX_HEIGHT = 50
start_x = 920
start_y = 386
account_file = 'accounts.txt'  # Persistent storage for accounts
proxy_file = 'proxy.txt'       # Persistent storage for proxies

# Telegram Info
def display_telegram_info():
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Fore.CYAN + " Follow me on Telegram: @virtusoses")
    print(Fore.CYAN + " Telegram Channel: https://t.me/virtusoses")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Clear terminal
def clear_terminal():
    os.system('clear')  # Works in Termux (Unix-like environments)

def get(path):
    space = ' '
    hash_sym = '#'
    dot = '.'
    star = '*'

    return [
        [space] * 15 + [hash_sym] * 10 + [space] * 15,
        [space] * 14 + [hash_sym] * 16 + [space] * 13,
        [space] * 12 + [hash_sym] * 14 + [dot] * 8 + [hash_sym] * 12 + [space] * 8,
        [space] * 10 + [hash_sym] * 10 + [dot] * 12 + [dot] * 9 + [hash_sym] * 10 + [space] * 7,
        [space] * 8  + [hash_sym] * 8  + [dot] * 18 + [hash_sym] * 8  + [space] * 8,
        [space] * 7  + [hash_sym] * 7  + [dot] * 7  + [star] * 17 + [dot] * 7  + [hash_sym] * 8  + [space] * 6,
        [space] * 6  + [hash_sym] * 6  + [dot] * 7  + [star] * 19 + [dot] * 7  + [hash_sym] * 8  + [space] * 6,
        [space] * 5  + [hash_sym] * 5  + [dot] * 8  + [star] * 3  + [dot] * 6  + [star] * 3  + [dot] * 8  + [hash_sym] * 9  + [space] * 6,
        [space] * 5  + [hash_sym] * 5  + [dot] * 8  + [star] * 3  + [dot] * 6  + [star] * 2  + [dot] * 9  + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 9  + [star] * 3  + [dot] * 7  + [star] * 1  + [dot] * 10 + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 9  + [star] * 3  + [dot] * 5  + [star] * 1  + [dot] * 11 + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 11 + [star] * 1  + [dot] * 11 + [hash_sym] * 8  + [space] * 7,
        [space] * 6  + [hash_sym] * 4  + [dot] * 8  + [star] * 6  + [dot] * 7  + [hash_sym] * 10 + [space] * 7,
        [space] * 7  + [hash_sym] * 4  + [dot] * 10 + [star] * 5  + [dot] * 7  + [hash_sym] * 8  + [space] * 7,
        [space] * 9  + [hash_sym] * 4  + [dot] * 12 + [hash_sym] * 6  + [space] * 8,
        [space] * 10 + [hash_sym] * 6  + [dot] * 14 + [hash_sym] * 6  + [space] * 10,
        [space] * 12 + [hash_sym] * 4  + [dot] * 6  + [dot] * 8  + [hash_sym] * 12 + [space] * 12,
        [space] * 13 + [hash_sym] * 6  + [dot] * 8  + [hash_sym] * 10 + [space] * 15,
        [space] * 19
    ]

image = get("")

c = {
    '#': "#000000",
    '.': "#3690EA",
    '*': "#ffffff"
}

def log_message(message, color=Style.RESET_ALL):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{Fore.LIGHTBLACK_EX}{current_time}{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

# Load accounts from persistent storage
def load_accounts_from_file(filename=account_file):
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r') as file:
        accounts = [f"initData {line.strip()}" for line in file if line.strip()]
    return accounts

# Save an account to file
def save_account(account):
    with open(account_file, 'a') as file:
        file.write(f"{account}\n")
    log_message("Account saved.", Fore.GREEN)

# Delete an account from file
def delete_account():
    accounts = load_accounts_from_file()
    if not accounts:
        log_message("No accounts to delete.", Fore.RED)
        return
    print("\nSelect account to delete:")
    for idx, acc in enumerate(accounts, start=1):
        print(f"{Fore.YELLOW}{idx}. {acc}")
    choice = input(Fore.CYAN + "\nEnter the number: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(accounts):
            del accounts[choice]
            with open(account_file, 'w') as file:
                file.writelines([f"{acc}\n" for acc in accounts])
            log_message("Account deleted.", Fore.GREEN)
        else:
            log_message("Invalid choice.", Fore.RED)
    except ValueError:
        log_message("Invalid input.", Fore.RED)

# Load proxies from persistent storage
def load_proxies():
    if not os.path.exists(proxy_file):
        return []
    
    with open(proxy_file, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Save a proxy to file
def save_proxy(proxy):
    with open(proxy_file, 'a') as file:
        file.write(f"{proxy}\n")
    log_message("Proxy saved.", Fore.GREEN)

# Delete a proxy from file
def delete_proxy():
    proxies = load_proxies()
    if not proxies:
        log_message("No proxies to delete.", Fore.RED)
        return
    print("\nSelect proxy to delete:")
    for idx, proxy in enumerate(proxies, start=1):
        print(f"{Fore.YELLOW}{idx}. {proxy}")
    choice = input(Fore.CYAN + "\nEnter the number: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(proxies):
            del proxies[choice]
            with open(proxy_file, 'w') as file:
                file.writelines([f"{proxy}\n" for proxy in proxies])
            log_message("Proxy deleted.", Fore.GREEN)
        else:
            log_message("Invalid choice.", Fore.RED)
    except ValueError:
        log_message("Invalid input.", Fore.RED)

def load_proxy_from_file(filename=proxy_file):
    proxies = load_proxies()
    if not proxies:
        log_message("No proxy found, proceeding without proxy.", Fore.YELLOW)
        return None
    
    return random.choice(proxies)

def extract_username_from_initdata(init_data):
    decoded_data = urllib.parse.unquote(init_data)
    username_start = decoded_data.find('"username":"') + len('"username":"')
    username_end = decoded_data.find('"', username_start)

    if username_start != -1 and username_end != -1:
        return decoded_data[username_start:username_end]

    return "Unknown"


proxy = load_proxy_from_file()

def get_session_with_proxy_and_retries(proxy, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}
        log_message("Proxy is being used.", Fore.CYAN)
    
    return session

session = get_session_with_proxy_and_retries(proxy)

def get_color(pixel, header):
    try:
        response = session.get(f"{url}/image/get/{str(pixel)}", headers=header, timeout=10)
        if response.status_code == 401:
            return -1
        return response.json()['pixel']['color']
    except KeyError:
        return "#000000"
    except requests.exceptions.Timeout:
        log_message("Request timeout.", Fore.RED)
        return "#000000"
    except requests.exceptions.ConnectionError as e:
        log_message("Connection error.", Fore.RED)
        return "#000000"
    except requests.exceptions.RequestException as e:
        log_message("Request failed.", Fore.RED)
        return "#000000"

def claim(header):
    log_message("Claiming...", Fore.CYAN)
    try:
        session.get(f"{url}/mining/claim", headers=header, timeout=10)
    except requests.exceptions.RequestException as e:
        log_message("Claim request failed.", Fore.RED)

def get_pixel(x, y):
    return y * 1000 + x + 1

def get_pos(pixel, size_x):
    return pixel % size_x, pixel // size_x

def get_canvas_pos(x, y):
    return get_pixel(start_x + x - 1, start_y + y - 1)

def paint(canvas_pos, color, header):
    data = {"pixelId": canvas_pos, "newColor": color}
    try:
        response = session.post(f"{url}/repaint/start", data=json.dumps(data), headers=header, timeout=10)
        x, y = get_pos(canvas_pos, 1000)

        if response.status_code == 400:
            log_message("No energy left.", Fore.RED)
            return False
        if response.status_code == 401:
            return -1

        log_message(f"Painted at {x},{y}.", Fore.GREEN)
        return True
    except requests.exceptions.RequestException as e:
        log_message("Painting failed.", Fore.RED)
        return False

def fetch_mining_data(header):
    try:
        response = session.get(f"https://notpx.app/api/v1/mining/status", headers=header, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_balance = data.get('userBalance', 'Unknown')
            log_message(f"Balance: {user_balance}", Fore.MAGENTA)
        else:
            log_message("Failed to fetch mining data.", Fore.RED)
    except requests.exceptions.RequestException as e:
        log_message("Mining data request failed.", Fore.RED)

def process_accounts(accounts):
    first_account_start_time = datetime.now()
    for account in accounts:
        username = extract_username_from_initdata(account)
        log_message(f"Starting for {username}.", Fore.BLUE)
        main(account, account)

    time_elapsed = datetime.now() - first_account_start_time
    time_to_wait = timedelta(minutes=30) - time_elapsed

    if time_to_wait.total_seconds() > 0:
        log_message(f"Waiting {int(time_to_wait.total_seconds() // 60)} minutes.", Fore.YELLOW)
        time.sleep(time_to_wait.total_seconds())
    else:
        log_message("No wait needed.", Fore.YELLOW)

# Menu
def menu():
    while True:
        clear_terminal()  # Clear the terminal every time before showing the menu
        display_telegram_info()
        
        print(Fore.GREEN + "╔══════════════════════════════════════╗")
        print(Fore.GREEN + "║            Main Menu                 ║")
        print(Fore.GREEN + "╠══════════════════════════════════════╣")
        print(Fore.GREEN + "║ 1. Add Account                       ║")
        print(Fore.GREEN + "║ 2. View Accounts                     ║")
        print(Fore.GREEN + "║ 3. Delete Account                    ║")
        print(Fore.GREEN + "║ 4. Add Proxy                         ║")
        print(Fore.GREEN + "║ 5. View Proxies                      ║")
        print(Fore.GREEN + "║ 6. Delete Proxy                      ║")
        print(Fore.GREEN + "║ 7. Start Script                      ║")
        print(Fore.GREEN + "║ 8. Exit                              ║")
        print(Fore.GREEN + "╚══════════════════════════════════════╝")
        
        choice = input(Fore.CYAN + "\nChoose an option (1-8): ")
        
        clear_terminal()  # Clear the terminal before proceeding to the action
        
        if choice == '1':
            url = input("Enter the account URL: ")
            save_account(url)
        elif choice == '2':
            accounts = load_accounts_from_file()
            if accounts:
                print(Fore.YELLOW + "Accounts:")
                for acc in accounts:
                    print(acc)
            else:
                log_message("No accounts found.", Fore.RED)
            input(Fore.YELLOW + "\nPress Enter to continue...")  # Wait for user to press Enter
        elif choice == '3':
            delete_account()
        elif choice == '4':
            proxy = input("Enter proxy (format http://user:pass@ip:port): ")
            save_proxy(proxy)
        elif choice == '5':
            proxies = load_proxies()
            if proxies:
                print(Fore.YELLOW + "Proxies:")
                for proxy in proxies:
                    print(proxy)
            else:
                log_message("No proxies found.", Fore.RED)
            input(Fore.YELLOW + "\nPress Enter to continue...")  # Wait for user to press Enter
        elif choice == '6':
            delete_proxy()
        elif choice == '7':
            accounts = load_accounts_from_file()
            process_accounts(accounts)
        elif choice == '8':
            break
        else:
            log_message("Invalid choice.", Fore.RED)

if __name__ == "__main__":
    menu()
