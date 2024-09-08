This Python script automates the gameplay of Hamster Kombat Hexa Puzzle using computer vision, color detection, and screen automation. The script detects game elements and moves pieces based on predefined logic. It uses threading and hotkeys to control the bot's operation, allowing you to start, stop, and quit the automation with ease.

Features:
Detects game elements (coins and cells) using OpenCV and color recognition.
Automatically moves coins to the best available positions based on game logic.
Uses EasyOCR for detecting in-game text and triggering specific actions.
Thread-based operation with customizable hotkeys for starting and stopping automation.
Installation Guide
Prerequisites:
Ensure that Python 3.x is installed.
Install pip, the Python package manager.




Here's a step-by-step guide for setting up the Python bot and Windows Subsystem for Android (WSA) to run your HexaPuzzleBot from GitHub:

1. Install Python
Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
During installation, ensure the Add Python to PATH option is checked.
2. Install Required Python Libraries
Open a terminal (Command Prompt or PowerShell).
Install the necessary packages:
pip install opencv-python numpy pyautogui keyboard easyocr
3. Set Up Windows Subsystem for Android (WSA)
Open Microsoft Store and search for "Windows Subsystem for Android™".
Install the WSA package and enable developer mode in WSA settings.
Download the Telegram APK.
4. Run the Bot
Launch the game on your WSA or Android emulator.
Navigate to the bot’s project folder and run the script:python HexaBot.py


Use hotkeys like Ctrl+A to start automation and Ctrl+S to stop.

The bot detects colored coins using OpenCV and moves them using PyAutoGUI.
Use EasyOCR to detect game text like "Claim" and "Play" for automated interaction.
The script runs in a separate thread for efficient operation and allows hotkey-based interaction.
