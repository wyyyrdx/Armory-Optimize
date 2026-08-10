import { useState } from 'react'
import Topbar from '../components/Topbar'
import { classifyFact } from '../api/client'
import { loadStats, saveStats } from '../utils/helpers'

export default function Submit() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit() {
    setError('')
    setResult(null)
    if (text.trim().length < 10) {
      setError('Please enter at least 10 characters.')
      return
    }
    setLoading(true)
    try {
      const data = await classifyFact(text.trim())
      const stats = loadStats()
      stats.submitted = true
      saveStats(stats)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="view active">
      <Topbar />
      <div className="submit-panel">
        <h2>Submit a Strange Fact</h2>
        <p className="hint">Hand it to the curator. Get scored.</p>
        <textarea
          id="fact-input"
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="e.g. Some turtles can breathe through their butts."
        />
        <button className="btn pink" onClick={onSubmit} disabled={loading}>
          {loading ? 'Curator is thinking…' : 'Hand to the Curator ✨'}
        </button>

        {error && <p className="play-hint" style={{ color: '#ffb4b4' }}>{error}</p>}

        {result && (
          <div className="classify-result">
            <div className="accepted">✓ Exhibit accepted · #{result.exhibit_id}</div>
            <div className="category-stamp">{result.category_emoji} {result.category}</div>
            <p style={{ fontWeight: 700, margin: '0.5rem 0' }}>{result.fact}</p>
            <div className="score-row">
              <div className="score-box">
                <label>Weirdness</label>
                <span className="value">{result.weirdness}</span>
              </div>
              <div className="score-box">
                <label>Freak Factor</label>
                <span className="value">{result.wtf}</span>
              </div>
            </div>
            <p className="explanation">{result.explanation}</p>
          </div>
        )}
      </div>
    </section>
  )
}