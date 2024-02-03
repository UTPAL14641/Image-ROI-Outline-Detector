from flask import Flask, render_template, request, send_file, send_from_directory, jsonify
import cv2
import rembg
import numpy as np
from utils import draw_object_outline
import io
import os

app = Flask(__name__)

# Route for serving the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for processing uploaded image
@app.route('/process_image', methods=['POST'])
def process_image():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        original_image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        max_display_height = 800
        height, width = original_image.shape[:2]
        if height > max_display_height:
            scale_factor = max_display_height / height
            original_image = cv2.resize(original_image, (int(width * scale_factor), max_display_height))

        roi = cv2.selectROI(original_image)

        selected_object = original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        result_with_alpha = rembg.remove(selected_object)

        alpha_channel = result_with_alpha[:, :, 3]
        result = cv2.resize(result_with_alpha[:, :, :3], (roi[2], roi[3]))
        mask = alpha_channel[:, :, np.newaxis] / 255.0

        original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])] = \
            original_image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])] * (1 - mask) + \
            result * mask

        draw_object_outline(original_image, alpha_channel, roi=roi)

        # Save the processed image to a BytesIO object
        _, img_encoded = cv2.imencode('.png', original_image)
        img_bytes = img_encoded.tobytes()

        return send_file(
            io.BytesIO(img_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='result.png'
        )

    return jsonify({'error': 'No file uploaded'})

# Route for serving static files (background image)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
