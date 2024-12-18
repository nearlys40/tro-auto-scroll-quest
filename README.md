# **The Ragnarok Auto Scroll Quest**

Automate quest actions in the TRO game using Python. This project interacts with the game screen (PC Version), identifies regions using template matching, and performs automated actions.

---

## **Table of Contents**
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Support](#support)

---

## **Features**
- **Automated Quest Scroll Activation**: Automatically finds and activates quest scrolls in the game.
- **Bag Management**: Opens the in-game bag to search for quest scrolls and closes it when done.
- **Respawn Handling**: Detects when the character dies and automatically respawns at the starting location.
- **Template Matching for Actions**: Uses images to identify specific game elements like quest buttons, scrolls, and menus.
- **Resolution Independence**: Supports various screen sizes by using a ratio-based coordinate system.
- **Fail-Safe Mechanism**: Ensures the script doesn't crash during unexpected situations by logging progress and retrying actions.
- **Customizable Regions**: Easily adjust screen regions to fit different emulator or game layouts.

---

## **Prerequisites**

### **Software Requirements**
- The Ragnarok [(PC Version)](https://theragnaroksea.com/clientdownload) in full screen mode
- Python 3.7 or higher
- pip (Python package manager)

---

## **Installation**

### **Python Libraries**
Install the following libraries:
```bash
pip install pyautogui pygetwindow opencv-python numpy pynput pywin32
```

---

## **Usage**

### **Running the script**

Start the automation with:
```bash
python main.py
```

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.


---

## **Support**

If you encounter any issues or have questions, please open an issue on GitHub or contact me at [visut.savangsuk@gmail.com](#visut.savangsuk@gmail.com)