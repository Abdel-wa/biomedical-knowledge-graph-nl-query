# Biomedical Knowledge Graph with Natural-Language Querying

Extracts entities (diseases, treatments, measures) from scientific abstracts with an LLM,
stores them as a knowledge graph in Neo4j, and answers natural-language questions by
translating them to Cypher.

## Pipeline
1. `extract_entities.py`: LLM-based entity and relation extraction (JSON output)
2. `build_graph.py`: loads the entities and relations into Neo4j
3. `query_nl.py`: question → Cypher (read-only) → graph results → answer

## Run
```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
# put ~10 abstracts as .txt files in data/articles/
python src/build_graph.py
python src/query_nl.py "Which treatments are used for type 2 diabetes?"
```

## Limits
Small corpus, no entity normalization (synonyms are not merged), and generated
Cypher is checked only by a keyword filter. Next steps: ontology alignment, RAG over
the source texts, evaluation on a labeled set.
