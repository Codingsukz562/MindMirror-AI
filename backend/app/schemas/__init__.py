"""Pydantic schemas for MindMirror AI."""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class HabitBase(BaseModel):
    """Base schema for habits."""
    name: str = Field(..., min_length=1, max_length=100)
    category: Literal[
        'social_media', 
        'screen_time', 
        'gaming', 
        'procrastination', 
        'junk_food', 
        'other'
    ]


class HabitCreate(HabitBase):
    """Schema for creating a habit."""
    pass


class Habit(HabitBase):
    """Schema for a habit with ID."""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReflectionBase(BaseModel):
    """Base schema for reflections."""
    content: str = Field(..., min_length=1, max_length=5000)


class ReflectionCreate(ReflectionBase):
    """Schema for creating a reflection."""
    pass


class Reflection(ReflectionBase):
    """Schema for a reflection with ID."""
    id: str
    habit_id: str
    emotion: Optional[str] = None
    trigger: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TriggerAnalysis(BaseModel):
    """Schema for trigger analysis."""
    primary_triggers: List[str]
    emotional_patterns: List[str]
    environmental_factors: List[str]


class RiskPrediction(BaseModel):
    """Schema for risk prediction."""
    high_risk_times: List[str]
    risk_level: Literal['low', 'medium', 'high']
    confidence: float = Field(..., ge=0, le=100)


class DailyPlan(BaseModel):
    """Schema for daily plan."""
    mission: str
    replacement_habit: str
    success_criteria: str


class ReplacementHabit(BaseModel):
    """Schema for replacement habit."""
    name: str
    description: str
    difficulty: Literal['easy', 'medium', 'hard']


class BehaviorGraphNode(BaseModel):
    """Schema for behavior graph node."""
    id: str
    label: str
    type: Literal['trigger', 'behavior', 'outcome']


class BehaviorGraphEdge(BaseModel):
    """Schema for behavior graph edge."""
    from_node: str = Field(..., alias='from')
    to: str
    label: str
    
    class Config:
        populate_by_name = True


class BehaviorGraph(BaseModel):
    """Schema for behavior graph."""
    nodes: List[BehaviorGraphNode]
    edges: List[BehaviorGraphEdge]


class WeeklySummary(BaseModel):
    """Schema for weekly summary."""
    progress: str
    insights: List[str]
    recommendations: List[str]


class CoachingPlanResponse(BaseModel):
    """Schema for coaching plan response from AI."""
    trigger_analysis: TriggerAnalysis
    risk_prediction: RiskPrediction
    daily_plan: DailyPlan
    replacement_habits: List[ReplacementHabit]
    behavior_graph: BehaviorGraph
    weekly_summary: Optional[WeeklySummary] = None
    motivation_message: str
    next_actions: List[str]


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    version: str
    timestamp: datetime
