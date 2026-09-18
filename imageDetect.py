import cv2
import mss 
import numpy as np
import logging

def findIconConfidenceEdge(templatePath, top=0, left=0, width=0, height=0):
    template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logging.error(f"Failed to load template image at path: {templatePath}")
        return 0.0

    with mss.mss() as sct:
        if width == 0 or height == 0:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

        region = {'top': top, 'left': left, 'width': width, 'height': height}
        screenshot = sct.grab(region)

    img = np.array(screenshot)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    if gray_img.shape[0] < template.shape[0] or gray_img.shape[1] < template.shape[1]:
        return 0.0

    # Extract Canny edges for both (ignores interior/exterior background fills)
    img_edges = cv2.Canny(gray_img, 100, 200)
    temp_edges = cv2.Canny(template, 100, 200)

    # Standard TM_CCOEFF_NORMED works reliably on edge maps
    result = cv2.matchTemplate(img_edges, temp_edges, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return float(max_val), (left + max_loc[0], top + max_loc[1])

def findIconConfidenceEdgeCenter(templatePath, top=0, left=0, width=0, height=0):
    template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logging.error(f"Failed to load template image at path: {templatePath}")
        return 0.0

    with mss.mss() as sct:
        if width == 0 or height == 0:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

        region = {'top': top, 'left': left, 'width': width, 'height': height}
        screenshot = sct.grab(region)

    img = np.array(screenshot)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    if gray_img.shape[0] < template.shape[0] or gray_img.shape[1] < template.shape[1]:
        return 0.0

    # Extract Canny edges for both (ignores interior/exterior background fills)
    img_edges = cv2.Canny(gray_img, 100, 200)
    temp_edges = cv2.Canny(template, 100, 200)

    # Standard TM_CCOEFF_NORMED works reliably on edge maps
    result = cv2.matchTemplate(img_edges, temp_edges, cv2.TM_CCOEFF_NORMED)
    
    temp_height, temp_width = template.shape[:2]
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    center_x = left + max_loc[0] + (temp_width // 2)
    center_y = top + max_loc[1] + (temp_height // 2)
    
    return float(max_val), (center_x, center_y)

def findIconConfidence(templatePath, top = 0, left = 0, width = 0, height = 0):
    # get screen width and height
    if (width == 0 or height == 0):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            width = monitor["width"]
            height = monitor["height"]
            
    template = cv2.imread(rf"{templatePath}")

    #get screenshot of screen
    region = {'top': top, 'left': left, 'width': width, 'height': height} #top is top left corner's y, left is its x
    with mss.mss() as sct:
        screenshot = sct.grab(region) 
        
    # reformat screenshot for in usable cv2 format
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    #get confidence and location
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return float(max_val), (left + max_loc[0], top + max_loc[1])

def findIconConfidenceCenter(templatePath, top = 0, left = 0, width = 0, height = 0):
    # get screen width and height
    if (width == 0 or height == 0):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            width = monitor["width"]
            height = monitor["height"]
            
    template = cv2.imread(rf"{templatePath}")

    #get screenshot of screen
    region = {'top': top, 'left': left, 'width': width, 'height': height} #top is top left corner's y, left is its x
    with mss.mss() as sct:
        screenshot = sct.grab(region) 
        
    # reformat screenshot for in usable cv2 format
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    #get confidence and location
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    
    #calculate returns
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    temp_height, temp_width = template.shape[:2]
    center_x = left + max_loc[0] + (temp_width // 2)
    center_y = top + max_loc[1] + (temp_height // 2)
    
    return float(max_val), (center_x, center_y)
