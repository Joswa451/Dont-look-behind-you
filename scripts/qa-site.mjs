import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'
import React from 'react'
import { renderToString } from 'react-dom/server'
import { StaticRouter } from 'react-router'
import { createServer } from 'vite'
import { isSameOrigin, safeDownloadUrl, safeWebPlayerUrl } from '../src/data/urlValidation.js'

globalThis.window = { location: { origin: 'https://site.test' } }

const server = await createServer({
  configFile: './vite.config.js',
  server: { middlewareMode: true, ws: false },
  appType: 'custom',
})

try {
  const { AppRoutes } = await server.ssrLoadModule('/src/App.jsx')
  const { default: Lightbox } = await server.ssrLoadModule('/src/components/Lightbox.jsx')
  const { default: DownloadCenter } = await server.ssrLoadModule('/src/components/DownloadCenter.jsx')

  const renderRoute = (path) => renderToString(
    React.createElement(StaticRouter, { location: path }, React.createElement(AppRoutes)),
  )

  const home = renderRoute('/')
  assert.match(home, /Some memories should/)
  assert.match(home, /Psychological horror/)
  assert.match(home, /href="\/#download"/)
  assert.equal((home.match(/aria-label="View /g) || []).length, 12, 'all gallery cards render')
  assert.match(home, /href="https:\/\/site\.test\/downloads\/DontLookBehindYou-Windows-v1\.0\.1\.zip"/, 'Windows archive is available')
  assert.match(home, /href="https:\/\/site\.test\/downloads\/DontLookBehindYou-Android-v1\.0\.1\.apk"/, 'Android APK is available')
  assert.match(home, /DOWNLOAD FOR WINDOWS/)
  assert.match(home, /DOWNLOAD ANDROID APK/)
  assert.match(home, /Play online\./)
  assert.match(home, /BROWSER BUILD COMING SOON/)
  assert.match(home, /Allowing this source|Allow this source/)
  assert.match(home, /SIX STEPS TO THE FIRST NIGHT/)
  assert.match(home, /do not turn Play Protect off/)
  assert.match(home, /Windows 10 \/ Windows 11/)
  assert.match(home, /Extract All/)
  assert.match(home, /DontLookBehindYou\.exe/)
  assert.ok(existsSync('release/windows/DontLookBehindYou-Windows-v1.0.1.zip'), 'Windows release archive exists')
  assert.ok(existsSync('release/android/DontLookBehindYou-Android-v1.0.1.apk'), 'Android release APK exists')
  assert.ok(existsSync('dist/downloads/DontLookBehindYou-Windows-v1.0.1.zip'), 'Windows release is copied into dist')
  assert.ok(existsSync('dist/downloads/DontLookBehindYou-Android-v1.0.1.apk'), 'Android release is copied into dist')
  assert.ok(existsSync('dist/images/bg_menu.jpg'), 'installation illustration background exists in production')
  assert.ok(existsSync('dist/favicon.svg'), 'Windows icon illustration exists in production')
  const siteData = readFileSync('src/data/site.js', 'utf8')
  const images = [...siteData.matchAll(/['"](\/images\/[^'"]+)['"]/g)].map(([, image]) => image)
  assert.ok(images.length > 0, 'site has image assets')
  for (const image of images) {
    assert.ok(existsSync(`public${image}`), `public asset exists: ${image}`)
    assert.ok(existsSync(`dist${image}`), `production asset exists: ${image}`)
  }
  console.log('PASS / — home, 12 gallery cards, Windows/Android releases, Play Online state, metadata, and install guides')

  const play = renderRoute('/play')
  assert.doesNotMatch(play, /SIGNAL NOT FOUND/)
  assert.doesNotMatch(play, /<iframe\b/)
  console.log('PASS /play — legacy path no longer displays the disconnected player')

  const privacy = renderRoute('/privacy')
  assert.match(privacy, /Privacy/)
  assert.match(privacy, /What this site collects/)
  console.log('PASS /privacy — privacy route renders')

  const unknown = renderRoute('/unrecognized-path')
  assert.match(unknown, /THE FILE/)
  console.log('PASS unknown route — returns to the home page')

  const lightbox = renderToString(React.createElement(Lightbox, {
    items: [{ src: '/image.jpg', title: 'Test frame', type: 'STORY CG' }],
    index: 0,
    onClose: () => {},
    onChange: () => {},
  }))
  for (const control of ['Close image preview', 'Previous image', 'Next image']) {
    assert.ok(lightbox.includes(control), `lightbox exposes ${control}`)
  }
  console.log('PASS gallery lightbox — close and previous/next controls render')

  const configuredDownload = renderToString(React.createElement(DownloadCenter))
  assert.match(configuredDownload, /href="https:\/\/site\.test\/downloads\/DontLookBehindYou-Windows-v1\.0\.1\.zip"/)
  assert.match(configuredDownload, /href="https:\/\/site\.test\/downloads\/DontLookBehindYou-Android-v1\.0\.1\.apk"/)
  assert.match(configuredDownload, /Windows Desktop Edition/)
  assert.match(configuredDownload, /ANDROID MOBILE EDITION/)
  assert.match(configuredDownload, /BROWSER BUILD COMING SOON/)
  assert.equal(safeDownloadUrl('javascript:alert(1)', 'https://site.test'), '')
  assert.equal(safeWebPlayerUrl('https://files.example/game.zip', 'https://site.test'), '')
  assert.equal(safeWebPlayerUrl('https://files.example/game.apk', 'https://site.test'), '')
  assert.equal(safeWebPlayerUrl('https://files.example/web/index.html', 'https://site.test'), 'https://files.example/web/index.html')
  assert.equal(isSameOrigin('/downloads/game.zip', 'https://site.test'), true)
  console.log('PASS configured links — valid archives work; unsafe schemes and desktop files are rejected for web play')
} finally {
  await server.close()
  delete globalThis.window
}
