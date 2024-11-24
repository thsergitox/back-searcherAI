from typing import List , Dict, Annotated, TypedDict, Optional
from enum import Enum

class QueryType(str, Enum):
    EMBEDDING = "embed_step"
    CYPHER = "cypher_step"

class KnowledgeGraphState(TypedDict, total = False):
    stage: str = ''
    next: str = 'supervisor'
    user_input: str = ''
    top_k: int = 5
    similarity_threshold: float = 0.7
    query_type: Optional[QueryType] = None
    embedding_result: Optional[List[dict]] = None
    cypher_result: Optional[List[dict]] = None
    answer: str = ''
