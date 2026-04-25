import random
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.logger import setup_logger
from utils.rag import rag_engine

logger = setup_logger(__name__)

# Advanced Suggestion Engine for actionable advice
SUGGESTIONS = {
    "anxiety": [
        "Try the '5-4-3-2-1' grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.",
        "Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s) to calm your nervous system.",
        "Consider reducing caffeine and focusing on your immediate surroundings."
    ],
    "depression": [
        "Try a small 'Behavioral Activation' task: do one tiny thing you used to enjoy, like making a cup of tea or listening to a favorite song.",
        "Step outside for just 5 minutes of fresh air and natural light.",
        "Be gentle with yourself; your value isn't tied to your productivity today."
    ],
    "stress": [
        "Try the Eisenhower Matrix: focus only on what is both urgent and important right now.",
        "Do a 5-minute 'Brain Dump'—write everything down on paper to get it out of your head.",
        "Set a 'hard stop' time for your responsibilities today to protect your rest."
    ],
    "sleep": [
        "Put away all screens 60 minutes before bed to allow your mind to settle.",
        "Keep your room cool and dark to signal to your body that it's time for rest.",
        "If thoughts are racing, write them down on a 'worry list' to handle tomorrow."
    ]
}

class ResponseGenerator:
    def __init__(self):
        logger.info("Initializing Elite Generative AI (FLAN-T5-Base)...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
            logger.info("Generative AI loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load AI: {e}")
            self.model = None

    def clean_clinical_text(self, text: str) -> str:
        """Removes Markdown headers and clean up RAG results for the LLM."""
        if not text: return ""
        text = re.sub(r'#.*?\n', '', text) # Remove headers
        text = text.replace('*', '').replace('\n', ' ').strip()
        return text[:300] # Limit length for prompt stability

    def get_tips(self, risk: str, emotion: str) -> str:
        """Dynamic tip selection."""
        category = "stress"
        if "anxious" in emotion or "fear" in emotion: category = "anxiety"
        elif "sad" in emotion or "depression" in risk: category = "depression"
        elif "sleep" in emotion: category = "sleep"
        
        tips = SUGGESTIONS.get(category, SUGGESTIONS["stress"])
        return random.choice(tips)

    def generate(self, risk: str, emotion: str, user_text: str, keywords: list[str]) -> str:
        if not self.model:
            return "I am here for you. Please consider reaching out to a professional for support."

        # 1. Prepare Grounded Context
        raw_context = rag_engine.query(user_text)
        clean_context = self.clean_clinical_text(raw_context)
        action_tip = self.get_tips(risk, emotion)
        
        # 2. SIMPLIFIED ELITE PROMPT (Optimized for FLAN-T5)
        # Few-Shot structure helps smaller models understand the 'Warmth' requirement
        prompt = (
            f"Context: You are a warm, kind, and professional mental health counselor.\n"
            f"User says: '{user_text}'\n"
            f"Advice to include: {action_tip} {clean_context}\n\n"
            f"Instruction: Write a deeply empathetic 3-sentence reply to the user. "
            f"Use a warm tone. Validate their feelings of {emotion}. Tell them there is hope.\n\n"
            f"Counselor Response:"
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=256, 
                min_length=60,
                do_sample=True, 
                temperature=0.8, 
                top_p=0.9,
                repetition_penalty=1.5
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 3. PREMIUM HYBRID FALLBACK (Guarantees Quality)
            response = response.replace("Counselor Response:", "").strip()
            
            # If model echoes or fails to be empathetic, use our Elite Template
            if len(response) < 50 or user_text.lower() in response.lower():
                return (
                    f"I want you to know that I truly hear you. It's completely valid to feel {emotion} right now, "
                    f"and I'm sorry things are so heavy. For a bit of relief, I suggest you {action_tip.lower()} "
                    f"Please remember that you don't have to carry this all at once—take it one small breath at a time. I'm here with you."
                )
                
            return response

        except Exception as e:
            logger.error(f"AI Error: {e}")
            return f"I hear you, and I want to support you. It's valid to feel {emotion}. Please try to {action_tip.lower()}"

# Singleton instance
ai_generator = ResponseGenerator()
