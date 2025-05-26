import React from 'react';
import './WeeklySummaryCard.css';

/**
 * Componente que muestra el resumen semanal de las diferentes categorías de salud
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.summaryData - Datos del resumen semanal
 * @param {boolean} props.hasData - Indica si hay datos disponibles
 */
const WeeklySummaryCard = ({ summaryData, hasData }) => {
  if (!hasData) {
    return (
      <div className="weekly-summary-container">
        <div className="no-data-message">
          <p>No hay datos de resumen semanal disponibles.</p>
          <p>Los datos aparecerán aquí cuando se recolecte información durante la semana.</p>
        </div>
      </div>
    );
  }

  // Función para determinar la clase de estado según la puntuación
  const getStatusClass = (score) => {
    if (score >= 8) return 'good';
    if (score >= 5) return 'moderate';
    return 'bad';
  };

  // Función para crear una card de categoría individual
  const renderCategoryCard = (categoryKey, categoryData) => {
    const categoryNames = {
      physical: 'Estado Físico',
      cognitive: 'Estado Cognitivo',
      emotional: 'Estado Emocional',
      autonomy: 'Autonomía'
    };

    const categoryIcons = {
      physical: '•',
      cognitive: '🙂',
      emotional: '•',
      autonomy: '•'
    };

    if (!categoryData || categoryData.score === null || categoryData.score === undefined) {
      return (
        <div key={categoryKey} className="summary-category no-data">
          <div className="category-header">
            <h3>{categoryNames[categoryKey]}</h3>
            <div className="status-circle no-data-circle">
              <span className="status-icon">?</span>
            </div>
          </div>
          <div className="category-no-data">
            Sin datos disponibles
          </div>
        </div>
      );
    }

    return (
      <div key={categoryKey} className="summary-category">
        <div className="category-header">
          <h3>{categoryNames[categoryKey]}</h3>
          <div className={`status-circle ${getStatusClass(categoryData.score)}`}>
            <span className="status-icon">{categoryIcons[categoryKey]}</span>
          </div>
        </div>
        <div className="category-score">
          Valoración: {categoryData.score}/10
        </div>
        <div className="category-description">
          "{categoryData.description}"
        </div>
      </div>
    );
  };

  return (
    <div className="weekly-summary-container">
      <div className="weekly-summary-grid">
        {renderCategoryCard('physical', summaryData?.physical)}
        {renderCategoryCard('cognitive', summaryData?.cognitive)}
        {renderCategoryCard('emotional', summaryData?.emotional)}
        {renderCategoryCard('autonomy', summaryData?.autonomy)}
      </div>
    </div>
  );
};

export default WeeklySummaryCard;