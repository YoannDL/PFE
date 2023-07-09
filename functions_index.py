from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display

# Set your OpenAI API key
api_key = "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"

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM (Language Model)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    # load documents from the specified directory
    documents = SimpleDirectoryReader(directory_path).load_data()

    # create a service context for indexing
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # create a GPTSimpleVectorIndex using the loaded documents and service context
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    # save the index to disk
    index.save_to_disk('index.json')

    return index

def ask_ai():
    # load the index from disk
    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    while True:
        # prompt the user for a query
        query = input("What do you want to ask? ")

        # query the index with the user's input
        response = index.query(query)

        # display the response using Markdown formatting
        display(Markdown(f"Response: <b>{response.response}</b>"))

# Specify the directory path when calling the construct_index function
directory_path = "/path/to/directory"
index = construct_index(directory_path)

# Start asking questions using the ask_ai function
ask_ai()