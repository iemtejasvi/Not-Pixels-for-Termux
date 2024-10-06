# Not-Pixels for Termux

This Python script automates interactions with the **NotPixel** API, allowing users to manage accounts and proxies for painting pixels and claiming rewards on the NotPixel platform. The script is optimized for **Termux** on Android and **bash environments**, making it ideal for use on mobile devices or lightweight Linux systems.

## Features

- Automatically claims rewards and paints pixels on the NotPixel platform.
- Supports multiple accounts and proxies with an interactive interface.
- Provides real-time feedback on painting operations and account balances.
- Optimized for **Termux** (no emojis, minimal dependencies).
- Can run in the background for long-term automation.

## Requirements

- **Python 3.x** (Ensure it's installed in your Termux or bash environment).
- **Termux** on Android or **any bash-compatible terminal** on Linux systems.

## Installation and Setup

### 1. Install Git and Python in Termux

Before running the script, install **Git** and **Python** in Termux. Use the following commands to install the necessary packages:

#### Update and Upgrade Termux:

```bash
pkg update && pkg upgrade
```

#### Install Git:

```bash
pkg install git
```

#### Install Python:

```bash
pkg install python
```

### 2. Clone the Repository

Once Git is installed, clone the Not-Pixels script repository:

```bash
git clone https://github.com/iemtejasvi/Not-Pixels-for-Termux.git
cd Not-Pixels-for-Termux
```

### 3. Install Required Python Packages

#### a. Using `requirements.txt`:

If a `requirements.txt` file exists, you can install all dependencies using:

```bash
pip install -r requirements.txt
```

#### b. Manually Installing Dependencies:

If there is no `requirements.txt`, install the required libraries manually:

- **Requests**: For handling HTTP requests.
- **Pillow**: For image processing.

Run the following commands:

```bash
pip install requests
pip install pillow
```

Once dependencies are installed, you're ready to run the script.

### 4. Retrieve API Data

To interact with the **NotPixel** platform, you need your **authorization token**. Follow these steps to retrieve the necessary data:

#### How to Retrieve API Data:

1. Go to the **NotPixel** website and log into your account.
2. Open the developer tools in your browser (press `F12` or `Ctrl + Shift + I`).
3. Navigate to the **Network** tab and filter requests related to the NotPixel API.
4. Find a request that contains the `Authorization` header.
5. Copy the `Authorization` token and save it in a text file or provide it directly to the script when prompted.

### 5. Running the Script

Once you have your **Authorization** token, you can run the script with:

```bash
python main.py
```

The script will guide you through the process of adding accounts and proxies.

## Account and Proxy Management

The script provides an interactive menu for managing accounts and proxies:

- **Add a new account**: Paste your **Authorization** token.
- **View all accounts**: Lists all saved accounts.
- **Delete an account**: Removes a selected account.
- **Add a proxy**: Add HTTP/S proxies for connection.
- **View all proxies**: Lists all saved proxies.
- **Delete a proxy**: Removes a selected proxy.

## Running the Script on Mobile Termux

The script is optimized for Termux, making it ideal for running on mobile devices. You can run the script in the background on Android using **tmux** or **wake lock** features to prevent your device from sleeping during execution.

### 1. Keep the Script Running in the Background

To keep the script running in the background, use **tmux**:

#### Install tmux:

```bash
pkg install tmux
```

#### Start a tmux session and run the script:

```bash
tmux new -s notpixel
python notpixel.py
```

To **detach** from the session without stopping the script, press:

```
Ctrl + B, then D
```

### 2. Reattach the tmux Session

If you want to check the script's progress, reattach the session with:

```bash
tmux attach -t notpixel
```

## Conclusion

The **Not-Pixels for Termux** script is a lightweight, mobile-friendly automation tool designed for seamless interaction with the NotPixel platform. It can be run efficiently on Android devices or lightweight Linux systems, making it ideal for long-term automation tasks.
