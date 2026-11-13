import { Link } from 'react-router-dom'
import { ArrowUpRight, Mail } from 'lucide-react'

const socials = [
  ['Instagram', import.meta.env.VITE_INSTAGRAM_URL],
  ['X / Twitter', import.meta.env.VITE_TWITTER_URL],
  ['YouTube', import.meta.env.VITE_YOUTUBE_URL],
]

export default function SiteFooter() {
  const email = import.meta.env.VITE_CONTACT_EMAIL
  return (
    <footer className="site-footer">
      <div className="footer-top">
        <Link to="/" className="footer-brand">
          <img src="/images/logo.png" alt="" />
          <span>DON’T LOOK<br /><b>BEHIND YOU</b></span>
        </Link>
        <p>Some memories should<br />never be remembered.</p>
        <div className="footer-links">
          <span className="eyebrow">FOLLOW THE SIGNAL</span>
          {socials.map(([name, url]) => url
            ? <a key={name} href={url} target="_blank" rel="noreferrer">{name}<ArrowUpRight size={13} /></a>
            : <span key={name} className="footer-muted">{name} <small>soon</small></span>)}
          {email && <a href={`mailto:${email}`}><Mail size={13} /> Contact</a>}
        </div>
      </div>
      <div className="footer-bottom">
        <span>© {new Date().getFullYear()} DON’T LOOK BEHIND YOU. All rights reserved.</span>
        <span>Created with care. Enter at your own risk.</span>
        <Link to="/privacy">Privacy</Link>
      </div>
    </footer>
  )
}
