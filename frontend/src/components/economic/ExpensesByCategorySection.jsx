import ExpensePieChart from './ExpensePieChart';
import CategoryList from './CategoryList';
import './ExpensesByCategorySection.css';

/**
 * Sección que muestra los gastos por categoría con un gráfico circular y una lista
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.categories - Array de objetos con datos de categorías
 * @param {boolean} props.loading - Indica si los datos están cargando
 * @param {string} props.error - Mensaje de error, si existe
 */
function ExpensesByCategorySection({ categories, loading, error }) {
  // Datos por defecto para mostrar cuando no hay categorías
  const defaultCategories = [
    { category: 'Sin datos', amount: 1, color: '#d1d5db' }
  ];

  return (
    <div className="expenses-by-category-section card">
      <h2>Gastos por categoría</h2>
      
      {loading && (
        <div className="loading-indicator">Cargando datos...</div>
      )}
      
      {error && (
        <div className="error-message">
          <i className="error-icon">⚠️</i>
          <span>Error: {error}</span>
        </div>
      )}
      
      <div className="chart-container">
        {/* Siempre mostramos el gráfico, con datos reales o por defecto */}
        <ExpensePieChart 
          data={(!loading && !error && categories && categories.length > 0) 
            ? categories 
            : defaultCategories}
          isEmpty={!categories || categories.length === 0}
        />
      </div>
      
      {!loading && !error && (!categories || categories.length === 0) && (
        <div className="no-data-message">
          <i className="warning-icon">📊</i>
          <p>No hay datos de gastos disponibles para este período</p>
          <p className="suggestion-message">
            Intenta seleccionar otro período o registra nuevos gastos
          </p>
        </div>
      )}
      
      {!loading && !error && categories && categories.length > 0 && (
        <CategoryList categories={categories} />
      )}
    </div>
  );
}

export default ExpensesByCategorySection;