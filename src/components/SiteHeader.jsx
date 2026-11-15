import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Menu, X } from 'lucide-react'

const links = [
  ['About', '/#about'],
  ['Story', '/#story'],
  ['Characters', '/#characters'],
  ['Gallery', '/#gallery'],
  ['Download', '/#download'],
]

export default function SiteHeader() {
  const [open, setOpen] = useState(false)
  const close = () => setOpen(false)

  return (
    <header className="site-header">
      <div className="header-inner">
        <Link to="/" className="brand" aria-label="Don't Look Behind You home" onClick={close}>
          <img src="/images/logo.png" alt="" className="brand-mark" />
          <span className="brand-name">DON’T LOOK<br /><b>BEHIND YOU</b></span>
        </Link>
        <button className="mobile-menu-button" type="button" aria-label={open ? 'Close navigation' : 'Open navigation'} aria-expanded={open} onClick={() => setOpen(!open)}>
          {open ? <X size={21} /> : <Menu size={21} />}
        </button>
        <nav className={`main-nav ${open ? 'is-open' : ''}`} aria-label="Main navigation">
          {links.map(([label, href]) => <a href={href} key={label} onClick={close}>{label}</a>)}
          <a href="/#download" className="nav-play" onClick={close}>Download the game <span aria-hidden="true">↗</span></a>
        </nav>
      </div>
    </header>
  )
}
