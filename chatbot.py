import os
from langchain.chat_models import ChatOpenAI #Provides the Model which will become the Chatbot
from langchain.agents import create_csv_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.utilities import WikipediaAPIWrapper
import gradio as gr


from system import openaiapikey
os.environ['OPENAI_API_KEY'] = openaiapikey

llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0)


first_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of olympic information retrieval. 
It uses 2 tools for this and its sources of information are a CSV file and wikipedia's information.
As a language model, Assistant is capable of generating human-like text based on the input it receives, enabling it to provide coherent 
and relevant responses that sound natural when it is responding to queries about olympics.'''

web_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of latest olympic information retrieval. 
Its source of information is information retrieved from search engine duckduckgo.
As a language model, Assistant is capable of generating human-like text based on the input it receives, enabling it to provide coherent 
and relevant responses that sound natural when it is responding to queries about olympics.'''

wiki_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of elaborate olympic information retrieval. 
Its source of information is wikipedia's data.As a language model, Assistant is capable of generating human-like text based on the
input it receives, enabling it to provide coherent and relevant responses that sound natural when it is responding to queries about olympics.'''

scrapper_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of olympic diet and exercise planning information retrieval. 
It uses 2 tools for this and its sources of information are information retrieved from search engine duckduckgo and wikipedia's information.
As a language model, Assistant is capable of generating human-like text based on the input it receives, enabling it to provide coherent 
and relevant responses that sound natural when it is responding to queries about olympics.'''

main_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of olympic information retrieval. 
It uses 3 tools for this and its sources of information are a CSV file, information retrieved from search engine duckduckgo and wikipedia's information.
As a language model, Assistant is capable of generating human-like text based on the input it receives, enabling it to provide coherent 
and relevant responses that sound natural when it is responding to queries about olympics.'''

sec_prompt=''' Assistant is a very helpful Large Language Model developed for the specific purpose of olympic diet and exercise planning information retrieval. 
It uses 2 tools for this and its sources of information are information retrieved from search engine duckduckgo and wikipedia's information.
As a language model, Assistant is capable of generating human-like text based on the input it receives, enabling it to provide coherent 
and relevant responses that sound natural when it is responding to queries about olympics.'''

def csv_reader_tool():
    csv_file = "modified_file.csv"
    data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Create a Tool instance using the CSV reader function
csv_tool = Tool(
    name="csv_reader",
    func=csv_reader_tool,
    description="Retrieves information about the Olympics from CSV file"
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
        name = "search",
        func = search.run,
        description="Uses search engine Duckduckgo to search information about olympics online for player information, country olympic record,olympic event itself, diet and exercise plans etc"
)

wikipedia = WikipediaAPIWrapper()
wikipedia_tool = Tool(
        name = "wikipedia",
        func = wikipedia.run,
        description = "Uses wikipedia to search information about olympics, such as player information, country olympic record,olympic event itself, diet and exercise plans etc"
)

memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

prim_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[csv_tool,wikipedia_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
prim_agent.agent.llm_chain.prompt.messages[0].prompt.template = first_prompt

web_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[search_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
web_agent.agent.llm_chain.prompt.messages[0].prompt.template = web_prompt

wiki_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[wikipedia_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
wiki_agent.agent.llm_chain.prompt.messages[0].prompt.template = wiki_prompt

scrapper_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[search_tool,wikipedia_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
scrapper_agent.agent.llm_chain.prompt.messages[0].prompt.template = scrapper_prompt

main_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[csv_tool,wikipedia_tool,search_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
prim_agent.agent.llm_chain.prompt.messages[0].prompt.template = main_prompt

sec_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=[wikipedia_tool,search_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=memory
)
sec_agent.agent.llm_chain.prompt.messages[0].prompt.template = sec_prompt

# def ask(question):
#     if "routine" or "plan" in question:
#         response=scrapper_agent.run(question)
#     elif "latest" in question:
#         response=web_agent.run(question)
#     else:
#         try:
#             response=prim_agent.run(question)
#         except:
#             print("\n\nCSV didn't work\n\n")
#             response=wiki_agent.run(question)
#     print(response)

def ask(question,display):
    
    display = display or []
    show = list(sum(display, ()))
    show.append(input)
    #ip = ' '.join(show)
    try:
        response=main_agent.run(question)
    except:
        response=sec_agent.run(question)
    display.append((question, response))
    return display,display
  
#ask("question")
import gradio as gr

block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>OLYMPIC GPT</center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Please ask your Olympic related Query!", label="QUESTION")
    state = gr.State()
    submit = gr.Button("ASK")
    submit.click(ask, inputs=[message, state], outputs=[chatbot, state])

# Launch the Gradio app on a specific local address and port
block.launch( server_port=7861, debug=True)



