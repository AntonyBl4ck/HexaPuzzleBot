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
Installation:
Clone this repository or download the project files:


pip install opencv-python numpy pyautogui keyboard easyocr
Verify the installation of the following packages:

opencv-python
numpy
pyautogui
keyboard
easyocr

Running the Script
Launch the Hamster Kombat Hexa Puzzle game on your computer.

Open a terminal and navigate to the project folder.

The bot will begin analyzing the game window. Use the following hotkeys to control the bot:

Ctrl + A: Start moving coins.
Ctrl + S: Stop the bot from moving coins.
Make sure the game window is visible and positioned correctly on your screen for the bot to detect game elements accurately.

The bot detects colored coins using OpenCV and moves them using PyAutoGUI.
Use EasyOCR to detect game text like "Claim" and "Play" for automated interaction.
The script runs in a separate thread for efficient operation and allows hotkey-based interaction.
