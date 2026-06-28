import { Shield, AlertTriangle, TrendingUp, Zap } from 'lucide-react'

const QUADRANTS = [
  {
    key: 'strengths',
    label: 'Strengths',
    icon: Shield,
    bg: 'bg-teal-50',
    border: 'border-teal-200',
    iconColor: 'text-brand-teal',
    dot: 'bg-brand-teal',
  },
  {
    key: 'weaknesses',
    label: 'Weaknesses',
    icon: AlertTriangle,
    bg: 'bg-red-50',
    border: 'border-red-200',
    iconColor: 'text-brand-coral',
    dot: 'bg-brand-coral',
  },
  {
    key: 'opportunities',
    label: 'Opportunities',
    icon: TrendingUp,
    bg: 'bg-violet-50',
    border: 'border-violet-200',
    iconColor: 'text-brand-purple',
    dot: 'bg-brand-purple',
  },
  {
    key: 'threats',
    label: 'Threats',
    icon: Zap,
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    iconColor: 'text-brand-amber',
    dot: 'bg-brand-amber',
  },
]

export default function SwotTable({ swot }) {
  if (!swot) return null
  return (
    <div className="card">
      <div className="section-title">SWOT Analysis</div>
      <div className="grid grid-cols-2 gap-3">
        {QUADRANTS.map(({ key, label, icon: Icon, bg, border, iconColor, dot }) => (
          <div key={key} className={`${bg} ${border} border rounded-xl p-4`}>
            <div className={`flex items-center gap-2 mb-3 ${iconColor}`}>
              <Icon size={15} />
              <span className="text-sm font-semibold">{label}</span>
            </div>
            <ul className="space-y-2">
              {(swot[key] || []).map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-slate-700 leading-relaxed">
                  <span className={`w-1.5 h-1.5 ${dot} rounded-full mt-1.5 flex-shrink-0`} />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}
