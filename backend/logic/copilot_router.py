# backend/ai/router.py

from ai.tasks.endpoint_suggester import suggest_endpoints
from ai.engine import chat
from logic.endpoint_suggester import suggest_endpoints
from logic.comparator_explorer import suggest_comparators
from logic.5ws_initializer import generate_5ws_structure 

# You could later expand this with phase-based or condition-based logic

def copilot_router(session_data):
    phase = session_data.get("phase")
    endpoint = session_data.get("endpoint")
    comparator = session_data.get("comparator")
    raw_prompt = session_data.get("raw_prompt")

    # Step 1: Phase but no endpoint → suggest endpoints
    if phase and not endpoint:
        return suggest_endpoints(session_data)

    # Step 2: Endpoint but no comparator → suggest comparator
    if endpoint and not comparator:
        return suggest_comparators(session_data)

    # Step 3: Fallback to GPT-driven chat or summarization
    return chat(prompt=raw_prompt or "Summarize this trial context.")

# backend/ai/tasks/endpoint_suggester.py

from ai.engine import chat

PROMPT = """
You are a clinical trial design assistant.
Given the following trial context, suggest 2–3 appropriate **primary endpoints**.
Be sure to consider the trial phase, therapeutic area, and patient population.
Only respond with endpoint names and a short reason for each.
"""

def suggest_endpoints(session_data):
    """
    Suggests endpoints based on session data using a template prompt.
    """
    return chat(
        prompt=PROMPT,
        context=session_data
    )
