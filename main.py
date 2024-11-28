import pyautogui
from pynput import mouse
import cv2
import numpy as np
import ctypes
import time

# Constants for mouse events
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
x_ratio = 1
y_ratio = 1

# Define paths and regions
IMAGE_PATHS = {
    "question_mark": "images/question-mark.png",
    "scroll": "images/scroll.png",
    "bag": "images/bag.png",
    "x_mark": "images/x-mark.png",
}

REGIONS = {
    "question_mark": (int(180 * x_ratio), int(350 * y_ratio), int(50 * x_ratio), int(50 * y_ratio)),
    "scroll": (int(840 * x_ratio), int(300 * y_ratio), int(710 * x_ratio), int(350 * y_ratio)),
    "bag": (int(1690 * x_ratio), int(360 * y_ratio), int(50 * x_ratio), int(50 * y_ratio)),
    "x_mark": (int(1690 * x_ratio), int(410 * y_ratio), int(50 * x_ratio), int(50 * y_ratio))
}


# Helper Functions
def click_at(x, y):
    """Simulates a mouse click at the specified screen coordinates."""
    time.sleep(1)
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def click_at2(x, y):
    """Simulates a mouse click at the specified screen coordinates."""
    x_with_ratio = int(x * x_ratio)
    y_with_ratio = int(y * y_ratio)

    time.sleep(1)

    ctypes.windll.user32.SetCursorPos(x_with_ratio, y_with_ratio)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, x_with_ratio, y_with_ratio, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, x_with_ratio, y_with_ratio, 0, 0)


def update_ratio_from_your_screen_size():
    # My screen size is (1920, 1080)
    # Get your screen width and height
    screen_width, screen_height = pyautogui.size()
    global x_ratio, y_ratio
    x_ratio = screen_width / 1920
    y_ratio = screen_height / 1080

def on_move(x, y):
    # Get the RGB color of the pixel at the current mouse position

    x_with_ratio = int(x * x_ratio)
    y_with_ratio = int(y * y_ratio)

    color = pyautogui.pixel(x_with_ratio, y_with_ratio)
    print(f"Mouse moved to ({x_with_ratio}, {y_with_ratio}) with color: {color}")


def is_quest_finished():
    x, y, target_color, tolerance = int(472 * x_ratio), int(360 * y_ratio), (247, 85, 82), 0

    # Get the pixel color at (x, y)
    pixel_color = pyautogui.pixel(x, y)

    # Check if the pixel color is within the tolerance range
    for i in range(3):  # Compare R, G, B channels
        if abs(pixel_color[i] - target_color[i]) > tolerance:
            return False
    return True


def match_template(target_image, region, confidence=0.8):
    """
    Matches a template image within a specified region of the screen.
    Returns the match status and coordinates of the center of the matched area.
    """
    time.sleep(1)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"Actual/Confidence (%) : {(max_val * 100):.2f}/{confidence * 100}")

    if max_val >= confidence:
        template_height, template_width = template.shape
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2
        return True, region[0] + center_x, region[1] + center_y
    return False, 0, 0


# Quest Management Functions
def is_already_have_quest():
    """Checks if the 'question mark' image is present."""
    print("Checking if the quest is already taken...")
    return match_template(IMAGE_PATHS["question_mark"], REGIONS["question_mark"], confidence=0.7)[0]


def find_scroll_in_the_bag():
    """Looks for the scroll image within the bag region."""
    print("Searching for the scroll in the bag...")
    return match_template(IMAGE_PATHS["scroll"], REGIONS["scroll"], confidence=0.8)


def check_pop_up_window():
    """Check the pop-up window at the screen."""
    print("Check pop-up window...")
    return match_template(IMAGE_PATHS["x_mark"], REGIONS["x_mark"], confidence=0.8)


def open_the_bag():
    """Opens the bag by clicking its icon."""
    print("Opening the bag...")
    found, x, y = match_template(IMAGE_PATHS["bag"], REGIONS["bag"], confidence=0.8)
    if found:
        click_at(x, y)
    else:
        print("Bag icon not found.")


def close_the_bag():
    """Closes the bag by clicking a fixed location."""
    print("Closing the bag...")
    click_at2(1600, 150)


def auto_scroll_quest():
    """Main logic for handling the quest scrolls."""
    if is_already_have_quest():
        if is_quest_finished():
            print("Quest finished. Clicking to turn in the quest.")
            click_at2(180, 350)
            click_at2(180, 350)
    else:
        found1, x1, y1 = check_pop_up_window()
        if found1:
            click_at(x1, y1)

        open_the_bag()

        found2, x2, y2 = find_scroll_in_the_bag()
        if found2:
            print("Scroll found. Using it...")
            click_at(x2, y2)  # Click the scroll
            click_at2(980, 910)  # Use the scroll
            close_the_bag()
            print("Activating the quest...")
            click_at2(180, 350)
        else:
            print("Scroll not found.")
            close_the_bag()


# Main Function
def main():
    # Set up a listener for mouse movements
    # with mouse.Listener(on_move=on_move) as listener:
    #     print("Move the mouse to see the pixel color. Press Ctrl+C to exit.")
    #     listener.join()

    # ------------------------------------------------------------------------------- #

    try:
        update_ratio_from_your_screen_size()
        print("Script is running...")
        while True:
            auto_scroll_quest()
            time.sleep(10)  # Delay between iterations
    except KeyboardInterrupt:
        print("\nProgram interrupted by Ctrl + C")


if __name__ == "__main__":
    main()
