import cv2
import numpy as np
import mss
import mss.tools

# Function that captures screenshot
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
    
def find_template(screenshot, template_path, threshold=0.8):
    template = cv2.imread(template_path)