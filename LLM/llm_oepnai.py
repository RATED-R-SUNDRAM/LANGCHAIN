from langchain_openai import OpenAI 

from dotenv import load_dotenv
import os

load_dotenv() 

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resullt = llm.invoke("Give one one line about any 4 indian players")

print(resullt)