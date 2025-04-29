from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:" + os.getenv("NEO4J_PORT")
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Load Sentence-Transformers Model (384-dim)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")





def query_vector_embeddings(uri, user, password, text,crime_type):
    """Classifies crime, converts to embeddings, and runs a filtered vector search."""
    
    # Step 2: Convert text to vector embeddings
    query_embedding = model.encode(text).tolist()

    # Step 4: Cypher query to filter by multiple types and perform vector search
    query = """
    MATCH (t:CrimeType {type: $crime_type})<-[:HAS_TYPE]-(c:Crime)-[:HAS_MODUS_OPERANDI]->(m:ModusOperandi)
    CALL db.index.vector.queryNodes('modusOperandiIndex', 3, $vector) 
    YIELD node, score 
    RETURN DISTINCT node.id AS crime_id, node.description AS modus_operandi, score
    ORDER BY score DESC;
    """

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        try:
            print("Executing query...")
            result = session.run(query, vector=query_embedding, crime_type=crime_type)
            
            print("Query executed successfully.")
            if(result):
                for record in result:
                    print(f"Modus Operandi: {record['modus_operandi']},Crime_id: {record['crime_id']}, Score: {record['score']}")
            else:
                print("No similar modus operandi found.")
            driver.close()
        except Exception as e:
            print(f"Query execution failed: {e}")
            driver.close()
            return

        

# Example Usage
query_text = "breached bank by breaking into glass"
type="Robbery"
query_vector_embeddings(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, query_text,type)
