import cv2
import rembg
import numpy as np
from utils import draw_object_outline

def process_image(input_image_path):
    original_image = cv2.imread(input_image_path)
    if original_image is None:
        return None, None

    max_display_height = 800
    height, width = original_image.shape[:2]
    if height > max_display_height:
        scale_factor = max_display_height / height
        original_image = cv2.resize(original_image, (int(width * scale_factor), max_display_height))

    # Draw ROI
    roi = cv2.selectROI(original_image)
    cv2.destroyAllWindows()

    selected_object = original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    result_with_alpha = rembg.remove(selected_object)

    alpha_channel = result_with_alpha[:, :, 3]
    result = cv2.resize(result_with_alpha[:, :, :3], (roi[2], roi[3]))
    mask = alpha_channel[:, :, np.newaxis] / 255.0

    original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])] = \
        original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])] * (1 - mask) + \
        result * mask

    draw_object_outline(original_image, alpha_channel, roi=roi)

    _, processed_image_encoded = cv2.imencode('.png', original_image)
    processed_image_bytes = processed_image_encoded.tobytes()

    _, input_image_encoded = cv2.imencode('.png', selected_object)
    input_image_bytes = input_image_encoded.tobytes()

    return processed_image_bytes, input_image_bytes