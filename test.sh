curl https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer xai-zJh8aGZhkr7eZ3mIsFG7xtaGSDt7oRJce3PLHmshUG2qxaLLZ6yTq3QSz5VtecrQdbN6I2LYljrnHKLM" \
  -d '{
  "messages": [
    {
      "role": "system",
      "content": "You are a test assistant."
    },
    {
      "role": "user",
      "content": "Testing. Just say hi and hello world and nothing else."
    }
  ],
  "model": "grok-3-latest",
  "stream": false,
  "temperature": 0
}'