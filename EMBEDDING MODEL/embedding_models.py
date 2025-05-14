from langchain_openai import OpenAIEmbeddings 

from dotenv import load_dotenv
import os
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

load_dotenv() 

embedding = OpenAIEmbeddings(model =  'text-embedding-3-large',dimensions= 300, openai_api_key=os.getenv("OPENAI_API_KEY"))

document= ["Virat Kohli's aggressive batting style strikes fear in the hearts of opposing teams.",
 "Ravindra Jadeja's all-round skills make him a valuable asset in any format of the game.",
 "Rishabh Pant's fearless and explosive batting has earned him a place in the Indian team at a young age.",
 "Jasprit Bumrah's deadly yorkers and accurate bowling make him one of the best pacers in the world."
]

embed_doc = embedding.embed_documents(document)

query = input("Enter your query: ")

embed_query = embedding.embed_query(query)

arr= [cosine_similarity([embed_query],[b])[0][0] for b in embed_doc]

print(document[np.argmax(np.array(arr))])