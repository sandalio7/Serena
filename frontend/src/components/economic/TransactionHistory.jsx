import './TransactionHistory.css';

/**
 * Componente para mostrar el historial de transacciones
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.transactions - Array de objetos con datos de transacciones
 * @param {boolean} props.loading - Indica si los datos están cargando
 * @param {string} props.error - Mensaje de error, si existe
 */
function TransactionHistory({ transactions, loading, error }) {
  if (loading) {
    return (
      <div className="transactions-history">
        <div className="loading-indicator">Cargando transacciones...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="transactions-history">
        <div className="error-message">Error: {error}</div>
      </div>
    );
  }

  if (!transactions || transactions.length === 0) {
    return (
      <div className="transactions-history">
        <div className="no-transactions">No hay transacciones para mostrar</div>
      </div>
    );
  }

  return (
    <div className="transactions-history">
      {transactions.map(transaction => (
        <div key={transaction.id} className="transaction-item">
          <div className="transaction-header">
            <div className="transaction-category">
              <div className="category-dot" style={{ backgroundColor: transaction.color }}></div>
              <span>{transaction.category}</span>
            </div>
            <div className="transaction-date">{transaction.date}</div>
          </div>
          
          <div className="transaction-description">"{transaction.description}"</div>
          
          <div className="transaction-details">
            <span className="transaction-amount">${transaction.amount.toLocaleString()}</span>
            <button className="edit-btn">editar</button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TransactionHistory;