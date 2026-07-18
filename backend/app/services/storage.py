"""In-memory storage for MindMirror AI."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import threading

from app.models import Habit, Reflection, CoachingPlan


class InMemoryStorage:
    """Thread-safe in-memory storage for development/demo."""
    
    def __init__(self):
        self._habits: Dict[str, Habit] = {}
        self._reflections: Dict[str, List[Reflection]] = {}
        self._coaching_plans: Dict[str, CoachingPlan] = {}
        self._lock = threading.Lock()
        
        # Initialize default habits
        self._init_default_habits()
    
    def _init_default_habits(self) -> None:
        """Initialize default habit categories."""
        default_habits = [
            ("social_media", "Social Media"),
            ("screen_time", "Screen Time"),
            ("gaming", "Gaming"),
            ("procrastination", "Procrastination"),
            ("junk_food", "Junk Food"),
        ]
        
        for category, name in default_habits:
            if category not in self._habits:
                self._habits[category] = Habit(name=name, category=category)
                self._reflections[category] = []
    
    def get_habit(self, habit_id: str) -> Optional[Habit]:
        """Get habit by ID."""
        with self._lock:
            return self._habits.get(habit_id)
    
    def get_all_habits(self) -> List[Habit]:
        """Get all habits."""
        with self._lock:
            return list(self._habits.values())
    
    def add_reflection(self, habit_id: str, content: str) -> Optional[Reflection]:
        """Add a reflection to a habit."""
        with self._lock:
            if habit_id not in self._habits:
                return None
            
            reflection = Reflection(habit_id=habit_id, content=content)
            
            if habit_id not in self._reflections:
                self._reflections[habit_id] = []
            
            self._reflections[habit_id].append(reflection)
            return reflection
    
    def get_reflections(self, habit_id: str, limit: int = 50) -> List[Reflection]:
        """Get reflections for a habit."""
        with self._lock:
            reflections = self._reflections.get(habit_id, [])
            # Sort by created_at descending and limit
            sorted_reflections = sorted(
                reflections, 
                key=lambda r: r.created_at, 
                reverse=True
            )
            return sorted_reflections[:limit]
    
    def save_coaching_plan(self, habit_id: str, plan: CoachingPlan) -> None:
        """Save coaching plan for a habit."""
        with self._lock:
            self._coaching_plans[habit_id] = plan
    
    def get_coaching_plan(self, habit_id: str) -> Optional[CoachingPlan]:
        """Get coaching plan for a habit."""
        with self._lock:
            return self._coaching_plans.get(habit_id)
    
    def get_weekly_reflections(self, habit_id: str) -> List[Reflection]:
        """Get reflections from the last 7 days."""
        with self._lock:
            reflections = self._reflections.get(habit_id, [])
            week_ago = datetime.utcnow() - timedelta(days=7)
            return [r for r in reflections if r.created_at >= week_ago]


# Singleton instance
_storage: Optional[InMemoryStorage] = None


def get_storage() -> InMemoryStorage:
    """Get or create storage singleton."""
    global _storage
    if _storage is None:
        _storage = InMemoryStorage()
    return _storage
