import { useEffect } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import SiteHeader from './components/SiteHeader.jsx'
import SiteFooter from './components/SiteFooter.jsx'
import HomePage from './pages/HomePage.jsx'
import PrivacyPage from './pages/PrivacyPage.jsx'
import PlayPage from './pages/PlayPage.jsx'
import { release } from './data/site.js'
import { safeWebPlayerUrl } from './data/urlValidation.js'

function ScrollManager() {
  const location = useLocation()
  useEffect(() => {
    const title = location.pathname === '/play'
      ? 'Play Online — DON’T LOOK BEHIND YOU'
      : location.pathname === '/privacy'
        ? 'Privacy — DON’T LOOK BEHIND YOU'
        : 'DON’T LOOK BEHIND YOU — Psychological Horror Visual Novel'
    document.title = title
    if (location.hash) {
      window.setTimeout(() => document.querySelector(location.hash)?.scrollIntoView({ behavior: 'smooth' }), 30)
    } else {
      window.scrollTo({ top: 0, behavior: 'auto' })
    }
  }, [location])
  return null
}

export function AppRoutes() {
  const webUrl = safeWebPlayerUrl(release.webUrl, typeof window === 'undefined' ? 'https://site.invalid' : window.location.origin)

  return (
    <>
      <ScrollManager />
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/play" element={webUrl ? <PlayPage /> : <Navigate to="/#download" replace />} />
          <Route path="/download" element={<Navigate to="/#download" replace />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </main>
      <SiteFooter />
    </>
  )
}

export default AppRoutes
