import os
from openai import OpenAI

# Set your API key
api_key = "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"

# Create a client
client = OpenAI(api_key=api_key)

# Test the API
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {str(e)}")
