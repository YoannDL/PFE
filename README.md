# PFE
Utilisation du Robot Humanoïde pour promouvoir la biodiversité et le développement durable.

Introduction
Creating our chatbot with custom knowledge base using GPT-3.

Follow the instructions for each steps and then run the code sample. In order to run the code, you need to press "play" button near each code sample.
Download the data for your custom knowledge base
For the demonstration purposes we are going to use our predefined text file as our knowledge base. You can download them to your local folder from the github repository by running the code below. Alternatively, you can put your own custom data into the local folder:

!git clone https://github.com/YoannDL/PFE.git

Install the dependicies
Run the code below to install the depencies we need for our functions

!pip install llama-index==0.5.6

!pip install langchain==0.0.148

Define the functions
Run the python code: functions_index.py which will define the functions we need to construct the index and query it

Set OpenAI API Key
You need an OPENAI API key to be able to run this code.
If you don't have one yet, get it by signing up. Then click your account icon on the top right of the screen and select "View API Keys". Create an API key.
Then run the code below and paste your API key into the text input:
os.environ["OPENAI_API_KEY"] = input("Paste your OpenAI key here and hit enter:")

Construct an index
Now we are ready to construct the index. This will take every file in the folder 'data', split it into chunks, and embed it with OpenAI's embeddings API.
Notice: running this code will cost you credits on your OpenAPI account ($0.02 for every 1,000 tokens). If you've just set up your account, the free credits that you have should be more than enough for this experiment:

construct_index("PFE/data")

Run the function that queries GPT and type your question into the input.

If you've used the provided data for your custom knowledge base, here are a few questions that you can ask these questions for example:
Biodiversity:
    What does biodiversity mean?
    Why is biodiversity important to us?
    Can you give examples of biodiversity?
    What happens if a species goes extinct?
    How does biodiversity affect the food we eat?
    Why are there so many different types of animals and plants?
    How can we help to protect biodiversity?

Sustainable Development:
    What is sustainable development?
    Why is sustainable development important?
    How can we live in a more sustainable way?
    What is a renewable resource? Can you give some examples?
    How does recycling help with sustainable development?
    How does planting trees help the environment?
    What are some ways that we can conserve water?

Finally run this line of code:
ask_ai()

You can also just run the python script queries.py

