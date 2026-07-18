import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { Progress } from './ui/progress'

interface DailyPlan {
  mission: string
  replacement_habit: string
  success_criteria: string
}

export default function DailyMission({ plan }: { plan: DailyPlan }) {
  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Today's Mission</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h4 className="font-medium mb-2">Primary Focus</h4>
          <p className="text-muted-foreground">{plan.mission}</p>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Replacement Habit</h4>
          <p className="text-muted-foreground">{plan.replacement_habit}</p>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Success Looks Like</h4>
          <p className="text-muted-foreground">{plan.success_criteria}</p>
        </div>
        
        <Progress value={33} className="mt-4" />
        <p className="text-xs text-muted-foreground text-right">1 of 3 actions completed</p>
      </CardContent>
    </Card>
  )
}
