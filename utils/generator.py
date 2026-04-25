import random
import re

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from core.logger import setup_logger
from utils.rag import rag_engine

logger = setup_logger(__name__)

# ELITE SUGGESTION ENGINE
CLINICAL_TIPS = {
    "anxiety": [
        "Try the '5-4-3-2-1' grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.",
        "Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s) to physically calm your nervous system.",
        "Consider a 10-minute 'Mindful Walk'—focus strictly on the sensation of your feet hitting the ground."
    ],
    "depression": [
        "Try 'Behavioral Activation': Choose one tiny task (like washing one dish) and do it now. Action often precedes motivation.",
        "Step outside for 5 minutes of sunlight. It helps regulate your circadian rhythm and mood.",
        "Write down three things you are grateful for, no matter how small they seem."
    ],
    "stress": [
        "Use the Eisenhower Matrix: Focus only on what is both 'Urgent' and 'Important'. Delegate or drop the rest.",
        "Set a 'Hard Stop' for your work today. Boundaries are essential for recovery.",
        "Try 'Progressive Muscle Relaxation': Tense and release each muscle group from your toes to your head."
    ],
    "sleep": [
        "The 10-3-2-1-0 Rule: No caffeine 10hrs before bed, no food 3hrs before, no work 2hrs before, no screens 1hr before.",
        "If you can't sleep after 20 minutes, get out of bed and do a dull task in dim light until you feel sleepy.",
        "Keep a 'Worry Journal' by your bed to dump thoughts so your brain can stop 'holding' them."
    ],
    "positive": [
        "This is a wonderful state to be in! Take a 'Mental Snapshot' of this moment to remember later.",
        "Share this energy—send a quick appreciation text to someone you care about.",
        "Reflect on what led to this good feeling. How can you create space for more moments like this?"
    ]
}

class ResponseGenerator:
    def __init__(self):
        logger.info("Initializing Elite AI Brain (google/flan-t5-large)...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
            logger.info("Elite AI Brain loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Elite AI: {e}")
            self.model = None

    @staticmethod
    def get_clinical_advice(risk: str, emotion: str) -> str:
        cat = "stress"
        emo = emotion.lower()
        if any(w in emo for w in ["joy", "love", "surprise"]):
            cat = "positive"
        elif any(w in emo for w in ["sad", "fear", "anger"]) or risk == "high":
            cat = "depression" if "sad" in emo else "anxiety"
        elif "sleep" in emo:
            cat = "sleep"
        return random.choice(CLINICAL_TIPS[cat])

    def generate(self, risk: str, emotion: str, user_text: str, history: list[dict] = None) -> str:
        if not self.model:
            return "I am here to support you. Please consider speaking with a professional."

        # 1. Fetch Context
        is_positive = emotion.lower() in ["joy", "love", "surprise"]
        raw_rag = rag_engine.query(user_text) if not is_positive else ""
        clean_rag = re.sub(r'#.*?\n', '', raw_rag).replace('*', '').strip()[:200]
        advice = self.get_clinical_advice(risk, emotion)

        # 2. Format History for Context
        history_str = ""
        if history:
            recent = history[-4:]
            history_str = "\n".join([f"{'User' if h['role'] == 'user' else 'Counselor'}: {h['content']}" for h in recent])

        # 3. ELITE MULTI-TURN PROMPT
        prompt = (
            f"Persona: You are a warm clinical counselor.\n"
            f"History:\n{history_str}\n"
            f"User: {user_text}\n"
            f"Context: Feeling {emotion}, Risk {risk}.\n"
            f"Instruction: Respond to the user in 2 kind sentences. Do not repeat their words. Continue the dialogue naturally.\n\n"
            f"Counselor:"
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_length=200,
                do_sample=True,
                temperature=0.75,
                repetition_penalty=2.5
            )
            ai_empathy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            ai_empathy = ai_empathy.replace("Counselor:", "").strip()

            # 4. Hybrid Constructor
            if is_positive:
                final_response = f"{ai_empathy} {advice}"
            else:
                final_response = f"{ai_empathy} Based on our conversation, I suggest you {advice.lower()} {'Also: ' + clean_rag if clean_rag else ''}"

            if len(ai_empathy) < 10 or "instruction" in final_response.lower():
                 return f"I truly hear you. It's completely valid to feel {emotion.lower()} right now. I suggest you {advice.lower()}"

            return final_response

        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"I am here for you. It's valid to feel {emotion.lower()}. I suggest you {advice.lower()}"

# Singleton instance
ai_generator = ResponseGenerator()
