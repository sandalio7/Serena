// frontend/src/components/health/PhysicalVarsCard.jsx
function PhysicalVarsCard({ data }) {
  // Si no hay datos disponibles
  if (!data || 
      (!data.bloodPressure?.value && 
       !data.temperature?.value && 
       !data.oxygenSaturation?.value && 
       !data.weight?.value)) {
    return (
      <div className="card">
        <h3>Variables físicas numéricas</h3>
        <p className="no-data-message">No hay datos disponibles para mostrar</p>
      </div>
    );
  }
  
  return (
    <div className="card">
      <h3>Variables físicas numéricas</h3>
      
      <div className="metrics-grid">
        {data.bloodPressure?.value && (
          <div className="metric">
            <h4>Presión arterial</h4>
            <p className="value">
              <span className="emoji">😊</span> {data.bloodPressure.value} mmHg
            </p>
            {data.bloodPressure.status && (
              <p className="status">{data.bloodPressure.status}</p>
            )}
          </div>
        )}
        
        {data.temperature?.value && (
          <div className="metric">
            <h4>Temperatura</h4>
            <p className="value">
              {data.temperature.value} °C
              {data.temperature.status && (
                <span className="status"> {data.temperature.status}</span>
              )}
            </p>
          </div>
        )}
        
        {data.oxygenSaturation?.value && (
          <div className="metric">
            <h4>Oxígeno en sangre</h4>
            <p className="value">
              <span className="emoji">😊</span> {data.oxygenSaturation.value}%
              {data.oxygenSaturation.status && (
                <span className="status"> {data.oxygenSaturation.status}</span>
              )}
            </p>
          </div>
        )}
        
        {data.weight?.value && (
          <div className="metric">
            <h4>Peso</h4>
            <p className="value">
              <span className="emoji">😊</span> {data.weight.value} kg
              {data.weight.bmi && (
                <span className="bmi"> / IMC {data.weight.bmi}</span>
              )}
            </p>
            {data.weight.status && (
              <p className="status">{data.weight.status}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default PhysicalVarsCard;