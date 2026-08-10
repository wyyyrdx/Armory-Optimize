import { Link } from 'react-router-dom'

export default function Topbar() {
  return (
    <nav className="topbar">
      <Link to="/" className="logo">Museum of Useless Knowledge</Link>
      <div className="topbar-links">
        <Link to="/play">Random</Link>
        <Link to="/gallery">Gallery</Link>
        <Link to="/museum">My Museum</Link>
        <Link to="/badges">Badges</Link>
        <Link to="/submit">Submit</Link>
        <Link to="/arm">Arm</Link>
      </div>
    </nav>
  )
}