from typing import Dict
from langchain_groq import ChatGroq
from  langchain.prompts import PromptTemplate

from src.research.settings import settings

def synth_step(state: Dict) -> Dict:
    llm = ChatGroq(
            model = settings.groq_model,
            temperature = 0,
            api_key=  settings.groq_api_key
        )
    prompt = PromptTemplate(
            template="""
            Answer the query regard the context information:
            Context: {context}
            Query: {query}
            """,
            input_variables=["query"]
        )
    if state["embedding_result"]:
        state["answer"] = llm.predict(
            prompt.format(
                context = state["embedding_result"], 
                query=state["user_input"]
            )
        )
    elif state["cypher_result"]:
        state["answer"] = llm.predict(
            prompt.format(
                context = state["cypher_result"],
                query = state["user_input"]    
            )
        )
    else:
          state["answer"] = ''
    state["stage"] = "synthetizer"
    state["next"] = "END"
    return state