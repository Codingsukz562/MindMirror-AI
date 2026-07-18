"""AI Chat API routes for real-time coaching conversations."""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from typing import Optional
import json
import logging

from app.schemas import ReflectionCreate
from app.services.storage import get_storage, InMemoryStorage
from app.services.ai_service import get_ai_service, AIService
from app.utils.validators import (
    sanitize_input,
    validate_reflection_content,
    validate_habit_id
)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_storage_dep() -> InMemoryStorage:
    """Dependency for storage."""
    return get_storage()


def get_ai_service_dep() -> AIService:
    """Dependency for AI service."""
    return get_ai_service()


@router.post("/habits/{habit_id}/chat")
async def chat_with_coach(
    habit_id: str,
    request: Request,
    message: dict,
    storage: InMemoryStorage = Depends(get_storage_dep),
    ai_service: AIService = Depends(get_ai_service_dep)
):
    """
    Chat with AI behavioral coach.

    Supports:

    Format 1:
    {
        "message": "hello",
        "context": {}
    }


    Format 2:
    {
        "message": {
            "message": "hello",
            "context": {}
        }
    }
    """

    if not validate_habit_id(habit_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid habit ID"
        )

    habit = storage.get_habit(habit_id)

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )


    # ==============================
    # FIX: Handle frontend payload
    # ==============================

    raw_message = message.get("message", "")

    if isinstance(raw_message, dict):

        user_message = raw_message.get(
            "message",
            ""
        ).strip()

        context = raw_message.get(
            "context",
            {}
        )

    else:

        user_message = raw_message.strip()

        context = message.get(
            "context",
            {}
        )


    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )


    # Sanitize input

    sanitized_message = sanitize_input(
        user_message
    )


    is_valid, error_msg = validate_reflection_content(
        sanitized_message
    )


    if not is_valid:

        if len(sanitized_message) < 3:
            raise HTTPException(
                status_code=400,
                detail="Message too short"
            )


    # Retrieve context

    reflections = storage.get_reflections(
        habit_id,
        limit=5
    )

    coaching_plan = storage.get_coaching_plan(
        habit_id
    )


    system_prompt = f"""
You are MindMirror AI, a compassionate behavioral coach.

Help the user overcome:

{habit.name.replace("_", " ")}

Your responsibilities:

- Listen empathetically
- Understand emotional triggers
- Identify patterns
- Suggest practical solutions
- Never shame the user
- Encourage positive behavioral change


Current Context:

Habit:
{habit.name}

Number of reflections:
{len(reflections)}

Recent reflections:

{
', '.join(
    [
        r.content[:50]
        for r in reflections[-3:]
    ]
)
if reflections
else
"None"
}


Respond naturally.

Keep responses concise.

Always end with encouragement.
"""


    if coaching_plan:

        system_prompt += f"""

Existing Coaching Plan:

Mission:
{coaching_plan.daily_plan.get(
    "mission",
    "N/A"
)}

Risk Level:
{coaching_plan.risk_prediction.get(
    "risk_level",
    "unknown"
)}

High Risk Times:
{
', '.join(
    coaching_plan.risk_prediction.get(
        "high_risk_times",
        []
    )
)
}

"""


    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": sanitized_message
        }
    ]


    async def generate_response():

        try:

            response_text = await ai_service.client.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )


            if response_text:

                cleaned = response_text.strip()


                if cleaned.startswith("```"):

                    cleaned = "\n".join(
                        cleaned.split("\n")[1:-1]
                    )


                yield (
                    "data: "
                    +
                    json.dumps(
                        {
                            "type": "message",
                            "content": cleaned
                        }
                    )
                    +
                    "\n\n"
                )


            else:

                yield (
                    "data: "
                    +
                    json.dumps(
                        {
                            "type": "message",
                            "content":
                            "I'm here with you. Tell me more about what you are experiencing."
                        }
                    )
                    +
                    "\n\n"
                )


            yield (
                "data: "
                +
                json.dumps(
                    {
                        "type": "done"
                    }
                )
                +
                "\n\n"
            )


        except Exception as e:

            logger.error(
                f"Error generating AI response: {e}"
            )


            yield (
                "data: "
                +
                json.dumps(
                    {
                        "type": "error",
                        "content":
                        "I am having trouble connecting right now. Please try again."
                    }
                )
                +
                "\n\n"
            )


    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )



@router.post("/habits/{habit_id}/quick-reflection")
async def quick_reflection(
    habit_id: str,
    reflection_data: ReflectionCreate,
    storage: InMemoryStorage = Depends(get_storage_dep),
    ai_service: AIService = Depends(get_ai_service_dep)
):

    if not validate_habit_id(habit_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid habit ID"
        )


    habit = storage.get_habit(
        habit_id
    )

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )


    content = sanitize_input(
        reflection_data.content
    )


    valid, error = validate_reflection_content(
        content
    )

    if not valid:
        raise HTTPException(
            status_code=400,
            detail=error
        )


    reflection = storage.add_reflection(
        habit_id,
        content
    )


    if not reflection:
        raise HTTPException(
            status_code=500,
            detail="Failed to add reflection"
        )


    reflections = storage.get_reflections(
        habit_id
    )


    coaching_plan = await ai_service.analyze_reflections(
        habit.name,
        reflections
    )


    return {
        "reflection": {
            "id": reflection.id,
            "content": reflection.content,
            "created_at": reflection.created_at.isoformat()
        },
        "coaching_plan": coaching_plan,
        "message":
        "Reflection recorded successfully"
    }



@router.get("/habits/{habit_id}/chat/suggestions")
async def get_chat_suggestions(
    habit_id: str,
    storage: InMemoryStorage = Depends(get_storage_dep)
):

    if not validate_habit_id(habit_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid habit ID"
        )


    habit = storage.get_habit(
        habit_id
    )

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )


    suggestions = [

        "I'm feeling an urge right now",

        "What should I do when I feel stressed?",

        "Help me understand my triggers",

        "Suggest a replacement habit",

    ]


    return {
        "suggestions": suggestions
    }