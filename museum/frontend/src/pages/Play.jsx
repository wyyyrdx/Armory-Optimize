import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Topbar from '../components/Topbar'
import FactCard from '../components/FactCard'
import { getRandom } from '../api/client'
import { addToCollection, loadStats, saveStats } from '../utils/helpers'

export default function Play() {
  const [fact, setFact] = useState(null)
  const [streak, setStreak] = useState(0)
  const [hint, setHint] = useState('')
  const [loading, setLoading] = useState(false)

  async function nextFact() {
    setLoading(true)
    setHint('')
    try {
      const data = await getRandom()
      setFact(data)
      setStreak((s) => {
        const next = s + 1
        const stats = loadStats()
        stats.maxStreak = Math.max(stats.maxStreak || 0, next)
        saveStats(stats)
        return next
      })
    } catch {
      setHint('Could not load fact. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    nextFact()
  }, [])

  function onSave() {
    if (!fact) return
    const added = addToCollection(fact)
    setHint(added ? 'Added to My Museum.' : 'Already in your museum.')
  }

  async function onShare() {
    if (!fact) return
    const text = `${fact.fact}\n\n— Museum of Useless Knowledge\nWeirdness ${fact.weirdness} · Freak ${fact.wtf}`
    try {
      if (navigator.share) {
        await navigator.share({ text, title: 'Useless Fact' })
        setHint('Shared!')
      } else {
        await navigator.clipboard.writeText(text)
        setHint('Copied to clipboard!')
      }
    } catch {
      setHint('Could not share.')
    }
  }

  let streakMsg = ''
  if (streak >= 20) streakMsg = 'Terminal curiosity unlocked.'
  else if (streak >= 10) streakMsg = 'You are now officially wasting time efficiently.'
  else if (streak >= 5) streakMsg = 'Nice streak. Keep going.'

  return (
    <section className="view active">
      <Topbar />
      <div className="play-stage">
        <div className="streak-bar">
          <span id="streak-text">Combo ×{streak}</span>
          <span>{streakMsg}</span>
        </div>

        <FactCard fact={fact} />

        <button className="btn primary large next-btn" onClick={nextFact} disabled={loading}>
          {loading ? 'Loading…' : 'Next Useless Fact ✨'}
        </button>

        <div className="play-actions">
          <button className="btn" onClick={onSave}>Save to My Museum</button>
          <button className="btn" onClick={onShare}>Share</button>
          <Link className="btn pink" to="/submit">Submit your own</Link>
        </div>

        <p className="play-hint">{hint}</p>
      </div>
    </section>
  )
}