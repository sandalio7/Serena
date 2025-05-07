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
  return (
    <div className="expenses-by-category-section card">
      <h2>Gastos por categoría</h2>
      
      {loading && (
        <div className="loading-indicator">Cargando datos...</div>
      )}
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
      
      {!loading && !error && categories && categories.length > 0 && (
        <>
          <div className="chart-container">
            <ExpensePieChart data={categories} />
          </div>
          
          <CategoryList categories={categories} />
        </>
      )}
      
      {!loading && !error && (!categories || categories.length === 0) && (
        <div className="no-data-message">
          <p>No hay datos disponibles</p>
          <p className="no-categories-message">No hay categorías disponibles</p>
        </div>
      )}
    </div>
  );
}

export default ExpensesByCategorySection;