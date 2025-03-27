from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def query_neo4j(query: str, params: dict = {}):
    with driver.session() as session:
        result = session.run(query, **params)
        return [record.data() for record in result]