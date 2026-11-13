import { useEffect, useRef } from 'react'
import { ArrowLeft, ArrowRight, X } from 'lucide-react'

export default function Lightbox({ items, index, onClose, onChange }) {
  const closeButton = useRef(null)
  const currentIndex = useRef(index)
  currentIndex.current = index
  useEffect(() => {
    const previouslyFocused = document.activeElement
    const handleKey = (event) => {
      if (event.key === 'Escape') onClose()
      if (event.key === 'ArrowRight') onChange((currentIndex.current + 1) % items.length)
      if (event.key === 'ArrowLeft') onChange((currentIndex.current + items.length - 1) % items.length)
      if (event.key === 'Tab') {
        const controls = Array.from(document.querySelectorAll('.lightbox button:not([disabled])'))
        const first = controls[0]
        const last = controls.at(-1)
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault()
          last?.focus()
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault()
          first?.focus()
        }
      }
    }
    document.addEventListener('keydown', handleKey)
    document.body.classList.add('lightbox-open')
    closeButton.current?.focus()
    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.classList.remove('lightbox-open')
      previouslyFocused?.focus?.()
    }
  }, [items.length, onChange, onClose])

  const item = items[index]
  return (
    <div className="lightbox" role="dialog" aria-modal="true" aria-label={`Gallery image: ${item.title}`} onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <button ref={closeButton} className="lightbox-close icon-button" aria-label="Close image preview" onClick={onClose}><X /></button>
      <button className="lightbox-prev icon-button" aria-label="Previous image" onClick={() => onChange((index + items.length - 1) % items.length)}><ArrowLeft /></button>
      <figure className="lightbox-content">
        <img src={item.src} alt={item.title} />
        <figcaption><span>{item.type}</span><strong>{item.title}</strong><small>{String(index + 1).padStart(2, '0')} / {String(items.length).padStart(2, '0')}</small></figcaption>
      </figure>
      <button className="lightbox-next icon-button" aria-label="Next image" onClick={() => onChange((index + 1) % items.length)}><ArrowRight /></button>
    </div>
  )
}
