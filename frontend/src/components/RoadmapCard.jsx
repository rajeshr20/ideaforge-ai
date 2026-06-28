import { MapPin, CheckCircle2 } from 'lucide-react'

const PHASE_STYLES = [
  { bg: 'bg-teal-50',   border: 'border-teal-200',  dot: 'bg-brand-teal',   num: 'bg-brand-teal text-white' },
  { bg: 'bg-violet-50', border: 'border-violet-200', dot: 'bg-brand-purple', num: 'bg-brand-purple text-white' },
  { bg: 'bg-amber-50',  border: 'border-amber-200',  dot: 'bg-brand-amber',  num: 'bg-brand-amber text-white' },
]

export default function RoadmapCard({ roadmap }) {
  if (!roadmap?.length) return null
  return (
    <div className="card">
      <div className="section-title flex items-center gap-2">
        <MapPin size={18} /> MVP Roadmap
      </div>
      <div className="space-y-4">
        {roadmap.map((phase, i) => {
          const style = PHASE_STYLES[i % PHASE_STYLES.length]
          return (
            <div key={i} className={`${style.bg} ${style.border} border rounded-xl p-4`}>
              <div className="flex items-center gap-3 mb-3">
                <span className={`w-7 h-7 rounded-full ${style.num} text-xs font-bold flex items-center justify-center flex-shrink-0`}>
                  {i + 1}
                </span>
                <div>
                  <p className="font-semibold text-navy text-sm">{phase.phase}</p>
                  <p className="text-xs text-slate-500">{phase.duration}</p>
                </div>
              </div>
              <ul className="space-y-2 ml-10">
                {(phase.milestones || []).map((m, j) => (
                  <li key={j} className="flex items-start gap-2 text-xs text-slate-700 leading-relaxed">
                    <CheckCircle2 size={13} className={`mt-0.5 flex-shrink-0 ${style.dot.replace('bg-', 'text-')}`} />
                    {m}
                  </li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>
    </div>
  )
}
