import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, MessageCircle, BarChart3, Target, Bot } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { useCoachingPlan, useHabits } from '@/hooks/useHabits'
import BehaviorGraph from '@/components/BehaviorGraph'
import RiskCard from '@/components/RiskCard'
import DailyMission from '@/components/DailyMission'
import AIChat from '@/components/ai/AIChat'
import { useState } from 'react'

export default function HabitPage() {
  const { habitId } = useParams<{ habitId: string }>()
  const { data: coachingPlan, isLoading } = useCoachingPlan(habitId!)
  const [showChat, setShowChat] = useState(false)

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3"></div>
          <div className="h-24 bg-muted rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center gap-4">
          <Link to="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold capitalize">{habitId?.replace('_', ' ')}</h1>
            <p className="text-muted-foreground">Your personalized coaching dashboard</p>
          </div>
        </div>
        <Button 
          onClick={() => setShowChat(!showChat)}
          variant={showChat ? "default" : "outline"}
          className={showChat ? "gradient-bg" : ""}
        >
          <Bot className="h-4 w-4 mr-2" />
          {showChat ? 'Hide Coach' : 'Ask AI Coach'}
        </Button>
      </motion.div>

      {/* AI Chat Panel */}
      {showChat && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <AIChat habitId={habitId!} onClose={() => setShowChat(false)} />
        </motion.div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Link to={`/habits/${habitId}/reflect`}>
          <Button className="gradient-bg">
            <MessageCircle className="h-4 w-4 mr-2" />
            Reflect Now
          </Button>
        </Link>
        <Button variant="outline">
          <BarChart3 className="h-4 w-4 mr-2" />
          View History
        </Button>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Today's Mission */}
        {coachingPlan?.daily_plan && (
          <DailyMission plan={coachingPlan.daily_plan} />
        )}

        {/* Risk Prediction */}
        {coachingPlan?.risk_prediction && (
          <RiskCard prediction={coachingPlan.risk_prediction} />
        )}

        {/* Trigger Analysis */}
        {coachingPlan?.trigger_analysis && (
          <Card className="glass-card">
            <CardHeader>
              <Target className="h-6 w-6 text-primary mb-2" />
              <CardTitle>Your Triggers</CardTitle>
              <CardDescription>Patterns detected from your reflections</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Emotional Triggers</h4>
                <div className="flex flex-wrap gap-2">
                  {coachingPlan.trigger_analysis.emotional_patterns.map((emotion, i) => (
                    <span key={i} className="px-3 py-1 bg-primary/20 rounded-full text-sm">
                      {emotion}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">Environmental Factors</h4>
                <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                  {coachingPlan.trigger_analysis.environmental_factors.map((factor, i) => (
                    <li key={i}>{factor}</li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Behavior Graph */}
        {coachingPlan?.behavior_graph && (
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Behavior Pattern</CardTitle>
              <CardDescription>How your triggers lead to outcomes</CardDescription>
            </CardHeader>
            <CardContent>
              <BehaviorGraph graph={coachingPlan.behavior_graph} />
            </CardContent>
          </Card>
        )}
      </div>

      {/* Replacement Habits */}
      {coachingPlan?.replacement_habits && coachingPlan.replacement_habits.length > 0 && (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Recommended Replacement Habits</CardTitle>
            <CardDescription>Healthy alternatives to try when urges hit</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              {coachingPlan.replacement_habits.map((habit, i) => (
                <Card key={i} className="bg-white/5">
                  <CardHeader>
                    <CardTitle className="text-lg">{habit.name}</CardTitle>
                    <CardDescription>{habit.description}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Motivation Message */}
      {coachingPlan?.motivation_message && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card p-6 text-center"
        >
          <p className="text-lg italic text-muted-foreground">
            "{coachingPlan.motivation_message}"
          </p>
        </motion.div>
      )}
    </div>
  )
}
