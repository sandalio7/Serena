import React from 'react';
import './VitalSignsCard.css';
import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';

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

  // Función para determinar el estado de un valor vital
  const getStatusIndicator = (value, type) => {
    if (!value || !value.available) return { status: 'normal', text: 'Sin datos' };
    
    // Usar el status ya determinado por el backend
    return { 
      status: value.status === 'Normal' ? 'normal' : 
             value.status === 'Moderado' ? 'moderate' : 'bad',
      text: value.status
    };
  };

  // Función para mostrar mensaje sobre la última medición
  const getLastMeasuredText = (value) => {
    if (!value || !value.available) return null;
    
    if (value.recent) {
      return `Última medición: ${formatDistanceToNow(new Date(value.lastMeasured), { 
        addSuffix: true, locale: es 
      })}`;
    } else {
      return `Última medición: hace más de 7 días`;
    }
  };

  // Determinar el estado de cada signo vital
  const bloodPressureStatus = getStatusIndicator(vitalSigns.bloodPressure, 'bloodPressure');
  const temperatureStatus = getStatusIndicator(vitalSigns.temperature, 'temperature');
  const oxygenationStatus = getStatusIndicator(vitalSigns.oxygenSaturation, 'oxygenation');

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
              {vitalSigns.bloodPressure && vitalSigns.bloodPressure.available 
                ? `${vitalSigns.bloodPressure.value}`
                : 'No disponible'}
              {vitalSigns.bloodPressure && vitalSigns.bloodPressure.available && (
                <span className={`status-indicator ${bloodPressureStatus.status}`}>
                  • {bloodPressureStatus.text}
                </span>
              )}
            </div>
            {vitalSigns.bloodPressure && vitalSigns.bloodPressure.available && (
              <div className="last-measured-text">
                {getLastMeasuredText(vitalSigns.bloodPressure)}
              </div>
            )}
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value">
              {vitalSigns.temperature && vitalSigns.temperature.available 
                ? `${vitalSigns.temperature.value}°C`
                : 'No disponible'}
              {vitalSigns.temperature && vitalSigns.temperature.available && (
                <span className={`status-indicator ${temperatureStatus.status}`}>
                  • {temperatureStatus.text}
                </span>
              )}
            </div>
            {vitalSigns.temperature && vitalSigns.temperature.available && (
              <div className="last-measured-text">
                {getLastMeasuredText(vitalSigns.temperature)}
              </div>
            )}
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value">
              {vitalSigns.oxygenSaturation && vitalSigns.oxygenSaturation.available 
                ? `${vitalSigns.oxygenSaturation.value}%`
                : 'No disponible'}
              {vitalSigns.oxygenSaturation && vitalSigns.oxygenSaturation.available && (
                <span className={`status-indicator ${oxygenationStatus.status}`}>
                  • {oxygenationStatus.text}
                </span>
              )}
            </div>
            {vitalSigns.oxygenSaturation && vitalSigns.oxygenSaturation.available && (
              <div className="last-measured-text">
                {getLastMeasuredText(vitalSigns.oxygenSaturation)}
              </div>
            )}
          </div>
        </div>
        
        <div className="vital-signs-column normal-values">
          <h3>Valores normales</h3>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Presión arterial</div>
            <div className="vital-sign-value normal">
              {normalValues.bloodPressure 
                ? `${normalValues.bloodPressure.systolic}/${normalValues.bloodPressure.diastolic}`
                : 'No definido'}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Temperatura</div>
            <div className="vital-sign-value normal">
              {normalValues.temperature 
                ? `${normalValues.temperature}°C`
                : 'No definido'}
            </div>
          </div>
          
          <div className="vital-sign-item">
            <div className="vital-sign-label">Oxigenación</div>
            <div className="vital-sign-value normal">
              {normalValues.oxygenation 
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