import React from 'react';

function ExpenseHistoryCard({ expenses }) {
  // Si no hay gastos o está vacío, mostrar mensaje
  if (!expenses || expenses.length === 0) {
    return (
      <div className="expense-history-card bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-2">Historial de Gastos</h3>
        <p className="text-gray-500">No hay historial de gastos disponible</p>
      </div>
    );
  }

  return (
    <div className="expense-history-card bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-3">Historial de Gastos</h3>
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {expenses.map((expense, index) => (
          <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
            <div>
              <p className="font-medium">{expense.category}</p>
              <p className="text-sm text-gray-500">{new Date(expense.date).toLocaleDateString()}</p>
            </div>
            <span className="text-red-500 font-medium">-${expense.amount.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExpenseHistoryCard;