import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowDownToLine, Check, CircleAlert, Gamepad2, Globe2 } from 'lucide-react'
import { release } from '../data/site.js'
import { isSameOrigin, safeDownloadUrl, safeWebPlayerUrl } from '../data/urlValidation.js'

function WindowsLogo() {
  return (
    <svg viewBox="0 0 24 24" role="img" aria-label="Windows" width="22" height="22">
      <path fill="currentColor" d="M2 4.7 10.8 3.5v7.9H2V4.7Zm9.8-1.4L22 2v9.4H11.8V3.3ZM2 12.4h8.8v7.9L2 19.1v-6.7Zm9.8 0H22v9.4l-10.2-1.4v-8Z" />
    </svg>
  )
}

function AndroidLogo() {
  return (
    <svg viewBox="0 0 24 24" role="img" aria-label="Android" width="23" height="23">
      <path fill="currentColor" d="M7.2 6.5h9.6c.7 0 1.2.5 1.2 1.2v7.1c0 .7-.5 1.2-1.2 1.2h-.8v2.8c0 .7-.5 1.2-1.2 1.2s-1.2-.5-1.2-1.2V16H10v2.8c0 .7-.5 1.2-1.2 1.2S7.6 19.5 7.6 18.8V16h-.4c-.7 0-1.2-.5-1.2-1.2V7.7c0-.7.5-1.2 1.2-1.2Zm-2.4.1c.6 0 1.1.5 1.1 1.1v5.6c0 .6-.5 1.1-1.1 1.1S3.7 13.9 3.7 13.3V7.7c0-.6.5-1.1 1.1-1.1Zm14.4 0c.6 0 1.1.5 1.1 1.1v5.6c0 .6-.5 1.1-1.1 1.1s-1.1-.5-1.1-1.1V7.7c0-.6.5-1.1 1.1-1.1ZM8.6 2.4l.8 1.4c.3-.1.7-.1 1-.1h3.2c.3 0 .7 0 1 .1l.8-1.4c.1-.2.4-.3.6-.2.2.1.3.4.2.6l-.8 1.5c1.1.5 1.9 1.4 2.1 2.5H5.5c.2-1.1 1-2 2.1-2.5L6.8 2.8c-.1-.2 0-.5.2-.6.2-.1.5 0 .6.2ZM8.5 5c-.4 0-.7.3-.7.7s.3.7.7.7.7-.3.7-.7S8.9 5 8.5 5Zm7 0c-.4 0-.7.3-.7.7s.3.7.7.7.7-.3.7-.7-.3-.7-.7-.7Z" />
    </svg>
  )
}

function ReleaseChecksum({ value }) {
  if (!value) return null
  return <p className="windows-checksum"><b>SHA-256</b><code>{value}</code></p>
}

