import openai
import re
import base64
import os

# === CONFIGURATION ===
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual API key
IMAGE_PATH = "Marksheet.jpg"  # Replace with your actual image file

def extract_text_with_gpt4o(image_path):
    """Extract handwritten text from an image using OpenAI GPT-4o."""
    try:
        client = openai.OpenAI()  # Use new API client structure

        # Open image and convert to Base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Send image to OpenAI API (GPT-4o)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an OCR assistant that extracts handwritten text from images."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract all handwritten text from this image:"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]}
            ],
            max_tokens=500
        )

        # Extracted text from response
        extracted_text = response.choices[0].message.content
        return extracted_text

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def separate_numbers_and_text(text):
    """Separate numbers and words from extracted text."""
    numbers = re.findall(r'\d+', text)  # Extract numbers
    words = re.findall(r'[a-zA-Z]+', text)  # Extract words
    return numbers, words

# === RUN SCRIPT ===
ocr_text = extract_text_with_gpt4o(IMAGE_PATH)

if ocr_text:
    print("\n✅ Extracted Text:\n", ocr_text)
    
    numbers, words = separate_numbers_and_text(ocr_text)
    print("\n🔢 Extracted Numbers:", numbers)
    print("\n🔤 Extracted Words:", words)
else:
    print("❌ Failed to extract text.")
