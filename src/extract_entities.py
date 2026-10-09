import json
import re
from llm import ask

SYSTEM = (
    "You extract biomedical knowledge from text. Return ONLY valid JSON: "
    '{"entities":[{"name":str,"type":"Disease|Treatment|Measure"}],'
    '"relations":[{"source":str,"target":str,'
    '"type":"TREATS|MEASURED_BY|ASSOCIATED_WITH"}]}. '
    "TREATS goes from a Treatment to a Disease. MEASURED_BY goes from a Disease "
    "to a Measure. ASSOCIATED_WITH links two Diseases. Use lowercase names."
)


def extract(text: str) -> dict:
    raw = ask(SYSTEM, text, max_tokens=1500)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)
