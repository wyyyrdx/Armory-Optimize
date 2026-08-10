import { Routes, Route } from 'react-router-dom'
import Entrance from './pages/Entrance'
import Play from './pages/Play'
import Gallery from './pages/Gallery'
import MyMuseum from './pages/MyMuseum'
import Badges from './pages/Badges'
import Submit from './pages/Submit'
import Arm from './pages/Arm'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Entrance />} />
      <Route path="/play" element={<Play />} />
      <Route path="/gallery" element={<Gallery />} />
      <Route path="/museum" element={<MyMuseum />} />
      <Route path="/badges" element={<Badges />} />
      <Route path="/submit" element={<Submit />} />
      <Route path="/arm" element={<Arm />} />
    </Routes>
  )
}