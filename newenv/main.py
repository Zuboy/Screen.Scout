import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

G_API = os.getenv("G_API")
if not G_API:
    raise EnvironmentError("Gemini API not found in .env file, please check")

genai.configure(api_key=G_API)

#####################################################################################################

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain what is a computer")
print(response.text)
