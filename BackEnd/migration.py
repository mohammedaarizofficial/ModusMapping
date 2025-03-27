from neo4j import GraphDatabase
import psycopg2
# neo4j_db_name="modusmapping DBMS"
# PostgreSQL Configuration
PG_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Aariz13518",
    "host": "localhost",
    "port": 1351
}

# Neo4j Configuration
NEO4J_CONFIG = {
    "uri": "bolt://localhost:7689",
    "user": "neo4j",
    "password": "Aariz13518"
}

def fetch_postgres_data():
    """Fetch data from PostgreSQL"""
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    queries = {
        "criminals": "SELECT id, name, date_of_birth, unique_identification FROM criminal_person;",
        "crimes": "SELECT crime_id, date, location, area, type FROM crime;",
        "crime_types": "SELECT DISTINCT type FROM crime;",
        "modus_operandi": "SELECT crime_id, modus_operandi FROM crime;",
        "fir": "SELECT fir_no, fir_status, victim_name, crime_id FROM crime;",
        "bail": "SELECT crime_id, bail_details, bail_grant_date FROM crime;",
        "trial_progress": "SELECT crime_id, trial_progress FROM crime;",
        "areas": "SELECT DISTINCT area FROM crime;",
        "cc_mapping": "SELECT crime_id, criminal_id FROM cc_mapping;",
        "related_to": "SELECT person_id, criminal_id, relationship FROM related_to;",
        "person":" SELECT person_id,name,date_of_birth FROM persons;"
    }

    data = {key: [] for key in queries}

    for key, query in queries.items():
        cur.execute(query)
        data[key] = cur.fetchall()

    cur.close()
    conn.close()
    # print(data["fir"])
    return data


def push_to_neo4j():
    """Push data from PostgreSQL to Neo4j"""
    driver = GraphDatabase.driver(NEO4J_CONFIG["uri"], auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"]))
    data = fetch_postgres_data()

    with driver.session() as session:
        # ❌ Delete all nodes and relationships
        session.run("MATCH (n) DETACH DELETE n;")
        print("🗑️ Deleted all existing nodes and relationships.")

        # Insert Criminals
        for criminal in data["criminals"]:
            session.run("""
                CREATE (:Criminal {id: $id, name: $name, date_of_birth: $dob, unique_identification: $uid})
            """, id=criminal[0], name=criminal[1], dob=str(criminal[2]), uid=criminal[3])

        # Insert Crimes
        for crime in data["crimes"]:
            session.run("""
                CREATE (:Crime {
                    crime_id: $id, 
                    date: $date, 
                    location: $location, 
                    area: $area,
                    fir_no: $fir_no, 
                    modus_operandi: $mo_id, 
                    bail_id: $bail_id, 
                    trial_progress_id: $trial_id,
                    type: $type
>>>>>>> b38377d (deletes before sync)
=======
>>>>>>> fdab5247d827034fe7df2b02cc0b4ad0ece18d93
                })
            """, id=crime[0], date=str(crime[1]), location=crime[2], area=crime[3],
                fir_no=crime[0], mo_id=crime[0], bail_id=crime[0], trial_id=crime[0], type=crime[4])

        # Insert Crime Types
        for ctype in data["crime_types"]:
            session.run("CREATE (:CrimeType {type: $type})", type=ctype[0])

        # Insert Modus Operandi
        for mo in data["modus_operandi"]:
            session.run("CREATE (:ModusOperandi {id: $id, description: $desc})", id=mo[0], desc=mo[1])

        # Insert FIR
        for fir in data["fir"]:
            session.run("""
                CREATE (:FIR {fir_no: $fir_no, fir_status: $status, victim_name: $victim,crime_id: $crime_id })
            """, fir_no=fir[0], status=fir[1], victim=fir[2], crime_id=fir[3])

        # Insert Bail
        for bail in data["bail"]:
            session.run("""
                CREATE (:Bail {id: $id, bail_details: $details, bail_grant_date: $date})
            """, id=bail[0], details=bail[1], date=str(bail[2]))

        # Insert Trial Progress
        for trial in data["trial_progress"]:
            session.run("""
                CREATE (:TrialProgress {id: $id, progress_details: $details})
            """, id=trial[0], details=trial[1])

        # Insert Areas
        for area in data["areas"]:
            session.run("CREATE (:Area {name: $name})", name=area[0])

        # Insert Criminal-Crime relationships
        for mapping in data["cc_mapping"]:
            session.run("""
                MATCH (c:Criminal {id: $criminal_id}), (cr:Crime {crime_id: $crime_id})
                CREATE (c)-[:COMMITTED]->(cr)
            """, criminal_id=mapping[1], crime_id=mapping[0])

        
        # Insert Related People
        for person in data["person"]:
            session.run("""
                MERGE (p:Person {id: $id})
                SET p.name = $name, p.date_of_birth = $dob
            """, id=person[0], name=person[1], dob=str(person[2]) if person[2] else None)

        #connections between related people
        for relation in data["related_to"]:
            session.run("""
                MATCH (c:Criminal {id: $criminal_id}), (p:Person {id: $id})
                MERGE (p)-[:RELATED_TO {relationship: $relationship}]->(c)
            """, criminal_id=relation[1], id=relation[0], relationship=relation[2])

        # Create relationships for Crime nodes
        session.run("""
            MATCH (c:Crime), (t:CrimeType)
            WHERE c.type = t.type
            CREATE (c)-[:HAS_TYPE]->(t)
        """)


        session.run("""
            MATCH (c:Crime), (a:Area)
            WHERE c.area = a.name
            CREATE (c)-[:OCCURRED_IN]->(a)
        """)

        session.run("""
            MATCH (c:Crime), (m:ModusOperandi)
            WHERE c.modus_operandi = m.id
            CREATE (c)-[:HAS_MODUS_OPERANDI]->(m)
        """)
        

        session.run("""
            MATCH (f:FIR), (c:Crime)
            WHERE f.crime_id = c.crime_id
            CREATE (f)-[:FILED_FOR]->(c)
        """)

        session.run("""
            MATCH (b:Bail), (c:Crime)
            WHERE c.bail_id = b.id
            CREATE (c)-[:HAS_BAIL]->(b)
        """)

        session.run("""
            MATCH (t:TrialProgress), (c:Crime)
            WHERE c.trial_progress_id = t.id
            CREATE (c)-[:HAS_TRIAL_PROGRESS]->(t)
        """)

    driver.close()
    print("✅ Data migration completed successfully!")


if __name__ == "__main__":
    push_to_neo4j()
