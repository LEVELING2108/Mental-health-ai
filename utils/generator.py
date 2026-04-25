import random
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.logger import setup_logger
from utils.rag import rag_engine

logger = setup_logger(__name__)

# Advanced Suggestion Engine
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
        if not text:
            return ""
        text = re.sub(r'#.*?\n', '', text)
        text = text.replace('*', '').replace('\n', ' ').strip()
        return text[:200]

    def get_tips(self, risk: str, emotion: str) -> str:
        if emotion.lower() in ["joy", "love", "surprise"]:
            return random.choice(SUGGESTIONS["positive"])
        category = "stress"
        if "anxious" in emotion or "fear" in emotion:
            category = "anxiety"
        elif "sad" in emotion or "depression" in risk:
            category = "depression"
        elif "sleep" in emotion:
            category = "sleep"
        return random.choice(SUGGESTIONS.get(category, SUGGESTIONS["stress"]))

    def generate(self, risk: str, emotion: str, user_text: str, keywords: list[str]) -> str:
        if not self.model:
            return "I am here for you. Please consider reaching out to a professional for support."

        is_positive = emotion.lower() in ["joy", "love", "surprise"]
        raw_context = rag_engine.query(user_text) if not is_positive else ""
        clean_context = self.clean_clinical_text(raw_context)
        action_tip = self.get_tips(risk, emotion)
        
        # FEW-SHOT PROMPT: Shows the model exactly how to behave
        prompt = (
            "User: I am feeling so sad today.\n"
            "Assistant: I am so sorry you are feeling this way. It is completely valid to feel sad right now. I suggest you try a small task you enjoy, and remember there is hope.\n"
            "User: I am having a great day!\n"
            "Assistant: That is wonderful to hear! I am so happy you are feeling good. Remember to savor this positive energy today!\n"
            f"User: {user_text}\n"
            f"Assistant:"
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=100, # Shorter is better for this model
                do_sample=True, 
                temperature=0.7, 
                top_p=0.9,
                repetition_penalty=1.5
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # THE "IDIOT-PROOF" FILTER
            # If the model leaks ANY instruction words, we block it and use the high-quality template
            instruction_leak = any(word in response.lower() for word in [
                "sentence", "instruction", "positive response", "negative response", 
                "validate", "persona", "clinical", "user says"
            ])

            if instruction_leak or len(response) < 15 or user_text.lower() in response.lower():
                if is_positive:
                    return f"It is so wonderful that you're feeling {emotion.lower()} today! {action_tip} Keep up this great energy!"
                else:
                    return (
                        f"I want you to know that I truly hear you. It's completely valid to feel {emotion.lower()} right now. "
                        f"I suggest you {action_tip.lower()} Please take it one small breath at a time. I'm here with you."
                    )
                
            return response

        except Exception as e:
            logger.error(f"AI Error: {e}")
            return f"I hear you, and I want to support you. It's valid to feel {emotion}. Please try to {action_tip.lower()}"

# Singleton instance
ai_generator = ResponseGenerator()
