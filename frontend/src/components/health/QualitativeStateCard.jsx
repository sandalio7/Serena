// frontend/src/components/health/QualitativeStateCard.jsx
function QualitativeStateCard({ title, rating, description }) {
  // Si no hay datos disponibles
  if (!rating && !description) {
    return (
      <div className="card qualitative-card">
        <h3>{title}</h3>
        <p className="no-data-message">No hay datos disponibles</p>
      </div>
    );
  }
  
  // Convertir rating a escala de 10 si viene en escala de 5
  const displayRating = rating > 5 ? rating : rating * 2;
  
  // Emoji según rating
  let emoji = '😐';
  if (displayRating >= 8) {
    emoji = '😊';
  } else if (displayRating >= 6) {
    emoji = '🙂';
  } else if (displayRating <= 4) {
    emoji = '😔';
  }
  
  return (
    <div className="card qualitative-card">
      <h3>{title}</h3>
      <p className="rating">
        Valoración: {displayRating}/10 <span className="emoji">{emoji}</span>
      </p>
      {description && (
        <p className="description">"{description}"</p>
      )}
    </div>
  );
}

export default QualitativeStateCard;