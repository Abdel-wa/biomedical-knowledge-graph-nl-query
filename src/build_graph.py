import glob
import os
from neo4j import GraphDatabase
from extract_entities import extract

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
LABELS = {"Disease", "Treatment", "Measure"}
RELS = {"TREATS", "MEASURED_BY", "ASSOCIATED_WITH"}


def load(tx, data):
    for e in data.get("entities", []):
        if e["type"] in LABELS:  # whitelist: labels cannot be parameterized
            tx.run(f"MERGE (n:{e['type']} {{name: $name}})", name=e["name"].lower())
    for r in data.get("relations", []):
        if r["type"] in RELS:
            tx.run(
                "MATCH (a {name: $s}), (b {name: $t}) "
                f"MERGE (a)-[:{r['type']}]->(b)",
                s=r["source"].lower(),
                t=r["target"].lower(),
            )


if __name__ == "__main__":
    driver = GraphDatabase.driver(URI, auth=AUTH)
    for path in sorted(glob.glob("data/articles/*.txt")):
        with open(path, encoding="utf-8") as f:
            data = extract(f.read())
        with driver.session() as session:
            session.execute_write(load, data)
        print(f"{path}: {len(data.get('entities', []))} entities, "
              f"{len(data.get('relations', []))} relations")
    driver.close()
