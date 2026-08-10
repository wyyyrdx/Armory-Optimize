export function categoryEmoji(cat) {
  const map = {
    Nature: '🦎',
    Human: '🧠',
    History: '🏺',
    Space: '🌌',
    Science: '🔬',
    'Why Does This Exist?': '🤨',
    Animals: '🐙',
    Earth: '🌍',
    Technology: '💻',
    'Random / Other': '🎲',
  }
  return map[cat] || '🎲'
}

const KEY = 'mouk_collection_v1'
const STATS_KEY = 'mouk_stats_v1'

export function loadCollection() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]')
  } catch {
    return []
  }
}

export function saveCollection(items) {
  localStorage.setItem(KEY, JSON.stringify(items))
}

export function addToCollection(fact) {
  const items = loadCollection()
  if (items.some((x) => x.id === fact.id)) return false
  items.unshift(fact)
  saveCollection(items)
  return true
}

export function weirdnessMeter(items) {
  if (!items.length) return 0
  const avg = items.reduce((s, x) => s + (x.weirdness || 0), 0) / items.length
  const volume = Math.min(20, items.length * 2)
  return Math.round(Math.min(100, avg * 0.8 + volume))
}

export function titleForMeter(m) {
  if (m >= 86) return 'Dangerously Unnecessary'
  if (m >= 61) return 'Certified Oddity'
  if (m >= 31) return 'Professionally Confused'
  return 'Mildly Curious'
}

export function loadStats() {
  try {
    return JSON.parse(localStorage.getItem(STATS_KEY) || '{}')
  } catch {
    return {}
  }
}

export function saveStats(s) {
  localStorage.setItem(STATS_KEY, JSON.stringify(s))
}