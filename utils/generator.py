from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.logger import setup_logger
from utils.rag import rag_engine  # New: RAG Engine

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

# Advanced Suggestion Engine for actionable advice
SUGGESTIONS = {
    "anxiety": [
        "Try the '5-4-3-2-1' grounding technique.",
        "Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s).",
        "Consider reducing caffeine intake for the next 24 hours."
    ],
    "depression": [
        "Try the 'Behavioral Activation' method: do one small task you used to enjoy, even if you don't feel like it.",
        "Step outside for 10 minutes of natural sunlight.",
        "Reach out to one trusted friend just to say 'hello'."
    ],
    "stress": [
        "Use the 'Eisenhower Matrix' to prioritize your tasks and delegate what isn't urgent.",
        "Try a 5-minute progressive muscle relaxation (tense and release each muscle group).",
        "Set a 'hard stop' time for work today to protect your evening."
    ],
    "sleep": [
        "Avoid blue light (phones/screens) at least 60 minutes before bed.",
        "Try a 'Brain Dump': write down everything worrying you on paper to clear your mind.",
        "Keep your bedroom temperature slightly cool (around 18°C/65°F)."
    ]
}

class ResponseGenerator:
    def __init__(self):
        logger.info("Initializing Generative LLM (google/flan-t5-base) manually...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
            logger.info("Generative LLM loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Generative LLM: {e}")
            self.model = None

    def get_actionable_suggestions(self, risk: str, keywords: list[str]) -> str:
        """Fetch concrete suggestions based on detected risk and keywords."""
        relevant_tips = []
        for kw in keywords:
            if kw.lower() in SUGGESTIONS:
                relevant_tips.extend(SUGGESTIONS[kw.lower()])

        if not relevant_tips:
            if risk == "high":
                relevant_tips = SUGGESTIONS["depression"]
            else:
                relevant_tips = SUGGESTIONS["stress"]

        import random
        return " ".join(random.sample(list(set(relevant_tips)), min(2, len(relevant_tips))))

    def generate(self, risk: str, emotion: str, user_text: str, keywords: list[str]) -> str:
        if not self.model:
            return "I am here to support you. Please consider speaking with a professional."

        # 1. RAG: Search the Vector DB for clinically verified guidance
        logger.info(f"Querying Vector DB for: {user_text}")
        clinical_context = rag_engine.query(user_text)

        # 2. Expert fallback guidance (from our existing dictionary)
        keyword_context = ""
        for kw in keywords:
            if kw.lower() in KEYWORD_GUIDANCE:
                keyword_context += KEYWORD_GUIDANCE[kw.lower()] + " "

        action_tips = self.get_actionable_suggestions(risk, keywords)

        # 3. ULTIMATE PROMPT (Tier 0.1%): Combines Search + Classifier + Emotion + LLM
        prompt = (
            f"As an elite mental health assistant, respond to: '{user_text}'.\n\n"
            f"User Profile: Emotion: {emotion}, Risk: {risk}.\n"
            f"Verified Clinical Knowledge (use this for your advice): {clinical_context}\n"
            f"Additional Expert Context: {keyword_context}\n"
            f"Specific Tips to include: {action_tips}\n\n"
            f"Instruction: Generate a deeply kind and empathetic response. "
            f"Start by validating their experience. Then, provide the specific advice from the 'Clinical Knowledge' and 'Tips' sections above. "
            f"Ensure the tone is warm and non-judgmental. Do not mention that you are an AI or searching a database."
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=300, 
                do_sample=True, 
                temperature=0.75,
                top_p=0.9,
                repetition_penalty=1.2
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Refinement cleanup
            response = response.replace("Response:", "").replace("Assistant:", "").strip()
            return response
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I'm sorry, I'm having trouble finding the words right now, but I want you to know I'm listening and I care."

# Singleton instance
ai_generator = ResponseGenerator()
