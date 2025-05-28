from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema import Document
# Load environment variables from .env file
load_dotenv()

# Fetch Pinecone and OpenAI API keys from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")


index_name = "wwe-stars-index"
embedding_oai = OpenAIEmbeddings(model =  'text-embedding-3-large',dimensions= 784, openai_api_key=os.getenv("OPENAI_API_KEY"))
vector_store = PineconeVectorStore(
    index_name=index_name,
    embedding=embedding_oai,
    pinecone_api_key=pinecone_api_key
)

""" RETREIVER FROM VECTOR STORE """

# retreiver = vector_store.as_retriever(search_kwargs={"k": 2})

# print(retreiver.invoke("Who is the most intimidating wrestler in the Attitude Era?"))

""" MAXIMUM MARGINAL RELEVANCE """

# retriver = vector_store.as_retriever(search_kwargs={"k": 2},include_metadata=False,search_type="mmr")

# print(retriver.invoke("Who is the most intimidating wrestler in the Attitude Era?"))


""" MULTI QUERY RETRIEVER"""

# multiquery_retriever = MultiQueryRetriever.from_llm(
#     retriever=vector_store.as_retriever(search_kwargs={"k": 2}),

#     llm=ChatOpenAI(model="gpt-3.5-turbo")
# )

# print(multiquery_retriever.invoke("Who is the most contributing wrestler in the Attitude Era?"))


""" CONTEXTUAL COMPRESSOR RETRIEVER """

from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

base_retriever = vector_store.as_retriever(search_kwargs={"k": 2})
llm = ChatOpenAI(model="gpt-3.5-turbo")
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=compressor
)

print(compression_retriever.invoke("Who is the most contributing wrestler in the Attitude Era?"))