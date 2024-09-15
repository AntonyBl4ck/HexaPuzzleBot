import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard  

import easyocr
import time
import random

reader = easyocr.Reader(['en'])

# Function to capture a screenshot
def capture_screen(region=None):
    img = pyautogui.screenshot(region=region)
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

# Function to find colored regions in an image
def find_colored_regions(image, color_range, min_area=6):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, color_range[0], color_range[1])
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cnt for cnt in contours if cv2.contourArea(cnt) >= min_area]

# Function to draw colored regions on an image
def draw_colored_regions(image, contours, color):
    cv2.drawContours(image, contours, -1, color, -1)

# Function to find colored regions with coordinates
def find_colored_regions_with_coordinates(image, color_range, min_area=6):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, color_range[0], color_range[1])
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_area]
    coordinates = [(int(cv2.moments(cnt)["m10"] / cv2.moments(cnt)["m00"]),
                    int(cv2.moments(cnt)["m01"] / cv2.moments(cnt)["m00"]))
                   for cnt in filtered_contours if cv2.moments(cnt)["m00"] != 0]
    
    return filtered_contours, coordinates

# Function to wait for keypresses to start and stop the clicking process
def wait_for_keypress():
    print("Press 'Ctrl + A' to start clicking.")
    while not key_pressed.is_set():
        time.sleep(0.1)
    print("Clicking started. Press 'Ctrl + S' to stop.")
    start_clicking.set()
    while not stop_clicking.is_set():
        time.sleep(0.1)
    print("Clicking stopped. Press 'Ctrl + A' to start again.")
# Function to set up hotkeys
def setup_hotkeys():
    keyboard.add_hotkey('ctrl+a', lambda: key_pressed.set())
    keyboard.add_hotkey('ctrl+s', lambda: stop_clicking.set())
    keyboard.add_hotkey('ctrl+q', lambda: stop_clicking.set())

def find_nearest_available_cell(coin_coord, available_cells):
    return min(available_cells, key=lambda cell: np.linalg.norm(np.array(coin_coord) - np.array(cell)), default=None)

def find_nearest_available_cell_for_same_color(lower_coin_coord, same_color_coords, available_cells):
    min_distance = float('inf')
    best_cell = None

    for upper_coin_coord in same_color_coords:
        for cell in available_cells:
            distance_to_upper_coin = np.linalg.norm(np.array(upper_coin_coord) - np.array(cell))
            
            if distance_to_upper_coin < min_distance:
                min_distance = distance_to_upper_coin
                best_cell = cell

    return best_cell

def match_and_move_coins(lower_coordinates, upper_coordinates, available_cells):
    for color, lower_coords in lower_coordinates.items():
        same_color_coords = upper_coordinates.get(color, [])
        for lower_coord in lower_coords:
            nearest_cell = find_nearest_available_cell_for_same_color(lower_coord, same_color_coords, available_cells)
            if nearest_cell:
                move_coin(lower_coord, nearest_cell)
                available_cells.remove(nearest_cell)
            else:
                print(f"No suitable available cell found for {color} coin at {lower_coord}")
                move_random_coin_to_random_cell(lower_coordinates, available_cells)

def move_coin(start_coord, end_coord):
    start_x = region_x + start_coord[0]
    start_y = region_y + start_coord[1] + (region_h - lower_region_height)
    end_x = region_x + end_coord[0]
    end_y = region_y + end_coord[1]

    pyautogui.moveTo(start_x, start_y)
    time.sleep(0.1)
    pyautogui.mouseDown(start_x, start_y)
    pyautogui.moveTo(end_x, end_y + 50, duration=0.7)
    pyautogui.mouseUp()

    print(f"Moved coin from {start_coord} to {end_coord}")            
def move_random_coin_to_random_cell(lower_coordinates, available_cells):
    if not lower_coordinates or not available_cells:
        return

    random_color = random.choice(list(lower_coordinates.keys()))
    random_coin_coord = random.choice(lower_coordinates[random_color])
    random_available_cell = random.choice(available_cells)

    move_coin(random_coin_coord, random_available_cell)
    available_cells.remove(random_available_cell)

