#import PIL
import requests
import json
import time
import random
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse
import os

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

# ANSI escape codes for colors (no need for colorama in Termux)
class Colors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    LIGHTBLACK_EX = "\033[90m"

# Telegram Info
def display_telegram_info():
    print(Colors.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Colors.CYAN + " Follow me on Telegram: @virtusoses")
    print(Colors.CYAN + " Telegram Channel: https://t.me/virtusoses")
    print(Colors.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Colors.RESET)

# Clear terminal
def clear_terminal():
    os.system('clear')

def get(path):
    space = ' '
    hash_sym = '#'
    dot = '.'
    star = '*'

    return [
        [space] * 15 + [hash_sym] * 10 + [space] * 15,
    ]

image = get("")

c = {
    '#': "#000000",
    '.': "#3690EA",
    '*': "#ffffff"
}

def log_message(message, color=Colors.RESET):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{Colors.LIGHTBLACK_EX}{current_time}{Colors.RESET} {color}{message}{Colors.RESET}")

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
    log_message("Account saved.", Colors.GREEN)

# Delete an account from file
def delete_account():
    accounts = load_accounts_from_file()
    if not accounts:
        log_message("No accounts to delete.", Colors.RED)
        return
    print("\nSelect account to delete:")
    for idx, acc in enumerate(accounts, start=1):
        print(f"{Colors.YELLOW}{idx}. {acc}{Colors.RESET}")
    choice = input(Colors.CYAN + "\nEnter the number: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(accounts):
            del accounts[choice]
            with open(account_file, 'w') as file:
                file.writelines([f"{acc}\n" for acc in accounts])
            log_message("Account deleted.", Colors.GREEN)
        else:
            log_message("Invalid choice.", Colors.RED)
    except ValueError:
        log_message("Invalid input.", Colors.RED)

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
    log_message("Proxy saved.", Colors.GREEN)

# Delete a proxy from file
def delete_proxy():
    proxies = load_proxies()
    if not proxies:
        log_message("No proxies to delete.", Colors.RED)
        return
    print("\nSelect proxy to delete:")
    for idx, proxy in enumerate(proxies, start=1):
        print(f"{Colors.YELLOW}{idx}. {proxy}{Colors.RESET}")
    choice = input(Colors.CYAN + "\nEnter the number: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(proxies):
            del proxies[choice]
            with open(proxy_file, 'w') as file:
                file.writelines([f"{proxy}\n" for proxy in proxies])
            log_message("Proxy deleted.", Colors.GREEN)
        else:
            log_message("Invalid choice.", Colors.RED)
    except ValueError:
        log_message("Invalid input.", Colors.RED)

def load_proxy_from_file(filename=proxy_file):
    proxies = load_proxies()
    if not proxies:
        log_message("No proxy found, proceeding without proxy.", Colors.YELLOW)
        return None
    
    return random.choice(proxies)

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
        log_message("Using proxy.", Colors.CYAN)
    
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
        log_message("Request timed out.", Colors.RED)
        return "#000000"
    except requests.exceptions.ConnectionError:
        log_message("Connection error.", Colors.RED)
        return "#000000"
    except requests.exceptions.RequestException:
        log_message("Request failed.", Colors.RED)
        return "#000000"

def claim(header):
    log_message("Claiming mining reward.", Colors.CYAN)
    try:
        session.get(f"{url}/mining/claim", headers=header, timeout=10)
    except requests.exceptions.RequestException:
        log_message("Failed to claim reward.", Colors.RED)

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
            log_message("Out of energy.", Colors.RED)
            return False
        if response.status_code == 401:
            return -1

        log_message(f"Painted pixel at {x},{y}.", Colors.GREEN)
        return True
    except requests.exceptions.RequestException:
        log_message("Painting failed.", Colors.RED)
        return False

def extract_username_from_initdata(init_data):
    decoded_data = urllib.parse.unquote(init_data)
    username_start = decoded_data.find('"username":"') + len('"username":"')
    username_end = decoded_data.find('"', username_start)
    
    if username_start != -1 and username_end != -1:
        return decoded_data[username_start:username_end]
    
    return "Unknown"

def fetch_mining_data(header):
    try:
        response = session.get(f"https://notpx.app/api/v1/mining/status", headers=header, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_balance = data.get('userBalance', 'Unknown')
            log_message(f"Your balance is {user_balance}.", Colors.MAGENTA)
        else:
            log_message("Failed to get mining data.", Colors.RED)
    except requests.exceptions.RequestException:
        log_message("Mining data request failed.", Colors.RED)

def main(auth, account):
    headers = {'authorization': auth}
    try:
        fetch_mining_data(headers)
        claim(headers)

        size = len(image) * len(image[0])
        order = [i for i in range(size)]
        random.shuffle(order)

        for pos_image in order:
            x, y = get_pos(pos_image, len(image[0]))
            time.sleep(0.05 + random.uniform(0.01, 0.1))
            try:
                color = get_color(get_canvas_pos(x, y), headers)
                if color == -1:
                    log_message("Authorization failed.", Colors.RED)
                    print(headers["authorization"])
                    break
                if image[y][x] == ' ' or color == c[image[y][x]]:
                    continue

                result = paint(get_canvas_pos(x, y), c[image[y][x]], headers)
                if result == -1:
                    log_message("Authorization expired.", Colors.RED)
                    print(headers["authorization"])
                    break
                elif result:
                    continue
                else:
                    break

            except IndexError:
                log_message("Index error.", Colors.RED)
    except requests.exceptions.RequestException:
        log_message(f"Connection error for {account}.", Colors.RED)

def process_accounts(accounts):
    first_account_start_time = datetime.now()
    for account in accounts:
        username = extract_username_from_initdata(account)
        log_message(f"Processing account {username}.", Colors.BLUE)
        main(account, account)

    time_elapsed = datetime.now() - first_account_start_time
    time_to_wait = timedelta(minutes=30) - time_elapsed

    if time_to_wait.total_seconds() > 0:
        log_message(f"Waiting for {int(time_to_wait.total_seconds() // 60)} minutes.", Colors.YELLOW)
        time.sleep(time_to_wait.total_seconds())
    else:
        log_message("No wait time required.", Colors.YELLOW)

# Menu
def menu():
    while True:
        clear_terminal()  # Clear the terminal every time before showing the menu
        display_telegram_info()
        
        print(Colors.GREEN + "╔══════════════════════════════════════╗")
        print(Colors.GREEN + "║           Main Menu                 ║")
        print(Colors.GREEN + "╠══════════════════════════════════════╣")
        print(Colors.GREEN + "║ 1. Add Account                      ║")
        print(Colors.GREEN + "║ 2. View Accounts                    ║")
        print(Colors.GREEN + "║ 3. Delete Account                   ║")
        print(Colors.GREEN + "║ 4. Add Proxy                        ║")
        print(Colors.GREEN + "║ 5. View Proxies                     ║")
        print(Colors.GREEN + "║ 6. Delete Proxy                     ║")
        print(Colors.GREEN + "║ 7. Start Script                     ║")
        print(Colors.GREEN + "║ 8. Exit                             ║")
        print(Colors.GREEN + "╚══════════════════════════════════════╝")
        
        choice = input(Colors.CYAN + "\nChoose an option (1-8): ")
        
        clear_terminal()  # Clear the terminal before proceeding to the action
        
        if choice == '1':
            url = input("Enter the account URL: ")
            save_account(url)
        elif choice == '2':
            accounts = load_accounts_from_file()
            if accounts:
                print(Colors.YELLOW + "Accounts:")
                for acc in accounts:
                    print(acc)
            else:
                log_message("No accounts found.", Colors.RED)
            input(Colors.YELLOW + "\nPress Enter to continue...")  # Wait for user to press Enter
        elif choice == '3':
            delete_account()
        elif choice == '4':
            proxy = input("Enter proxy (format http://user:pass@ip:port): ")
            save_proxy(proxy)
        elif choice == '5':
            proxies = load_proxies()
            if proxies:
                print(Colors.YELLOW + "Proxies:")
                for proxy in proxies:
                    print(proxy)
            else:
                log_message("No proxies found.", Colors.RED)
            input(Colors.YELLOW + "\nPress Enter to continue...")  # Wait for user to press Enter
        elif choice == '6':
            delete_proxy()
        elif choice == '7':
            accounts = load_accounts_from_file()
            process_accounts(accounts)
        elif choice == '8':
            break
        else:
            log_message("Invalid choice.", Colors.RED)

if __name__ == "__main__":
    menu()
