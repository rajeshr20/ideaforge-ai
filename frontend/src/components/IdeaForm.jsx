import { useState } from 'react'
import { Lightbulb, Users, Target, DollarSign, ChevronRight, ChevronLeft, Send } from 'lucide-react'

const DOMAINS = [
  { value: 'fintech', label: 'Fintech' },
  { value: 'edtech', label: 'Edtech' },
  { value: 'healthtech', label: 'Healthtech' },
  { value: 'ecommerce', label: 'E-commerce' },
  { value: 'saas', label: 'SaaS' },
  { value: 'agritech', label: 'Agritech' },
  { value: 'logistics', label: 'Logistics' },
  { value: 'social', label: 'Social Media / Creator Economy' },
  { value: 'ai_ml', label: 'AI / ML Product' },
  { value: 'other', label: 'Other' },
]

const BUDGETS = [
  { value: '< ₹5 lakhs (bootstrap)', label: '< ₹5 Lakhs — Bootstrap' },
  { value: '₹5–50 lakhs (seed)', label: '₹5–50 Lakhs — Seed' },
  { value: '₹50 lakhs – ₹5 crore (Series A)', label: '₹50L – ₹5 Cr — Series A' },
  { value: '> ₹5 crore', label: '> ₹5 Crore' },
]

const STEPS = [
  { icon: Lightbulb, label: 'Idea', fields: ['idea_name', 'description', 'domain'] },
  { icon: Users,     label: 'Audience', fields: ['target_audience', 'unique_value'] },
  { icon: DollarSign, label: 'Budget', fields: ['budget_range'] },
]

const CHAR_LIMITS = {
  idea_name: 100,
  description: 2000,
  target_audience: 300,
  unique_value: 500,
}

