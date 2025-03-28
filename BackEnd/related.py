import json
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:" + os.getenv("NEO4J_PORT")
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def find_connected_criminals(uri, user, password, criminal_name):
    query = """
    MATCH (c1:Criminal {name: $criminal_name})-[:RELATED_TO]-(p:Person)-[:RELATED_TO]-(c2:Criminal) 
    RETURN DISTINCT c1.name AS Criminal, c2.name AS Connected_Criminal, p.name AS Intermediary_Person
    """
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run(query, criminal_name=criminal_name)
        criminals = [
            {
                "criminal": record["Criminal"],
                "connected_criminal": record["Connected_Criminal"],
                "intermediary_person": record["Intermediary_Person"]
            }
            for record in result
        ]
    driver.close()
    
    return json.dumps(criminals, indent=4)

# Example Usage
print(find_connected_criminals(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, "John Smith"))
