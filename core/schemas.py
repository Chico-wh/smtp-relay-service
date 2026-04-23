from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailPayload(BaseModel):
    to: EmailStr
    subject: str
    html: str
    text: Optional[str] = None           # fallback plaintext (opcional)
    reply_to: Optional[EmailStr] = None  # reply-to customizado (opcional)


class EmailResponse(BaseModel):
    success: bool
    message: str