import { Card, CardHeader, CardTitle, CardContent } from './ui/card'
import { AlertTriangle, Shield } from 'lucide-react'

interface RiskPrediction {
  high_risk_times: string[]
  risk_level: 'low' | 'medium' | 'high'
  confidence: number
}

export default function RiskCard({ prediction }: { prediction: RiskPrediction }) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-500 bg-red-500/20'
      case 'medium': return 'text-yellow-500 bg-yellow-500/20'
      case 'low': return 'text-green-500 bg-green-500/20'
      default: return 'text-muted-foreground'
    }
  }

  const getRiskIcon = (level: string) => {
    return level === 'high' || level === 'medium' ? (
      <AlertTriangle className="h-6 w-6" />
    ) : (
      <Shield className="h-6 w-6" />
    )
  }

  return (
    <Card className="glass-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Risk Prediction</CardTitle>
          <div className={`p-2 rounded-full ${getRiskColor(prediction.risk_level)}`}>
            {getRiskIcon(prediction.risk_level)}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-sm text-muted-foreground mb-1">Current Risk Level</p>
          <p className={`text-2xl font-bold capitalize ${getRiskColor(prediction.risk_level).split(' ')[0]}`}>
            {prediction.risk_level} Risk
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            {prediction.confidence}% confidence
          </p>
        </div>
        
        <div>
          <p className="text-sm text-muted-foreground mb-2">High-Risk Times Today</p>
          <div className="flex flex-wrap gap-2">
            {prediction.high_risk_times.map((time, i) => (
              <span
                key={i}
                className="px-3 py-1 bg-destructive/20 text-destructive rounded-full text-sm"
              >
                {time}
              </span>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
