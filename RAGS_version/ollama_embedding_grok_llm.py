from langchain_community.embeddings import OllamaEmbeddings  # Updated import for Ollama
from langchain_pinecone import PineconeVectorStore 
from pinecone import Pinecone, ServerlessSpec 
import os 
from dotenv import load_dotenv 
from langchain.schema import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.document_loaders import PyPDFLoader 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda 
from langchain_core.output_parsers import StrOutputParser 
from langchain.prompts import PromptTemplate 
import streamlit as st 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI 

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
grok_api_key = os.getenv("GROK_API_KEY")
print(f"grok_api_key : {grok_api_key}")

""" VARIABLES """
# Replace OpenAI embeddings with Ollama embeddings
embedding_oai = OllamaEmbeddings(model="nomic-embed-text")  # Use nomic-embed-text model

llm = ChatOpenAI(
    model="grok-3-latest",
    temperature=0.2,
    max_tokens=None,
    max_retries=2,
    api_key=grok_api_key,
    base_url="https://api.x.ai/v1",
    http_client=None,
    default_headers={"Authorization": f"Bearer {grok_api_key}"}
)

# """ PDF LOADER """
# loader = PyPDFLoader('./29_jan_morning.pdf')
# doc = loader.load()

# """ SPLITTING DOCUMENTS INTO TEXTS """
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=120)
# split = text_splitter.split_documents(doc)
# print(f"Type of split : {type(split)}")
# print(f"Length of split : {len(split)}")

""" VECTOR DATABASE SETUP """
pc = Pinecone(api_key=pinecone_api_key)
embedding_dimension = 768  # Updated to match nomic-embed-text's dimension (previously 784)

index_name = "rhl-project-4"

# Check if index exists, and create it with the correct dimension if it doesn't
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        metric="cosine",
        dimension=embedding_dimension,
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

vector_store = PineconeVectorStore(index_name=index_name, embedding=embedding_oai, pinecone_api_key=pinecone_api_key)
print("connection to Pinecone Established !!!!")

print("TEST 1")
# vector_store.add_documents(split)  # Uncomment to add documents
# print("data added to database !!!")

""" MODEL AND RETRIEVER """
print("TEST 2")
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

print("TEST 3")
arr = retriever.invoke('what are indications for Continuous positive airway pressure?')
# print(f"arr", arr)
# for i in arr:
#     print(i.page_content)
#     print()

# """ CHAINS """
# print("TEST 4")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="As a medical professional referring to the content: {context} /n Answer the following query: {question} in roughly 100 words only if you find confidence that the context has relevant information. If you are not confident that question belong to the context, return 'I have no information on this topic' and nothing else no other explanation "
)
parser = StrOutputParser()

def agg_func(docs):
    return "/n/n".join(a.page_content for a in docs)

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(agg_func),
    'question': RunnablePassthrough()
})

chain = parallel_chain | prompt | llm | parser

""" UI """
st.header("LangChain OLLAMA EMBEDDER GROk AI")
st.markdown("""
Welcome! This tool answers medical-related questions using context from the uploaded PDF.
Just type your question below and click *Submit*.
""")
user_input = st.text_input("Enter a prompt")

if st.button("Generate"):
    response = chain.invoke(user_input)
    st.write(response)