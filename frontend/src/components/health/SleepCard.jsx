// frontend/src/components/health/SleepCard.jsx
function SleepCard({ data }) {
  // Si no hay datos disponibles
  if (!data || !data.hours) {
    return (
      <div className="card sleep-card">
        <h3>Sueño</h3>
        <p className="no-data-message">No hay datos de sueño disponibles</p>
      </div>
    );
  }
  
  return (
    <div className="card sleep-card">
      <span className="sleep-icon">🌙</span>
      <p className="sleep-text">Sueño: {data.hours} hs dormidas</p>
      {data.status && (
        <span className="quality-indicator">
          <span className="emoji">😊</span> {data.status}
        </span>
      )}
    </div>
  );
}

export default SleepCard;