export default function DownloadCenter() {
  const [status, setStatus] = useState({ platform: '', message: '' })
  const windowsTarget = safeDownloadUrl(release.windows.downloadUrl, window.location.origin)
  const androidTarget = safeDownloadUrl(release.android.downloadUrl, window.location.origin)
  const webTarget = safeWebPlayerUrl(release.webUrl, window.location.origin)
  const windowsSameOrigin = windowsTarget && isSameOrigin(windowsTarget, window.location.origin)
  const androidSameOrigin = androidTarget && isSameOrigin(androidTarget, window.location.origin)

  const downloadProps = (target, sameOrigin) => ({
    href: target,
    download: sameOrigin ? true : undefined,
    target: sameOrigin ? undefined : '_blank',
    rel: sameOrigin ? undefined : 'noreferrer',
  })

  return (
    <div className="release-options">
      <article className={`windows-release-card ${windowsTarget ? 'is-ready' : 'is-unavailable'}`}>
        <div className="windows-release-art" aria-hidden="true">
          <div className="windows-eye"><img src="/favicon.svg" alt="" /></div>
          <span className="windows-release-edition">WINDOWS DESKTOP EDITION</span>
          <span className="windows-release-version">VERSION {release.version}</span>
        </div>
        <div className="windows-release-details">
          <div className="download-card-head">
            <div className="platform-icon"><WindowsLogo /></div>
            <span className={windowsTarget ? 'availability available' : 'availability'}><i />{windowsTarget ? 'READY TO DOWNLOAD' : 'NOT YET AVAILABLE'}</span>
          </div>
          <h3>{release.title}</h3>
          <p className="download-copy">Windows Desktop Edition</p>
          <dl className="release-meta windows-release-meta">
            <div><dt>VERSION</dt><dd>{release.version}</dd></div>
            <div><dt>ARCHITECTURE</dt><dd>{release.architecture}</dd></div>
            <div><dt>FILE FORMAT</dt><dd>{release.format}</dd></div>
            <div><dt>FILE SIZE</dt><dd>{release.windows.fileSize}</dd></div>
            <div><dt>SUPPORTED OS</dt><dd>{release.supportedOS}</dd></div>
          </dl>
          {windowsTarget ? (
            <a className="button button-download windows-download-button" {...downloadProps(windowsTarget, windowsSameOrigin)} onClick={() => setStatus({ platform: 'windows', message: 'Windows download started. Check your browser’s downloads.' })}>
              <ArrowDownToLine size={19} /> DOWNLOAD FOR WINDOWS <span>↗</span>
            </a>
          ) : (
            <button className="button button-disabled windows-download-button" type="button" disabled><CircleAlert size={17} /> WINDOWS DOWNLOAD UNAVAILABLE</button>
          )}
          <ReleaseChecksum value={release.windows.sha256} />
          {status.platform === 'windows' && <p className="download-status" role="status"><Check size={14} />{status.message}</p>}
        </div>
      </article>

      <div className="platform-choice-grid">
        <article id="android-download" className={`platform-card ${androidTarget ? 'is-ready' : 'is-unavailable'}`}>
          <div className="download-card-head">
            <div className="platform-icon"><AndroidLogo /></div>
            <span className={androidTarget ? 'availability available' : 'availability'}><i />{androidTarget ? 'READY TO INSTALL' : 'NOT YET AVAILABLE'}</span>
          </div>
          <span className="platform-edition">ANDROID MOBILE EDITION</span>
          <h3>Take Ashgrove<br /><em>with you.</em></h3>
          <p className="download-copy">Universal APK for Android phones and tablets.</p>
          <dl className="release-meta platform-meta">
            <div><dt>VERSION</dt><dd>{release.version}</dd></div>
            <div><dt>FILE FORMAT</dt><dd>{release.android.format}</dd></div>
            <div><dt>FILE SIZE</dt><dd>{release.android.fileSize}</dd></div>
            <div><dt>MINIMUM</dt><dd>{release.android.minimumOS}</dd></div>
            <div><dt>ORIENTATION</dt><dd>{release.android.orientation}</dd></div>
            <div><dt>ARCHITECTURE</dt><dd>{release.android.architecture}</dd></div>
          </dl>
          {androidTarget ? (
            <a className="button button-download windows-download-button" {...downloadProps(androidTarget, androidSameOrigin)} onClick={() => setStatus({ platform: 'android', message: 'Android download started. Follow the six-step install guide below.' })}>
              <ArrowDownToLine size={19} /> DOWNLOAD ANDROID APK <span>↗</span>
            </a>
          ) : (
            <button className="button button-disabled windows-download-button" type="button" disabled><CircleAlert size={17} /> ANDROID DOWNLOAD UNAVAILABLE</button>
          )}
          <ReleaseChecksum value={release.android.sha256} />
          {status.platform === 'android' && <p className="download-status" role="status"><Check size={14} />{status.message}</p>}
          <p className="platform-note">Android may ask you to allow installs from your browser or file manager. Only install the APK from this official page, and never disable Play Protect.</p>
          <a className="text-link platform-guide-link" href="#android-install">See the six-step install guide</a>
        </article>

        <article className={`platform-card play-online-card ${webTarget ? 'is-ready' : 'is-unavailable'}`}>
          <div className="download-card-head">
            <div className="platform-icon"><Globe2 size={22} /></div>
            <span className={webTarget ? 'availability available' : 'availability'}><i />{webTarget ? 'WEB BUILD ONLINE' : 'COMING SOON'}</span>
          </div>
          <span className="platform-edition">BROWSER EDITION</span>
          <h3>Play online.<br /><em>No download.</em></h3>
          <p className="download-copy">A browser-ready Ren’Py Web build.</p>
          <div className="web-signal" aria-hidden="true"><Gamepad2 size={30} /><span>03:00 AM</span><i /></div>
          {webTarget ? (
            <Link className="button button-download windows-download-button" to="/play">
              <Gamepad2 size={19} /> PLAY IN BROWSER <span>↗</span>
            </Link>
          ) : (
            <button className="button button-disabled windows-download-button" type="button" disabled><CircleAlert size={17} /> BROWSER BUILD COMING SOON</button>
          )}
          <p className="platform-note">Play Online becomes available only when a working, browser-ready Ren’Py Web build is configured. Desktop and Android files cannot be played in the browser.</p>
        </article>
      </div>
    </div>
  )
}
