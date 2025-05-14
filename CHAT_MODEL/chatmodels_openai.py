from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create a ChatOpenAI object
model = ChatOpenAI(model_name="o1-mini-2024-09-12", openai_api_key=OPENAI_API_KEY)

result = model.invoke("give me rules for baseball in 100 words")

print(result)