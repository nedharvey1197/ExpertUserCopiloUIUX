# backend/ai/router.py

from ai.tasks.endpoint_suggester import suggest_endpoints
from ai.engine import chat

# You could later expand this with phase-based or condition-based logic

def copilot_router(session_data):
    """
    Main logic router for Copilot tasks.
    Determines what Copilot should do based on current session state.
    """
    phase = session_data.get("phase")
    endpoint = session_data.get("endpoint")
    why = session_data.get("why")

    # Example logic: suggest endpoints if phase exists but endpoint does not
    if phase and not endpoint:
        return suggest_endpoints(session_data)

    # Otherwise, fallback to default Copilot chat mode
    return chat(
        prompt=session_data.get("raw_prompt", "Summarize this trial context."),
        context=session_data
    )


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
