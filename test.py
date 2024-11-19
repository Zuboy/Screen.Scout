import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDPVzmLy8zLphOjnrJOHgyYYSgt6deVi80")

model=genai.GenerativeModel("gemini-1.5-flash")
response=model.generate_content("Explain what is a computer")
print(response.text)