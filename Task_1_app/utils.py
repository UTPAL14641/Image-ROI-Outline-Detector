import cv2
import numpy as np

def draw_object_outline(image, mask, color=(0, 255, 0), thickness=2, roi=None):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        contour[:, 0, 0] += int(roi[0])
        contour[:, 0, 1] += int(roi[1])
    cv2.drawContours(image, contours, -1, color, thickness)
