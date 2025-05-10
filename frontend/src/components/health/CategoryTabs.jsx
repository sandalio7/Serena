import React from 'react';
import './CategoryTabs.css';

/**
 * Componente de pestañas para filtrar el historial por categoría
 * @param {Object} props - Propiedades del componente 
 * @param {string} props.activeCategory - Categoría activa (all, physical, cognitive, etc)
 * @param {Function} props.onCategoryChange - Función para cambiar la categoría
 */
const CategoryTabs = ({ activeCategory, onCategoryChange }) => {
  return (
    <div className="category-tabs-card">
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
          className={`category-tab ${activeCategory === 'autonomy' ? 'active' : ''}`}
          onClick={() => onCategoryChange('autonomy')}
        >
          Autonomía
        </button>
      </div>
    </div>
  );
};

export default CategoryTabs;