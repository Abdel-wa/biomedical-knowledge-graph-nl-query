import os
import re
import sys
from neo4j import GraphDatabase, READ_ACCESS
from llm import ask

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

SCHEMA = """Nodes: Disease(name), Treatment(name), Measure(name). All names are lowercase.
Relations: (Treatment)-[:TREATS]->(Disease), (Disease)-[:MEASURED_BY]->(Measure),
(Disease)-[:ASSOCIATED_WITH]->(Disease)."""

CYPHER_SYSTEM = (
    f"You translate questions into Cypher for Neo4j.\n{SCHEMA}\n"
    "Return ONLY one read-only Cypher query, no explanation. "
    "Match names with toLower(n.name) CONTAINS '...'."
)
FORBIDDEN = re.compile(r"\b(CREATE|DELETE|SET|MERGE|REMOVE|DROP|CALL)\b", re.I)


def answer(question: str) -> str:
    cypher = re.sub(r"```cypher|```", "", ask(CYPHER_SYSTEM, question)).strip()
    if FORBIDDEN.search(cypher):
        return "Refused: generated query is not read-only."
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session(default_access_mode=READ_ACCESS) as session:
        rows = [r.data() for r in session.run(cypher)]
    driver.close()
    print(f"Cypher: {cypher}\nRows: {rows}\n")
    return ask(
        "Answer the question using only the provided graph results.",
        f"Question: {question}\nResults: {rows}",
    )


if __name__ == "__main__":
    print(answer(" ".join(sys.argv[1:])))
