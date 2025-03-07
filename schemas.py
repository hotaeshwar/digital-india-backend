from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class ContactSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=1)  # Name must be at least 1 character long
    phone: str = Field(..., min_length=10, max_length=10)  # Phone must be exactly 10 digits
    email: EmailStr  # Email must be a valid email address
    message: str = Field(..., min_length=1)  # Message must be at least 1 character long

def contact_submission_serializer(submission) -> dict:
    """
    Serialize MongoDB document to dictionary
    Converts ObjectId to string and handles datetime
    """
    return {
        "id": str(submission["_id"]),
        "name": submission.get("name", ""),
        "phone": submission.get("phone", ""),
        "email": submission.get("email", ""),
        "message": submission.get("message", ""),
        "submitted_at": submission.get("submitted_at", datetime.utcnow())
    }