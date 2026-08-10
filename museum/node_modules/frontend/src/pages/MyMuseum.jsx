import { useState } from 'react'
import Topbar from '../components/Topbar'
import {
  loadCollection,
  saveCollection,
  weirdnessMeter,
  titleForMeter,
  categoryEmoji,
} from '../utils/helpers'

export default function MyMuseum() {
  const [items, setItems] = useState(loadCollection())
  const meter = weirdnessMeter(items)

  function clearAll() {
    if (!confirm('Clear your entire museum?')) return
    saveCollection([])
    setItems([])
  }

  return (
    <section className="view active">
      <Topbar />
      <div className="museum-panel">
        <h2>My Museum</h2>
        <p className="lead">Your private collection of unnecessary knowledge.</p>

        <div className="meter-card">
          <div className="meter-label">Weirdness Meter</div>
          <div className="meter-value">{meter}</div>
          <div className="meter-track">
            <div className="meter-fill" style={{ width: `${meter}%` }} />
          </div>
          <div className="meter-title">{titleForMeter(meter)}</div>
          <p className="meter-sub">
            {items.length
              ? `${items.length} saved fact${items.length > 1 ? 's' : ''} shaping your rank.`
              : 'Save weird facts to raise your rank.'}
          </p>
        </div>

        <div className="collection-header">
          <h3>Saved exhibits ({items.length})</h3>
          {items.length > 0 && (
            <button className="btn" onClick={clearAll}>Clear</button>
          )}
        </div>

        <div className="collection-grid">
          {items.length === 0 && (
            <p className="empty-state">Nothing saved yet. Go play and hit Save.</p>
          )}
          {items.map((x) => (
            <div className="collection-card" key={x.id}>
              {x.fact}
              <div className="mini-meta">
                {categoryEmoji(x.category)} {x.category} · W {x.weirdness} · F {x.wtf}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}