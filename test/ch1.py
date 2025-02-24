import cv2
import pytesseract
from pytesseract import Output
import numpy as np

# Specify the path to the tesseract executable (update it based on your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust this path if needed

# === CONFIGURATION ===
IMAGE_PATH = "Marksheet1.jpg"

def preprocess_image(image_path):
    """
    Preprocess image to enhance text quality by resizing, contrast enhancement,
    noise reduction, and adaptive thresholding.
    """
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the image for better OCR accuracy (upscaling)
    scale_factor = 1.5  # Adjust the scaling factor based on the input image resolution
    resized = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # Enhance contrast using histogram equalization
    contrast_enhanced = cv2.equalizeHist(resized)

    # Reduce noise while preserving edges using bilateral filtering
    denoised = cv2.bilateralFilter(contrast_enhanced, d=9, sigmaColor=75, sigmaSpace=75)

    # Apply adaptive thresholding to create a binary image
    thresholded = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Save the processed image (optional, for debugging purposes)
    cv2.imwrite("preprocessed_image.jpg", thresholded)

    return thresholded

def crop_and_extract_text(image, coords, description):
    """
    Crop the image to the specified coordinates and extract text using pytesseract.
    Args:
    - image: The original image.
    - coords: A tuple (left, top, right, bottom) for cropping.
    - description: Label for the cropped section.
    
    Returns:
    - Extracted text for the specified region.
    """
    left, top, right, bottom = coords
    cropped = image[top:bottom, left:right]
    
    # Save the cropped image (optional)
    cv2.imwrite(f"{description}_cropped.jpg", cropped)

    # Extract text from the cropped region
    text = pytesseract.image_to_string(cropped, config="--psm 6")  # Adjust psm mode if needed
    return text

# === RUN SCRIPT ===
# Preprocess the image
image = cv2.imread(IMAGE_PATH)
preprocessed_image = preprocess_image(IMAGE_PATH)

# Define cropping regions (update as needed)
height, width = preprocessed_image.shape[:2]

register_number_coords = (190, 140, width, int(height * 0.2))
two_marks_coords = (140, int(height * 0.53), 200, int(height * 0.89))
big_question_coords = (int(width * 0.67), int(height * 0.54), int(width * 0.8), int(height * 0.88))

# Crop and extract text for each region
register_number_text = crop_and_extract_text(preprocessed_image, register_number_coords, "register_number")
two_marks_text = crop_and_extract_text(preprocessed_image, two_marks_coords, "two_marks")
big_question_text = crop_and_extract_text(preprocessed_image, big_question_coords, "big_question")

# Print the results
print("Register Number:", register_number_text)
print("Two Marks Questions:", two_marks_text)
print("Big Questions:", big_question_text)