export default function IdeaForm({ onSubmit, loading }) {
  const [step, setStep] = useState(0)
  const [form, setForm] = useState({
    idea_name: '',
    description: '',
    domain: '',
    target_audience: '',
    unique_value: '',
    budget_range: '',
  })
  const [errors, setErrors] = useState({})

  const set = (key, val) => {
    setForm(f => ({ ...f, [key]: val }))
    if (errors[key]) setErrors(e => ({ ...e, [key]: '' }))
  }

  const validate = (stepIndex) => {
    const e = {}
    if (stepIndex === 0) {
      if (!form.idea_name.trim()) e.idea_name = 'Idea name is required'
      if (form.description.trim().length < 50) e.description = 'Please describe your idea in at least 50 characters'
      if (!form.domain) e.domain = 'Please select a domain'
    }
    if (stepIndex === 1) {
      if (form.target_audience.trim().length < 5) e.target_audience = 'Please describe your target audience'
      if (form.unique_value.trim().length < 10) e.unique_value = 'Please describe what makes your idea unique'
    }
    if (stepIndex === 2) {
      if (!form.budget_range) e.budget_range = 'Please select a budget range'
    }
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const next = () => {
    if (validate(step)) setStep(s => s + 1)
  }

  const back = () => setStep(s => s - 1)

  const handleSubmit = () => {
    if (validate(step)) onSubmit(form)
  }

  const progress = ((step + 1) / STEPS.length) * 100

  return (
    <div className="max-w-2xl mx-auto">
      {/* Step indicators */}
      <div className="flex items-center gap-2 mb-8">
        {STEPS.map((s, i) => {
          const Icon = s.icon
          const active = i === step
          const done = i < step
          return (
            <div key={i} className="flex items-center gap-2 flex-1">
              <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all
                ${done ? 'bg-brand-teal text-white' : active ? 'bg-navy text-white' : 'bg-slate-100 text-slate-400'}`}>
                <Icon size={13} />
                <span>{s.label}</span>
              </div>
              {i < STEPS.length - 1 && (
                <div className={`flex-1 h-0.5 rounded ${done ? 'bg-brand-teal' : 'bg-slate-200'}`} />
              )}
            </div>
          )
        })}
      </div>

      {/* Step 0 — Idea basics */}
      {step === 0 && (
        <div className="space-y-5">
          <div>
            <label className="label">Startup idea name <span className="text-red-500">*</span></label>
            <input
              className="input"
              placeholder="e.g. GreenTrack, MediConnect, AgriSense"
              value={form.idea_name}
              onChange={e => set('idea_name', e.target.value)}
              maxLength={100}
            />
            {errors.idea_name && <p className="text-red-500 text-xs mt-1">{errors.idea_name}</p>}
          </div>

          <div>
            <label className="label">
              Describe your idea <span className="text-red-500">*</span>
              <span className="text-slate-400 font-normal ml-1">— what problem it solves and how</span>
            </label>
            <textarea
              className="input resize-none"
              rows={5}
              placeholder="Describe the problem you're solving, your solution, and how it works. The more detail you give, the better the analysis."
              value={form.description}
              onChange={e => set('description', e.target.value)}
              maxLength={2000}
            />
            <div className="flex justify-between mt-1">
              {errors.description
                ? <p className="text-red-500 text-xs">{errors.description}</p>
                : <span />}
              <span className="text-xs text-slate-400">{form.description.length}/2000</span>
            </div>
          </div>

          <div>
            <label className="label">Domain / Industry <span className="text-red-500">*</span></label>
            <select className="input" value={form.domain} onChange={e => set('domain', e.target.value)}>
              <option value="">Select domain...</option>
              {DOMAINS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
            </select>
            {errors.domain && <p className="text-red-500 text-xs mt-1">{errors.domain}</p>}
          </div>
        </div>
      )}

      {/* Step 1 — Audience */}
      {step === 1 && (
        <div className="space-y-5">
          <div>
            <label className="label">
              Target audience <span className="text-red-500">*</span>
              <span className="text-slate-400 font-normal ml-1">— be as specific as possible</span>
            </label>
            <textarea
              className="input resize-none"
              rows={3}
              placeholder="e.g. Small business owners in tier-2 Indian cities aged 30–50 who manage inventory manually"
              value={form.target_audience}
              onChange={e => set('target_audience', e.target.value)}
              maxLength={300}
            />
            <div className="flex justify-between mt-1">
              {errors.target_audience
                ? <p className="text-red-500 text-xs">{errors.target_audience}</p>
                : <span />}
              <span className="text-xs text-slate-400">{form.target_audience.length}/300</span>
            </div>
          </div>

          <div>
            <label className="label">
              Unique value proposition <span className="text-red-500">*</span>
              <span className="text-slate-400 font-normal ml-1">— what makes you different?</span>
            </label>
            <textarea
              className="input resize-none"
              rows={4}
              placeholder="e.g. Unlike existing solutions that require expensive hardware, our app uses the smartphone camera and AI to do the same job at 1/10th the cost."
              value={form.unique_value}
              onChange={e => set('unique_value', e.target.value)}
              maxLength={500}
            />
            <div className="flex justify-between mt-1">
              {errors.unique_value
                ? <p className="text-red-500 text-xs">{errors.unique_value}</p>
                : <span />}
              <span className="text-xs text-slate-400">{form.unique_value.length}/500</span>
            </div>
          </div>
        </div>
      )}

      {/* Step 2 — Budget */}
      {step === 2 && (
        <div className="space-y-4">
          <p className="text-sm text-slate-500 mb-6">
            Select your estimated initial budget. This helps us give you realistic feasibility and roadmap advice.
          </p>
          {BUDGETS.map(b => (
            <button
              key={b.value}
              onClick={() => set('budget_range', b.value)}
              className={`w-full text-left px-5 py-4 rounded-xl border-2 transition-all duration-150 font-medium text-sm
                ${form.budget_range === b.value
                  ? 'border-navy bg-navy text-white'
                  : 'border-slate-200 bg-white text-slate-700 hover:border-navy/40'}`}
            >
              {b.label}
            </button>
          ))}
          {errors.budget_range && <p className="text-red-500 text-xs mt-1">{errors.budget_range}</p>}
        </div>
      )}

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8 pt-6 border-t border-slate-200">
        <button
          onClick={back}
          disabled={step === 0}
          className={`flex items-center gap-1.5 text-sm font-medium transition-colors
            ${step === 0 ? 'text-slate-300 cursor-not-allowed' : 'text-slate-600 hover:text-navy'}`}
        >
          <ChevronLeft size={16} /> Back
        </button>

        {step < STEPS.length - 1 ? (
          <button onClick={next} className="btn-primary flex items-center gap-2">
            Continue <ChevronRight size={16} />
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="btn-primary flex items-center gap-2"
          >
            {loading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Starting...
              </>
            ) : (
              <>
                <Send size={16} /> Validate My Idea
              </>
            )}
          </button>
        )}
      </div>
    </div>
  )
}
