import os
import sys

import constants 
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Set your OpenAI API key here
OPENAI_API_KEY = "api_key"

# Set the environment variable for compatibility with OpenAIEmbeddings
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

query = sys.argv[1]

# loader = TextLoader('data.txt')
loader = DirectoryLoader(".", glob="*.txt")

# Initialize the ChatOpenAI model with the API key as a named parameter
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query, llm=chat_model))


