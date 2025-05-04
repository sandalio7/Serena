import React from 'react';

function ExpenseHistoryList({ expenseHistory }) {
  // Si no hay datos de historial, mostrar mensaje
  if (!expenseHistory || expenseHistory.length === 0) {
    return (
      <div className="expense-history-list card">
        <h3>Historial de Gastos</h3>
        <p className="empty-message">No hay historial de gastos disponible</p>
      </div>
    );
  }

  return (
    <div className="expense-history-list card">
      <h3>Historial de Gastos</h3>
      <div className="history-container">
        {expenseHistory.map((item, index) => (
          <div key={index} className="history-item">
            <div className="history-item-header">
              <div className="category-info">
                <span 
                  className="color-indicator" 
                  style={{ backgroundColor: item.category.color }}
                ></span>
                <span className="category-name">{item.category.name}</span>
              </div>
              <span className="amount">${item.amount.toLocaleString()}</span>
            </div>
            
            <div className="date-info">
              {new Date(item.date).toLocaleDateString()}
            </div>
            
            <p className="message-content">
              Gasto de ${item.amount.toLocaleString()} en {item.category.name.toLowerCase()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExpenseHistoryList;