/**
 * TextSection — renders multi-line text from LLM agents cleanly.
 * Handles bold (**text**), numbered headings, and bullet points.
 */
export default function TextSection({ title, content }) {
  if (!content) return null

  const lines = content.split('\n').filter(l => l.trim())

  const renderLine = (line, i) => {
    const trimmed = line.trim()

    // Numbered heading: "1. Title" or "**Title**"
    const isHeading = /^(\d+\.|#{1,3}|\*{2}.+\*{2}$)/.test(trimmed)
    if (isHeading) {
      const clean = trimmed.replace(/^[\d.#*\s]+/, '').replace(/\*\*/g, '').trim()
      return <p key={i} className="text-sm font-semibold text-navy mt-4 mb-1">{clean}</p>
    }

    // Bullet line
    if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
      const text = trimmed.replace(/^[-•]\s*/, '')
      return (
        <li key={i} className="text-sm text-slate-700 leading-relaxed ml-4 list-disc">
          {renderInline(text)}
        </li>
      )
    }

    return <p key={i} className="text-sm text-slate-700 leading-relaxed">{renderInline(trimmed)}</p>
  }

  // Render inline **bold** markers
  const renderInline = (text) => {
    const parts = text.split(/\*\*(.*?)\*\*/g)
    return parts.map((part, i) =>
      i % 2 === 1 ? <strong key={i} className="font-semibold text-slate-800">{part}</strong> : part
    )
  }

  return (
    <div className="card">
      <div className="section-title">{title}</div>
      <div className="space-y-1">
        {lines.map((line, i) => renderLine(line, i))}
      </div>
    </div>
  )
}
