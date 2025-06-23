import cv2
import numpy as np

def find_template(screen_path: str, template_path: str, threshold: float = 0.75):
    screen = cv2.imread(screen_path)
    template = cv2.imread(template_path)

    if screen is None or template is None:
        raise FileNotFoundError("Screenshot or template missing.")

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return list(zip(*locations[::-1]))
