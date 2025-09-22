import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    print("Testing OpenAI API connection...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}],
        max_tokens=50
    )
    print("\n✅ Success! API Key is valid.")
    print("Response:", response.choices[0].message.content)
    
except Exception as e:
    print("\n❌ Error occurred:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    if "Incorrect API key" in str(e):
        print("\n⚠️ Your API key appears to be invalid. Please check your .env file.")
    elif "connect" in str(e).lower():
        print("\n⚠️ Connection error. Please check your internet connection.")