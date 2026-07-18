"""Models for MindMirror AI (in-memory storage)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class Habit:
    """Habit model."""
    name: str
    category: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Reflection:
    """Reflection model."""
    habit_id: str
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    emotion: Optional[str] = None
    trigger: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CoachingPlan:
    """Coaching plan model."""
    habit_id: str
    trigger_analysis: dict
    risk_prediction: dict
    daily_plan: dict
    replacement_habits: List[dict]
    behavior_graph: dict
    motivation_message: str
    next_actions: List[str]
    weekly_summary: Optional[dict] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
