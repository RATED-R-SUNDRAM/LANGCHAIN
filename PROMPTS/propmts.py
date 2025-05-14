from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo")

system_message = SystemMessage(content="You are a teacher of physics who will solve doubts of students in less than 100 words")

prompt = ChatPromptTemplate(
    [
        SystemMessage(content="You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{query}")])


history = []
while(True):
    query = input("Enter your query: ")
    if query == "exit":
        break
    
    history.append(HumanMessage(content=query))

    chain = prompt | model

    response = chain.invoke({"history": history,"query": query}).content
    print("Teacher: ", response)
    history.append(AIMessage(content=response))
print(prompt)

