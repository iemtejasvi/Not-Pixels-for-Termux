# No longer maintained/halted

# Not-Pixels for Termux

This Python script automates interactions with the **NotPixel** API, allowing users to manage accounts and proxies for painting pixels and claiming rewards on the NotPixel platform. The script is optimized for **Termux** on Android and other **bash environments**, making it ideal for use on mobile devices or lightweight Linux systems.

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

Before running the script, you need to install **Git** and **Python** in Termux. Use the following commands to install the necessary packages:

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

### 3. Install Required Python Packages Manually

Since there’s no `requirements.txt` file, you’ll need to manually install the required Python libraries. Use the following commands to install them:

- **Requests**: For handling HTTP requests.
- **Pillow**: For image processing.
- **Colorama**: For terminal text coloring.

Install these dependencies in Termux by running:

```bash
pip install requests
pkg install python-pillow
pip install colorama
pkg install python libjpeg-turbo libpng zlib freetype
```

Once these packages are installed, you’ll be ready to run the script.

### 4. Retrieve API Data

To interact with the **NotPixel** platform, you need your **authorization token**. Follow these steps to retrieve the necessary data:

#### How to Retrieve API Data:

1. Install the Telegram app on your PC (do **not** log in through a browser; use the web app).
2. Open Telegram, navigate to **Settings** > **Advanced** > **Experimental Settings**, and enable **Webview Inspecting**.
3. Search for "Not Pixels" in Telegram and ensure the account has a blue check mark, confirming it's official.
4. Open the official account and click on **Play Game** to start.
5. Press `Ctrl + Shift + J` to open the inspection console.
6. In the console, type `allow pasting` manually, then paste the following:
   ```javascript
   copy(Telegram.WebApp.initData)
   ```
   You should see "undefined," indicating you've successfully copied the data.
7. Paste this data into a Notepad or directly into the script.

For a more detailed guide, refer to this [video tutorial](https://youtu.be/K66LMX513n4?si=aR5o_VMaVnget6t_).

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
python main.py
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

