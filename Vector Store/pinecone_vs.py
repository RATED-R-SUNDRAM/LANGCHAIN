from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from langchain.schema import Document
# Load environment variables from .env file
load_dotenv()

# Fetch Pinecone and OpenAI API keys from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# # Validate API keys
# if not pinecone_api_key:
#     raise ValueError("PINECONE_API_KEY environment variable not set.")
# if not openai_api_key:
#     raise ValueError("OPENAI_API_KEY environment variable not set.")

# # Initialize Pinecone client (optional, only if you need to manage indexes directly)
# pc = Pinecone(api_key=pinecone_api_key)
# embedding_dimension = 784
index_name = "wwe-stars-index"
# pc.create_index(
#     name=index_name,
#     metric="cosine",
#     dimension=embedding_dimension,
#     spec=ServerlessSpec(cloud="aws", region="us-east-1")
# )
# print(f"Index '{index_name}' created successfully.")


# 
doc1 = Document(
    page_content="Stone Cold Steve Austin is a defining figure of the Attitude Era, known for his rebellious attitude and intense brawls. His defiance against authority and iconic stunner made him a legend.",
    metadata={"real_name": "Steven James Anderson", "stage_name_feature": "The Texas Rattlesnake"}
)

doc2 = Document(
    page_content="The Rock electrified audiences during the Attitude Era with his charisma and mic skills. His fast-paced matches and catchphrases made him a global superstar.",
    metadata={"real_name": "Dwayne Douglas Johnson", "stage_name_feature": "The People's Champion"}
)

doc3 = Document(
    page_content="Triple H, a cerebral assassin of the Attitude and Ruthless Aggression Eras, dominated with his strategic mind and sledgehammer. He led D-Generation X and later Evolution to prominence.",
    metadata={"real_name": "Paul Michael Levesque", "stage_name_feature": "The Game"}
)

doc4 = Document(
    page_content="Eddie Guerrero brought heart and flair to the Ruthless Aggression Era. Known for his technical wrestling and 'Lie, Cheat, Steal' persona, he won fans with his passion and charisma.",
    metadata={"real_name": "Eduardo Gory Guerrero Llanes", "stage_name_feature": "Latino Heat"}
)

doc5 = Document(
    page_content="Kurt Angle, an Olympic gold medalist, excelled in the Attitude and Ruthless Aggression Eras with his technical prowess and intense style. His ankle lock and charisma made him a standout.",
    metadata={"real_name": "Kurt Steven Angle", "stage_name_feature": "The Wrestling Machine"}
)
docs= [doc1, doc2, doc3, doc4, doc5]

embedding_oai = OpenAIEmbeddings(model =  'text-embedding-3-large',dimensions= 784, openai_api_key=os.getenv("OPENAI_API_KEY"))
vector_store = PineconeVectorStore(
    index_name=index_name,
    embedding=embedding_oai,
    pinecone_api_key=pinecone_api_key
)

#vector_store.add_documents(docs)

updated_doc = Document(
    page_content="The Undertaker, a master of the Attitude and Ruthless Aggression Eras, is known for his intimidating presence and signature 'Death's Door' match. His longevity and fear factor made him a legend.",
    metadata={"real_name": "Mark William Calaway", "stage_name_feature": "The Undertaker"}
)

vector_store.add_documents([updated_doc])

updated_doc2 = Document(
    page_content="Randy Savage, a charismatic force in the Attitude Era, was known for his 'Bat Signal' catchphrase and intense matches. His 'Savage Intensity' and 'Bat Signal' made him a memorable figure.",
    metadata={"real_name": "Randal Scott Savage", "stage_name_feature": "Macho Man"}
)

#vector_store.update_document(document_id=' ', document=updated_doc2)


