import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Brain, Target, TrendingUp, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'

export default function HomePage() {
  const habits = [
    { id: 'social_media', name: 'Social Media', icon: '📱', category: 'social_media' },
    { id: 'screen_time', name: 'Screen Time', icon: '💻', category: 'screen_time' },
    { id: 'gaming', name: 'Gaming', icon: '🎮', category: 'gaming' },
    { id: 'procrastination', name: 'Procrastination', icon: '⏰', category: 'procrastination' },
    { id: 'junk_food', name: 'Junk Food', icon: '🍔', category: 'junk_food' },
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-6 py-12"
      >
        <h1 className="text-5xl font-bold gradient-text">
          Understand why you relapse. Change what triggers you.
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          MindMirror AI is your personal behavioral coach. It learns from your reflections,
          discovers your triggers, and helps you build sustainable habits.
        </p>
        <Button size="lg" className="gradient-bg">
          Start Your Journey
        </Button>
      </motion.section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-6">
        <Card className="glass-card">
          <CardHeader>
            <Brain className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Trigger Intelligence</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Discover the emotional and environmental patterns that drive your habits.
            </CardDescription>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <Target className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Predictive Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Get AI-powered predictions about your highest-risk moments before they happen.
            </CardDescription>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <Sparkles className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Adaptive Coaching</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Receive personalized daily missions that adapt to your progress and challenges.
            </CardDescription>
          </CardContent>
        </Card>
      </section>

      {/* Habit Selection */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-center">Choose a Habit to Work On</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {habits.map((habit) => (
            <Link key={habit.id} to={`/habits/${habit.id}`}>
              <Card className="glass-card hover:bg-white/10 transition-colors cursor-pointer">
                <CardHeader>
                  <div className="text-4xl mb-2">{habit.icon}</div>
                  <CardTitle>{habit.name}</CardTitle>
                  <CardDescription className="capitalize">
                    {habit.category.replace('_', ' ')} addiction
                  </CardDescription>
                </CardHeader>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-center">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-4">
          {[
            { icon: '💭', title: 'Reflect', desc: 'Share your thoughts naturally' },
            { icon: '🔍', title: 'Discover', desc: 'AI finds your patterns' },
            { icon: '📊', title: 'Understand', desc: 'See your trigger graph' },
            { icon: '🎯', title: 'Act', desc: 'Get daily missions' },
          ].map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="text-center space-y-2"
            >
              <div className="text-4xl">{step.icon}</div>
              <h3 className="font-semibold">{step.title}</h3>
              <p className="text-sm text-muted-foreground">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  )
}
