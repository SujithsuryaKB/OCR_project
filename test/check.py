import cv2
import io
from google.cloud import vision
from google.auth import default  # Auto-detects credentials

# === CONFIGURATION ===
IMAGE_PATH = "Marksheet.jpg"

def crop_image(image, left, top, right, bottom):
    """Crop an image based on given dimensions."""
    return image[top:bottom, left:right]

def extract_text_from_image(image):
    """
    Extract text from an image using Google Vision API.
    """
    try:
        # Authenticate using default credentials
        credentials, _ = default()
        client = vision.ImageAnnotatorClient(credentials=credentials)

        # Encode the image to bytes
        _, encoded_image = cv2.imencode(".jpg", image)
        content = encoded_image.tobytes()
        vision_image = vision.Image(content=content)

        # Perform text detection
        response = client.text_detection(image=vision_image)
        texts = response.text_annotations

        if texts:
            return texts[0].description.strip()
        else:
            return ""
    except Exception as e:
        print(f"Google Vision API failed: {e}")
        return ""

def main(image_path):
    # Load the original image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Define original cropping dimensions
    register_number_crop = (190, 150, width, int(height * 0.195))
    two_marks_crop = (145, int(height * 0.50), 200, int(height * 0.865))
    big_ques_crop = (int(width * 0.67), int(height * 0.54), int(width * 0.8), int(height * 0.88))

    # Crop images
    register_number_img = crop_image(image, *register_number_crop)
    two_marks_img = crop_image(image, *two_marks_crop)
    big_ques_img = crop_image(image, *big_ques_crop)

    # Save cropped images
    cv2.imwrite("register_number.jpg", register_number_img)
    cv2.imwrite("two_marks.jpg", two_marks_img)
    cv2.imwrite("big_questions.jpg", big_ques_img)

    # Extract text using Google Vision API
    register_number_text = extract_text_from_image(register_number_img)
    two_marks_text = extract_text_from_image(two_marks_img)
    big_ques_text = extract_text_from_image(big_ques_img)

    # Process extracted text
    register_number = [int(num) for num in register_number_text.split() if num.isdigit()]
    two_marks = [int(num) for num in two_marks_text.split() if num.isdigit()]
    big_ques = [int(num) for num in big_ques_text.split() if num.isdigit()]

    # Return results
    return {
        "register_number": register_number,
        "TWO_marks": two_marks,
        "BIG_QUES": big_ques,
    }

# Run the script
if __name__ == "__main__":
    results = main(IMAGE_PATH)
    print("Extracted Data:", results)
