import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

export default function PrivacyPage() {
  return (
    <section className="privacy-page page-shell">
      <Link to="/" className="back-link"><ArrowLeft size={15} /> Back to the website</Link>
      <span className="eyebrow"><i /> THE SMALL PRINT</span>
      <h1>Privacy<br /><em>policy.</em></h1>
      <p className="privacy-updated">LAST UPDATED: 14 NOVEMBER 2026</p>
      <div className="privacy-copy">
        <h2>What this site collects</h2><p>This static website does not provide accounts, forms, or analytics by default. Your browser may send standard connection information to the hosting provider when you visit.</p>
        <h2>Downloads and the browser game</h2><p>Download links and the optional Ren’Py Web player may point to services configured by the developer. Those services can have their own privacy practices. No game download or browser build is currently configured on this site.</p>
        <h2>Contact</h2><p>Contact information will be published here when an official support address is configured.</p>
      </div>
    </section>
  )
}
