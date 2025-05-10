import React from 'react';
import './WeeklySummaryCard.css';

/**
 * Componente que muestra el resumen semanal de las diferentes categorías de salud
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.summaryData - Datos del resumen semanal
 */
const WeeklySummaryCard = ({ summaryData }) => {
  // Función para determinar la clase de estado según la puntuación
  const getStatusClass = (score) => {
    if (score >= 8) return 'good';
    if (score >= 5) return 'moderate';
    return 'bad';
  };

  return (
    <div className="weekly-summary-container">
      <div className="weekly-summary-grid">
        {/* Estado Físico */}
        <div className="summary-category">
          <div className="category-header">
            <h3>Estado Físico</h3>
            <div className={`status-circle ${getStatusClass(summaryData.physical.score)}`}>
              <span className="status-icon">•</span>
            </div>
          </div>
          <div className="category-score">
            Valoración: {summaryData.physical.score}/10
          </div>
          <div className="category-description">
            "{summaryData.physical.description}"
          </div>
        </div>
        
        {/* Estado Cognitivo */}
        <div className="summary-category">
          <div className="category-header">
            <h3>Estado Cognitivo</h3>
            <div className={`status-circle ${getStatusClass(summaryData.cognitive.score)}`}>
              <span className="status-icon">🙂</span>
            </div>
          </div>
          <div className="category-score">
            Valoración: {summaryData.cognitive.score}/10
          </div>
          <div className="category-description">
            "{summaryData.cognitive.description}"
          </div>
        </div>
        
        {/* Estado Emocional */}
        <div className="summary-category">
          <div className="category-header">
            <h3>Estado Emocional</h3>
            <div className={`status-circle ${getStatusClass(summaryData.emotional.score)}`}>
              <span className="status-icon">•</span>
            </div>
          </div>
          <div className="category-score">
            Valoración: {summaryData.emotional.score}/10
          </div>
          <div className="category-description">
            "{summaryData.emotional.description}"
          </div>
        </div>
        
        {/* Autonomía */}
        <div className="summary-category">
          <div className="category-header">
            <h3>Autonomía</h3>
            <div className={`status-circle ${getStatusClass(summaryData.autonomy.score)}`}>
              <span className="status-icon">•</span>
            </div>
          </div>
          <div className="category-score">
            Valoración: {summaryData.autonomy.score}/10
          </div>
          <div className="category-description">
            "{summaryData.autonomy.description}"
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeeklySummaryCard;