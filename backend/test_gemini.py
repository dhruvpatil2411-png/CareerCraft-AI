from dotenv import load_dotenv
from google import genai
import os


# Load .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")


# Check whether key is loaded
if not api_key:
    print("❌ GEMINI_API_KEY was NOT loaded from .env")
    raise SystemExit


print("✅ API key loaded from .env")
print("Key starts with:", api_key[:3])
print("Key length:", len(api_key))


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Test Gemini connection
try:

    print("\n🤖 Testing Gemini API...")

    models = list(client.models.list())

    print("\n✅ Gemini API authentication is working!")
    print("Available models found:", len(models))

    for model in models[:5]:

        print(
            "-",
            model.name
        )


except Exception as error:

    print("\n❌ Gemini API test failed!")
    print(error)