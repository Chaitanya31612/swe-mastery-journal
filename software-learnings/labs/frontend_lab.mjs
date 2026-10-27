// Run: node frontend_lab.mjs. No network, browser, or packages needed.
import assert from 'node:assert/strict'

const order = []
order.push('A')
const timer = new Promise(resolve => setTimeout(() => { order.push('B'); resolve() }, 0))
Promise.resolve().then(() => order.push('C'))
order.push('D')
await timer
assert.deepEqual(order, ['A', 'D', 'C', 'B'])

function deferred() {
  let resolve
  const promise = new Promise(r => { resolve = r })
  return { promise, resolve }
}
let latest = 0
let rows = []
let loading = false
async function acceptLatest(response) {
  const identity = ++latest
  loading = true
  try {
    const data = await response
    if (identity === latest) rows = data
  } finally {
    if (identity === latest) loading = false
  }
}
const old = deferred(), current = deferred()
const oldRun = acceptLatest(old.promise)
const currentRun = acceptLatest(current.promise)
old.resolve(['old'])
await oldRun
assert.equal(loading, true, 'an old response must not clear current loading')
current.resolve(['current'])
await currentRun
assert.deepEqual(rows, ['current'])
assert.equal(loading, false)
console.log('Passed: event-loop order and latest-response/loading guards')
