import google.generativeai as genai
import os
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

load_dotenv()

G_API = os.getenv("G_API")
if not G_API:
    raise EnvironmentError("Gemini API not found in .env file, please check")

genai.configure(api_key=G_API)

#####################################################################################################

def get_dynamic_screenshot_path():

    Tk().withdraw()  
    file_path = askopenfilename(
        title="Select a Screenshot",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not file_path:
        raise FileNotFoundError("No file selected. Please select a valid screenshot.")
    return file_path

screenshot_path = get_dynamic_screenshot_path()

media = Path(screenshot_path)

print(f"Selected media file: {media}")

myfile=genai.upload_file(media)
# print(f"{myfile}") use only if you want to check what file u uploaded..

#################################################################################################

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content(
    [myfile,"\n\n","Explain the error in the image and suggest troubleshooting steps along with links to websites to fix the error"]
)
print(f"{result.text=}")

##################################################################################################