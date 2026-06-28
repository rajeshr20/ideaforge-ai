import { useState, useRef, useCallback } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || ''

export function useValidation() {
  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState('idle')   // idle | processing | done | error
  const [stage, setStage] = useState(0)
  const [stageLabel, setStageLabel] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const pollRef = useRef(null)

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }, [])

  const pollStatus = useCallback(async (id) => {
    try {
      const { data } = await axios.get(`${API_BASE}/api/status/${id}`)
      setStage(data.stage || 0)
      setStageLabel(data.stage_label || '')
      setStatus(data.status)

      if (data.status === 'done') {
        setResult(data.result)
        stopPolling()
      } else if (data.status === 'error') {
        setError(data.error || 'Something went wrong during validation.')
        stopPolling()
      }
    } catch (err) {
      setError('Could not reach the server. Is the backend running?')
      stopPolling()
    }
  }, [stopPolling])

  const submit = useCallback(async (formData) => {
    setStatus('processing')
    setStage(1)
    setStageLabel('Receiving idea')
    setError(null)
    setResult(null)

    try {
      const { data } = await axios.post(`${API_BASE}/api/validate`, formData)
      const id = data.job_id
      setJobId(id)

      // Poll every 2.5 seconds
      pollRef.current = setInterval(() => pollStatus(id), 2500)
      return id
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to submit idea. Check your input.'
      setError(msg)
      setStatus('error')
      return null
    }
  }, [pollStatus])

  const reset = useCallback(() => {
    stopPolling()
    setJobId(null)
    setStatus('idle')
    setStage(0)
    setStageLabel('')
    setResult(null)
    setError(null)
  }, [stopPolling])

  return { jobId, status, stage, stageLabel, result, error, submit, reset }
}
