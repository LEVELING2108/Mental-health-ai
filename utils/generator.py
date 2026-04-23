from transformers import pipeline

from core.logger import setup_logger

logger = setup_logger(__name__)

# Keyword-specific Knowledge Base for precise intervention
KEYWORD_GUIDANCE = {
    "exam": "Academic stress is very common. Remember to take 5-minute breaks every hour and stay hydrated.",
    "sleep": "Sleep hygiene is crucial. Try to avoid screens 30 minutes before bed and keep a consistent wake-up time.",
    "lonely": "Feeling lonely is a heavy burden. Reaching out to even one person, or joining a community group, can make a difference.",
    "work": "Workplace burnout is real. Ensure you are setting clear boundaries between your professional and personal life.",
    "hopeless": "When things feel hopeless, it's the 'depression voice' talking, not reality. Please reach out to a professional who can help you navigate this fog.",
    "anxiety": "When anxiety hits, try the 5-4-3-2-1 grounding technique: acknowledge 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.",
    "anxious": "When anxiety hits, try the 5-4-3-2-1 grounding technique: acknowledge 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.",
    "grief": "Grief isn't a linear process; it's okay to have 'waves' of sadness. Be gentle with yourself and allow the feelings to pass without judgment.",
    "loss": "Grief isn't a linear process; it's okay to have 'waves' of sadness. Be gentle with yourself and allow the feelings to pass without judgment.",
    "breakup": "Healing after a relationship takes time. Focus on 'self-fullness'—reconnecting with the hobbies and friends that make you who you are.",
    "relationship": "Relationships can be complex. Communication and setting healthy boundaries are the foundations of emotional safety.",
    "family": "Family dynamics can be one of our biggest stressors. Remember that you are only responsible for your own reactions, not theirs.",
    "social": "Social battery drainage is real. It's perfectly okay to decline invitations to protect your peace of mind.",
    "health": "Physical and mental health are deeply linked. Small movements, like a 10-minute walk, can sometimes shift your internal state.",
    "future": "If the future feels overwhelming, try to bring your focus back to the next 10 minutes. Small, present-moment steps are enough.",
    "worth": "Your value isn't tied to your productivity or others' opinions. You are inherently worthy of care and respect exactly as you are.",
    "trauma": "Healing from the past is a brave journey. If memories feel intrusive, remind yourself: 'I am safe now, and that was then.'",
    "motivation": "When motivation is low, 'action creates momentum.' Try doing just one tiny task for two minutes—often, that's enough to start the flow."
}

class ResponseGenerator:
    def __init__(self):
        logger.info("Initializing Generative LLM (google/flan-t5-base)...")
        try:
            # Using FLAN-T5-Base: Efficient, high-quality instruction follower (~900MB)
            self.generator = pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                device=-1 # CPU
            )
            logger.info("Generative LLM loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Generative LLM: {e}")
            self.generator = None

    def get_keyword_context(self, keywords):
        """Inject specific expert guidance if certain keywords are detected."""
        context_snippets = []
        for kw in keywords:
            if kw.lower() in KEYWORD_GUIDANCE:
                context_snippets.append(KEYWORD_GUIDANCE[kw.lower()])
        return " ".join(context_snippets)

    def generate(self, risk, emotion, user_text, keywords):
        if not self.generator:
            return "I am here to support you. Please consider speaking with a professional."

        # Build a sophisticated prompt for the LLM
        keyword_context = self.get_keyword_context(keywords)

        prompt = (
            f"Context: You are a highly empathetic mental health support assistant. "
            f"The user is feeling {emotion}. Their risk level is {risk}. "
            f"Specific guidance: {keyword_context} "
            f"User says: '{user_text}' "
            f"Task: Generate a short, deeply supportive, and empathetic response. "
            f"Do not give medical advice. Encourage self-care."
        )

        try:
            response = self.generator(
                prompt,
                max_length=120,
                do_sample=True,
                temperature=0.8,
                top_p=0.9
            )
            return response[0]['generated_text']
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I'm sorry, I'm having trouble finding the words right now, but I want you to know I'm listening and I care."

# Singleton instance
ai_generator = ResponseGenerator()
