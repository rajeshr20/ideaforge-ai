import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Sparkles, Loader2 } from 'lucide-react'
import axios from 'axios'
import ScoreCard from '../components/ScoreCard.jsx'
import SwotTable from '../components/SwotTable.jsx'
import RoadmapCard from '../components/RoadmapCard.jsx'
import ReportButton from '../components/ReportButton.jsx'
import TextSection from '../components/TextSection.jsx'
import ProgressBar from '../components/ProgressBar.jsx'

export default function Results() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [status, setStatus] = useState('loading')
  const [stage, setStage] = useState(1)
  const [stageLabel, setStageLabel] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!jobId) return
    let interval

    const poll = async () => {
      try {
        const res = await axios.get(`/api/status/${jobId}`)
        setStage(res.data.stage || 1)
        setStageLabel(res.data.stage_label || '')
        setStatus(res.data.status)

        if (res.data.status === 'done') {
          setData(res.data.result)
          clearInterval(interval)
        } else if (res.data.status === 'error') {
          setError(res.data.error || 'Validation failed.')
          clearInterval(interval)
        }
      } catch (e) {
        setError('Could not reach the server.')
        clearInterval(interval)
      }
    }

    poll()
    interval = setInterval(poll, 2500)
    return () => clearInterval(interval)
  }, [jobId])

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-navy text-white py-4 px-6 flex items-center gap-3">
        <button onClick={() => navigate('/')} className="text-white/60 hover:text-white flex items-center gap-1.5 text-sm">
          <ArrowLeft size={15} /> New idea
        </button>
        <div className="flex items-center gap-2 ml-4">
          <Sparkles size={15} className="text-white" />
          <span className="font-bold text-lg tracking-tight">IdeaForge AI</span>
        </div>
        {data && (
          <div className="ml-auto">
            <ReportButton jobId={jobId} />
          </div>
        )}
      </header>

      <main className="max-w-4xl mx-auto px-4 py-10">
        {/* Still processing */}
        {(status === 'loading' || status === 'processing') && (
          <ProgressBar currentStage={stage} stageLabel={stageLabel} />
        )}

        {/* Error */}
        {status === 'error' && (
          <div className="card border-red-200 bg-red-50 text-center py-12">
            <p className="text-red-600 font-semibold mb-2">Validation failed</p>
            <p className="text-red-500 text-sm mb-4">{error}</p>
            <button onClick={() => navigate('/')} className="btn-outline">
              Try again
            </button>
          </div>
        )}

        {/* Results */}
        {status === 'done' && data && (
          <>
            {/* Idea header */}
            <div className="mb-8">
              <p className="text-sm text-slate-500 mb-1">Validation Report</p>
              <h1 className="text-3xl font-bold text-navy">{data.idea_name}</h1>
              {data.executive_summary && (
                <p className="text-slate-600 mt-3 leading-relaxed">{data.executive_summary}</p>
              )}
            </div>

            {/* Download button (mobile) */}
            <div className="mb-6 md:hidden">
              <ReportButton jobId={jobId} />
            </div>

            {/* Grid layout */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Left column */}
              <div className="space-y-6">
                <ScoreCard score={data.score} />
                <SwotTable swot={data.swot} />
              </div>

              {/* Right column */}
              <div className="space-y-6">
                <TextSection title="Market Research" content={data.market_research} />
                <TextSection title="Competitor Analysis" content={data.competitor_analysis} />
              </div>
            </div>

            {/* Full-width sections */}
            <div className="mt-6 space-y-6">
              <TextSection title="Feasibility & Risk Analysis" content={data.feasibility} />
              <TextSection title="Business Model Recommendation" content={data.business_model} />
              <RoadmapCard roadmap={data.roadmap} />
            </div>

            {/* Footer CTA */}
            <div className="mt-10 text-center py-8 border-t border-slate-200">
              <p className="text-slate-500 text-sm mb-4">
                Download the full report to share with your team or investors.
              </p>
              <ReportButton jobId={jobId} />
            </div>
          </>
        )}
      </main>
    </div>
  )
}
