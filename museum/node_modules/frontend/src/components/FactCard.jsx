import { categoryEmoji } from '../utils/helpers'

export default function FactCard({ fact }) {
  if (!fact) return null
  return (
    <div className="fact-card">
      <div className="fact-card-id">Exhibit #{fact.id}</div>
      <div className="fact-card-emoji">{categoryEmoji(fact.category)}</div>
      <h1 className="fact-card-text">{fact.fact}</h1>
      <div className="fact-card-meta">
        <span className="pill">{categoryEmoji(fact.category)} {fact.category}</span>
        <span className="pill score">Weirdness {fact.weirdness}</span>
        <span className="pill score">Freak {fact.wtf}</span>
      </div>
    </div>
  )
}