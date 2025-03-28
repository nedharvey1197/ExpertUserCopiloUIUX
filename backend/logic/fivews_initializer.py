"""
5ws_initializer.py

Purpose:
Extract structured 5Ws (Who, What, Where, When, Why) trial design fields from a raw user prompt using
basic NLP, pattern matching, and optionally GPT-enhanced reasoning.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any

# Load mappings from synopsis_mapping.json
MAPPING_PATH = Path(__file__).parent / "../assets/synopsis_mapping.json"
with open(MAPPING_PATH, "r") as f:
    MAPPINGS = json.load(f)

def match_pattern(category: str, text: str) -> str:
    """Apply first matching rule from mappings."""
    for rule in MAPPINGS.get(category, []):
        if re.search(rule["pattern"], text, re.IGNORECASE):
            return rule["value"].replace("{MATCH}", re.search(rule["pattern"], text).group())
    return "Unknown"

def get_5w_context(raw_input: str) -> Dict[str, Any]:
    """Parses a raw trial description into structured 5Ws."""
    text = raw_input.strip()

    # Apply rule-based matching (future: augment with GPT / RAG)
    what = match_pattern("FiveWs_What", text)
    efficacy = match_pattern("FiveEs_Efficacy", text)
    control = match_pattern("FiveCs_Control", text)

    return {
        "who": {
            "population": "(extract via NLP/GPT or patterns — future module)"
        },
        "what": {
            "intervention": what,
            "control": control
        },
        "why": efficacy,
        "where": {
            "geography": "(infer from site mentions or input — future)"
        },
        "when": {
            "timeline": "(infer if date ranges or durations mentioned)"
        }
    }

# Example CLI test
if __name__ == "__main__":
    example = "We're planning a trial of a targeted therapy for EGFR+ NSCLC, focused on PFS, likely using platinum-based chemotherapy as comparator."
    result = get_5w_context(example)
    print(json.dumps(result, indent=2))