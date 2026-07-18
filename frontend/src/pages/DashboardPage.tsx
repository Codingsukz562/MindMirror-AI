import { motion } from 'framer-motion'
import { TrendingUp, Calendar, CheckCircle } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

export default function DashboardPage() {
  // Mock data - would come from API in production
  const stats = {
    reflectionsThisWeek: 12,
    triggersIdentified: 5,
    successfulReplacements: 8,
    consistencyScore: 73,
  }

  const weeklyProgress = [
    { day: 'Mon', reflections: 2, success: true },
    { day: 'Tue', reflections: 1, success: true },
    { day: 'Wed', reflections: 3, success: false },
    { day: 'Thu', reflections: 2, success: true },
    { day: 'Fri', reflections: 1, success: true },
    { day: 'Sat', reflections: 2, success: true },
    { day: 'Sun', reflections: 1, success: true },
  ]

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">Your Dashboard</h1>
        <p className="text-muted-foreground">
          Track your progress and insights over time
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="glass-card">
          <CardHeader>
            <TrendingUp className="h-6 w-6 text-primary mb-2" />
            <CardTitle className="text-sm">Reflections</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.reflectionsThisWeek}</p>
            <p className="text-xs text-muted-foreground">This week</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <CheckCircle className="h-6 w-6 text-green-500 mb-2" />
            <CardTitle className="text-sm">Success Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.consistencyScore}%</p>
            <p className="text-xs text-muted-foreground">Habit replacements</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <Calendar className="h-6 w-6 text-primary mb-2" />
            <CardTitle className="text-sm">Active Days</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">5/7</p>
            <p className="text-xs text-muted-foreground">This week</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <TrendingUp className="h-6 w-6 text-purple-500 mb-2" />
            <CardTitle className="text-sm">Triggers Found</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.triggersIdentified}</p>
            <p className="text-xs text-muted-foreground">Patterns identified</p>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Progress */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Weekly Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between items-end h-32">
            {weeklyProgress.map((day, i) => (
              <div key={i} className="flex flex-col items-center gap-2">
                <div
                  className={`w-8 rounded-t-lg transition-all ${
                    day.success ? 'bg-primary' : 'bg-muted'
                  }`}
                  style={{ height: `${day.reflections * 30}px` }}
                />
                <span className="text-xs text-muted-foreground">{day.day}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Insights */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>AI Insights</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-start gap-3">
            <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
            <div>
              <p className="font-medium">Your best days are weekdays</p>
              <p className="text-sm text-muted-foreground">
                You show 40% better consistency Monday through Friday
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
            <div>
              <p className="font-medium">Evening reflection helps</p>
              <p className="text-sm text-muted-foreground">
                Days with evening reflections have 25% higher success rates
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Consistency Progress */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>30-Day Consistency</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Progress value={stats.consistencyScore} />
          <p className="text-sm text-muted-foreground text-right">
            {stats.consistencyScore}% on track to beat last month
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
