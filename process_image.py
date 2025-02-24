import os
import cv2
import pandas as pd
from google.cloud import vision
from google.auth import default
from openpyxl import load_workbook

# === CONFIGURATION ===
UPLOAD_FOLDER = "uploads"
OUTPUT_EXCEL_PATH = "output/marksheet_data.xlsx"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists("output"):
    os.makedirs("output")

def crop_image(image, left, top, right, bottom):
    """Crop an image based on given dimensions."""
    return image[top:bottom, left:right]

def extract_text_from_image(image):
    """Extract text from an image using Google Vision API."""
    try:
        credentials, _ = default()
        client = vision.ImageAnnotatorClient(credentials=credentials)

        _, encoded_image = cv2.imencode(".jpg", image)
        content = encoded_image.tobytes()
        vision_image = vision.Image(content=content)

        response = client.text_detection(image=vision_image)
        texts = response.text_annotations

        return texts[0].description.strip() if texts else ""
    except Exception as e:
        print(f"Google Vision API failed: {e}")
        return ""

def adjust_column_widths(excel_path):
    """Adjust column widths in an Excel file."""
    wb = load_workbook(excel_path)
    ws = wb.active

    for column in ws.columns:
        max_length = max((len(str(cell.value)) for cell in column if cell.value), default=0)
        column_letter = column[0].column_letter
        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(excel_path)

def save_to_excel(data):
    """Save extracted data into an Excel sheet."""
    register_number = data["register_number"]
    two_marks = data["TWO_marks"]
    big_ques = data["BIG_QUES"]

    two_marks_questions = [f"Q{i}" for i in range(1, len(two_marks) + 1)]
    big_ques_questions = [f"Q{i}" for i in range(11, 11 + len(big_ques))]

    max_length = max(len(two_marks), len(big_ques))
    two_marks.extend([None] * (max_length - len(two_marks)))
    big_ques.extend([None] * (max_length - len(big_ques)))
    two_marks_questions.extend([""] * (max_length - len(two_marks_questions)))
    big_ques_questions.extend([""] * (max_length - len(big_ques_questions)))

    df = pd.DataFrame({
        "Register Number": [register_number] + [""] * (max_length - 1),
        "2-Marks Questions": two_marks_questions,
        "2-Marks (Q1-Q10)": two_marks,
        "Big Questions Numbers": big_ques_questions,
        "Big Questions (Q11-Q16)": big_ques,
    })

    df.to_excel(OUTPUT_EXCEL_PATH, index=False)
    adjust_column_widths(OUTPUT_EXCEL_PATH)

def process_image(image_path):
    """Processes the image and extracts text data."""
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    register_number_crop = (190, 150, width, int(height * 0.195))
    two_marks_crop = (145, int(height * 0.5), 200, int(height * 0.85))
    big_ques_crop = (int(width * 0.67), int(height * 0.54), int(width * 0.8), int(height * 0.83))

    register_number_img = crop_image(image, *register_number_crop)
    two_marks_img = crop_image(image, *two_marks_crop)
    big_ques_img = crop_image(image, *big_ques_crop)

    register_number_text = extract_text_from_image(register_number_img)
    two_marks_text = extract_text_from_image(two_marks_img)
    big_ques_text = extract_text_from_image(big_ques_img)

    register_number = "".join(filter(str.isdigit, register_number_text))
    two_marks = [int(num) for num in two_marks_text.split() if num.isdigit()]
    big_ques = [int(num) for num in big_ques_text.split() if num.isdigit()]

    results = {
        "register_number": register_number,
        "TWO_marks": two_marks,
        "BIG_QUES": big_ques,
    }

    save_to_excel(results)
    return results
