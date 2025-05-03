// frontend/src/components/health/ConclusionCard.jsx
function ConclusionCard({ status }) {
  // Si no hay datos disponibles
  if (!status) {
    return (
      <div className="card conclusion-card">
        <h3>Conclusión general</h3>
        <p className="no-data-message">No hay conclusión disponible</p>
      </div>
    );
  }
  
  // Determinar color y emoji según estado
  let statusClass = 'status-neutral';
  let emoji = '😐';
  
  if (status.toLowerCase().includes('bueno')) {
    statusClass = 'status-good';
    emoji = '😊';
  } else if (status.toLowerCase().includes('malo')) {
    statusClass = 'status-bad';
    emoji = '😔';
  }
  
  return (
    <div className="card conclusion-card">
      <h3>Conclusión general</h3>
      <div className={`status-indicator ${statusClass}`}>
        <span className="emoji">{emoji}</span>
        <p className="status-text">{status}</p>
      </div>
    </div>
  );
}

export default ConclusionCard;