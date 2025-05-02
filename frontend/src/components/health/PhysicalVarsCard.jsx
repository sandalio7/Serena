// src/components/health/PhysicalVarsCard.jsx
function PhysicalVarsCard({ data }) {
    // Función para determinar el emoji según el estado
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
      <div className="card">
        <h3>Variables físicas numéricas</h3>
        
        <div className="physical-vars-grid">
          <div className="physical-var">
            <p className="var-name">Presión arterial</p>
            <p className="var-value">
              {getStatusEmoji(data.bloodPressure.status)} {data.bloodPressure.value} mmHg
            </p>
          </div>
          
          <div className="physical-var">
            <p className="var-name">Temperatura</p>
            <p className="var-value">
              {data.temperature.value}°C <span className={`status-${data.temperature.status.toLowerCase()}`}>
                {data.temperature.status}
              </span>
            </p>
          </div>
          
          <div className="physical-var">
            <p className="var-name">Oxígeno en sangre</p>
            <p className="var-value">
              {getStatusEmoji(data.oxygenSaturation.status)} {data.oxygenSaturation.value}% <span className="status-moderate">
                {data.oxygenSaturation.status}
              </span>
            </p>
          </div>
          
          <div className="physical-var">
            <p className="var-name">Peso</p>
            <p className="var-value">
              {getStatusEmoji(data.weight.status)} {data.weight.value} kg / IMC {data.weight.bmi}
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  export default PhysicalVarsCard;