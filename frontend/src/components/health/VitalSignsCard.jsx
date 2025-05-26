import React from 'react';
import './VitalSignsCard.css';

/**
 * Componente que muestra los signos vitales diarios
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.vitalSigns - Objeto con los signos vitales
 * @param {Object} props.normalValues - Valores normales para comparación
 * @param {boolean} props.hasData - Indica si hay datos disponibles
 */
const VitalSignsCard = ({ vitalSigns, normalValues, hasData }) => {
  if (!hasData) {
    return (
      <div className="vital-signs-card">
        <div className="no-data-message">
          <p>No hay datos de signos vitales disponibles para hoy.</p>
          <p>Los datos aparecerán aquí cuando el cuidador reporte información.</p>
        </div>
      </div>
    );
  }

  // Función para determinar el estado de un valor vital
  const getStatusIndicator = (value, type) => {
    let status = 'normal';
    let text = 'Normal';
    
    switch(type) {
      case 'bloodPressure':
        if (value.systolic > 140 || value.diastolic > 90) {
          status = 'bad';
          text = 'Mal';
        } else if (value.systolic > 130 || value.diastolic > 85) {
          status = 'moderate';
          text = 'Moderado';
        }
        break;
      case 'temperature':
        if (value > 37.5 && value <= 38) {
          status = 'moderate';
          text = 'Moderado';
        } else if (value > 38) {
          status = 'bad';
          text = 'Mal';
        }
        break;
      case 'oxygenation':
        if (value >= 95 && value < 98) {
          status = 'moderate';
          text = 'Moderado';
        } else if (value < 95) {
          status = 'bad';
          text = 'Mal';
        }
        break;
      default:
        break;
    }
    
    return { status, text };
  };

  // Determinar el estado de cada signo vital
  const bloodPressureStatus = getStatusIndicator(vitalSigns.bloodPressure, 'bloodPressure');
  const temperatureStatus = getStatusIndicator(vitalSigns.temperature, 'temperature');
  const oxygenationStatus = getStatusIndicator(vitalSigns.oxygenation, 'oxygenation');

  return (
    <div className="vital-signs-card">
      <div className="vital-signs-content">
        <div className="vital-signs-column">
          <h3>Estado Físico</h3>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Presión arterial</div>
            <div className="vital-sign-value">
              {`${vitalSigns.bloodPressure.systolic}/${vitalSigns.bloodPressure.diastolic}`}
              <span className={`status-indicator ${bloodPressureStatus.status}`}>
                • {bloodPressureStatus.text}
              </span>
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value">
              {`${vitalSigns.temperature}°C`}
              <span className={`status-indicator ${temperatureStatus.status}`}>
                • {temperatureStatus.text}
              </span>
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value">
              {`${vitalSigns.oxygenation}%`}
              <span className={`status-indicator ${oxygenationStatus.status}`}>
                • {oxygenationStatus.text}
              </span>
            </div>
          </div>
        </div>
        
        <div className="vital-signs-column">
          <h3>Valores normales</h3>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Presión arterial</div>
            <div className="vital-sign-value">
              {`${normalValues.bloodPressure.systolic}/${normalValues.bloodPressure.diastolic}`}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value">
              {`${normalValues.temperature}°C`}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value">
              {`${normalValues.oxygenation}%`}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VitalSignsCard;