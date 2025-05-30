import React from 'react';
import './HistoryTabs.css';

/**
 * Componente de pestañas para filtrar el historial
 * @param {Object} props - Propiedades del componente 
 * @param {string} props.activePeriod - Período activo (day, week, month, custom)
 * @param {Function} props.onPeriodChange - Función para cambiar el período
 * @param {string} props.activeCategory - Categoría activa (all, physical, cognitive, emotional, medication, autonomy)
 * @param {Function} props.onCategoryChange - Función para cambiar la categoría
 */
const HistoryTabs = ({ 
  activePeriod, 
  onPeriodChange, 
  activeCategory, 
  onCategoryChange 
}) => {
  return (
    <div className="history-tabs">
      <h3 className="history-title">Historial</h3>
      
      {/* Pestañas de período */}
      <div className="period-tabs">
        <button 
          className={`period-tab ${activePeriod === 'day' ? 'active' : ''}`}
          onClick={() => onPeriodChange('day')}
        >
          Último Día
        </button>
        <button 
          className={`period-tab ${activePeriod === 'week' ? 'active' : ''}`}
          onClick={() => onPeriodChange('week')}
        >
          Última Semana
        </button>
        <button 
          className={`period-tab ${activePeriod === 'month' ? 'active' : ''}`}
          onClick={() => onPeriodChange('month')}
        >
          Último Mes
        </button>
        <button 
          className={`period-tab ${activePeriod === 'custom' ? 'active' : ''}`}
          onClick={() => onPeriodChange('custom')}
        >
          Elegir
        </button>
      </div>
      
      {/* Pestañas de categoría */}
      <div className="category-tabs">
        <button 
          className={`category-tab ${activeCategory === 'all' ? 'active' : ''}`}
          onClick={() => onCategoryChange('all')}
        >
          Todos
        </button>
        <button 
          className={`category-tab ${activeCategory === 'physical' ? 'active' : ''}`}
          onClick={() => onCategoryChange('physical')}
        >
          Físico
        </button>
        <button 
          className={`category-tab ${activeCategory === 'cognitive' ? 'active' : ''}`}
          onClick={() => onCategoryChange('cognitive')}
        >
          Cognitivo
        </button>
        <button 
          className={`category-tab ${activeCategory === 'emotional' ? 'active' : ''}`}
          onClick={() => onCategoryChange('emotional')}
        >
          Emocional
        </button>
        <button 
          className={`category-tab ${activeCategory === 'medication' ? 'active' : ''}`}
          onClick={() => onCategoryChange('medication')}
        >
          Medicación
        </button>
        <button 
          className={`category-tab ${activeCategory === 'autonomy' ? 'active' : ''}`}
          onClick={() => onCategoryChange('autonomy')}
        >
          Autonomía
        </button>
      </div>
    </div>
  );
};

export default HistoryTabs;