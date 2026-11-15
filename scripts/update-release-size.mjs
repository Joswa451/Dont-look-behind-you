import { createHash } from 'node:crypto'
import { readFile, writeFile } from 'node:fs/promises'
import { resolve } from 'node:path'

const manifestPath = resolve('src/data/release.json')
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'))

for (const platform of ['windows', 'android']) {
  const archive = await readFile(resolve(manifest[platform].archivePath))
  const mib = archive.byteLength / (1024 * 1024)
  manifest[platform].fileSize = `${mib.toFixed(1)} MiB`
  manifest[platform].sha256 = createHash('sha256').update(archive).digest('hex')

  const label = platform === 'windows' ? 'Windows' : 'Android'
  console.log(`${label} release metadata: ${manifest[platform].fileSize}, SHA-256 ${manifest[platform].sha256}`)
}

await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`)
