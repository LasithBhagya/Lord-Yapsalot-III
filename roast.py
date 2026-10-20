import sys
from google import genai
from dotenv import load_dotenv
import subprocess

load_dotenv()   # Load the API keys and stuff
client = genai.Client()    # Client automatically picks up the API key

def roast(data: str):
    prompt = f"""
    Write a mean, aggressive, and funny message roasting someone based on this data: "{data}". Use internet slang, casual phrasing, and throw in some swear words to spice it up. Do NOT be polite. Keep it punchy (around 2-3 sentences).
    """
    response = client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt)
    if response.candidates and response.candidates[0].content.parts:
        return response.text

if __name__ == "__main__":
    userInput = input('data: ')
    print('\nCooking the Roast...')
    message = roast(userInput)
    print(message)
    subprocess.run([sys.executable, "speech.py", message])
