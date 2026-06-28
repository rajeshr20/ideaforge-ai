import { TrendingUp } from 'lucide-react'

const DIMS = [
  { key: 'market_size',           label: 'Market Size' },
  { key: 'competition_gap',       label: 'Competition Gap' },
  { key: 'technical_feasibility', label: 'Technical Feasibility' },
  { key: 'idea_uniqueness',       label: 'Idea Uniqueness' },
  { key: 'monetisation_potential',label: 'Monetisation Potential' },
]

function scoreColor(val, max = 20) {
  const pct = val / max
  if (pct >= 0.70) return { bar: 'bg-brand-teal', text: 'text-brand-teal' }
  if (pct >= 0.50) return { bar: 'bg-brand-amber', text: 'text-brand-amber' }
  return { bar: 'bg-brand-coral', text: 'text-brand-coral' }
}

function totalColor(total) {
  if (total >= 70) return 'text-brand-teal'
  if (total >= 50) return 'text-brand-amber'
  return 'text-brand-coral'
}

function totalBg(total) {
  if (total >= 70) return 'bg-teal-50 border-teal-200'
  if (total >= 50) return 'bg-amber-50 border-amber-200'
  return 'bg-red-50 border-red-200'
}

export default function ScoreCard({ score }) {
  if (!score) return null
  return (
    <div className="card">
      <div className="section-title flex items-center gap-2">
        <TrendingUp size={18} /> Validation Score
      </div>

      {/* Total score hero */}
      <div className={`flex flex-col items-center justify-center py-6 mb-6 rounded-xl border ${totalBg(score.total)}`}>
        <p className={`text-6xl font-bold ${totalColor(score.total)}`}>{Math.round(score.total)}</p>
        <p className="text-slate-500 text-sm mt-1">out of 100</p>
        <span className={`mt-3 px-4 py-1 rounded-full text-sm font-semibold border ${totalBg(score.total)} ${totalColor(score.total)}`}>
          {score.verdict}
        </span>
      </div>

      {/* Dimension bars */}
      <div className="space-y-4">
        {DIMS.map(({ key, label }) => {
          const val = score[key] ?? 0
          const { bar, text } = scoreColor(val, 20)
          return (
            <div key={key}>
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-sm text-slate-700">{label}</span>
                <span className={`text-sm font-semibold ${text}`}>{val.toFixed(0)}/20</span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${bar} rounded-full transition-all duration-700`}
                  style={{ width: `${(val / 20) * 100}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
