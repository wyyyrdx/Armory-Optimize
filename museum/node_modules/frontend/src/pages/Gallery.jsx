import { useEffect, useState } from 'react'
import Topbar from '../components/Topbar'
import { getCategories, getExhibits } from '../api/client'
import { categoryEmoji } from '../utils/helpers'

export default function Gallery() {
  const [categories, setCategories] = useState([])
  const [category, setCategory] = useState('All')
  const [sort, setSort] = useState('weirdness')
  const [exhibits, setExhibits] = useState([])
  const [count, setCount] = useState(0)

  useEffect(() => {
    getCategories()
      .then((d) => setCategories(d.categories || []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    getExhibits({ category, sort })
      .then((d) => {
        setExhibits(d.exhibits || [])
        setCount(d.count || 0)
      })
      .catch(() => setExhibits([]))
  }, [category, sort])

  return (
    <section className="view active">
      <Topbar />

      <div className="category-bar">
        <button
          className={`filter-chip ${category === 'All' ? 'active' : ''}`}
          onClick={() => setCategory('All')}
        >
          🏛️ All
        </button>
        {categories.map((c) => (
          <button
            key={c.name}
            className={`filter-chip ${category === c.name ? 'active' : ''}`}
            onClick={() => setCategory(c.name)}
          >
            {c.emoji} {c.name}
          </button>
        ))}
      </div>

      <div className="gallery-toolbar">
        <span>{count} exhibits</span>
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="weirdness">Sort by Weirdness</option>
          <option value="wtf">Sort by Freak Factor</option>
          <option value="id">Sort by Exhibit #</option>
        </select>
      </div>

      <div className="gallery-feed">
        {exhibits.map((ex) => (
          <article className="feed-card" key={ex.id}>
            <div className="feed-id">Exhibit #{ex.id}</div>
            <div className="feed-fact">{categoryEmoji(ex.category)} {ex.fact}</div>
            <div className="feed-meta">
              <span className="pill">{categoryEmoji(ex.category)} {ex.category}</span>
              <span className="pill score">Weirdness {ex.weirdness}</span>
              <span className="pill score">Freak {ex.wtf}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}