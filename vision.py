import cv2
import numpy as np
import mss
import mss.tools

#function that captures screenshot
def screen_capture(region=None):
    with mss.mss() as sct:
        if region:
            monitor={
                "top": region[1],
                "left": region[0],
                "width": region[2],
                "height": region[3]
            }
        else: #if user doesnt select region, capture whole screen
            monitor = sct.monitors[1]
        
        #captures the screenshot
        screenshot = sct.grab(monitor)
        #converts said screenshot to a numpy array and then to a format that opencv can read
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

# Function that finds template image in screenshot and returns the coordinates 
def find_template(screenshot, template_path, threshold=0.8): #threshold is the minimum similarity score for a match to be considered valid (1 is perfect match)
    template = cv2.imread(template_path)

    if template is None:
        raise FileNotFoundError(f"Template image was not found: {template_path}")
    # Convert both images to grayscale for template matching (colors can interfere with matching)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # OpenCVs template matching function
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    #This looks for the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #is the best match above threshold?
    if max_val >= threshold:
        #returns the center of the matching image (Standard is top left)
        template_h, template_w = template_gray.shape
        center_x = max_loc[0] + template_w // 2
        center_y = max_loc[1] + template_h // 2
        return (center_x, center_y), max_val
    
    return None, max_val

#combines the 2 functions above to find the tree and return its coordinates and confidence score
def find_tree(template_path="templates/tree.png", threshold=0.8, region=None):
    screenshot = screen_capture(region=region)
    position, confidence = find_template(screenshot, template_path, threshold)
    return position, confidence

#calculates the position of slot 28
def get_slot28_position(inventory_region):
    inv_x, inv_y, inv_w, inv_h = inventory_region
    slot_w = inv_w / 4  # 4 columns
    slot_h = inv_h / 7  # 7 rows

    #slot 28
    slot_x = int(inv_x + 3 * slot_w + slot_w / 2)
    slot_y = int(inv_y + 6 * slot_h + slot_h / 2)
    return slot_x, slot_y

#checks if slot 28 is occupied by analyzing the color of the slot
def is_inventory_full(inventory_region, empty_slot_color=(55, 64, 73), tolerance=20):
    slot_x, slot_y = get_slot28_position(inventory_region)

    #capture a small area around the center of slot 28
    slot_size = 10
    slot_region = (slot_x - slot_size, slot_y - slot_size, slot_size * 2, slot_size * 2)
    screenshot = screen_capture(region=slot_region)

    #calculate average color of the slot
    avg_color = screenshot.mean(axis=(0, 1))  #average BGR
    b, g, r = avg_color

    #compare to the known empty slot color
    eb, eg, er = empty_slot_color
    if abs(b - eb) < tolerance and abs(g - eg) < tolerance and abs(r - er) < tolerance:
        return False  #slot is empty, inventory not full
    return True  #slot is occupied, inventory full