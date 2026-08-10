export async function getRandom() {
  const res = await fetch('/api/random')
  if (!res.ok) throw new Error('Failed to load fact')
  return res.json()
}

export async function getExhibits({ category = 'All', sort = 'weirdness', limit = 200 } = {}) {
  const params = new URLSearchParams({ sort, limit })
  if (category && category !== 'All') params.set('category', category)
  const res = await fetch(`/api/exhibits?${params}`)
  if (!res.ok) throw new Error('Failed to load exhibits')
  return res.json()
}

export async function getCategories() {
  const res = await fetch('/api/categories')
  if (!res.ok) throw new Error('Failed to load categories')
  return res.json()
}

export async function classifyFact(fact) {
  const res = await fetch('/api/classify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fact }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Classification failed')
  }
  return res.json()
}

export async function getArmBenchmarks() {
  const res = await fetch('/api/arm/benchmarks')
  if (!res.ok) throw new Error('Failed to load benchmarks')
  return res.json()
}