color_ranges = {
    "red": ((0, 100, 100), (10, 255, 255)),
    "orange": ((10, 100, 100), (25, 255, 255)),
    "yellow": ((25, 100, 100), (35, 255, 255)),
    "green": ((35, 100, 100), (70, 255, 255)),
    "blue": ((85, 100, 100), (125, 255, 255)),
    "purple": ((125, 100, 100), (150, 255, 255)),
    "field": ((0, 0, 224), (180, 20, 245))
}

display_colors = {
    "red": (0, 0, 255),
    "orange": (0, 165, 255),
    "green": (0, 255, 0),
    "purple": (255, 0, 255),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "field": (64, 64, 64)
}

def display_in_window(fps=60):
    try:
        delay = 1 / fps
        screen_res = (1920, 1080)
        global region_x, region_y, region_w, region_h, lower_region_height
        region_x = 3 * screen_res[0] // 4
        region_y = 0
        region_w = screen_res[0] // 4
        region_h = screen_res[1] - 100
        region = (region_x, region_y, region_w, region_h)

        cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)
        
        min_area_lower = 2000
        min_area_upper = 1500
        min_area_field = 500
        
        while True:
            start_time = time.time()
            img_np = capture_screen(region)
 
            lower_region_height = int(region_h * 0.2)
            lower_region = img_np[-lower_region_height:]
            upper_region = img_np[:-lower_region_height]
            
            ignore_zone_height = int(region_h * 0.3)
            analyzable_region_height = region_h - ignore_zone_height
            analyzable_region = upper_region[:analyzable_region_height]

            coin_colors_lower = {}
            lower_contours_dict = {}
            lower_coordinates = {}
            for color_name, color_range in color_ranges.items():
                if color_name != "field":
                    contours, coordinates = find_colored_regions_with_coordinates(lower_region, color_range, min_area=min_area_lower)
                    if contours:
                        lower_contours_dict[color_name] = contours
                        coin_colors_lower[color_name] = len(contours)
                        lower_coordinates[color_name] = coordinates
                        draw_colored_regions(lower_region, contours, display_colors[color_name])
                        print(f"Lower region - {color_name.capitalize()}: {coordinates}")
            
            # Analyze the analyzable part of the upper region for colored coins with minimum area of 1500 pixels
            coin_colors_upper = {}
            upper_coordinates = {}
            for color_name, color_range in color_ranges.items():
                if color_name != "field":
                    contours, coordinates = find_colored_regions_with_coordinates(analyzable_region, color_range, min_area=min_area_upper)
                    if contours:
                        coin_colors_upper[color_name] = len(contours)
                        upper_coordinates[color_name] = coordinates
                        draw_colored_regions(analyzable_region, contours, display_colors[color_name])
                        # Print the coordinates of detected coins
                        print(f"Upper region - {color_name.capitalize()}: {coordinates}")
            
            # Analyze upper region for empty cells
            field_contours, field_coordinates = find_colored_regions_with_coordinates(analyzable_region, color_ranges["field"], min_area=min_area_field)
            available_cells = field_coordinates
            
            # Display results in console
            if coin_colors_lower:
                print("Coins in the lower region with minimum area of 2000 pixels:")
                for color_name, count in coin_colors_lower.items():
                    print(f"{color_name.capitalize()} (Display color: {display_colors[color_name]}): {count} found")
            else:
                print("No coins found in the lower region with the minimum area of 2000 pixels.")
            
            if coin_colors_upper:
                print("Coins in the upper region with minimum area of 1500 pixels (excluding the top 30%):")
                for color_name, count in coin_colors_upper.items():
                    print(f"{color_name.capitalize()} (Display color: {display_colors[color_name]}): {count} found")
            else:
                print("No coins found in the upper region with the minimum area of 1500 pixels (excluding the top 30%).")
            
            # Print available cells information and their coordinates
            print(f"Available cells in the analyzable part of the upper region (with minimum area of 500 pixels): {len(available_cells)}")
            if available_cells:
                print("Coordinates of available cells:")
                for coord in available_cells:
                    print(f"Cell at: {coord}")
            else:
                print("No available cells found in the upper region.")
                if not find_and_click_claim(region):
                    print("Claim button not found. Moving to random free slot.")
            
            # Draw detected regions on the full image
            for color_name, color_range in color_ranges.items():
                contours = find_colored_regions(img_np, color_range, min_area=6)
                draw_colored_regions(img_np, contours, display_colors[color_name])

            if start_clicking.is_set() and not stop_clicking.is_set():
                match_and_move_coins(lower_coordinates, upper_coordinates, available_cells)

            cv2.imshow("Screen Capture", img_np)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(max(0, delay - (time.time() - start_time)))
        
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error in display_in_window: {e}")
def convert_to_screen_coordinates(center, region):
    region_x, region_y, region_w, region_h = region
    x, y = center
    return region_x + x, region_y + y

