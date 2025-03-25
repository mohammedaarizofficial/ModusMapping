import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from neo4j import GraphDatabase
import ollama
import time
import threading

# PostgreSQL Connection
pg_conn = psycopg2.connect(
    dbname="ModusMapping",
    user="postgres",
    password="Aariz13518",  # Replace with your actual password
    host="localhost",
    port="1351"
)
pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
pg_cursor = pg_conn.cursor()

# Neo4j Connection
neo4j_uri = "bolt://localhost:7689"
neo4j_user = "neo4j"
neo4j_password = "Aariz13518"  # Replace with your actual password
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Listen for changes in PostgreSQL
pg_cursor.execute("LISTEN modus_mapping_changes;")  # The trigger will send notifications here

# Function to sync data from PostgreSQL to Neo4j
def sync_data():
    print("🔄 Syncing data from PostgreSQL to Neo4j...")

    # Fetch updated data from PostgreSQL
    pg_cursor.execute("SELECT criminal_name, age, date_of_crime, modus_operandi, related_to, location_crime FROM modus_mapping;")
    rows = pg_cursor.fetchall()

    # Get existing Neo4j criminals
    def get_neo4j_criminals(tx):
        query = "MATCH (c:Criminal) RETURN c.name"
        result = tx.run(query)
        return {record["c.name"] for record in result}

    with neo4j_driver.session() as session:
        neo4j_criminals = session.execute_read(get_neo4j_criminals)

    # Prepare a set of PostgreSQL criminal names
    postgres_criminals = {row[0] for row in rows}

    # Delete criminals that are no longer in PostgreSQL
    to_delete = neo4j_criminals - postgres_criminals
    def delete_criminal(tx, criminal_name):
        query = "MATCH (c:Criminal {name: $criminal_name}) DETACH DELETE c"
        tx.run(query, criminal_name=criminal_name)

    with neo4j_driver.session() as session:
        for criminal in to_delete:
            session.execute_write(delete_criminal, criminal)
            print(f"🗑️ Deleted {criminal} from Neo4j")

    # Insert or Update data in Neo4j
    def update_neo4j(tx, criminal_name, age, date_of_crime, modus_operandi, related_to, location_crime):
        query = """
            MERGE (c:Criminal {name: $criminal_name})
            SET c.age = $age, 
                c.date_of_crime = $date_of_crime, 
                c.modus_operandi = $modus_operandi, 
                c.location_crime = $location_crime
        """
        tx.run(query, 
            criminal_name=criminal_name, 
            age=age, 
            date_of_crime=date_of_crime, 
            modus_operandi=modus_operandi, 
            location_crime=location_crime)

        # Ensure relationships are created even if related_to is missing
        if related_to:
            rel_query = """
                MERGE (c1:Criminal {name: $criminal_name})
                MERGE (c2:Criminal {name: $related_to})
                MERGE (c1)-[:RELATED_TO]->(c2)
            """
            tx.run(rel_query, criminal_name=criminal_name, related_to=related_to)


    with neo4j_driver.session() as session:
        for row in rows:
            session.execute_write(update_neo4j, row[0], row[1], row[2], row[3], row[4], row[5])

    print("✅ Crime Data Sync Completed! 🚀")

# Function to listen for database changes
def listen_for_changes():
    print("🔊 Listening for database changes...")
    while True:
        pg_conn.poll()
        while pg_conn.notifies:
            notify = pg_conn.notifies.pop(0)
            print(f"📢 Change detected: {notify.payload}")
            sync_data()

# Function to get a criminal's details from Neo4j
def get_criminal_details(criminal_name):
    with neo4j_driver.session() as session:
        query = """
        MATCH (c:Criminal {name: $criminal_name})
        OPTIONAL MATCH (c)-[:RELATED_TO]->(r:Criminal)
        RETURN c.name AS name, c.age AS age, c.date_of_crime AS date_of_crime, 
               c.modus_operandi AS modus_operandi, c.location_crime AS location_crime,
               COLLECT(r.name) AS related_criminals
        """
        result = session.run(query, criminal_name=criminal_name)
        record = result.single()
        
        if record:
            return {
                "name": record["name"],
                "age": record["age"],
                "date_of_crime": record["date_of_crime"],
                "modus_operandi": record["modus_operandi"],
                "location_crime": record["location_crime"],
                "related_criminals": [r for r in record["related_criminals"] if r]  # Remove None values
            }
        else:
            return None


# Function to summarize criminal details using Ollama
def summarize_criminal(criminal_name):
    details = get_criminal_details(criminal_name)
    
    if not details:
        return f"No records found for {criminal_name}."

    related = ", ".join(details["related_criminals"]) if details["related_criminals"] else "None"

    prompt = f"""
    Based on the following criminal record, generate an analytical summary in a natural and professional tone:
    
    Name: {details['name']}
    Age: {details['age']}
    Date of Crime: {details['date_of_crime']}
    Modus Operandi: {details['modus_operandi']}
    Location of Crime: {details['location_crime']}
    Related Individuals: {related}
    
    The summary should provide insights into the criminal's behavior, potential connections, and any notable patterns observed. Keep it concise but informative.
    """

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    
    return response['message']['content']


# Example: Search for a criminal and generate summary
if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_changes, daemon=True)
    listener_thread.start()

    try:
        while True:
            name = input("\nEnter the criminal's name to search: ").strip()
            if name:
                summary = summarize_criminal(name)
                print("\n🔍 Criminal Summary:\n")
                print(summary)
            else:
                print("❌ Please enter a valid name.")
    except KeyboardInterrupt:
        print("\n❌ Server stopped.")

    # Cleanup
    pg_cursor.close()
    pg_conn.close()
    neo4j_driver.close()
