import { Archive, Check, ChevronRight, FolderOpen, MousePointer2, Play, ShieldCheck } from 'lucide-react'

const steps = [
  {
    number: '01', title: 'Download the ZIP',
    text: 'Save the Windows package from the official game website.',
    art: <div className="windows-mock-window browser-mock"><div className="mock-titlebar"><span className="mock-dots" /> Downloads</div><div className="mock-download-row"><span className="mock-file-icon"><Archive size={18} /></span><span><b>DontLookBehindYou-Windows-v1.0.1.zip</b><small>Download complete</small></span><Check size={15} className="mock-check" /></div></div>,
  },
  {
    number: '02', title: 'Choose Extract All',
    text: 'Right-click the ZIP and select “Extract All…” from its menu.',
    art: <div className="windows-mock-window context-mock"><div className="mock-zip-row"><Archive size={17} /> DontLookBehindYou-Windows-v1.0.1.zip</div><div className="mock-context-menu"><span>Open</span><span className="mock-selected"><Archive size={13} /> Extract All… <ChevronRight size={12} /></span><span>Copy</span></div><MousePointer2 className="mock-cursor" size={23} /></div>,
  },
  {
    number: '03', title: 'Open the game folder',
    text: 'Keep the extracted files together, then open DontLookBehindYou.',
    art: <div className="windows-mock-window explorer-mock"><div className="mock-titlebar"><span className="mock-dots" /> DontLookBehindYou-win</div><div className="mock-file-list"><span><FolderOpen size={16} /> game</span><span><FolderOpen size={16} /> lib</span><span><FolderOpen size={16} /> renpy</span></div></div>,
  },
  {
    number: '04', title: 'Double-click the game',
    text: 'Open DontLookBehindYou.exe. Python and the Ren’Py SDK are included.',
    art: <div className="windows-mock-window exe-mock"><div className="mock-titlebar"><span className="mock-dots" /> DontLookBehindYou</div><div className="mock-exe-card"><span className="mock-game-icon">◉</span><span><b>DontLookBehindYou.exe</b><small>Application · 64-bit</small></span><MousePointer2 className="mock-cursor" size={23} /></div></div>,
  },
  {
    number: '05', title: 'Enter Ashgrove',
    text: 'Choose New Game and follow Ethan through seven nights.',
    art: <div className="windows-mock-window launch-mock"><img src="/images/bg_menu.jpg" alt="" /><div className="launch-overlay"><span>DON’T LOOK</span><b>BEHIND YOU</b><i><Play size={12} fill="currentColor" /> NEW GAME</i></div></div>,
  },
]

export default function WindowsInstallGuide() {
  return (
    <>
      <section id="install" className="section windows-install-section">
        <div className="page-shell">
          <div className="windows-guide-heading"><span className="eyebrow"><i /> FIVE STEPS TO THE FIRST NIGHT</span><h2>Download.<br /><em>Extract. Play.</em></h2><p>No setup wizard or extra software. Keep the extracted folder intact and start the game from its executable.</p></div>
          <div className="windows-install-grid">
            {steps.map((step) => <article className="windows-install-step" key={step.number}><div className={`install-illustration install-art-${step.number}`}>{step.art}</div><div className="install-step-caption"><span>{step.number}</span><div><h3>{step.title}</h3><p>{step.text}</p></div></div></article>)}
          </div>
          <p className="windows-guide-note"><ShieldCheck size={15} /> The release is unsigned. Windows may show an unknown-publisher notice; check the official source and SHA-256 before deciding whether to run it.</p>
        </div>
      </section>
      <section id="troubleshooting" className="section windows-troubleshooting-section">
        <div className="page-shell troubleshooting-layout">
          <div><span className="eyebrow"><i /> IF THE NIGHT GOES WRONG</span><h2>Windows<br /><em>troubleshooting.</em></h2><p>Keep the ZIP intact and use the official release package when you need to reinstall.</p></div>
          <div className="windows-faq">
            <details><summary>Windows SmartScreen says “Unknown publisher”</summary><p>This build is not digitally signed, so Windows may show that warning. Confirm the ZIP came from the official game website and compare its SHA-256 with the value on the download page. If you are unsure, cancel and contact the developer.</p></details>
            <details><summary>My antivirus flags or removes a game file</summary><p>Do not disable protection. Check the file against the official SHA-256, restore nothing unless the package matches, and submit the file to your antivirus vendor for review. You can also contact the developer with the detection name.</p></details>
            <details><summary>A DLL is missing</summary><p>Extract the whole ZIP again and keep the game, lib, and renpy folders together beside DontLookBehindYou.exe. Do not download individual DLLs from third-party sites. If the message remains, send the exact DLL name to the developer.</p></details>
            <details><summary>The game opens and immediately closes</summary><p>Re-download the ZIP from the official site, use Extract All, and check whether your security software quarantined a file. Try extracting to a short folder path such as Documents\Games\DontLookBehindYou.</p></details>
            <details><summary>I see a black screen</summary><p>Update your graphics driver from your PC or graphics-card manufacturer's official support site. In the game, press Shift+G to open Ren’Py graphics options, then try another renderer or windowed mode.</p></details>
            <details><summary>There is no audio</summary><p>Check the in-game Preferences sliders, Windows volume mixer, and selected audio output device. Restart the game after changing the Windows output device.</p></details>
            <details><summary>There is not enough disk space</summary><p>Keep at least 2 GB free before extraction. Extract All needs room for both the downloaded ZIP and the installed game folder.</p></details>
          </div>
        </div>
      </section>
    </>
  )
}
