import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { API_BASE_URL } from '@/services/api'

export interface Habit {
  id: string
  name: string
  category: 'social_media' | 'screen_time' | 'gaming' | 'procrastination' | 'junk_food' | 'other'
  created_at: string
}

export interface Reflection {
  id: string
  habit_id: string
  content: string
  emotion?: string
  trigger?: string
  created_at: string
}

export interface CoachingPlan {
  trigger_analysis: {
    primary_triggers: string[]
    emotional_patterns: string[]
    environmental_factors: string[]
  }
  risk_prediction: {
    high_risk_times: string[]
    risk_level: 'low' | 'medium' | 'high'
    confidence: number
  }
  daily_plan: {
    mission: string
    replacement_habit: string
    success_criteria: string
  }
  replacement_habits: Array<{
    name: string
    description: string
    difficulty: 'easy' | 'medium' | 'hard'
  }>
  behavior_graph: {
    nodes: Array<{ id: string; label: string; type: 'trigger' | 'behavior' | 'outcome' }>
    edges: Array<{ from: string; to: string; label: string }>
  }
  weekly_summary?: {
    progress: string
    insights: string[]
    recommendations: string[]
  }
  motivation_message: string
  next_actions: string[]
}

export function useHabits() {
  return useQuery({
    queryKey: ['habits'],
    queryFn: async () => {
      const response = await fetch(`${API_BASE_URL}/api/habits`)
      if (!response.ok) throw new Error('Failed to fetch habits')
      return response.json() as Promise<Habit[]>
    },
  })
}

export function useReflections(habitId: string) {
  return useQuery({
    queryKey: ['reflections', habitId],
    queryFn: async () => {
      const response = await fetch(`${API_BASE_URL}/api/habits/${habitId}/reflections`)
      if (!response.ok) throw new Error('Failed to fetch reflections')
      return response.json() as Promise<Reflection[]>
    },
    enabled: !!habitId,
  })
}

export function useSubmitReflection() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ habitId, content }: { habitId: string; content: string }) => {
      const response = await fetch(`${API_BASE_URL}/api/habits/${habitId}/reflections`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      })
      if (!response.ok) throw new Error('Failed to submit reflection')
      return response.json()
    },
    onSuccess: (_, { habitId }) => {
      queryClient.invalidateQueries({ queryKey: ['reflections', habitId] })
      queryClient.invalidateQueries({ queryKey: ['coaching'] })
    },
  })
}

export function useCoachingPlan(habitId: string) {
  return useQuery({
    queryKey: ['coaching', habitId],
    queryFn: async () => {
      const response = await fetch(`${API_BASE_URL}/api/habits/${habitId}/coaching`)
      if (!response.ok) throw new Error('Failed to fetch coaching plan')
      return response.json() as Promise<CoachingPlan>
    },
    enabled: !!habitId,
  })
}
