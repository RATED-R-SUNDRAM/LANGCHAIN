import requests
import json

api_key = "xai-zJh8aGZhkr7eZ3mIsFG7xtaGSDt7oRJce3PLHmshUG2qxaLLZ6yTq3QSz5VtecrQdbN6I2LYljrnHKLM"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
payload = {
    "messages": [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "testing. JUST say hi and hello world do nothing else."}
    ],
    "model": "grok-3-latest",  # Changed from llama-3.1-8b-instant
    "stream": False,
    "temperature": 0
}
response = requests.post("https://api.x.ai/v1/chat/completions", json=payload, headers=headers)
print(response.json())