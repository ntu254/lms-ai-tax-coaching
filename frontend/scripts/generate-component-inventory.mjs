import { readdir, writeFile } from 'node:fs/promises'
import path from 'node:path'

const source = path.resolve('src')
async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true })
  const lists = await Promise.all(entries.map(async entry => {
    const file = path.join(dir, entry.name)
    if (entry.isDirectory()) return walk(file)
    if (!entry.name.endsWith('.vue')) return []
    const relative = path.relative(source, file).split(path.sep).join('/')
    if (!relative.startsWith('components/') && !relative.includes('/components/')) return []
    return [{ name: entry.name.slice(0, -4), path: `src/${relative}`, group: relative.startsWith('components/') ? (relative.split('/')[1].endsWith('.vue') ? 'Chung' : relative.split('/')[1]) : relative.split('/').slice(0, 2).join('/') }]
  }))
  return lists.flat()
}
const items = (await walk(source)).sort((a, b) => a.path.localeCompare(b.path, 'en'))
await writeFile(path.join(source, 'component-inventory.json'), JSON.stringify(items, null, 2) + '\n')
console.log(`Component inventory: ${items.length} Vue files`)
