from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import TypedDict, Annotated,Optional , Literal 
from dotenv import load_dotenv 
from pydantic import BaseModel , Field
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser,PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from typing import TypedDict, Annotated,Optional , Literal 
from dotenv import load_dotenv 
from pydantic import BaseModel , Field

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

model = ChatOpenAI(model_name="gpt-4.1-2025-04-14", openai_api_key=OPENAI_API_KEY)

### str output parser 

# prompt1 = PromptTemplate(
#     input_variables=["query"],
#     template="Write a joke about following topic: {query}?",
# )

# output_parser = StrOutputParser()

# prompt2 = PromptTemplate(
#     input_variables=["query"],
#     template="reireate the joke and Rate the joke on scale of 1 to 10 : {query}?",
# )

# chain = prompt1 | model | output_parser | prompt2 | model | output_parser

# print(chain.invoke("Navjot singh siddhu"))


### Json output parser 

# str_parser = StrOutputParser()
# json_parser = JsonOutputParser()

# prompt1 = PromptTemplate(
#     input_variables=["query"],
#     template="Write a joke about following topic: {query}?",
# )

# prompt2 = PromptTemplate(
#     input_variables=["joke"],
#     template=" list the rating 1-10, joke and all common nouns in the {joke} in the format :{output_format}",
#     partial_variables={"output_format": json_parser.get_format_instructions()} # partial_variables are variables filled directly not at run time
# )

# chain = prompt1 | model | str_parser | prompt2 | model | json_parser

# print(chain.invoke("Navjot singh siddhu"))

### Pydantic output parser 


str_parser = StrOutputParser()
class scheama (BaseModel):
    joke : str = Field(description="The joke")
    rating : int = Field(description="The rating of the joke")
    nouns : list[str] = Field(description="The list of common nouns in the joke")

pydantic_parser = PydanticOutputParser(pydantic_object=scheama)

prompt1 = PromptTemplate(
    input_variables=["query"],
    template="Write a joke about following topic: {query}?",
)

prompt2 = PromptTemplate(
    input_variables=["joke"],
    template=" list the rating 1-10, joke and all common nouns in the {joke} in the format :{output_format}",
    partial_variables={"output_format": pydantic_parser.get_format_instructions()} # partial_variables are variables filled directly not at run time
)

chain = prompt1 | model | str_parser | prompt2 | model | pydantic_parser

print(chain.invoke("Navjot singh siddhu"))