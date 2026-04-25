import random
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.logger import setup_logger
from utils.rag import rag_engine

logger = setup_logger(__name__)

# ELITE SUGGESTION ENGINE (Decoupled for guaranteed quality)
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
        # TIER 1 UPGRADE: Using the LARGE model for significantly better reasoning
        logger.info("Initializing Elite AI Brain (google/flan-t5-large)...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
            logger.info("Elite AI Brain loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Elite AI: {e}")
            self.model = None

    def get_clinical_advice(self, risk: str, emotion: str) -> str:
        """Guaranteed high-quality clinical advice."""
        cat = "stress"
        emo = emotion.lower()
        if any(w in emo for w in ["joy", "love", "surprise"]): cat = "positive"
        elif any(w in emo for w in ["sad", "fear", "anger"]) or risk == "high": cat = "depression" if "sad" in emo else "anxiety"
        elif "sleep" in emo: cat = "sleep"
        
        return random.choice(CLINICAL_TIPS[cat])

    def generate(self, risk: str, emotion: str, user_text: str, keywords: list[str]) -> str:
        if not self.model:
            return "I am here to support you. Please consider speaking with a professional."

        # 1. Fetch data
        is_positive = emotion.lower() in ["joy", "love", "surprise"]
        raw_rag = rag_engine.query(user_text) if not is_positive else ""
        # Clean RAG data (remove markdown)
        clean_rag = re.sub(r'#.*?\n', '', raw_rag).replace('*', '').strip()[:200]
        
        advice = self.get_clinical_advice(risk, emotion)

        # 2. THE CONSTRAINED PROMPT (Prevents instruction leaking)
        prompt = (
            f"Provide a warm, 2-sentence empathetic response to a person who says: '{user_text}'. "
            f"The person is feeling {emotion}. Be supportive and kind."
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=150, 
                do_sample=True, 
                temperature=0.7, 
                repetition_penalty=2.0
            )
            ai_empathy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 3. THE HYBRID CONSTRUCTOR (Guarantees Tier 1 Quality)
            # We combine the AI's natural empathy with our guaranteed clinical advice
            if is_positive:
                final_response = f"{ai_empathy} It's so good to see you in this space. {advice}"
            else:
                final_response = (
                    f"{ai_empathy} I hear how much you are carrying. "
                    f"Based on what you've shared, I suggest you {advice.lower()} "
                    f"{'Also, remember: ' + clean_rag if clean_rag else ''} "
                    f"Please be gentle with yourself today."
                )

            # Final safety check against robotic output
            if "instruction" in final_response.lower() or len(ai_empathy) < 10:
                 return f"I truly hear you, and it's valid to feel {emotion.lower()} right now. I suggest you {advice.lower()} You don't have to face this alone."

            return final_response

        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"I am here for you. It's completely valid to feel {emotion.lower()}. I suggest you {advice.lower()}"

# Singleton instance
ai_generator = ResponseGenerator()
