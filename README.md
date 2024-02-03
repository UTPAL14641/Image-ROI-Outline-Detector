# Image ROI Outline Detector

## Overview

The Image ROI Outline Detector is a web application built with Flask that allows users to upload an image, select a region of interest (ROI), and detect and outline the selected object within the ROI. The application utilizes background removal and contour detection techniques to highlight the object in the processed image.

## Features

- **Image Processing:** Utilizes OpenCV and rembg for image processing and background removal.
- **Flask Web Application:** Implements a user-friendly web interface for users to upload images and visualize the processed results.
- **ROI Selection:** Allows users to choose a region of interest (ROI) in the uploaded image.

## Setup and Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/UTPAL14641/Image-ROI-Outline-Detector.git
   cd Image-ROI-Outline-Detector

   
2. **Install Dependencies:**
   pip install -r requirements.txt
4. Run the Flask Application:
   python app.py
Open your browser and navigate to http://127.0.0.1:5000/ to access the application.

Usage:

Upload an image using the provided form.
Select a region of interest (ROI) within the image.
Click "Process Image" to detect and outline the object within the selected ROI.
View the processed image.
Project Structure
app.py: Flask application with routes for rendering the web interface and processing images.
image_processing.py: Module containing image processing functions.
utils.py: Utility functions, including the outline drawing function.
templates/: Folder containing HTML templates for the web interface.
static/: Folder for static files, including the background image.
Dependencies
Flask
OpenCV
rembg
