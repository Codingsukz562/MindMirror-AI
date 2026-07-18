"""Habits API routes."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

from app.schemas import Habit as HabitSchema, HabitCreate
from app.schemas import Reflection as ReflectionSchema, ReflectionCreate
from app.schemas import CoachingPlanResponse
from app.services.storage import get_storage, InMemoryStorage
from app.services.ai_service import get_ai_service, AIService
from app.models import CoachingPlan
from app.utils.validators import sanitize_input, validate_reflection_content, validate_habit_id

router = APIRouter()


def get_storage_dep() -> InMemoryStorage:
    """Dependency for storage."""
    return get_storage()


def get_ai_service_dep() -> AIService:
    """Dependency for AI service."""
    return get_ai_service()


@router.get("/habits", response_model=List[HabitSchema])
async def list_habits(storage: InMemoryStorage = Depends(get_storage_dep)):
    """List all available habits."""
    habits = storage.get_all_habits()
    return habits


@router.get("/habits/{habit_id}", response_model=HabitSchema)
async def get_habit(
    habit_id: str,
    storage: InMemoryStorage = Depends(get_storage_dep)
):
    """Get a specific habit."""
    if not validate_habit_id(habit_id):
        raise HTTPException(status_code=400, detail="Invalid habit ID")
    
    habit = storage.get_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/habits/{habit_id}/reflections", response_model=List[ReflectionSchema])
async def list_reflections(
    habit_id: str,
    limit: int = 50,
    storage: InMemoryStorage = Depends(get_storage_dep)
):
    """List reflections for a habit."""
    if not validate_habit_id(habit_id):
        raise HTTPException(status_code=400, detail="Invalid habit ID")
    
    habit = storage.get_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Validate limit
    if limit < 1 or limit > 100:
        limit = 50
    
    reflections = storage.get_reflections(habit_id, limit=limit)
    return reflections


@router.post("/habits/{habit_id}/reflections", response_model=ReflectionSchema)
async def create_reflection(
    habit_id: str,
    reflection_data: ReflectionCreate,
    storage: InMemoryStorage = Depends(get_storage_dep),
    ai_service: AIService = Depends(get_ai_service_dep)
):
    """Submit a new reflection and trigger AI analysis."""
    if not validate_habit_id(habit_id):
        raise HTTPException(status_code=400, detail="Invalid habit ID")
    
    habit = storage.get_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Sanitize and validate content
    sanitized_content = sanitize_input(reflection_data.content)
    is_valid, error_message = validate_reflection_content(sanitized_content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Add reflection
    reflection = storage.add_reflection(habit_id, sanitized_content)
    if not reflection:
        raise HTTPException(status_code=500, detail="Failed to add reflection")
    
    # Get all reflections for AI analysis
    all_reflections = storage.get_reflections(habit_id)
    
    # Generate new coaching plan using AI
    coaching_plan = await ai_service.analyze_reflections(habit.name, all_reflections)
    
    if coaching_plan:
        # Convert Pydantic model to dict for storage
        plan_dict = coaching_plan.model_dump()
        coaching_plan_obj = CoachingPlan(
            habit_id=habit_id,
            trigger_analysis=plan_dict["trigger_analysis"],
            risk_prediction=plan_dict["risk_prediction"],
            daily_plan=plan_dict["daily_plan"],
            replacement_habits=plan_dict["replacement_habits"],
            behavior_graph=plan_dict["behavior_graph"],
            motivation_message=plan_dict["motivation_message"],
            next_actions=plan_dict["next_actions"],
            weekly_summary=plan_dict.get("weekly_summary")
        )
        storage.save_coaching_plan(habit_id, coaching_plan_obj)
    
    return reflection


@router.get("/habits/{habit_id}/coaching", response_model=CoachingPlanResponse)
async def get_coaching_plan(
    habit_id: str,
    storage: InMemoryStorage = Depends(get_storage_dep),
    ai_service: AIService = Depends(get_ai_service_dep)
):
    """Get current coaching plan for a habit."""
    if not validate_habit_id(habit_id):
        raise HTTPException(status_code=400, detail="Invalid habit ID")
    
    habit = storage.get_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Check if we have a cached coaching plan
    cached_plan = storage.get_coaching_plan(habit_id)
    
    # Get reflections
    reflections = storage.get_reflections(habit_id)
    
    # If no plan or very old, generate new one
    if not cached_plan:
        coaching_plan = await ai_service.analyze_reflections(habit.name, reflections)
        
        if coaching_plan:
            plan_dict = coaching_plan.model_dump()
            coaching_plan_obj = CoachingPlan(
                habit_id=habit_id,
                trigger_analysis=plan_dict["trigger_analysis"],
                risk_prediction=plan_dict["risk_prediction"],
                daily_plan=plan_dict["daily_plan"],
                replacement_habits=plan_dict["replacement_habits"],
                behavior_graph=plan_dict["behavior_graph"],
                motivation_message=plan_dict["motivation_message"],
                next_actions=plan_dict["next_actions"],
                weekly_summary=plan_dict.get("weekly_summary")
            )
            storage.save_coaching_plan(habit_id, coaching_plan_obj)
            return coaching_plan
    
    # Return cached plan converted to response schema
    if cached_plan:
        return CoachingPlanResponse(
            trigger_analysis=cached_plan.trigger_analysis,
            risk_prediction=cached_plan.risk_prediction,
            daily_plan=cached_plan.daily_plan,
            replacement_habits=cached_plan.replacement_habits,
            behavior_graph=cached_plan.behavior_graph,
            motivation_message=cached_plan.motivation_message,
            next_actions=cached_plan.next_actions,
            weekly_summary=cached_plan.weekly_summary
        )
    
    # Fallback: generate default plan
    coaching_plan = await ai_service.analyze_reflections(habit.name, [])
    return coaching_plan
