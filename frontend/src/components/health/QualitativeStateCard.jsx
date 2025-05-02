// src/components/health/QualitativeStateCard.jsx
function QualitativeStateCard({ title, rating, description, maxRating = 10 }) {
    // Determinar el emoji según el rating
    const getEmoji = (rating, maxRating) => {
      const percentage = (rating / maxRating) * 100;
      if (percentage >= 70) return '🙂';
      if (percentage >= 40) return '😐';
      return '😟';
    };
  
    return (
      <div className="card qualitative-card">
        <h3>{title}</h3>
        <p className="rating">
          Valoración: {rating}/{maxRating} {getEmoji(rating, maxRating)}
        </p>
        <p className="description">"{description}"</p>
      </div>
    );
  }
  
  export default QualitativeStateCard;