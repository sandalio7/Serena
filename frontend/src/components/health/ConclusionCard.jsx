// src/components/health/ConclusionCard.jsx
function ConclusionCard({ status }) {
    // Determinar el emoji según el estado
    const getEmoji = (status) => {
      switch (status.toLowerCase()) {
        case 'bueno':
          return '🙂';
        case 'regular':
          return '😐';
        case 'malo':
          return '😟';
        default:
          return '😐';
      }
    };
    
    // Determinar la clase de color según el estado
    const getStatusClass = (status) => {
      switch (status.toLowerCase()) {
        case 'bueno':
          return 'conclusion-good';
        case 'regular':
          return 'conclusion-moderate';
        case 'malo':
          return 'conclusion-bad';
        default:
          return 'conclusion-moderate';
      }
    };
  
    return (
      <div className={`card conclusion-card ${getStatusClass(status)}`}>
        <div className="conclusion-content">
          <span className="conclusion-emoji">{getEmoji(status)}</span>
          <p className="conclusion-text">
            Conclusión general de estado:
            <span className="conclusion-status">{status}</span>
          </p>
        </div>
      </div>
    );
  }
  
  export default ConclusionCard;