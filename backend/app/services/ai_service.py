"""AI Service for behavioral coaching."""

import json
import logging
from typing import Optional, List
from datetime import datetime

from app.services.nvidia_client import get_nvidia_client
from app.schemas import (
    CoachingPlanResponse,
    TriggerAnalysis,
    RiskPrediction,
    DailyPlan,
    ReplacementHabit,
    BehaviorGraph,
    BehaviorGraphNode,
    BehaviorGraphEdge,
    WeeklySummary,
)
from app.models import Reflection as ReflectionModel

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered behavioral coaching."""
    
    def __init__(self):
        self.client = get_nvidia_client()
    
    def _build_prompt(self, habit_name: str, reflections: List[ReflectionModel]) -> str:
        """Build prompt for AI analysis."""
        
        reflection_texts = "\n".join([
            f"- {r.content} (at {r.created_at.strftime('%Y-%m-%d %H:%M')})"
            for r in reflections[-10:]  # Last 10 reflections
        ])
        
        return f"""You are MindMirror AI, a compassionate behavioral coach specializing in habit change.

Your task is to analyze the user's reflections about their struggle with: {habit_name}

REFLECTIONS:
{reflection_texts}

IMPORTANT: You MUST respond with ONLY valid JSON. No markdown, no explanations, just JSON.

Respond with this exact JSON schema:
{{
  "trigger_analysis": {{
    "primary_triggers": ["trigger1", "trigger2"],
    "emotional_patterns": ["emotion1", "emotion2"],
    "environmental_factors": ["factor1", "factor2"]
  }},
  "risk_prediction": {{
    "high_risk_times": ["10:00 PM", "3:00 PM"],
    "risk_level": "low|medium|high",
    "confidence": 85
  }},
  "daily_plan": {{
    "mission": "Today's specific mission",
    "replacement_habit": "Specific replacement behavior",
    "success_criteria": "How to measure success today"
  }},
  "replacement_habits": [
    {{"name": "Habit 1", "description": "Description", "difficulty": "easy|medium|hard"}},
    {{"name": "Habit 2", "description": "Description", "difficulty": "easy|medium|hard"}}
  ],
  "behavior_graph": {{
    "nodes": [
      {{"id": "1", "label": "Stress", "type": "trigger"}},
      {{"id": "2", "label": "Scrolling", "type": "behavior"}},
      {{"id": "3", "label": "Sleep loss", "type": "outcome"}}
    ],
    "edges": [
      {{"from": "1", "to": "2", "label": "leads to"}},
      {{"from": "2", "to": "3", "label": "causes"}}
    ]
  }},
  "weekly_summary": {{
    "progress": "Summary of progress",
    "insights": ["Insight 1", "Insight 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
  }},
  "motivation_message": "A compassionate, encouraging message",
  "next_actions": ["Action 1", "Action 2", "Action 3"]
}}

Guidelines:
- Be compassionate and non-judgmental
- Focus on understanding WHY habits occur, not shame
- Provide actionable, specific advice
- Consider emotional and environmental triggers
- Suggest realistic replacement habits
- Base predictions on patterns in the reflections
- If insufficient data, make reasonable estimates based on common patterns for {habit_name}

JSON Response:"""

    async def analyze_reflections(
        self, 
        habit_name: str, 
        reflections: List[ReflectionModel]
    ) -> Optional[CoachingPlanResponse]:
        """Analyze reflections and generate coaching plan."""
        
        if not reflections:
            # Generate default plan for new users
            return self._generate_default_plan(habit_name)
        
        prompt = self._build_prompt(habit_name, reflections)
        
        messages = [
            {
                "role": "system",
                "content": "You are MindMirror AI, a compassionate behavioral coach. Always respond with valid JSON only."
            },
            {"role": "user", "content": prompt}
        ]
        
        response_text = await self.client.chat_completion(messages)
        
        if not response_text:
            logger.warning("AI returned no response, using default plan")
            return self._generate_default_plan(habit_name)
        
        # Parse JSON response
        try:
            # Clean up response - remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            data = json.loads(cleaned)
            
            # Validate and create response object
            coaching_plan = CoachingPlanResponse(**data)
            return coaching_plan
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI JSON response: {e}")
            logger.debug(f"Raw response: {response_text}")
            return self._generate_default_plan(habit_name)
        except Exception as e:
            logger.error(f"Error processing AI response: {e}")
            return self._generate_default_plan(habit_name)
    
    def _generate_default_plan(self, habit_name: str) -> CoachingPlanResponse:
        """Generate a default coaching plan when AI fails or no data."""
        
        habit_display = habit_name.replace("_", " ").title()
        
        return CoachingPlanResponse(
            trigger_analysis=TriggerAnalysis(
                primary_triggers=["Stress", "Boredom", "Fatigue"],
                emotional_patterns=["Anxiety", "Loneliness", "Overwhelm"],
                environmental_factors=["Late night", "Alone at home", "After work"]
            ),
            risk_prediction=RiskPrediction(
                high_risk_times=["10:00 PM", "3:00 PM", "Right after work"],
                risk_level="medium",
                confidence=70.0
            ),
            daily_plan=DailyPlan(
                mission=f"Awareness: Notice your urge to engage in {habit_display} without acting on it",
                replacement_habit="Take 3 deep breaths and drink a glass of water when urge hits",
                success_criteria="Successfully paused before acting on an urge at least once today"
            ),
            replacement_habits=[
                ReplacementHabit(
                    name="5-minute rule",
                    description="Wait 5 minutes before giving in to the urge",
                    difficulty="easy"
                ),
                ReplacementHabit(
                    name="Mindful breathing",
                    description="Practice 4-7-8 breathing technique",
                    difficulty="easy"
                ),
                ReplacementHabit(
                    name="Quick walk",
                    description="Take a 10-minute walk outside",
                    difficulty="medium"
                )
            ],
            behavior_graph=BehaviorGraph(
                nodes=[
                    BehaviorGraphNode(id="1", label="Stress/Boredom", type="trigger"),
                    BehaviorGraphNode(id="2", label=habit_display, type="behavior"),
                    BehaviorGraphNode(id="3", label="Guilt/Regret", type="outcome")
                ],
                edges=[
                    BehaviorGraphEdge(**{"from": "1", "to": "2", "label": "triggers"}),
                    BehaviorGraphEdge(**{"from": "2", "to": "3", "label": "leads to"})
                ]
            ),
            weekly_summary=WeeklySummary(
                progress="Starting your journey of self-discovery",
                insights=["Awareness is the first step to change", "Triggers are normal and manageable"],
                recommendations=["Reflect daily", "Celebrate small wins", "Be patient with yourself"]
            ),
            motivation_message="Every moment of awareness is a victory. You're building new neural pathways, and that takes time. Be kind to yourself.",
            next_actions=[
                "Complete today's reflection",
                "Try one replacement habit when urge hits",
                "Notice your triggers without judgment"
            ]
        )


# Singleton instance
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Get or create AI service singleton."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
