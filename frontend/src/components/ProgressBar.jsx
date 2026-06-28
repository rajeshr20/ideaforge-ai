import { CheckCircle, Loader2, Circle } from 'lucide-react'

const STAGES = [
  'Receiving idea',
  'Processing & structuring idea',
  'Researching market',
  'Analysing competitors',
  'Assessing feasibility & risks',
  'Running SWOT analysis',
  'Recommending business model',
  'Computing validation score',
  'Generating MVP roadmap',
  'Building final report',
]

export default function ProgressBar({ currentStage, stageLabel }) {
  return (
    <div className="card max-w-2xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-navy rounded-full flex items-center justify-center flex-shrink-0">
          <Loader2 size={20} className="text-white animate-spin" />
        </div>
        <div>
          <p className="font-semibold text-navy">Validating your idea...</p>
          <p className="text-sm text-slate-500">{stageLabel || 'Please wait'}</p>
        </div>
      </div>

      {/* Overall progress bar */}
      <div className="h-2 bg-slate-100 rounded-full mb-6 overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-navy to-brand-teal rounded-full transition-all duration-700"
          style={{ width: `${(currentStage / 10) * 100}%` }}
        />
      </div>

      {/* Stage list */}
      <div className="space-y-2.5">
        {STAGES.map((label, i) => {
          const stageNum = i + 1
          const done = stageNum < currentStage
          const active = stageNum === currentStage
          const pending = stageNum > currentStage

          return (
            <div key={i} className={`flex items-center gap-3 py-1.5 px-3 rounded-lg transition-colors
              ${active ? 'bg-slate-50' : ''}`}>
              {done ? (
                <CheckCircle size={16} className="text-brand-teal flex-shrink-0" />
              ) : active ? (
                <Loader2 size={16} className="text-navy animate-spin flex-shrink-0" />
              ) : (
                <Circle size={16} className="text-slate-300 flex-shrink-0" />
              )}
              <span className={`text-sm transition-colors ${
                done ? 'text-slate-400 line-through' :
                active ? 'text-navy font-medium' :
                'text-slate-400'
              }`}>
                <span className={`text-xs mr-1.5 ${active ? 'text-navy/60' : 'text-slate-300'}`}>
                  {String(stageNum).padStart(2, '0')}
                </span>
                {label}
              </span>
            </div>
          )
        })}
      </div>

      <p className="text-xs text-slate-400 text-center mt-6">
        This usually takes 60–90 seconds. Please don't close the tab.
      </p>
    </div>
  )
}
