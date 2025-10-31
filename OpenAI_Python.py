from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from your .env file
load_dotenv(dotenv_path=r"C:\Users\Brian Pacio\source\repos\OpenAI-Python\OpenAI-Python\API_KEY.env")

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Verify the key was found
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your API_KEY.env file path and contents.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Ask the user for input
prompt = input("Greetings! How May I Help You Today? ")

# Send the request to the API
response = client.responses.create(
    model="gpt-4.1-nano",
    input=prompt
)

# Print the model’s reply
print("\nResponse:")
print(response.output_text)





# Pause so the window stays open
input("\nPress Enter to exit...")