import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { copyFileSync, mkdirSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import release from './src/data/release.json' with { type: 'json' }

function copyWindowsRelease() {
  return {
    name: 'copy-windows-release',
    apply: 'build',
    closeBundle() {
      const source = resolve(release.windows.archivePath)
      const downloadDirectory = resolve('dist/downloads')
      mkdirSync(downloadDirectory, { recursive: true })
      copyFileSync(source, resolve(downloadDirectory, basename(source)))
    },
  }
}

export default defineConfig({
  plugins: [react(), tailwindcss(), copyWindowsRelease()],
})
