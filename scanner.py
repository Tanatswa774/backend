import cv2
import numpy as np

def find_template(screen_path: str, template_path: str, threshold: float = 0.75):
    screen = cv2.imread(screen_path)
    template = cv2.imread(template_path)

    if screen is None or template is None:
        raise FileNotFoundError("Missing screen or template image.")

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    matches = list(zip(*locations[::-1]))  # Convert to (x, y)
    return matches
