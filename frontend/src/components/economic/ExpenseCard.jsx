import './ExpenseCard.css';

/**
 * Tarjeta que muestra los gastos totales
 * @param {Object} props - Propiedades del componente
 * @param {number} props.amount - Monto total de gastos
 * @param {boolean} props.loading - Indica si los datos están cargando
 * @param {string} props.error - Mensaje de error, si existe
 */
function ExpenseCard({ amount, loading, error }) {
  return (
    <div className="expense-card card">
      <h2>Gastos Totales</h2>
      
      {loading && (
        <div className="loading-indicator">Cargando...</div>
      )}
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
      
      {!loading && !error && (
        <div className="expense-amount">
          <span className="amount">${amount?.toLocaleString() || '0'}</span>
        </div>
      )}
    </div>
  );
}

export default ExpenseCard;