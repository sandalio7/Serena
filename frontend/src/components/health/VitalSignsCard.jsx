import React from 'react';
import './VitalSignsCard.css';

/**
 * Componente que muestra los signos vitales diarios
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.vitalSigns - Objeto con los signos vitales
 * @param {Object} props.normalValues - Valores normales para comparación
 * @param {boolean} props.hasData - Indica si hay datos disponibles
 */
const VitalSignsCard = ({ vitalSigns = {}, normalValues = {}, hasData }) => {
  if (!hasData || !vitalSigns) {
    return (
      <div className="vital-signs-card">
        <div className="no-data-message">
          <p>No hay datos de signos vitales disponibles para hoy.</p>
          <p>Los datos aparecerán aquí cuando el cuidador reporte información.</p>
        </div>
      </div>
    );
  }

  // Verificar que cada propiedad exista antes de usarla
  const hasBloodPressure = vitalSigns.bloodPressure && 
                          typeof vitalSigns.bloodPressure === 'object' && 
                          'systolic' in vitalSigns.bloodPressure && 
                          'diastolic' in vitalSigns.bloodPressure;
                          
  const hasTemperature = vitalSigns.temperature !== undefined;
  const hasOxygenation = vitalSigns.oxygenation !== undefined;

  // Función para determinar el estado de un valor vital
  const getStatusIndicator = (value, type) => {
    if (!value) return { status: 'normal', text: 'Sin datos' };
    
    let status = 'normal';
    let text = 'Normal';
    
    switch(type) {
      case 'bloodPressure':
        // Verificar que value contenga las propiedades necesarias
        if (!value.systolic || !value.diastolic) return { status: 'normal', text: 'Sin datos' };
        
        // Lógica simplificada, en un caso real sería más compleja
        if (value.systolic > 140 || value.diastolic > 90) {
          status = 'bad';
          text = 'Mal';
        } else if (value.systolic > 130 || value.diastolic > 85) {
          status = 'moderate';
          text = 'Moderado';
        }
        break;
      case 'temperature':
        if (value > 37.5) {
          status = 'moderate';
          text = 'Moderado';
        } else if (value > 38) {
          status = 'bad';
          text = 'Mal';
        }
        break;
      case 'oxygenation':
        if (value < 95) {
          status = 'moderate';
          text = 'Moderado';
        } else if (value < 90) {
          status = 'bad';
          text = 'Mal';
        }
        break;
      default:
        break;
    }
    
    return { status, text };
  };

  // Determinar el estado de cada signo vital con comprobaciones de seguridad
  const bloodPressureStatus = hasBloodPressure 
    ? getStatusIndicator(vitalSigns.bloodPressure, 'bloodPressure') 
    : { status: 'normal', text: 'Sin datos' };
    
  const temperatureStatus = hasTemperature 
    ? getStatusIndicator(vitalSigns.temperature, 'temperature') 
    : { status: 'normal', text: 'Sin datos' };
    
  const oxygenationStatus = hasOxygenation 
    ? getStatusIndicator(vitalSigns.oxygenation, 'oxygenation') 
    : { status: 'normal', text: 'Sin datos' };

  // Verificar valores normales
  const hasNormalBloodPressure = normalValues.bloodPressure && 
                                typeof normalValues.bloodPressure === 'object' &&
                                'systolic' in normalValues.bloodPressure && 
                                'diastolic' in normalValues.bloodPressure;
                                
  const hasNormalTemperature = normalValues.temperature !== undefined;
  const hasNormalOxygenation = normalValues.oxygenation !== undefined;

  return (
    <div className="vital-signs-card">
      <div className="vital-signs-header">
        <span>Ultimo día</span>
      </div>
      
      <div className="vital-signs-content">
        <div className="vital-signs-column">
          <h3>Estado Físico</h3>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Presión arterial</div>
            <div className="vital-sign-value">
              {hasBloodPressure 
                ? `${vitalSigns.bloodPressure.systolic}/${vitalSigns.bloodPressure.diastolic}`
                : 'No disponible'}
              <span className={`status-indicator ${bloodPressureStatus.status}`}>
                • {bloodPressureStatus.text}
              </span>
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value">
              {hasTemperature 
                ? `${vitalSigns.temperature}°C`
                : 'No disponible'}
              <span className={`status-indicator ${temperatureStatus.status}`}>
                • {temperatureStatus.text}
              </span>
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value">
              {hasOxygenation 
                ? `${vitalSigns.oxygenation}%`
                : 'No disponible'}
              <span className={`status-indicator ${oxygenationStatus.status}`}>
                • {oxygenationStatus.text}
              </span>
            </div>
          </div>
        </div>
        
        <div className="vital-signs-column normal-values">
          <h3>Valores normales</h3>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Presión arterial</div>
            <div className="vital-sign-value normal">
              {hasNormalBloodPressure 
                ? `${normalValues.bloodPressure.systolic}/${normalValues.bloodPressure.diastolic}`
                : 'No definido'}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value normal">
              {hasNormalTemperature 
                ? `${normalValues.temperature}°C`
                : 'No definido'}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value normal">
              {hasNormalOxygenation 
                ? `${normalValues.oxygenation}%`
                : 'No definido'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VitalSignsCard;