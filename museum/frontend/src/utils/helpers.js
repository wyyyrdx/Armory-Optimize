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

const REACTIONS_KEY = 'mouk_reactions_v1'

export function loadReactions() {
  try {
    return JSON.parse(localStorage.getItem(REACTIONS_KEY) || '{}')
  } catch {
    return {}
  }
}

export function setReaction(factId, emoji) {
  const reactions = loadReactions()

  if (reactions[factId] === emoji) {
    delete reactions[factId]
  } else {
    reactions[factId] = emoji
  }
  localStorage.setItem(REACTIONS_KEY, JSON.stringify(reactions))
  return reactions[factId] || null
}

const VISITOR_KEY = 'mouk_visitor_no_v1'

export function getVisitorNumber() {
  let n = localStorage.getItem(VISITOR_KEY)
  if (!n) {
    n = 3000 + Math.floor(Math.random() * 6000)
    localStorage.setItem(VISITOR_KEY, String(n))
  }
  return n
}

const STOPWORDS = new Set([
  'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'to', 'of', 'in', 'on',
  'and', 'or', 'but', 'than', 'then', 'that', 'this', 'it', 'its', "it's", 'their',
  'they', 'you', 'your', 'has', 'have', 'had', 'can', 'could', 'will', 'would',
  'for', 'with', 'at', 'by', 'as', 'so', 'not', 'no', 'do', 'does', 'did', 'more',
  'most', 'some', 'about', 'up', 'out', 'if', 'while', 'per', 'also',
])

export function videoSearchQueryForFact(fact) {
  if (!fact) return 'weird facts documentary'
  const tagWords = Array.isArray(fact.tags) ? fact.tags : []
  let words = tagWords.slice(0, 2)
  if (words.length < 2) {
    const fromText = (fact.fact || '')
      .replace(/[^a-zA-Z\s]/g, ' ')
      .split(/\s+/)
      .filter((w) => w.length > 3 && !STOPWORDS.has(w.toLowerCase()))
    for (const w of fromText) {
      if (words.length >= 2) break
      if (!words.includes(w)) words.push(w)
    }
  }
  const topic = words.join(' ') || (fact.category || 'weird facts')
  return `${topic} documentary weird facts`
}