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
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

model = ChatOpenAI(model_name="gpt-4.1-2025-04-14", openai_api_key=OPENAI_API_KEY)

# parallel chains 
parser =StrOutputParser()

class output(BaseModel):
    topic : str = Field(description="The topic of the joke")
    rating : int = Field(description="The rating of the joke on scale of 5")
    
parser2 = PydanticOutputParser(pydantic_object=output)

# prompt1= PromptTemplate(
#     template ='Write a joke about  {topic}'
#     ,input_variables=['topic']
# )

# prompt2 =PromptTemplate(
#     template ='Write a strange fact about {topic}'
#     ,input_variables=['topic']
# )
# prompt3 =PromptTemplate(
#     template ='Write a funny short fictional story about  using the {joke} and the {fact}'
#     ,input_variables=['joke','fact']
# )

# chain = RunnableParallel({
#     'joke' : prompt1 | model|parser ,
#     'fact' : prompt2 | model | parser
# })

# final_chain = chain | prompt3 | model | parser

# print(final_chain.invoke({'topic':"Navjot Singh Siddhu"}))


### CONDITIONAL PARSER

prompt1= PromptTemplate(
    template ='Write a very good joke about  {topic}'
    ,input_variables=['topic']
)

prompt2 =PromptTemplate(
    template ='Rate the {joke} on scale of 5 in following {output_format}',
    input_variables=['joke']
    ,partial_variables={"output_format":parser2.get_format_instructions()}
)

prompt3 = PromptTemplate(
    template ='applozige for bad joke and write a better joke on {topic}'
    ,input_variables=['topic']
)

prompt4 =PromptTemplate(
    template ='feel proud for good joke and write a awesome fact about {topic}'
    ,input_variables=['topic']
)

base_chain  = prompt1 |model |parser|prompt2 |model |parser2 | RunnableLambda(lambda x: {"rating": x.rating, "topic": x.topic})


print(base_chain.invoke({"topic": "Navjot singh siddhu"}))

# branch chain 
prompt3 = PromptTemplate(
    template ='applozige for bad joke and write a better joke on {topic}'
    ,input_variables=['topic']
)

prompt4 =PromptTemplate(
    template ='what is the {topic}'
    ,input_variables=['topic'])

branch_chain = RunnableBranch(
    (lambda x: x["rating"] > 3, prompt3 | model | parser),
    (lambda x: x["rating"] <= 3, prompt4 | model | parser),
    RunnableLambda(lambda x: "Haha fallback!")
)


final_chain = base_chain | branch_chain

print(final_chain.invoke({"topic": "Navjot singh siddhu"}))