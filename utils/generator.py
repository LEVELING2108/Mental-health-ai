import random
import re

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from core.logger import setup_logger
from utils.rag import rag_engine

logger = setup_logger(__name__)

# ELITE SUGGESTION ENGINE (Local specialized knowledge)
CLINICAL_TIPS = {
    "anxiety": [
        "Try the '5-4-3-2-1' grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.",
        "Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s) to physically calm your nervous system.",
        "Maybe it's time for a 'Caffeine Vacation'—try switching to herbal tea for the next 24 hours.",
        "When anxiety hits, try 'The Worry Window': Set aside exactly 15 minutes at 4 PM to worry, and postpone any anxious thoughts until then.",
        "Try the 'Ice Water Reset'—splashing very cold water on your face can instantly lower your heart rate and ground you."
    ],
    "depression": [
        "Try 'Behavioral Activation': Choose one tiny task, like washing one single dish. Action often precedes motivation!",
        "Step outside for 5 minutes of sunlight. It's like a free battery recharge for your mood.",
        "Write down one thing you're proud of today. Even if it's just 'I made it through the morning'.",
        "Try the 'Opposite Action' skill: If you feel like isolating, call one person. If you feel like staying in bed, sit in a different chair for 5 minutes.",
        "Connect with a 'Sensory Anchor'—touch something soft, or smell a scent you love, to bring yourself back to the present."
    ],
    "stress": [
        "Use the Eisenhower Matrix: Focus only on what is 'Urgent' and 'Important'. The rest can wait (really).",
        "Set a 'Hard Stop' for your responsibilities today. You aren't a machine, even machines need to cool down.",
        "Try 'Progressive Muscle Relaxation': Tense and release each muscle group—start from your toes!",
        "Try 'The 10-10-10 Rule': Ask yourself, will this matter in 10 minutes? 10 months? 10 years? This usually puts stress in perspective.",
        "Identify your 'One Big Thing' for today and ignore everything else until that is done."
    ],
    "sleep": [
        "The 10-3-2-1-0 Rule: No caffeine 10hrs before, no food 3hrs, no work 2hrs, no screens 1hr before bed.",
        "If you can't sleep after 20 minutes, get out of bed. Your bed is for sleep, not for 'worry-olympics'.",
        "Keep a 'Brain Dump' notebook by your bed. Write the worries down so your brain can let go.",
        "Try 'Cognitive Shuffling': Think of a random word (like 'BED'), then visualize items starting with B, then E, then D until you fall asleep.",
        "Ensure your room is cool and your feet are warm; this temperature drop triggers your body's sleep mode."
    ],
    "positive": [
        "This is a wonderful space! Take a 'Mental Snapshot' of this feeling to look back on later.",
        "Share the wealth—send a quick 'thinking of you' text to a friend.",
        "Savor this. You've worked hard to feel this good, so enjoy every bit of it!",
        "Write down what specifically triggered this good feeling. Is it something you can intentionally repeat next week?",
        "Celebrate this win! Treat yourself to something small that makes you smile—you deserve it."
    ]
}

class ResponseGenerator:
    def __init__(self):
        logger.info("Initializing Counselor AI (google/flan-t5-large)...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
            logger.info("Counselor AI Brain loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load AI: {e}")
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
            return "I'm right here with you. Please consider reaching out to a professional for support."

        # 1. Fetch Context
        is_positive = emotion.lower() in ["joy", "love", "surprise"]
        raw_rag = rag_engine.query(user_text) if not is_positive else ""
        clean_rag = re.sub(r'#.*?\n', '', raw_rag).replace('*', '').strip()[:200]
        advice = self.get_clinical_advice(risk, emotion)

        # 2. Format History
        history_str = ""
        if history:
            recent = history[-3:]
            history_str = "\n".join([f"{'User' if h['role'] == 'user' else 'Counselor'}: {h['content']}" for h in recent])

        # 3. ELITE COUNSELOR PROMPT (Infused with Humour & Consolation)
        prompt = (
            f"Role: You are a warm, wise, and slightly witty clinical counselor.\n"
            f"Goal: Console the user and offer a gentle perspective.\n"
            f"History:\n{history_str}\n"
            f"User: {user_text}\n"
            f"Emotion: {emotion}, Risk: {risk}.\n\n"
            f"Task: Respond in 2-3 kind sentences. Validate them first. "
            f"If appropriate, use a tiny bit of gentle, self-deprecating humour or a relatable metaphor. "
            f"Always end with a consoling thought. Do not be robotic.\n\n"
            f"Counselor:"
        )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs, 
                max_length=200, 
                do_sample=True, 
                temperature=0.85, # Higher temp for more "human" flair
                repetition_penalty=2.5
            )
            ai_empathy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            ai_empathy = ai_empathy.replace("Counselor:", "").strip()
            
            # 4. Premium Hybrid Construction
            if is_positive:
                final_response = f"{ai_empathy} It's a breath of fresh air to see you feeling this way! {advice}"
            else:
                final_response = (
                    f"{ai_empathy} Remember, we're navigating this together. "
                    f"A small step for today: {advice.lower()} "
                    f"{'Plus, a little wisdom from the books: ' + clean_rag if clean_rag else ''} "
                    f"You're doing better than you think."
                )

            # Reliability Safety
            if len(ai_empathy) < 15 or "instruction" in final_response.lower():
                 return (
                     f"I truly hear you, and it's valid to feel {emotion.lower()} right now. "
                     f"Life can be a bit of a chaotic puzzle sometimes, can't it? "
                     f"Let's try one small thing: {advice.lower()} I'm here with you."
                 )

            return final_response

        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"I hear you, and I'm here to support you. It's valid to feel {emotion.lower()}. Let's try to {advice.lower()}"

# Singleton instance
ai_generator = ResponseGenerator()
