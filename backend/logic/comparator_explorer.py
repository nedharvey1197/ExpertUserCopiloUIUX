"""
comparator_explorer.py

Purpose:
Suggest appropriate comparators for a clinical trial design based on phase, condition, intervention, and primary endpoint.
Uses historical precedent, condition-specific norms, and knowledge graph inputs (planned).
"""

from typing import List, Dict

# Mock database (to be replaced by embedding + KG queries)
COMPARATOR_KNOWLEDGE_BASE = [
    {
        "condition": "NSCLC",
        "phase": "Phase 3",
        "endpoint": "Overall Survival",
        "intervention_type": "Targeted Therapy",
        "comparator": "Platinum-based chemotherapy",
        "type": "Active Comparator",
        "precedent_count": 43,
        "notes": "Standard of care in >75% of similar Phase 3 NSCLC OS trials"
    },
    {
        "condition": "NSCLC",
        "phase": "Phase 2",
        "endpoint": "Progression-Free Survival",
        "intervention_type": "Immunotherapy",
        "comparator": "Placebo",
        "type": "Placebo Comparator",
        "precedent_count": 12,
        "notes": "Used in maintenance immunotherapy trials when SOC is observation"
    }
    # Add more mock precedents as needed
]

def suggest_comparators(design_inputs: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Return a list of comparator suggestions based on trial design context.
    
    Required keys in design_inputs: 'condition', 'phase', 'endpoint', 'intervention_type'
    """
    results = []
    for entry in COMPARATOR_KNOWLEDGE_BASE:
        if all([
            entry["condition"] == design_inputs.get("condition"),
            entry["phase"] == design_inputs.get("phase"),
            entry["endpoint"] == design_inputs.get("endpoint"),
            entry["intervention_type"] == design_inputs.get("intervention_type")
        ]):
            results.append({
                "comparator": entry["comparator"],
                "type": entry["type"],
                "precedent_count": entry["precedent_count"],
                "notes": entry["notes"]
            })
    
    # Fallback if no exact match (add fuzzy logic later)
    if not results:
        results.append({
            "comparator": "Standard of care",
            "type": "Active Comparator",
            "precedent_count": 0,
            "notes": "No exact precedent found; defaulting to SOC"
        })
    return results

if __name__ == "__main__":
    example_input = {
        "condition": "NSCLC",
        "phase": "Phase 3",
        "endpoint": "Overall Survival",
        "intervention_type": "Targeted Therapy"
    }
    suggestions = suggest_comparators(example_input)
    for s in suggestions:
        print(f"Suggested Comparator: {s['comparator']} ({s['type']})\nNotes: {s['notes']}\n")
