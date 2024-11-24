import numpy as np
from scipy.spatial.distance import cosine
from typing import Dict

from src.research.settings import client_openai, settings, neo4j_driver

def get_embedding(text, model: str = "text-embedding-ada-002"):
    embedding_result = client_openai.embeddings.create(
        model = model,
        input = [text]
    )
    return embedding_result.data[0].embedding

def embed_step(state: Dict)->Dict:
        query_embedding = np.array(get_embedding(state["user_input"]))
        with neo4j_driver.session() as session:
            # Fetch all paper embeddings
            result = session.run(
            """
            MATCH (p:Paper)
            WHERE p.abstract_embedding IS NOT NULL
            RETURN
            p.id as id,
            p.abstract as abstract,
            p.abstract_embedding as embedding
            """
            )
            similarities = []
            threshold = state["similarity_threshold"]

            for record in result:
                paper_embedding = np.array(record['embedding'])
                # Calculate cosine similarity
                similarity = 1 - cosine(query_embedding, paper_embedding)
                # Add to results if above threshold
                if similarity >=  threshold:
                    similarities.append({
                        'title': record['id'],
                        'abstract': record['abstract'],
                        'similarity_score': similarity
                    })
            # Sort by similarity score and return top k
            state["embedding_result"] = sorted(
                similarities, 
                key=lambda x: x['similarity_score'], 
                reverse=True
            )[:state["top_k"]]
        return state