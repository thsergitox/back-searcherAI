export interface Neo4jConfig {
  serverUrl: string;
  serverUser: string;
  serverPassword: string;
  initialCypher: string;
}

export const DEFAULT_CONFIG: Neo4jConfig = {
  serverUrl: process.env.NEXT_PUBLIC_NEO4J_URI || "bolt://localhost:7687",
  serverUser: process.env.NEXT_PUBLIC_NEO4J_USER || "neo4j",
  serverPassword: process.env.NEXT_PUBLIC_NEO4J_PASSWORD || "password",
  initialCypher: "MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 25"
};