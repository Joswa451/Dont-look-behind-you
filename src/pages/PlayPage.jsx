import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle, ArrowLeft, Expand, Gamepad2, MonitorPlay, RotateCw } from 'lucide-react'
import { release } from '../data/site.js'
import { safeWebPlayerUrl } from '../data/urlValidation.js'

export default function PlayPage() {
  const url = safeWebPlayerUrl(release.webUrl, window.location.origin)
  const [loaded, setLoaded] = useState(false)
  const [fullscreenError, setFullscreenError] = useState('')
  useEffect(() => { document.title = 'Play Online — DON’T LOOK BEHIND YOU' }, [])

  const fullscreen = async () => {
    const frame = document.querySelector('#renpy-player')
    try {
      if (!frame) return
      if (frame.requestFullscreen) await frame.requestFullscreen()
      else setFullscreenError('Fullscreen is not supported in this browser.')
    } catch {
      setFullscreenError('Your browser blocked fullscreen. Use the player’s own fullscreen control instead.')
    }
  }

  return (
    <section className="play-page">
      <div className="play-backdrop" />
      <div className="page-shell play-shell">
        <Link to="/#download" className="back-link"><ArrowLeft size={15} /> Back to the case file</Link>
        <div className="play-heading"><span className="eyebrow"><i /> WEB PLAYER</span><h1>Don’t look<br /><em>behind you.</em></h1><p>The browser version runs a dedicated Ren’Py Web build. Desktop downloads cannot run inside this player.</p></div>
        <div className={`player-frame ${url ? 'player-connected' : ''}`}>
          {!url ? (
            <div className="player-empty"><div className="player-icon"><Gamepad2 size={31} /></div><span className="eyebrow">SIGNAL NOT FOUND</span><h2>The browser build<br />isn’t connected yet.</h2><p>Set <code>VITE_RENPY_WEB_URL</code> to the public URL of the Ren’Py Web build, then rebuild the site. It must point to a browser-ready HTML player, not a Windows or Linux archive.</p><Link to="/#download" className="text-link">Check desktop downloads <ArrowLeft size={14} /></Link></div>
          ) : <>
            {!loaded && <div className="player-loading" role="status"><span className="loader-ring" /><strong>Connecting to Ashgrove…</strong><small>Loading the browser build</small></div>}
            <iframe id="renpy-player" title="DON'T LOOK BEHIND YOU browser game" src={url} allow="autoplay; fullscreen; gamepad" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" onLoad={() => setLoaded(true)} />
          </>}
        </div>
        <div className="player-controls"><span><MonitorPlay size={15} /> For the best experience, use a current desktop browser with hardware acceleration enabled.</span>{url && <button className="player-tool" onClick={fullscreen}><Expand size={15} /> Fullscreen</button>}</div>
        {fullscreenError && <p className="inline-error" role="status"><AlertTriangle size={15} />{fullscreenError}</p>}
        {url && <p className="browser-note"><RotateCw size={14} /> If the player stays blank, check that the configured Web build allows iframe embedding and is served over HTTPS.</p>}
      </div>
    </section>
  )
}
