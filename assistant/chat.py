from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.prompts import PromptTemplate
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from config import get_config

global llm
global chain

def load_embedding_model(model_path, normalize_embedding=True):
    return OllamaEmbeddings(model=model_path)
    
def get_response(query, chain):
    return chain.invoke(input=query)["response"]

def input_message(inp):
    global chain
    return get_response(inp, chain)
    
    
def setup_chat():
    llm = Ollama(model=get_config()["models"]["llm_model"]["model"])
    PROMPT = PromptTemplate(input_variables=['entities', 'history', 'input'], template=get_config()["models"]["llm_model"]["template"])
    global chain
    chain = ConversationChain(llm=llm, memory=ConversationEntityMemory(llm=llm), prompt=PROMPT, verbose=get_config()["models"]["llm_model"]["verbose"])