def find_and_click_text(region, text_to_find, ignore_position_check=False):
    img_np = capture_screen(region)
    img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    results = reader.readtext(img_rgb)

    screen_height = pyautogui.size().height 
    for result in results:
        text = result[1]
        if text_to_find.lower() in text.lower():
            x1, y1 = int(result[0][0][0]), int(result[0][0][1])
            x2, y2 = int(result[0][2][0]), int(result[0][2][1])
            x = (x1 + x2) // 2
            y = (y1 + y2) // 2

            fx, fy = convert_to_screen_coordinates((x, y), region)

            if ignore_position_check or fy > screen_height // 2:
                print(f"Found '{text_to_find}' button at ({fx}, {fy}), clicking.")
                pyautogui.moveTo(fx, fy, duration=0.3)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                return (fx, fy) 

    return False   

def find_and_click_text2(region, text_to_find):
    img_np = capture_screen(region)
    img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    results = reader.readtext(img_rgb)

    for result in results:
        text = result[1]
        if text_to_find.lower() in text.lower():
            x1, y1 = int(result[0][0][0]), int(result[0][0][1])
            x2, y2 = int(result[0][2][0]), int(result[0][2][1])
            x = (x1 + x2) // 2
            y = (y1 + y2) // 2

            fx, fy = convert_to_screen_coordinates((x, y), region)
            print(f"Found '{text_to_find}' button at ({fx}, {fy}), clicking.")
            pyautogui.moveTo(fx, fy, duration=0.3)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            return True

    return False

def find_and_click_claim(region):
    try:
        screen_height = pyautogui.size().height  

        claim_pos = find_and_click_text(region, "Claim")
        if claim_pos and claim_pos[1] > screen_height // 2:
            time.sleep(1)

            # Attempt to find and click "Hexa Puzzle"
            while True:
                try:
                    if find_and_click_text2(region, "Hexa Puzzle"):
                        print("Found and clicked 'Hexa Puzzle'.")
                        break
                except Exception as e:
                    print(f"Error while clicking 'Hexa Puzzle': {e}")
                time.sleep(1)

            time.sleep(1)

            # Attempt to find and click "Play"
            while True:
                try:
                    play_pos = find_and_click_text(region, "Play")
                    if play_pos and play_pos[1] > screen_height // 2:
                        print("Found and clicked 'Play'.")
                        break
                except Exception as e:
                    print(f"Error while clicking 'Play': {e}")
                time.sleep(1)

            return True

        return False
    
    except Exception as e:
        print(f"Error in find_and_click_claim: {e}")
        return False


key_pressed = threading.Event()
start_clicking = threading.Event()
stop_clicking = threading.Event()

setup_hotkeys()

display_thread = threading.Thread(target=display_in_window)
display_thread.start()

wait_for_keypress()
