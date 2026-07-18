import { Card } from './ui/card'

interface Node {
  id: string
  label: string
  type: 'trigger' | 'behavior' | 'outcome'
}

interface Edge {
  from: string
  to: string
  label: string
}

interface BehaviorGraph {
  nodes: Node[]
  edges: Edge[]
}

export default function BehaviorGraph({ graph }: { graph: BehaviorGraph }) {
  const getNodeColor = (type: string) => {
    switch (type) {
      case 'trigger': return 'bg-yellow-500/20 border-yellow-500'
      case 'behavior': return 'bg-primary/20 border-primary'
      case 'outcome': return 'bg-red-500/20 border-red-500'
      default: return 'bg-muted border-border'
    }
  }

  return (
    <div className="space-y-4">
      {/* Nodes */}
      <div className="flex flex-wrap justify-center gap-4">
        {graph.nodes.map((node) => (
          <Card
            key={node.id}
            className={`p-4 border-2 ${getNodeColor(node.type)} min-w-[120px] text-center`}
          >
            <p className="font-medium">{node.label}</p>
            <p className="text-xs text-muted-foreground capitalize">{node.type}</p>
          </Card>
        ))}
      </div>

      {/* Edges - Simplified visualization */}
      <div className="space-y-2">
        {graph.edges.map((edge, i) => (
          <div key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>→</span>
            <span>{edge.label}</span>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-4 pt-4 border-t">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500" />
          <span className="text-xs">Trigger</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-primary/20 border border-primary" />
          <span className="text-xs">Behavior</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500" />
          <span className="text-xs">Outcome</span>
        </div>
      </div>
    </div>
  )
}
