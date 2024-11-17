import pytesseract
import cv2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

image_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

if image_path:
    print(f"Selected image: {image_path}")
else:
    print("No file selected.")
    exit()  

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image from {image_path}")
        exit()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image_path):
    pimage = preprocess(image_path)
    text = pytesseract.image_to_string(pimage)
    return text

extracted_text = extract_text(image_path)
print(f"Extracted Text: \n{extracted_text}")
