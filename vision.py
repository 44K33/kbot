import cv2
import numpy as np
import mss

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

#finds a tree by detecting the cyan color marker in the game region
def find_tree(region=None):
    screenshot = screen_capture(region=region)

    #convert to HSV for color detection
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    #cyan HSV range
    lower_cyan = np.array([85, 100, 100])
    upper_cyan = np.array([95, 255, 255])

    #create a mask of all cyan pixels
    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)

    #find all contours (connected cyan areas) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, 0.0

    #pick the largest cyan area (most likely the tree marker)
    largest = max(contours, key=cv2.contourArea)

    #only return if the area is large enough to be a real marker
    if cv2.contourArea(largest) < 50:
        return None, 0.0

    #calculate center of the largest contour
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, 0.0

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    return (cx, cy), 1.0

#checks if an xp drop is visible in the xp drop region
def check_xp_drop(xp_region):
    screenshot = screen_capture(region=xp_region)

    #convert to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    #threshold to isolate bright pixels (xp drop text is bright yellow/white)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    #count bright pixels
    bright_pixels = cv2.countNonZero(thresh)

    #if enough bright pixels are present, an xp drop is visible
    return bright_pixels > 50