import psycopg2
from neo4j import GraphDatabase

# PostgreSQL Connection
pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Aariz13518",  # Replace with actual password
    host="localhost",
    port="1351"
)
pg_cursor = pg_conn.cursor()

# Neo4j Connection
neo4j_uri = "bolt://localhost:7689"
neo4j_user = "neo4j"
neo4j_password = "Aariz13518"
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def sync_data():
    print("🔄 Syncing data from PostgreSQL to Neo4j...")

    # Fetch Criminals and Crimes
    pg_cursor.execute("""
        SELECT 
            cp.id AS criminal_id, 
            cp.name AS criminal_name, 
            cp.date_of_birth, 
            cp.unique_identification,
            c.crime_id, 
            c.date AS crime_date, 
            c.location, 
            c.area, 
            c.type AS crime_type, 
            c.modus_operandi, 
            c.fir_no, 
            c.fir_status, 
            c.victim_name, 
            c.bail_details, 
            c.bail_grant_date, 
            c.trial_progress
        FROM criminal_person cp
        JOIN cc_mapping ccm ON cp.id = ccm.criminal_id
        JOIN crime c ON ccm.crime_id = c.crime_id;
    """)
    crimes = pg_cursor.fetchall()

    # Fetch Related Persons
    pg_cursor.execute("""
        SELECT 
            r.person_id, r.name, r.date_of_birth, 
            r.relationship, r.criminal_id 
        FROM related_to r;
    """)
    related_people = pg_cursor.fetchall()

    # Insert data into Neo4j
    def update_neo4j(tx, criminal_id, criminal_name, date_of_birth, unique_id,
                     crime_id, crime_date, location, area, crime_type, modus_operandi,
                     fir_no, fir_status, victim_name, bail_details, bail_grant_date, trial_progress):
        query = """
            MERGE (c:Criminal {id: $criminal_id})
            SET c.name = $criminal_name, 
                c.date_of_birth = $date_of_birth,
                c.unique_identification = $unique_id
            
            MERGE (cr:Crime {id: $crime_id})
            SET cr.date = $crime_date, 
                cr.location = $location, 
                cr.area = $area,
                cr.type = $crime_type, 
                cr.modus_operandi = $modus_operandi

            MERGE (c)-[:COMMITTED]->(cr)

            MERGE (a:Area {name: $area})
            MERGE (cr)-[:OCCURRED_IN]->(a)

            MERGE (t:CrimeType {type: $crime_type})
            MERGE (cr)-[:HAS_TYPE]->(t)

            MERGE (m:ModusOperandi {description: $modus_operandi})
            MERGE (cr)-[:HAS_MODUS_OPERANDI]->(m)

            MERGE (f:FIR {fir_no: $fir_no})
            SET f.fir_status = $fir_status, f.victim_name = $victim_name
            MERGE (cr)-[:HAS_FIR]->(f)

            MERGE (b:Bail {id: $crime_id})  // Bail linked to crime
            SET b.bail_details = $bail_details, b.bail_grant_date = $bail_grant_date
            MERGE (f)-[:HAS_BAIL]->(b)

            MERGE (tp:TrialProgress {id: $crime_id})  // Trial progress linked to crime
            SET tp.progress_details = $trial_progress
            MERGE (f)-[:HAS_TRIAL_PROGRESS]->(tp);
        """
        tx.run(query, criminal_id=criminal_id, criminal_name=criminal_name, date_of_birth=date_of_birth,
               unique_id=unique_id, crime_id=crime_id, crime_date=crime_date, location=location,
               area=area, crime_type=crime_type, modus_operandi=modus_operandi, fir_no=fir_no,
               fir_status=fir_status, victim_name=victim_name, bail_details=bail_details,
               bail_grant_date=bail_grant_date, trial_progress=trial_progress)

    def update_related_persons(tx, person_id, person_name, date_of_birth, criminal_id, relationship):
        query = """
            MATCH (c:Criminal {id: $criminal_id}) 
            SET c.name = $person_name
            WITH c
            MATCH (p:Person {person_id: $person_id})
            SET p.date_of_birth = $date_of_birth
            MERGE (p)-[:RELATED_TO {relationship: $relationship}]->(c)
        """
        tx.run(query, person_id=person_id, person_name=person_name, date_of_birth=date_of_birth,
            criminal_id=criminal_id, relationship=relationship)



    with neo4j_driver.session() as session:
        for crime in crimes:
            session.execute_write(update_neo4j, *crime)

        for person in related_people:
            session.execute_write(update_related_persons, *person)

    print("✅ Data Sync Completed! 🚀")

if __name__ == "__main__":
    sync_data()
    print("Go to Neo4j Browser: http://localhost:7474/")

# Cleanup
pg_cursor.close()
pg_conn.close()
neo4j_driver.close()
