import React from 'react';
import './HealthStatusCard.css';

/**
 * Componente que muestra el estado general de salud actual
 * @param {Object} props - Propiedades del componente
 * @param {string} props.status - Estado de salud (ej: "Regular")
 * @param {string|number} props.score - Puntuación numérica (ej: "6")
 * @param {string} props.emoji - Emoji representativo del estado
 */
const HealthStatusCard = ({ status = "Regular", score = "6", emoji = "🙂" }) => {
  return (
    <div className="health-status-card">
      <div className="health-status-header">
        <span>Estado de salud Actual</span>
      </div>
      <div className="health-status-content">
        <div className="health-status-icon">
          <span className="arrow-icon">→</span>
        </div>
        <div className="health-status-score">
          <span className="status-text">{status}</span>
          <span className="score-text">{score}/10</span>
        </div>
        <div className="health-status-emoji">
          {emoji}
        </div>
      </div>
    </div>
  );
};

export default HealthStatusCard;