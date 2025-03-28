import ollama
import threading
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import time

load_dotenv()

# Neo4j Configuration
NEO4J_CONFIG = {
    "uri": "bolt://localhost:"+os.getenv("NEO4J_PORT"),
    "user": "neo4j",
    "password": os.getenv("NEO4J_PASSWORD"),
}

def check_input():
    """Check for user input while listening for database changes"""
    while True:
        name = input("\nEnter a criminal's name to search (or type 'exit' to quit): ").strip()
        if name.lower() == "exit":
            print("Exiting...")
            os._exit(0)  # Force exit safely
        elif name:
            summary = summarize_criminal(name)
            print("\n🔍 Criminal Summary:\n", summary)


threading.Thread(target=check_input, daemon=True).start()

def get_criminal_summary(name):
    """Fetch criminal details from Neo4j and summarize"""
    driver = GraphDatabase.driver(NEO4J_CONFIG["uri"], auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"]))

    with driver.session() as session:
        query = """
        MATCH (c:Criminal {name: $name})
        OPTIONAL MATCH (c)-[:COMMITTED]->(cr:Crime)
        OPTIONAL MATCH (c)-[:RELATED_TO]->(p:Person)
        RETURN 
            c.name AS name, 
            c.date_of_birth AS dob, 
            c.unique_identification AS uid, 
            c.description AS desc,
            COLLECT(DISTINCT {crime_id: cr.crime_id, type: cr.type, location: cr.location, date: cr.date}) AS crimes,
            COLLECT(DISTINCT {person: p.name, relation: p.relationship}) AS relations
        """

        result = session.run(query, name=name)
        data = result.single()

    driver.close()
    
    if data:
        return {
            "name": data["name"],
            "date_of_birth": data["dob"],
            "unique_id": data["uid"],
            "description": data["desc"],
            "crimes": data["crimes"],
            "relations": data["relations"]
        }
    return None

        
def summarize_criminal(name):
    """Use Ollama to summarize criminal details"""
    details = get_criminal_summary(name)
    if not details:
        return f"No data found for {name}."

    prompt = f"""
    Generate a detailed summary of the criminal.
    Name: {details['name']}
    Date of Birth: {details['date_of_birth']}
    Unique ID: {details['unique_id']}
    Physical Attributes: {details['description']}
    Crimes: {details['crimes']}
    Relations: {details['relations']}
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


while True:
    time.sleep(1)

    