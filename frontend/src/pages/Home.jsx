import { useNavigate } from 'react-router-dom'
import { Sparkles, BarChart2, Shield, Map } from 'lucide-react'
import IdeaForm from '../components/IdeaForm.jsx'
import ProgressBar from '../components/ProgressBar.jsx'
import { useValidation } from '../hooks/useValidation.js'

const FEATURES = [
  { icon: BarChart2, label: 'Market Research', desc: 'TAM/SAM, trends, pain points' },
  { icon: Shield,    label: 'SWOT & Risk',    desc: 'Competitor & feasibility analysis' },
  { icon: Sparkles,  label: 'Validation Score', desc: '0–100 confidence score' },
  { icon: Map,       label: 'MVP Roadmap',    desc: '3-phase step-by-step plan' },
]

export default function Home() {
  const navigate = useNavigate()
  const { status, stage, stageLabel, error, submit, jobId } = useValidation()

  const handleSubmit = async (formData) => {
    const id = await submit(formData)
    if (id) {
      // Wait for status to update, then navigate
      const interval = setInterval(async () => {
        try {
          const res = await fetch(`/api/status/${id}`)
          const data = await res.json()
          if (data.status === 'done') {
            clearInterval(interval)
            navigate(`/results/${id}`)
          } else if (data.status === 'error') {
            clearInterval(interval)
          }
        } catch (_) {}
      }, 2500)
    }
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-navy text-white py-4 px-6 flex items-center gap-3">
        <div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">
          <Sparkles size={16} className="text-white" />
        </div>
        <span className="font-bold text-lg tracking-tight">IdeaForge AI</span>
        <span className="text-white/40 text-sm ml-auto">Powered by Gemini</span>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12">
        {status === 'idle' && (
          <>
            {/* Hero */}
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-navy mb-4 leading-tight">
                Validate your startup idea<br />
                <span className="text-brand-teal">before you build</span>
              </h1>
              <p className="text-slate-500 text-lg max-w-xl mx-auto">
                Get AI-powered market research, competitor analysis, SWOT, validation score,
                and MVP roadmap — in under 2 minutes.
              </p>
            </div>

            {/* Feature pills */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-12">
              {FEATURES.map(({ icon: Icon, label, desc }) => (
                <div key={label} className="bg-white border border-slate-200 rounded-xl p-4 text-center">
                  <Icon size={20} className="text-navy mx-auto mb-2" />
                  <p className="text-xs font-semibold text-navy">{label}</p>
                  <p className="text-xs text-slate-400 mt-0.5">{desc}</p>
                </div>
              ))}
            </div>

            {/* Form card */}
            <div className="card">
              <h2 className="text-xl font-bold text-navy mb-6">Tell us about your idea</h2>
              <IdeaForm onSubmit={handleSubmit} loading={false} />
            </div>
          </>
        )}

        {status === 'processing' && (
          <ProgressBar currentStage={stage} stageLabel={stageLabel} />
        )}

        {error && (
          <div className="card border-red-200 bg-red-50 text-center">
            <p className="text-red-600 font-medium mb-2">Something went wrong</p>
            <p className="text-red-500 text-sm">{error}</p>
            <button onClick={() => window.location.reload()} className="btn-outline mt-4 text-sm">
              Try again
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
