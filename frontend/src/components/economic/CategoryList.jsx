import './CategoryList.css';

/**
 * Componente para mostrar la lista de categorías con sus montos
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.categories - Array de objetos con datos de categorías (category, amount, color)
 */
function CategoryList({ categories }) {
  // Si no hay categorías, mostramos un mensaje
  if (!categories || categories.length === 0) {
    return <div className="no-categories">No hay categorías disponibles</div>;
  }

  return (
    <div className="categories-list">
      {categories.map((category, index) => (
        <div key={`${category.category}-${index}`} className="category-item">
          <div className="category-info">
            <div 
              className="category-indicator" 
              style={{ backgroundColor: category.color }}
            ></div>
            <span className="category-name">{category.category}</span>
          </div>
          <span className="category-amount">${category.amount.toLocaleString()}</span>
        </div>
      ))}
    </div>
  );
}

export default CategoryList;