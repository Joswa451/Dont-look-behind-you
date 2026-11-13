import { useCallback, useState } from 'react'
import { ArrowDown, ArrowDownToLine, ArrowRight, BookOpen, Eye, Heart, Layers3, Search, ShieldAlert, Split, Zap } from 'lucide-react'
import SectionHeading from '../components/SectionHeading.jsx'
import DownloadCenter from '../components/DownloadCenter.jsx'
import WindowsInstallGuide from '../components/WindowsInstallGuide.jsx'
import Lightbox from '../components/Lightbox.jsx'
import { characters, features, gallery } from '../data/site.js'

const featureIcons = { eye: Eye, split: Split, heart: Heart, search: Search, zap: Zap, layers: Layers3 }

function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-title">
      <div className="hero-image" />
      <div className="hero-grain" />
      <div className="hero-content page-shell">
        <div className="hero-kicker"><span className="status-dot" /> AN ANIME PSYCHOLOGICAL HORROR VISUAL NOVEL</div>
        <h1 id="hero-title">DON’T LOOK<br /><span data-text="BEHIND YOU">BEHIND YOU</span></h1>
        <p className="hero-tagline">Some memories should<br className="mobile-only" /> never be remembered.</p>
        <div className="hero-actions">
          <a className="button button-primary" href="#download"><ArrowDownToLine size={17} /> Download for Windows <span className="button-arrow">↗</span></a>
          <a className="button button-outline" href="#install"><BookOpen size={17} /> How to install</a>
        </div>
        <div className="hero-meta"><span>7 CHAPTERS</span><i /> <span>4 ENDINGS</span><i /> <span>ONE LAST CALL</span></div>
      </div>
      <a href="#about" className="scroll-cue" aria-label="Scroll to about the game"><span>SCROLL TO DESCEND</span><ArrowDown size={16} /></a>
      <div className="hero-side-note"><span>ASHGROVE STREET</span><span>3:00 AM</span></div>
    </section>
  )
}

function About() {
  return (
    <section id="about" className="section about-section">
      <div className="page-shell">
        <SectionHeading kicker="THE FILE" title={<>A home that<br /><em>remembers you.</em></>} number="01" />
        <div className="about-layout">
          <p className="about-lead">Ethan returns to the apartment he left as a child. At 3:00 AM, a photograph arrives from a number that does not exist. It shows him asleep.</p>
          <div className="about-copy"><p>Over seven nights, the rooms begin to open onto something older than memory. A neighbor leaves coffee at the door. A girl speaks through the walls. Somewhere, a phone keeps ringing.</p><p>Every clue points toward a promise Ethan cannot remember making—and a voice that has been waiting years for him to answer.</p></div>
        </div>
        <div className="fact-grid">
          <div><span>GENRE</span><strong>Psychological horror</strong></div>
          <div><span>FORMAT</span><strong>Choice-driven visual novel</strong></div>
          <div><span>PLAYTIME</span><strong>Approx. 2–3 hours</strong></div>
          <div><span>CHAPTERS</span><strong>Seven nights</strong></div>
          <div><span>ENDINGS</span><strong>Four possible endings</strong></div>
          <div><span>PLATFORM</span><strong>Windows 10 / 11</strong></div>
        </div>
        <p className="fact-note">64-bit Windows desktop edition. No separate Python or Ren’Py installation required.</p>
      </div>
    </section>
  )
}

function Story() {
  return (
    <section id="story" className="section story-section">
      <div className="story-backdrop" />
      <div className="page-shell story-shell">
        <SectionHeading kicker="THE STORY SO FAR" title={<>Seven nights.<br /><em>One unanswered call.</em></>} number="02" />
        <div className="story-body">
          <div className="story-image-wrap"><img src="/images/gallery/cg_girl_first.jpg" alt="A pale girl stands at the far end of a dark apartment hallway" loading="lazy" /><span className="image-index">FIG. 01 — THE HALLWAY</span></div>
          <div className="story-text"><span className="eyebrow">THE RETURN</span><p>You come back to Ashgrove Street with two suitcases and a key that feels older than you do.</p><p>The apartment is cheap. The neighbors are kind. The photographs are all turned face-down.</p><p>Then the phone rings at three in the morning. Someone says you promised to come back.</p><p className="story-final">You have seven days to remember why.</p><a className="text-link" href="#download">Get the Windows edition <ArrowRight size={15} /></a></div>
        </div>
        <div className="story-foot"><span>001 / A MEMORY WITH ITS FACE TURNED AWAY</span><span>ASHGROVE, 3B — RAINING</span></div>
      </div>
    </section>
  )
}

