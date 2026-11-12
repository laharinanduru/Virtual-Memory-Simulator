
import os
from google import genai

# Read the API key securely from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key is missing!")
else:
    try:
        # Connect to Gemini
        client = genai.Client(api_key=api_key)

        # Ask Gemini to generate an explanation
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=(
                "Explain virtual memory in simple words. "
                "Include one real-life example and explain "
                "why virtual memory is important."
            )
        )

        print("\n===== GEMINI CONNECTION SUCCESSFUL =====")
        print("\nGemini's Answer:\n")
        print(response.text)

    except Exception as error:
        print("\nGemini connection failed:")
        print(error)
