from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List
import logging

# Absolute imports
from database import contact_collection  # Direct collection import
from schemas import ContactSubmissionCreate, contact_submission_serializer
from models import ContactSubmission
from utils import EmailService  # Base model without DB fields

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/submit-contact", response_model=dict, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(submission: ContactSubmission):
    """Handle contact form submissions with validation and storage"""
    try:
        # Create document with timestamp
        submission_data = submission.dict()
        submission_data["submitted_at"] = datetime.utcnow()

        # Insert into MongoDB (add await)
        result = await contact_collection.insert_one(submission_data)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save submission"
            )
        
        # Send notification email to the submitter
        email_service = EmailService()
        email_sent = email_service.send_contact_confirmation(
            recipient_email=submission.email, 
            submission_data=submission_data
        )

        if not email_sent:
            logger.warning(f"Failed to send confirmation email to {submission.email}")

        return {"message": "Contact form submitted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
@router.get("/submissions", response_model=dict)
async def get_contact_submissions(limit: int = 10, skip: int = 0):
    """Retrieve paginated contact form submissions"""
    try:
        # Get total count for pagination metadata
        total = contact_collection.count_documents({})

        # Get paginated results
        cursor = contact_collection.find().skip(skip).limit(limit)
        submissions = await cursor.to_list(length=limit)

        # Serialize and return with pagination info
        return {
            "data": [contact_submission_serializer(sub) for sub in submissions],
            "pagination": {
                "total": total,
                "limit": limit,
                "skip": skip
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve submissions: {str(e)}"
        )