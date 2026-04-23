def generate_safe_response(prediction_result):
    risk = prediction_result["risk"]

    responses = {
        "low": "It's good to hear that you're feeling well! Remember to keep practicing self-care and reach out if things change.",
        "medium": "It sounds like you're going through a bit of a stressful time. Taking some time for yourself or talking to a friend might help. If it persists, consider speaking with a professional.",
        "high": "It sounds like you're going through a very difficult time. Please know that you're not alone and there is support available. We strongly encourage you to reach out to a mental health professional or a crisis helpline immediately."
    }

    return responses.get(risk.lower(), "I'm here to listen and support you. How can I help today?")

# Adding some crisis resources for "high" risk
CRISIS_RESOURCES = """
- **National Suicide Prevention Lifeline:** 988
- **Crisis Text Line:** Text HOME to 741741
- **Emergency Services:** 911 (or your local emergency number)
"""

def get_resources(risk):
    if risk.lower() == "high":
        return CRISIS_RESOURCES
    return ""
