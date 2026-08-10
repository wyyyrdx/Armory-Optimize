import Topbar from '../components/Topbar'
import { loadCollection, loadStats, weirdnessMeter } from '../utils/helpers'

const BADGES = [
  { id: 'first_save', icon: '💾', name: 'First Specimen', desc: 'Save your first fact', check: (s, c) => c.length >= 1 },
  { id: 'collector_5', icon: '📦', name: 'Hoarder Lite', desc: 'Save 5 facts', check: (s, c) => c.length >= 5 },
  { id: 'streak_10', icon: '⚡', name: 'Time Waster Pro', desc: 'Hit combo ×10', check: (s) => (s.maxStreak || 0) >= 10 },
  { id: 'meter_60', icon: '🤨', name: 'Professionally Confused', desc: 'Reach meter 60+', check: (s, c) => weirdnessMeter(c) >= 60 },
  { id: 'meter_86', icon: '☠️', name: 'Dangerously Unnecessary', desc: 'Reach meter 86+', check: (s, c) => weirdnessMeter(c) >= 86 },
  { id: 'submitter', icon: '✨', name: 'Contributor of Chaos', desc: 'Submit a fact', check: (s) => !!s.submitted },
]

export default function Badges() {
  const stats = loadStats()
  const col = loadCollection()
  const earned = new Set(BADGES.filter((b) => b.check(stats, col)).map((b) => b.id))

  return (
    <section className="view active">
      <Topbar />
      <div className="badges-panel">
        <h2>Badges & Stickers</h2>
        <p className="lead">Earn badges for peak uselessness.</p>
        <h3 className="section-title">Your Badges</h3>
        <div className="badges-grid">
          {BADGES.map((b) => (
            <div key={b.id} className={`badge-card ${earned.has(b.id) ? 'earned' : ''}`}>
              <div className="badge-icon">{b.icon}</div>
              <div className="badge-name">{b.name}</div>
              <div className="badge-desc">{b.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}