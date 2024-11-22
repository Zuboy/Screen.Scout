import google.generativeai as genai
import os
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

load_dotenv()

G_API = os.getenv("G_API")
if not G_API:
    raise EnvironmentError("Gemini API not found in .env file, please check")

genai.configure(api_key=G_API)

#####################################################################################################

def extract_text_from_image(image_path):
    """
    Uses Google Gemini Vision API to extract text from an image.
    
    Args:
        image_path (str): Path to the screenshot file.
    
    Returns:
        str: Extracted text or an error message.
    """
    try:
        # Load image file as binary
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Perform text extraction using Gemini Vision API
        vision_response = vision_client.analyze_image(
            image=image_data,
            features=["TEXT_EXTRACTION"]  # Specify text extraction feature
        )
        extracted_text = vision_response.get("text", "").strip()

        if not extracted_text:
            return "No text detected in the image."
        return extracted_text
    except Exception as e:
        return f"Error during Vision API processing: {e}"

# Function to generate content using extracted text
def troubleshoot_issue_from_image(image_path):
    """
    Extracts text from an image and generates a troubleshooting response using Generative AI.

    Args:
        image_path (str): Path to the screenshot file.
    """
    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    if extracted_text.startswith("Error"):
        print(extracted_text)
        return

    print(f"Extracted Text: {extracted_text}")

    # Generate troubleshooting content
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Troubleshoot the following issue: {extracted_text}"
        response = model.generate_content(prompt)
        print(f"AI Response: {response.text}")
    except Exception as e:
        print(f"Error during Generative AI processing: {e}")

# Function to get dynamic file input from the user
def get_dynamic_screenshot_path():
    """
    Opens a file dialog for the user to select a screenshot dynamically.

    Returns:
        str: Path to the selected file.
    """
    Tk().withdraw()  # Hide the root Tk window
    file_path = askopenfilename(
        title="Select a Screenshot",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not file_path:
        raise FileNotFoundError("No file selected. Please select a valid screenshot.")
    return file_path

# Example usage
if __name__ == "__main__":
    try:
        # Get the screenshot file dynamically
        screenshot_path = get_dynamic_screenshot_path()
        troubleshoot_issue_from_image(screenshot_path)
    except Exception as e:
        print(f"Error: {e}")