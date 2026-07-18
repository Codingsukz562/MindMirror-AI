import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Send, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { useSubmitReflection } from '@/hooks/useHabits'
import { useToast } from '@/hooks/useToast'

export default function ReflectionPage() {
  const { habitId } = useParams<{ habitId: string }>()
  const navigate = useNavigate()
  const [content, setContent] = useState('')
  const submitReflection = useSubmitReflection()
  const { addToast } = useToast()
  const [isThinking, setIsThinking] = useState(false)
  const [thinkingSteps, setThinkingSteps] = useState<string[]>([])

  const thinkingMessages = [
    '🧠 Understanding today\'s emotions...',
    '🔍 Detecting behavioral patterns...',
    '📈 Predicting relapse risk...',
    '🎯 Building today\'s mission...',
    '✨ Personalizing your coaching plan...',
  ]

  const handleSubmit = async () => {
    if (!content.trim() || !habitId) return

    setIsThinking(true)
    
    // Simulate AI thinking steps
    for (let i = 0; i < thinkingMessages.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800))
      setThinkingSteps(prev => [...prev, thinkingMessages[i]])
    }

    try {
      await submitReflection.mutateAsync({ habitId, content })
      addToast({
        title: 'Reflection submitted',
        description: 'AI has analyzed your reflection and updated your coaching plan.',
      })
      navigate(`/habits/${habitId}`)
    } catch (error) {
      addToast({
        title: 'Error',
        description: 'Failed to submit reflection. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setIsThinking(false)
    }
  }

  const prompts = [
    "How are you feeling right now?",
    "What triggered the urge today?",
    "Where were you when you felt the impulse?",
    "What emotion preceded the behavior?",
    "What happened just before you relapsed?",
  ]

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">Reflect on Your Experience</h1>
        <p className="text-muted-foreground">
          Share openly. There's no judgment here. Every reflection helps AI understand your patterns better.
        </p>
      </motion.div>

      {/* Prompts */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Need inspiration?</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {prompts.map((prompt, i) => (
              <Button
                key={i}
                variant="outline"
                size="sm"
                onClick={() => setContent(prev => prev + (prev ? ' ' : '') + prompt)}
                className="text-xs"
              >
                {prompt}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Reflection Input */}
      <Card className="glass-card">
        <CardContent className="pt-6 space-y-4">
          <Textarea
            placeholder="Share what's on your mind... What happened? How did you feel? What triggered you?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-[200px] text-lg"
            disabled={isThinking}
          />
          
          <div className="flex justify-between items-center">
            <p className="text-sm text-muted-foreground">
              {content.length} characters
            </p>
            <Button 
              onClick={handleSubmit} 
              disabled={!content.trim() || isThinking}
              className="gradient-bg"
            >
              {isThinking ? (
                <>
                  <Sparkles className="h-4 w-4 mr-2 animate-pulse" />
                  Processing...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Submit Reflection
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* AI Thinking Animation */}
      {isThinking && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-2"
        >
          {thinkingSteps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass-card p-3 text-sm"
            >
              {step}
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  )
}
