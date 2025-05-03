import React from 'react';

function ExpenseSummaryCard({ categories }) {
  if (!categories || categories.length === 0) {
    return (
      <div className="expense-summary-card bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-2">Resumen de Gastos</h3>
        <p className="text-gray-500">No hay datos de gastos disponibles</p>
      </div>
    );
  }

  // Ordenar categorías por monto (de mayor a menor)
  const sortedCategories = [...categories].sort((a, b) => b.amount - a.amount);

  return (
    <div className="expense-summary-card bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-3">Resumen de Gastos</h3>
      <div className="space-y-2">
        {sortedCategories.map((category, index) => (
          <div key={index} className="flex justify-between items-center py-1 border-b border-gray-100">
            <div className="flex items-center">
              <div 
                className="w-3 h-3 rounded-full mr-2" 
                style={{ backgroundColor: category.color }}
              ></div>
              <span>{category.name}</span>
            </div>
            <span className="font-medium">${category.amount.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExpenseSummaryCard;