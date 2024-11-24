from typing import Dict, List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from src.research.settings import settings

def format_embedding_results(results: List[Dict]) -> str:
    """Format embedding results into a readable context string"""
    formatted_contexts = []
    for idx, result in enumerate(results, 1):
        content = result.get('content', '')
        source = result.get('source', 'Unknown')
        similarity = result.get('similarity', 0)
        formatted_contexts.append(
            f"Document {idx}:\n"
            f"Content: {content}\n"
            f"Source: {source}\n"
            f"Relevance Score: {similarity:.2f}\n"
        )
    return "\n".join(formatted_contexts)

def format_cypher_results(results: List[Dict]) -> str:
    """Format cypher query results into a readable context string"""
    formatted_results = []
    for idx, record in enumerate(results, 1):
        formatted_record = [f"Result {idx}:"]
        
        for key, value in record.items():
            if isinstance(value, dict):
                # Handle node or relationship
                if "properties" in value:
                    props_str = ", ".join(f"{k}: {v}" for k, v in value["properties"].items())
                    if "labels" in value:  # Node
                        formatted_record.append(f"{key} (Node - {', '.join(value['labels'])}): {props_str}")
                    else:  # Relationship
                        formatted_record.append(f"{key} (Relationship - {value['type']}): {props_str}")
            else:
                formatted_record.append(f"{key}: {value}")
                
        formatted_results.append("\n".join(formatted_record))
    
    return "\n\n".join(formatted_results)

def synth_step(state: Dict) -> Dict:
    """
    Synthesize an answer from either embedding or cypher results using LLM.
    """
    try:
        llm = ChatGroq(
            model=settings.groq_model,
            temperature=0,
            api_key=settings.groq_api_key
        )

        # Enhanced prompt template with better instruction and structure
        prompt = PromptTemplate(
            template="""
            Based on the following context information, provide a comprehensive answer to the user's query.
            
            Context Information:
            {context}
            
            User Query:
            {query}
            
            Instructions:
            1. Use only the information provided in the context
            2. If the context doesn't contain enough information to answer fully, acknowledge this
            3. Provide specific references to support your answer
            4. Use a clear and concise writing style
            
            Answer:
            """,
            input_variables=["context", "query"]
        )

        # Process results based on type
        if state.get("embedding_result"):
            formatted_context = format_embedding_results(state["embedding_result"])
        elif state.get("cypher_result"):
            formatted_context = format_cypher_results(state["cypher_result"])
        else:
            state.update({
                "stage": "synthetizer",
                "next": "END",
                "answer": "No results available to synthesize an answer."
            })
            return state

        # Generate answer using LLM
        answer = llm.predict(
            prompt.format(
                context=formatted_context,
                query=state["user_input"]
            )
        )

        # Update state with results
        state.update({
            "stage": "synthetizer",
            "next": "END",
            "answer": answer
        })

        return state

    except Exception as e:
        # Handle errors gracefully
        state.update({
            "stage": "synthetizer_error",
            "next": "END",
            "answer": f"Error during synthesis: {str(e)}",
            "error": str(e)
        })
        
        # Log the error
        print(f"Error in synth_step: {str(e)}")
        
        return state