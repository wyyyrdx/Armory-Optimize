import { useEffect, useState } from 'react'
import Topbar from '../components/Topbar'
import { getArmBenchmarks } from '../api/client'

export default function Arm() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getArmBenchmarks().then(setData).catch(() => {})
  }, [])

  return (
    <section className="view active">
      <Topbar />
      <div className="arm-panel">
        <h2>The Engine Behind the Museum</h2>
        <p className="lead">
          Every exhibit is classified by a lightweight pipeline. The original Arm64 optimization work lives in the same repo.
        </p>

        <div className="bench-grid">
          {(data?.results || []).map((r, i) => (
            <div key={i} className={`bench-card ${r.highlight ? 'highlight' : ''}`}>
              <div>
                <div className="backend">{r.backend}</div>
                <div className="arch">
                  {r.arch}{r.model_size_mb ? ` · ${r.model_size_mb} MB` : ''}
                </div>
              </div>
              <div className="metric">
                <span className="num">{r.latency_ms}</span>
                <span className="label">ms latency</span>
              </div>
              <div className="metric">
                <span className="num">{r.throughput_rps}</span>
                <span className="label">req/s</span>
              </div>
            </div>
          ))}
        </div>

        {data?.honest_finding && (
          <blockquote className="honest">
            <strong>Honest finding:</strong> {data.honest_finding}
          </blockquote>
        )}
      </div>
    </section>
  )
}