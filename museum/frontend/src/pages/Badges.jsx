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

const STICKERS = [
  { art: '🐙', label: '3 Hearts Club', sub: 'Octopus energy' },
  { art: '🍌', label: 'Berry Identity Crisis', sub: 'Botanically confusing' },
  { art: '🐢', label: 'Butt Breathing Unit', sub: 'Certified unnecessary' },
  { art: '🧊', label: 'Cube Poop Society', sub: 'Wombat approved' },
  { art: '🌌', label: 'Venus Day Shift', sub: 'Time is fake' },
  { art: '⚡', label: 'Arm Optimized', sub: '12.98 ms energy' },
  { art: '🎲', label: 'Useless & Proud', sub: 'Museum member' },
  { art: '🤨', label: 'Why Does This Exist?', sub: 'Valid question' },
]

function downloadSticker(s) {
  const canvas = document.createElement('canvas')
  canvas.width = 512
  canvas.height = 512
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#fff8e7'
  ctx.fillRect(0, 0, 512, 512)
  ctx.strokeStyle = '#1a1030'
  ctx.lineWidth = 16
  ctx.strokeRect(12, 12, 488, 488)
  ctx.setLineDash([14, 10])
  ctx.lineWidth = 4
  ctx.strokeRect(36, 36, 440, 440)
  ctx.setLineDash([])
  ctx.font = '120px serif'
  ctx.textAlign = 'center'
  ctx.fillText(s.art, 256, 220)
  ctx.fillStyle = '#1a1030'
  ctx.font = 'bold 32px sans-serif'
  ctx.fillText(s.label, 256, 320)
  ctx.font = '20px sans-serif'
  ctx.fillStyle = '#5a4f70'
  ctx.fillText(s.sub, 256, 360)
  ctx.font = '16px sans-serif'
  ctx.fillStyle = '#1e6bff'
  ctx.fillText('Museum of Useless Knowledge', 256, 460)
  const a = document.createElement('a')
  a.download = `mouk-sticker-${s.label.toLowerCase().replace(/\s+/g, '-')}.png`
  a.href = canvas.toDataURL('image/png')
  a.click()
}

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
        <h3 className="section-title">Printable Stickers</h3>
        <p className="hint-block">Click a sticker to download it as an image-ready card. Print, cut, cause mild confusion.</p>
        <div className="stickers-grid">
          {STICKERS.map((s) => (
            <div key={s.label} className="sticker" onClick={() => downloadSticker(s)}>
              <div className="sticker-art">{s.art}</div>
              <div className="sticker-label">{s.label}</div>
              <div className="sticker-sub">{s.sub}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}