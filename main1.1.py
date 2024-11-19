import os
import requests
from dotenv import load_dotenv

G_API = os.getenv("G_API")
if not G_API:
    raise EnvironmentError("Gemini API not found in .env file, please check")

GEMINI_VISION_ENDPOINT = "https://gemini.googleapis.com/v1/vision:analyze"  # Replace with actual Gemini Vision API endpoint
GEMINI_LANGUAGE_ENDPOINT = "https://gemini.googleapis.com/v1/language:generate"  # Replace with actual Gemini Language API endpoint

def extract_text_with_gemini(image_path):
    
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Authorization": f"Bearer {G_API}",
        "Content-Type": "application/octet-stream",
    }

    params = {
        "features": "TEXT_DETECTION"  # Adjust based on Gemini Vision's feature specifications
    }

    try:
        response = requests.post(
            GEMINI_VISION_ENDPOINT,
            headers=headers,
            params=params,
            data=image_data
        )
        response.raise_for_status()
        result = response.json()

        extracted_text = ""
        for annotation in result.get("textAnnotations", []):
            extracted_text += annotation.get("description", "") + "\n"

        return extracted_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Gemini Vision API Request Failed: {e}")
        return None

def generate_troubleshooting_steps(error_text):
    """
    Generates troubleshooting steps using Gemini Language API based on the extracted error text.
    """
    headers = {
        "Authorization": f"Bearer {G_API}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": f"The following error code was encountered: '{error_text}'. Provide detailed troubleshooting steps to resolve this error.",
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.9,
        "n": 1,
        "stop": None
    }

    try:
        response = requests.post(
            GEMINI_LANGUAGE_ENDPOINT,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()

        troubleshooting_steps = result.get("choices", [{}])[0].get("text", "").strip()
        return troubleshooting_steps

    except requests.exceptions.RequestException as e:
        print(f"Gemini Language API Request Failed: {e}")
        return None

def main(image_path):
    """
    Main function to extract text from an image and generate troubleshooting steps.
    """
    # Step 1: Extract text from the screenshot
    extracted_text = extract_text_with_gemini(image_path)
    if not extracted_text:
        print("No text extracted from the image.")
        return

    print(f"Extracted Text:\n{extracted_text}\n")

    # Step 2: Generate troubleshooting steps using the extracted text
    troubleshooting_steps = generate_troubleshooting_steps(extracted_text)
    if troubleshooting_steps:
        print(f"Troubleshooting Steps:\n{troubleshooting_steps}")
    else:
        print("Failed to generate troubleshooting steps.")

# Example Usage
if __name__ == "__main__":
    screenshot_path = "screenshot.png"  # Replace with your screenshot path
    main(screenshot_path)
