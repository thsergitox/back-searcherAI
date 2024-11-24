from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import logging

<<<<<<< HEAD:src/research/retriever/translator_query.py
from src.research.settings import settings
=======
from app.research.settings import settings
from app.research.settings import client_openai
>>>>>>> 3918bbc (Implement FastAPI routing and restructure application files):src/app/research/retriever/translator_query.py

# Use settings for logging configuration
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

class ReActRetrieverSystem():
    def __init__(self, model:str = settings.groq_model):
        self.llm = ChatGroq(
            model = model,
            temperature = 0,
            api_key=  settings.groq_api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","""
            Analyze the following query and determine if it should be processed as:
            1. A semantic search query (for general knowledge questions)
            2. A Cypher query (for specific graph relationships, patterns, or structural questions)

            Query: {query}

            Think step by step:
            1. Is the query asking about specific relationships or patterns?
            2. Does it involve graph-like structures (connections, paths, relationships)?
            3. Would it benefit from precise graph traversal?
            4. Or is it more about general knowledge/similarity?

            Respond with EITHER 'embed_step' OR 'cypher_step'
            """),
            ("user", "Question: {question}")]
        )

def supervisor_step(state: Dict)->Dict:
    ret = ReActRetrieverSystem()
    state["stage"] = "supervisor"
    response = ret.llm.invoke(
        ret.prompt.format_messages(
            question=state["user_input"]
        )
    )
    veredict:str = response.content
    state["next"] = veredict
    return state

def type_query(state: Dict)->str:
    return state["next"].value
    

    
    
