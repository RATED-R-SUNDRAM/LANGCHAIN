from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the Chat Model
model = ChatOpenAI(model_name="gpt-4.1-2025-04-14", openai_api_key=OPENAI_API_KEY)

# System prompt for the sports expert
system_prompt = (
    "You are a telecaller , you are going to inform customers about there missed payments, ask them about reasons, inform them implication such as poor cibil incase of non payment and ask for date when they will pay. start the call replying to customers Hello by introducing youreself as bank representative named rahul, whenever you feel the purpose of call is done just reply back thanks and have a nice day , always remember you are representing to a bank and always stay on topic even when user  makes threatning remark say you'll forward calls to seniors and have a nice day and if theres a vqague request from user ask them to stay on topic politely "
)

# Initialize message history with system prompt
message_history = [SystemMessage(content=system_prompt)]

print("TELECALLER DEMO")

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print()
        print()
        print()
        print("Please find summary of the call : ")
        message_history.append(HumanMessage(content= "Understand the chat history and ouptut in format : the customer was unable to pay because <reason> , he promised to pay on <promise date if available or refused> and the tone was <tone of conversation> , fill text between <> by understanding the conversation and dont use <> in final text "))
        print(model.invoke(message_history).content)

        break

    # Add user message to history
    message_history.append(HumanMessage(content=user_input))

    # Get response
    response = model.invoke(message_history)
    message_history.append(AIMessage(content=response.content))

    # Print response and history

    print(f"Bot: {response.content}")

    

print("Thanks for chatting!")
