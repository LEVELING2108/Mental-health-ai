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
    ],
    "positive": [
        "That is wonderful to hear! Consider taking a moment to practice gratitude for this feeling.",
        "Why not share this positive energy with someone else today? A small kind gesture can go a long way.",
        "Remember to savor this moment—take a mental snapshot of what's going well right now."
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
        if not text:
            return ""
        text = re.sub(r'#.*?\n', '', text) # Remove headers
        text = text.replace('*', '').replace('\n', ' ').strip()
        return text[:300] # Limit length for prompt stability

    def get_tips(self, risk: str, emotion: str) -> str:
        """Dynamic tip selection."""
        # JOY/LOVE/SURPRISE are treated as positive regardless of small risk fluctuations
        if emotion.lower() in ["joy", "love", "surprise"]:
            return random.choice(SUGGESTIONS["positive"])

        category = "stress"
        if "anxious" in emotion or "fear" in emotion:
            category = "anxiety"
        elif "sad" in emotion or "depression" in risk:
            category = "depression"
        elif "sleep" in emotion:
            category = "sleep"

        tips = SUGGESTIONS.get(category, SUGGESTIONS["stress"])
        return random.choice(tips)

    def generate(self, risk: str, emotion: str, user_text: str, keywords: list[str]) -> str:
        if not self.model:
            return "I am here for you. Please consider reaching out to a professional for support."

        # 1. Determine Context Type (Force positive if emotion is Joy)
        is_positive = emotion.lower() in ["joy", "love", "surprise"]
        
        # 2. Prepare Grounded Context
        # Don't use RAG clinical guidance if the user is happy
        raw_context = rag_engine.query(user_text) if not is_positive else ""
        clean_context = self.clean_clinical_text(raw_context)
        action_tip = self.get_tips(risk, emotion)
        
        # 3. SELECT PERSONA & TONE
        if is_positive:
            persona = "supportive, enthusiastic life coach"
            instruction = f"Write a cheerful 2-sentence response celebrating that they feel {emotion}. Include this advice: {action_tip}"
        else:
            persona = "warm, professional mental health counselor"
            instruction = f"Write a deeply empathetic 3-sentence response validating their {emotion}. Include this clinical advice: {action_tip} {clean_context}"

        prompt = (
            f"Context: You are a {persona}.\n"
            f"User says: '{user_text}'\n"
            f"Instruction: {instruction} Do not repeat these instructions. Use a first-person perspective.\n\n"
            f"Response:"
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=256, 
                min_length=30 if is_positive else 60,
                do_sample=True, 
                temperature=0.8, 
                top_p=0.9,
                repetition_penalty=1.5
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.replace("Response:", "").strip()
            
            # 4. PREMIUM HYBRID FALLBACK (Guarantees Quality & Logic)
            if len(response) < 20 or user_text.lower() in response.lower() or "instruction" in response.lower():
                if is_positive:
                    return f"I'm so incredibly happy to hear that you're feeling {emotion.lower()} today! {action_tip} Keep shining and enjoying this wonderful energy!"
                else:
                    return (
                        f"I want you to know that I truly hear you. It's completely valid to feel {emotion.lower()} right now, "
                        f"and I'm sorry things are so heavy. I suggest you {action_tip.lower()} "
                        f"Please remember that you don't have to carry this all at once. I'm here with you."
                    )
                
            return response

        except Exception as e:
            logger.error(f"AI Error: {e}")
            return f"I'm so glad to hear you're feeling {emotion.lower()}! {action_tip}"

# Singleton instance
ai_generator = ResponseGenerator()
