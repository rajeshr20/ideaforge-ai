import { Download } from 'lucide-react'

export default function ReportButton({ jobId }) {
  if (!jobId) return null
  return (
    <a
      href={`/report/${jobId}`}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-2 bg-navy text-white font-semibold
                 px-6 py-3 rounded-xl hover:bg-navy-light transition-colors duration-200 text-sm"
    >
      <Download size={16} />
      Download PDF Report
    </a>
  )
}
