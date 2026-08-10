import { Link } from 'react-router-dom'

export default function Entrance() {
  return (
    <section id="view-entrance" className="view active entrance">
      <span className="deco d1">🐙</span>
      <span className="deco d2">⭐</span>
      <span className="deco d3">🍌</span>
      <span className="deco d4">💫</span>
      <span className="deco d5">🐸</span>
      <span className="deco d6">❤️</span>

      <header className="entrance-header">
        <img src="/logo.svg" alt="Museum mascot" className="site-logo" />
        <p className="eyebrow">Arm Create · Cloud AI · 2026</p>
        <h1>Museum of<br />Useless Knowledge</h1>
        <p className="tagline">Facts you absolutely did not need to know.</p>
        <p className="sub">Powered by Waad · Optimized for Arm · Completely unnecessary.</p>

        <div className="entrance-actions">
          <Link className="btn primary" to="/play">Enter Museum</Link>
          <Link className="btn pink" to="/play">Random Exhibit</Link>
          <Link className="btn ghost" to="/submit">Submit a Fact</Link>
        </div>

        <nav className="entrance-nav">
          <Link to="/gallery">Browse All Exhibits</Link>
          <Link to="/museum">My Collection</Link>
          <Link to="/badges">Badges & Stickers</Link>
          <Link to="/arm">Arm Performance</Link>
        </nav>
      </header>
    </section>
  )
}