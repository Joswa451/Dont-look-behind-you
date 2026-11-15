import { Download, FolderDown, Play, RotateCw, ShieldCheck, ShieldAlert, Smartphone } from 'lucide-react'

const steps = [
  {
    number: '01', title: 'Download the APK',
    text: 'On this page, tap Download Android APK and keep the file in your Downloads folder.',
    art: <div className="android-mock browser-mock android-browser-mock"><div className="mock-titlebar"><span className="mock-dots" /> Downloads</div><div className="mock-download-row"><span className="mock-file-icon"><Download size={18} /></span><span><b>DontLookBehindYou-Android-v1.0.1.apk</b><small>Download complete</small></span><span className="mock-check">✓</span></div></div>,
  },
  {
    number: '02', title: 'Open the download',
    text: 'Open your phone’s Downloads or Files app and tap the APK file.',
    art: <div className="android-mock"><div className="android-phone"><span className="android-notch" /><div className="android-file-row"><FolderDown size={18} /><span><b>Downloads</b><small>DontLookBehindYou-Android-v1.0.1.apk</small></span></div><div className="android-file-row is-tapped"><Download size={18} /><span><b>Open APK</b><small>Install this package?</small></span></div></div></div>,
  },
  {
    number: '03', title: 'Allow this source',
    text: 'If Android asks, allow your browser or file manager to install unknown apps. You can turn this permission off afterward.',
    art: <div className="android-mock"><div className="android-settings"><span className="android-setting-label">INSTALL UNKNOWN APPS</span><div className="android-setting-row"><span>Chrome</span><i className="android-toggle on" /></div><div className="android-setting-row"><span>Files</span><i className="android-toggle" /></div><small>Enable only the app you use to open the APK.</small></div></div>,
  },
  {
    number: '04', title: 'Install the game',
    text: 'Review the permission summary Android shows, then tap Install. The APK is signed for direct distribution outside Google Play.',
    art: <div className="android-mock"><div className="android-dialog"><span className="android-app-icon"><img src="/favicon.svg" alt="" /></span><b>Don’t Look Behind You</b><small>Version 1.0.0</small><div className="android-permission"><ShieldCheck size={14} /> Review permissions</div><span className="android-dialog-button">INSTALL</span></div></div>,
  },
  {
    number: '05', title: 'Launch the game',
    text: 'Tap Open, or find Don’t Look Behind You in your app drawer. Start a new game when the title screen appears.',
    art: <div className="android-mock"><div className="android-launcher"><span className="android-app-tile"><img src="/favicon.svg" alt="" /></span><strong>DON’T LOOK<br />BEHIND YOU</strong><small>Tap to open</small></div></div>,
  },
  {
    number: '06', title: 'Turn the phone sideways',
    text: 'The game is designed for landscape. Enable auto-rotate, turn your phone, and use the on-screen arrows to continue.',
    art: <div className="android-mock landscape-mock"><div className="android-phone is-landscape"><div className="android-game-frame"><span>DON’T LOOK</span><b>BEHIND YOU</b><i><Play size={10} fill="currentColor" /> NEW GAME</i></div></div><RotateCw className="android-rotate-icon" size={22} /></div>,
  },
]

export default function AndroidInstallGuide() {
  return (
    <section id="android-install" className="section android-install-section">
      <div className="page-shell">
        <div className="windows-guide-heading">
          <span className="eyebrow"><i /> SIX STEPS TO THE FIRST NIGHT</span>
          <h2>Android.<br /><em>Download. Install. Play.</em></h2>
          <p>The Android build is a direct APK, not a Google Play download. Your phone may ask for permission the first time you install it.</p>
        </div>
        <div className="android-install-grid">
          {steps.map((step) => (
            <article className="android-install-step" key={step.number}>
              <div className={`install-illustration install-art-${step.number}`}>{step.art}</div>
              <div className="install-step-caption"><span>{step.number}</span><div><h3>{step.title}</h3><p>{step.text}</p></div></div>
            </article>
          ))}
        </div>
        <div className="android-guide-notes">
          <p className="windows-guide-note"><ShieldCheck size={15} /> Minimum Android version: 5.0 (API 21). The game runs in landscape and needs about 300 MB of free storage.</p>
          <p className="windows-guide-note is-warning"><ShieldAlert size={15} /> If Google Play Protect shows a warning, do not turn Play Protect off. Confirm that you downloaded the APK from this official page and compare its SHA-256 with the value in the download card. If anything looks wrong, cancel the install.</p>
          <p className="windows-guide-note"><Smartphone size={15} /> Only install APKs from sources you trust. You can revoke the “install unknown apps” permission after the game is installed.</p>
        </div>
      </div>
    </section>
  )
}
