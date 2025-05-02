// src/components/health/SleepCard.jsx
function SleepCard({ data }) {
    const getStatusEmoji = (status) => {
      switch (status) {
        case 'Normal':
          return '🙂';
        case 'Moderado':
          return '😐';
        case 'Bajo':
          return '😟';
        default:
          return '😐';
      }
    };
  
    return (
      <div className="card sleep-card">
        <div className="sleep-info">
          <span className="sleep-icon">🌙</span>
          <p className="sleep-title">Sueño: {data.hours} hs dormidas</p>
          <p className="sleep-status">
            {getStatusEmoji(data.status)} {data.status}
          </p>
        </div>
      </div>
    );
  }
  
  export default SleepCard;