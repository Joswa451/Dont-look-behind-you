import { useState } from 'react'
import { ArrowDownToLine, Check, CircleAlert } from 'lucide-react'
import { release } from '../data/site.js'
import { isSameOrigin, safeDownloadUrl } from '../data/urlValidation.js'

function WindowsLogo() {
  return (
    <svg viewBox="0 0 24 24" role="img" aria-label="Windows" width="22" height="22">
      <path fill="currentColor" d="M2 4.7 10.8 3.5v7.9H2V4.7Zm9.8-1.4L22 2v9.4H11.8V3.3ZM2 12.4h8.8v7.9L2 19.1v-6.7Zm9.8 0H22v9.4l-10.2-1.4v-8Z" />
    </svg>
  )
}

export default function DownloadCenter() {
  const [status, setStatus] = useState('')
  const target = safeDownloadUrl(release.windows.downloadUrl, window.location.origin)
  const sameOrigin = target && isSameOrigin(target, window.location.origin)

  return (
    <article className={`windows-release-card ${target ? 'is-ready' : 'is-unavailable'}`}>
      <div className="windows-release-art" aria-hidden="true">
        <div className="windows-eye"><img src="/favicon.svg" alt="" /></div>
        <span className="windows-release-edition">WINDOWS DESKTOP EDITION</span>
        <span className="windows-release-version">VERSION {release.version}</span>
      </div>
      <div className="windows-release-details">
        <div className="download-card-head">
          <div className="platform-icon"><WindowsLogo /></div>
          <span className={target ? 'availability available' : 'availability'}><i />{target ? 'READY TO DOWNLOAD' : 'NOT YET AVAILABLE'}</span>
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
        {target ? (
          <a className="button button-download windows-download-button" href={target} download={sameOrigin ? true : undefined} target={sameOrigin ? undefined : '_blank'} rel={sameOrigin ? undefined : 'noreferrer'} onClick={() => setStatus('Download started. Check your browser’s downloads.') }>
            <ArrowDownToLine size={19} /> DOWNLOAD FOR WINDOWS <span>↗</span>
          </a>
        ) : (
          <button className="button button-disabled windows-download-button" type="button" disabled><CircleAlert size={17} /> WINDOWS DOWNLOAD UNAVAILABLE</button>
        )}
        {release.windows.sha256 && <p className="windows-checksum"><b>SHA-256</b><code>{release.windows.sha256}</code></p>}
        {status && <p className="download-status" role="status"><Check size={14} />{status}</p>}
      </div>
    </article>
  )
}
