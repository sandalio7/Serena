import React from 'react';

function FinancialSummaryCard({ type, amount, period }) {
  const isIncome = type === 'income';
  const title = isIncome ? 'Ingresos' : 'Gastos';
  const icon = isIncome ? '💰' : '💸';
  const colorClass = isIncome ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
  
  // Formatear el período para mostrarlo
  let periodText = '';
  switch (period) {
    case 'day':
      periodText = 'de hoy';
      break;
    case 'week':
      periodText = 'de esta semana';
      break;
    case 'fortnight':
      periodText = 'de esta quincena';
      break;
    default:
      periodText = 'de este mes';
  }
  
  return (
    <div className={`financial-summary-card p-4 rounded-lg shadow ${colorClass}`}>
      <div className="flex items-center mb-2">
        <span className="text-2xl mr-2">{icon}</span>
        <h3 className="text-lg font-semibold">{title} {periodText}</h3>
      </div>
      <p className="text-3xl font-bold">${amount?.toLocaleString() || '0'}</p>
    </div>
  );
}

export default FinancialSummaryCard;