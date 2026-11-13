export default function SectionHeading({ kicker, title, text, number }) {
  return (
    <div className="section-heading">
      <div>
        <span className="eyebrow"><i />{kicker}</span>
        <h2>{title}</h2>
      </div>
      {text && <p>{text}</p>}
      {number && <span className="section-number">{number}</span>}
    </div>
  )
}
