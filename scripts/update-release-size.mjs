import { createHash } from 'node:crypto'
import { readFile, writeFile } from 'node:fs/promises'
import { resolve } from 'node:path'

const manifestPath = resolve('src/data/release.json')
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'))
const archivePath = resolve(manifest.windows.archivePath)
const archive = await readFile(archivePath)
const mib = archive.byteLength / (1024 * 1024)
manifest.windows.fileSize = `${mib.toFixed(1)} MiB`
manifest.windows.sha256 = createHash('sha256').update(archive).digest('hex')
await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`)
console.log(`Windows release metadata: ${manifest.windows.fileSize}, SHA-256 ${manifest.windows.sha256}`)
