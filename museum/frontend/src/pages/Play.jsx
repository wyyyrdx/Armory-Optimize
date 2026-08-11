import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Topbar from '../components/Topbar'
import FactCard from '../components/FactCard'
import { getRandom } from '../api/client'
import {
  addToCollection,
  loadStats,
  saveStats,
  loadReactions,
  setReaction,
  getVisitorNumber,
  videoSearchQueryForFact,
} from '../utils/helpers'

const REACTION_EMOJIS = ['😂', '🤯', '😐', '❤️']

export default function Play() {
  const [fact, setFact] = useState(null)
  const [streak, setStreak] = useState(0)
  const [hint, setHint] = useState('')
  const [loading, setLoading] = useState(false)
  const [reaction, setReactionState] = useState(null)
  const [visitorNo] = useState(getVisitorNumber)

  async function nextFact() {
    setLoading(true)
    setHint('')
    try {
      const data = await getRandom()
      setFact(data)
      setReactionState(loadReactions()[data.id] || null)
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

  function onReact(emoji) {
    if (!fact) return
    const result = setReaction(fact.id, emoji)
    setReactionState(result)
  }

  let streakMsg = ''
  if (streak >= 20) streakMsg = 'Terminal curiosity unlocked.'
  else if (streak >= 10) streakMsg = 'You are now officially wasting time efficiently.'
  else if (streak >= 5) streakMsg = 'Nice streak. Keep going.'

  const videoQuery = fact ? videoSearchQueryForFact(fact) : null

  return (
    <section className="view active">
      <Topbar />
      <div className="play-stage">
        <div className="streak-bar">
          <span id="streak-text">Combo ×{streak}</span>
          <span>{streakMsg}</span>
        </div>

        <FactCard fact={fact} />

        {/* Reaction buttons */}
        <div className="reaction-bar">
          {REACTION_EMOJIS.map((emoji) => (
            <button
              key={emoji}
              className={`reaction-btn ${reaction === emoji ? 'active' : ''}`}
              onClick={() => onReact(emoji)}
              disabled={!fact}
              aria-label={`React ${emoji}`}
            >
              {emoji}
            </button>
          ))}
        </div>

        <button className="btn primary large next-btn" onClick={nextFact} disabled={loading}>
          {loading ? 'Loading…' : 'Next Useless Fact ✨'}
        </button>

        <div className="play-actions">
          <button className="btn" onClick={onSave}>Save to My Museum</button>
          <button className="btn" onClick={onShare}>Share</button>
          <Link className="btn pink" to="/submit">Submit your own</Link>
        </div>

        <p className="play-hint">{hint}</p>

        {/* Related weird documentary video suggestion */}
        {videoQuery && (
          <div className="weird-video-block">
            <h3 className="section-title">🎥 Curious? Watch More About This</h3>
            <p className="hint-block">Real weird documentaries / facts videos related to this exhibit.</p>
            <a
              className="video-search-card"
              href={`https://www.youtube.com/results?search_query=${encodeURIComponent(videoQuery)}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <span className="video-search-icon">▶</span>
              <span className="video-search-text">
                Search YouTube: <strong>{videoQuery}</strong>
              </span>
            </a>
          </div>
        )}

        {/* Fake visitor counter */}
        <p className="visitor-counter">You are visitor #{visitorNo.toLocaleString()} to this museum. Congratulations, probably.</p>
      </div>
    </section>
  )
}
