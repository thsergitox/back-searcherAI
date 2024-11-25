from langgraph.graph import StateGraph, END
from typing import Optional, Dict, List
import logging

from app.research.tools.arxiv_tool import ArxivSearcher
from app.research.states.state_query import QueryState
from app.research.states.state_sugerence import SugerenceState
from app.research.states.state_graph import KnowledgeGraphState
from app.research.states.state_constructor import StateConstructor

from app.research.settings import settings
from app.research.agents.translator import translator_step
from app.research.first_search.analyze_papers import analyze_step
from app.research.first_search.recommender import recommender_step
from app.research.first_search.reference_extractor import extract_reference_papers
from app.research.first_search.query_enhancer import enhance_query

from app.research.retriever.translator_query import supervisor_step, type_query
from app.research.retriever.embedding import embed_step
from app.research.retriever.cypher import cypher_step
from app.research.retriever.synthetizer import synth_step

MAX_LEN_CONTEXT_WINDOW = 10

# Use settings for logging configuration

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


# REFINEMENT

def create_refinement_workflow() -> StateGraph:
    workflow = StateGraph(QueryState)
    
    workflow.add_node("ref_extractor", extract_reference_papers)
    workflow.add_node("query_enhancer", enhance_query)
    
    workflow.set_entry_point("ref_extractor")
    workflow.add_edge("ref_extractor", "query_enhancer")
    workflow.add_edge("query_enhancer", END)

    return workflow.compile()

def run_refinement(topic: str) -> Optional[Dict]:
    try:
        workflow = create_refinement_workflow()
        initial_state = QueryState()
        initial_state["query"] = topic
        return workflow.invoke(initial_state) # Run the workflow
    except Exception as e:
        logger.error(f"x - Error during refinement: {e}")
        return None


# SEARCH

def run_search(queries: List, max_results = 1, sort_by="Relevance"):
    arxiv_searcher = ArxivSearcher()
    all_results = []
    for enhanced_query in queries:
        results = arxiv_searcher.search(
                        enhanced_query,
                        max_results=max_results,
                        sort_by=sort_by)
        all_results.extend(results)
    # Remove duplicates based on entry_id
    unique_results = list({paper['entry_id']: paper for paper in all_results}.values())
    
    return unique_results

#[
#{
#    title:,
#    abstract,
#    ...
#},
#{
#    title:
#}
#]

# SUGERENCE

def create_sugerence_workflow() -> StateGraph:
    """Create and configure the research workflow graph with chat-like interface"""
    workflow = StateGraph(state_schema=SugerenceState)

    workflow.add_node("analyze", analyze_step)
    workflow.add_node("recommend", recommender_step)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "recommend")
    workflow.add_edge("recommend", END) 
    return workflow.compile()

def run_sugerence(papers: List[Dict]) -> Optional[Dict]:
    try:
        workflow = create_sugerence_workflow()
        initial_state = SugerenceState()
        initial_state["papers"] = papers
        response = workflow.invoke(initial_state) # Run the workflow
        response.pop()
        return workflow.invoke(initial_state) # Run the workflow
    except Exception as e:
        logger.error(f"x - Error during sugerence: {e}")
        return None

# GRAPH CONSTRUCTOR

def init_constructor_state(papers: List[Dict]) -> StateConstructor:
    """
    Initializes a StateConstructor with the given papers.
    Args:
        papers: List of paper dictionaries
    Returns:
        StateConstructor: Initialized state with default values
    """
    return StateConstructor(
        papers=papers,
        atomized_answer= [],
        stage='',
        next='',
        source='arxiv'
    )

def run_construction(papers: List[Dict]) -> Optional[Dict]:
    try:
        initial_state = init_constructor_state(papers=papers)
        return translator_step(initial_state)
    except Exception as e:
        logger.error(f"x - Error during construction of the Knowledge Graph: {e}")
        return None

# RETRIEVER

def init_retriever_state(topic: str)->KnowledgeGraphState:
    return KnowledgeGraphState(
        stage = "",
        next = "",
        user_input = topic,
        top_k = 1,
        similarity_threshold= 0.7,
        query_type = [],
        embeddings_result = [],
        cypher_result = [],
        answer=''
    )

def retriever_workflow() -> StateGraph:
    workflow = StateGraph(KnowledgeGraphState)
    # NODES
    workflow.add_node("supervisor", supervisor_step)
    workflow.add_node("embedding", embed_step)
    workflow.add_node("cypher", cypher_step)
    workflow.add_node("synthetizer", synth_step)
    # EDGES
    workflow.add_conditional_edges(
                                    "supervisor",
                                    type_query, 
                                    {
                                        "embed_step": "embedding",
                                        "cypher_step": "cypher"
                                    }
                                )
    workflow.add_edge("supervisor","embedding")
    workflow.add_edge("embedding", "synthetizer")
    workflow.add_edge("cypher", "synthetizer")
    workflow.add_edge("synthetizer", END)
    workflow.set_entry_point("supervisor")
    return workflow.compile()

def query_graph(topic: str) -> Optional[Dict]:
    try:
        logger.warning(topic)
        workflow = retriever_workflow()
        initial_state = init_retriever_state(topic=topic)
        return workflow.invoke(initial_state) # Run the workflow
    except Exception as e:
        logger.error(f"y - Error during retrieve: {e}")
