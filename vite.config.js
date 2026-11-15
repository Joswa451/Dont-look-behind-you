import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { copyFileSync, mkdirSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import release from './src/data/release.json' with { type: 'json' }

function copyReleaseArchives() {
  return {
    name: 'copy-release-archives',
    apply: 'build',
    closeBundle() {
      const downloadDirectory = resolve('dist/downloads')
      mkdirSync(downloadDirectory, { recursive: true })
      for (const archive of [release.windows, release.android]) {
        const source = resolve(archive.archivePath)
        copyFileSync(source, resolve(downloadDirectory, basename(source)))
      }
    },
  }
}

export default defineConfig({
  plugins: [react(), tailwindcss(), copyReleaseArchives()],
})
