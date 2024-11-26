from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import logging

from app.research.settings import settings

# Use settings for logging configuration
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

def supervisor_step(state: Dict)->Dict:
    llm = ChatGroq(
            model = settings.groq_model,
            temperature = 0,
            api_key=  settings.groq_api_key
        )
    template = """
            Analyze the following query and determine if it should be processed as:
            1. A semantic search query (for general knowledge questions)
            2. A Cypher query (for specific graph relationships, patterns, or structural questions)

            Query: {query}

            Think step by step:
            1. Is the query asking about specific relationships or patterns?
            2. Does it involve graph-like structures (connections, paths, relationships)?
            3. Would it benefit from precise graph traversal?
            4. Or is it more about general knowledge/similarity?

            Respond ONLY WITH "cypher_step" or "embed_step", nothing else
            """
    prompt = PromptTemplate(template=template, input_variables=["query"])
    chain = prompt | llm
    response = chain.invoke({"query": state["user_input"]})
    veredict:str = response.content
    state["next"] = veredict
    return state

def type_query(state: Dict)->str:
    state["next"] = "embed_step" #gaaa
    return state["next"]
    

    
    
