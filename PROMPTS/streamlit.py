from langchain_openai import OpenAI 

from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv() 

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.header("LangChain OpenAI Demo")

user_input = st.text_input("Enter a prompt")

if st.button("Generate"):
    response = llm(user_input)
    st.write(response)