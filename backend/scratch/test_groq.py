import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key: {api_key[:10]}...")

client = Groq(api_key=api_key)

try:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Respond with a JSON object containing 'title' and 'description' keys only. Keep the description under 200 characters."},
            {"role": "user", "content": "Generate a new startup idea."}
        ],
        response_format={"type": "json_object"}
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
