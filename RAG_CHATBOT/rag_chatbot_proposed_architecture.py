""" IMPORTS AND ENV VAR """
from langchain_community.embeddings import OllamaEmbeddings  # Changed to OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os 
from dotenv import load_dotenv 
from langchain.schema import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.document_loaders import PyPDFLoader 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda 
from langchain_core.output_parsers import StrOutputParser 
from langchain.prompts import PromptTemplate ,ChatPromptTemplate
import streamlit as st 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from pydantic import BaseModel , Field 
from typing import TypedDict, Annotated,Optional , Literal 
from langchain_core.output_parsers import JsonOutputParser,PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
grok_api_key = os.getenv("GROK_API_KEY")
print(f"grok_api_key : {grok_api_key}")

""" VARIABLES """
embedding_hf = OllamaEmbeddings(model="snowflake-arctic-embed")  # Changed to Snowflake Arctic Embed
grok_api= grok_api_key
llm = ChatOpenAI(
    model="grok-3-latest",
    temperature=0.2,
    max_tokens=None,
    max_retries=2,
    api_key=grok_api_key,
    base_url="https://api.x.ai/v1",
    http_client=None,
    default_headers={"Authorization": f"Bearer {grok_api}"}
)


# # """ PDF LOADER """
# # loader = PyPDFLoader('./29_jan_morning.pdf')
# # doc = loader.load()

# # """ SPLITTING DOCUMENTS INTO TEXTS """
# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=120)
# # split = text_splitter.split_documents(doc)

# """ VECTOR DATABASE SETUP """
# persist_directory = "./chroma_db_snowflake"  # New directory for Snowflake
# collection_name = "rhl-project-snowflake"

# # Initialize or load Chroma vector store
# if os.path.exists(persist_directory):
#     print("Loading existing Chroma vector store...")
#     vector_store = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embedding_hf,
#         collection_name=collection_name,
#     )
# else:
#     print("Creating new Chroma vector store...")
#     vector_store = Chroma.from_documents(
#         documents=split,
#         embedding=embedding_hf,
#         persist_directory=persist_directory,
#         collection_name=collection_name
#     )
# print("Chroma vector store initialized and documents added !!!!")

# # Persist the database to disk
# vector_store.persist()

# """ MODEL AND RETRIEVER """
# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# arr = retriever.invoke('what are indications for Continuous positive airway pressure?')

# """ CHAINS """

query = "Alright buddy see ya later"

system_prompt = "As a highly professional medical officer , who's only source of knowledge is the content provided with the question, answer the question in roughly 100 words only if you find confidence that the context has relevant information. If you are not confident that question belong to the context, return 'I have no information on this topic' and nothing else no other explanation"


# Initialize message history with system prompt
message_history = [SystemMessage(content=system_prompt)]

message_history.append(HumanMessage(content=query))

class schema(BaseModel):
    category: Literal['greeting', 'non-greeting'] = Field(description="Identify if it's a greeting or closing statement, else a question or statement")

prompt = PromptTemplate(
    input_variables=["query"],
    template="Identify if the statement is a generic greeting or closing statement in a conversation, categorize as 'greeting' or 'non-greeting': {query}"
)

# Use with_structured_output directly
structured_llm = llm.with_structured_output(schema)
chain1 = prompt | structured_llm

result = chain1.invoke({"query": query})
print(chain1.invoke(query).category)


if result.category == 'greeting':
    prompt2 = ChatPromptTemplate(
    [
        SystemMessage(content="You are a helpful medical assistant having a conversation with a user and the conversation is mentioned below, be very polite and porofessional be very polite and limited in words to reply , dont answer any information basis facts you know beyond the conversation, just continue the conversation using history here and generic greets"),
        MessagesPlaceholder(variable_name="history")])
    chain = prompt2 | llm
    print(chain.invoke(message_history))


else:
    print("blah blah")

    

# system_prompt = "As a medical professional referring to the content: {context} /n Answer the following query: {question} in roughly 100 words only if you find confidence that the context has relevant information. If you are not confident that question belong to the context, return 'I have no information on this topic' and nothing else no other explanation "


# # Initialize message history with system prompt
# message_history = [SystemMessage(content=system_prompt)]

# prompt = ChatPromptTemplate(
#     [
      
#         MessagesPlaceholder(variable_name="history"),
#         HumanMessage(content="{query}")])

# parser = StrOutputParser()

# def agg_func(docs):
#     return "/n/n".join(a.page_content for a in docs)

# parallel_chain = RunnableParallel({
#     'context': retriever | RunnableLambda(agg_func),
#     'question': RunnablePassthrough(),
#     'history' : RunnablePassthrough()
# })

# chain = parallel_chain | prompt | llm | parser

