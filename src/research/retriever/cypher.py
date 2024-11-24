from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph

from typing import Dict
from src.research.settings import neo4j_driver, settings

# TODO
def cypher_step(state: Dict)->Dict:
        llm = ChatGroq(
            model = settings.groq_model,
            temperature = 0,
            api_key=  settings.groq_api_key
        )
        
        graph = Neo4jGraph(
            url = settings.url,
            username = settings.username,
            password = settings.password
        )

        cypher_generation_template = """
        Task: Generate a Cypher query to query a graph database.  
        Instructions: 
        - Use only the types of relationships and properties provided in the schema. 
        - Do not include explanations or apologies in your responses. 
        - Do not answer questions that do not require the construction of a Cypher query. 
        - Do not include any additional text besides the generated Cypher query.

        Schema: {schema}

        Examples of Cypher queries:  
        
        ...

        The question is:  
        {question}
        """

        cypher_prompt = PromptTemplate(
            template = cypher_generation_template,
            input_variables = ["schema", "question"]
        )   
        rendered_prompt = cypher_prompt.format(
            schema= graph.get_schema(),
            question=state["user_input"]
        )
        cypher_query = llm.predict(rendered_prompt)
        with neo4j_driver.session() as session:
            session.run(query = cypher_query)
        return state

