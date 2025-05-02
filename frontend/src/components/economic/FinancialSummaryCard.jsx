// src/components/economic/FinancialSummaryCard.jsx
function FinancialSummaryCard({ type, amount }) {
    const isIncome = type === 'income';
    
    return (
      <div className={isIncome ? 'income-card' : 'expense-card'}>
        <h3>{isIncome ? 'Ingresos totales' : 'Gastos totales'}</h3>
        <p className="amount">${amount.toLocaleString()}</p>
      </div>
    );
  }
  
  export default FinancialSummaryCard;