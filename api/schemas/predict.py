from pydantic import BaseModel, Field


class SupportRequest(BaseModel):
    text: str = Field(..., description="User input text expressing their feelings.", min_length=1)
    history: list[dict] | None = Field(None, description="Previous messages in the session for context.")

class SupportResponse(BaseModel):
    risk: str = Field(..., description="Calculated risk level (low, medium, high).")
    score: float = Field(..., description="Confidence score of the prediction (blended).")
    emotion: str = Field(..., description="Detected primary emotion from Advanced AI.")
    keywords: list[str] = Field(..., description="Top keywords detected in the text.")
    response: str = Field(..., description="Safety-checked rule-based response.")
    ai_generated_response: str = Field(..., description="LLM-generated empathetic response.")
    resources: str = Field("", description="Crisis resources if applicable.")