function Characters() {
  return (
    <section id="characters" className="section characters-section">
      <div className="page-shell">
        <SectionHeading kicker="WHO IS IN THE ROOM" title={<>Some faces are<br /><em>hard to forget.</em></>} text="You are not the only one who remembers." number="03" />
        <div className="character-grid">
          {characters.map((character, index) => (
            <article className={`character-card accent-${character.accent}`} key={character.name}>
              <div className="character-art"><span className="character-id">0{index + 1}</span><img src={character.image} alt={`${character.name} character illustration`} loading="lazy" /><span className="character-scan" /></div>
              <div className="character-info"><span className="eyebrow">{character.role}</span><h3>{character.name}</h3><p>{character.description}</p><span className="character-rule" /></div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

function Features() {
  return (
    <section id="features" className="section features-section">
      <div className="page-shell">
        <SectionHeading kicker="INSIDE THE APARTMENT" title={<>The quiet is<br /><em>part of the horror.</em></>} text="A story shaped by what you notice—and what you choose to do with it." number="04" />
        <div className="feature-grid">
          {features.map((feature) => {
            const Icon = featureIcons[feature.icon]
            return <article className="feature-card" key={feature.number}><div className="feature-top"><span>{feature.number} / 06</span><Icon size={22} strokeWidth={1.4} /></div><h3>{feature.title}</h3><p>{feature.text}</p><span className="feature-line" /></article>
          })}
        </div>
      </div>
    </section>
  )
}

function Gallery() {
  const [active, setActive] = useState(null)
  const change = useCallback((next) => setActive(next), [])
  const close = useCallback(() => setActive(null), [])
  return (
    <section id="gallery" className="section gallery-section">
      <div className="page-shell">
        <SectionHeading kicker="EVIDENCE LOG" title={<>A glimpse of<br /><em>what waits inside.</em></>} text="Captured from Ethan’s seven nights in Apartment 3B." number="05" />
        <div className="gallery-grid">
          {gallery.map((item, index) => <button className={`gallery-item gallery-item-${index % 5}`} key={item.src} type="button" onClick={() => setActive(index)} aria-label={`View ${item.title}`}><img src={item.src} alt={item.title} loading="lazy" /><span className="gallery-overlay"><small>{item.type} · {String(index + 1).padStart(2, '0')}</small><strong>{item.title}</strong><i>VIEW FRAME ↗</i></span></button>)}
        </div>
      </div>
      {active !== null && <Lightbox items={gallery} index={active} onChange={change} onClose={close} />}
    </section>
  )
}

function Downloads() {
  return (
    <section id="download" className="section download-section">
      <div className="download-backdrop" />
      <div className="page-shell download-shell">
        <SectionHeading kicker="WINDOWS DESKTOP EDITION" title={<>Take it<br /><em>with you.</em></>} text="A complete 64-bit Windows build for Windows 10 and Windows 11. Download, extract, and start the game." number="06" />
        <DownloadCenter />
        <p className="download-footnote"><ShieldAlert size={14} /> Unsigned Windows builds may show an unknown-publisher warning. Review the SHA-256 and troubleshooting notes below before running the game.</p>
      </div>
    </section>
  )
}

function Requirements() {
  return (
    <section id="requirements" className="section requirements-section">
      <div className="page-shell requirements-layout">
        <div><span className="eyebrow"><i /> RUNNING THE GAME</span><h2>System<br /><em>requirements.</em></h2><p>Baseline requirements for a Ren’Py visual novel, based on the packaged v1.0 desktop builds.</p></div>
        <div className="requirements-table" role="table" aria-label="System requirements">
          <div className="requirements-row requirements-head" role="row"><span role="columnheader">COMPONENT</span><span role="columnheader">MINIMUM</span><span role="columnheader">RECOMMENDED</span></div>
          <div className="requirements-row" role="row"><span>Operating system</span><span>Windows 10 64-bit</span><span>Windows 11 64-bit</span></div>
          <div className="requirements-row" role="row"><span>Processor</span><span>2.0 GHz, 64-bit</span><span>2.0 GHz, 64-bit</span></div>
          <div className="requirements-row" role="row"><span>Memory</span><span>2 GB RAM</span><span>4 GB RAM</span></div>
          <div className="requirements-row" role="row"><span>Graphics</span><span>OpenGL 3.0 / DirectX 11</span><span>Hardware accelerated graphics</span></div>
          <div className="requirements-row" role="row"><span>Storage</span><span>2 GB available space</span><span>2 GB available space</span></div>
        </div>
        <p className="requirements-note">These are baseline estimates; actual performance depends on your device and graphics drivers.</p>
      </div>
    </section>
  )
}

function WindowsPublishingSections() {
  return <WindowsInstallGuide />
}

export default function HomePage() {
  return <><Hero /><About /><Story /><Characters /><Features /><Gallery /><Downloads /><Requirements /><WindowsPublishingSections /></>
}
