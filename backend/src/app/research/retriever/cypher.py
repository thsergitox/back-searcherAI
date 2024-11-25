from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph
from typing import Dict, List, Any
from app.research.settings import neo4j_driver, settings
from neo4j.graph import Node, Relationship

def node_to_dict(node: Node) -> Dict[str, Any]:
    """Convert Neo4j Node to dictionary format"""
    return {
        "id": node.id,
        "labels": list(node.labels),
        "properties": dict(node.items())
    }

def relationship_to_dict(rel: Relationship) -> Dict[str, Any]:
    """Convert Neo4j Relationship to dictionary format"""
    return {
        "id": rel.id,
        "type": rel.type,
        "properties": dict(rel.items()),
        "start_node": rel.start_node.id,
        "end_node": rel.end_node.id
    }

def process_neo4j_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Process a Neo4j record and convert all nodes and relationships to dictionaries"""
    processed_record = {}
    
    for key, value in record.items():
        if isinstance(value, Node):
            processed_record[key] = node_to_dict(value)
        elif isinstance(value, Relationship):
            processed_record[key] = relationship_to_dict(value)
        elif isinstance(value, list):
            processed_record[key] = [
                node_to_dict(item) if isinstance(item, Node)
                else relationship_to_dict(item) if isinstance(item, Relationship)
                else item
                for item in value
            ]
        else:
            processed_record[key] = value
            
    return processed_record

def cypher_step(state: Dict) -> Dict:
    """
    Execute Cypher query and store results in state
    """
    state["next"] = "synthetizer"
    try:
        # Initialize LLM and graph
        llm = ChatGroq(
            model=settings.groq_model,
            temperature=0.1,
            api_key=settings.groq_api_key
        )
        
        graph = Neo4jGraph(
            url=settings.url,
            username=settings.username,
            password=settings.password
        )

        # Cypher query generation template
        cypher_generation_template = """
        Task: Generate a Cypher query to query a graph database.  
        Instructions: 
        - Use only the types of relationships and properties provided in the schema. 
        - Do not include explanations or apologies in your responses. 
        - Do not answer questions that do not require the construction of a Cypher query. 
        - Do not include any additional text besides the generated Cypher query.
        - id is the attribute that keeps the node name, so keep in mind that id = name
        Schema: {schema}

        Examples of Cypher queries:  
        "MATCH (p:Paper)->[r:RELATED_TO]->(m:Model) WHERE m.id='<User requirement>' RETURN p AS papers,r AS relationship,m AS Model"
        "MATCH (p:Paper) WHERE p.year>2023 RETURN p AS papers"
        "(a:Author)-[r:AUTHOR_OF]->(p:Paper) WHERE p.id = '<User requirement>' RETURN a AS author"

        The question is:  
        {question}
        """

        cypher_prompt = PromptTemplate(
            template=cypher_generation_template,
            input_variables=["schema", "question"]
        )
        
        # Generate Cypher query
        rendered_prompt = cypher_prompt.format(
            schema=graph.get_schema(),
            question=state["user_input"]
        )
        cypher_query = llm.predict(rendered_prompt)
        
        # Execute query and process results
        results: List[Dict[str, Any]] = []
        with neo4j_driver.session() as session:
            # Execute the query
            result = session.run(query=cypher_query)
            
            # Process each record
            for record in result:
                # Convert record to dictionary
                record_dict = dict(record)
                # Process all nodes and relationships in the record
                processed_record = process_neo4j_record(record_dict)
                results.append(processed_record)

        # Update state with results
        state["query_type"] = "cypher_step"
        state["cypher_result"] = results
        return state

    except Exception as e:
        error_state = state.copy()
        error_state["next"] = "end"
        error_state["query_type"] = "cypher_step"
        error_state["cypher_result"] = []
        error_state["error"] = str(e)
        print(f"Error in cypher_step: {str(e)}")
        
        return error_state