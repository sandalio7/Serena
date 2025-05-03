import React, { useState, useEffect } from 'react';
import { financialService } from '../../services/api';
import FinancialSummaryCard from './FinancialSummaryCard';
import ExpensePieChart from './ExpensePieChart';
import ExpenseSummaryCard from './ExpenseSummaryCard';
import ExpenseHistoryCard from './ExpenseHistoryCard';
import AddTransactionForm from './AddTransactionForm';

function FinancialDashboard({ patientId }) {
  const [financialData, setFinancialData] = useState(null);
  const [categories, setCategories] = useState([]);
  const [period, setPeriod] = useState('month');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Función para cargar datos financieros
  const loadFinancialData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Cargar el resumen financiero
      const summary = await financialService.getSummary(patientId, period);
      setFinancialData(summary);
      
      // Cargar las categorías de gastos
      const expenseCategories = await financialService.getExpensesByCategory(patientId, period);
      setCategories(expenseCategories);
      
    } catch (err) {
      console.error('Error loading financial data:', err);
      setError('No se pudieron cargar los datos financieros');
    } finally {
      setLoading(false);
    }
  };

  // Cargar datos cuando cambia el paciente o el período
  useEffect(() => {
    if (patientId) {
      loadFinancialData();
    }
  }, [patientId, period]);

  // Manejar registro de nueva transacción
  const handleAddTransaction = async (transactionData) => {
    // Agregar el ID del paciente a los datos
    const dataToSend = {
      ...transactionData,
      patient_id: patientId
    };
    
    // Enviar al backend
    await financialService.registerTransaction(dataToSend);
    
    // Recargar datos
    loadFinancialData();
  };

  // Manejar cambio de período
  const handlePeriodChange = (e) => {
    setPeriod(e.target.value);
  };

  // Si está cargando, mostrar indicador
  if (loading && !financialData) {
    return (
      <div className="financial-dashboard p-4">
        <p className="text-center">Cargando datos financieros...</p>
      </div>
    );
  }

  // Si hay error, mostrar mensaje
  if (error) {
    return (
      <div className="financial-dashboard p-4">
        <div className="bg-red-100 text-red-700 p-3 rounded">
          <p>{error}</p>
          <button 
            onClick={loadFinancialData}
            className="mt-2 bg-red-700 text-white px-3 py-1 rounded text-sm"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="financial-dashboard p-4">
      <div className="mb-4 flex flex-wrap justify-between items-center">
        <h2 className="text-xl font-bold">Dashboard Financiero</h2>
        
        <div className="flex items-center">
          <label className="mr-2">Período:</label>
          <select 
            value={period} 
            onChange={handlePeriodChange}
            className="p-2 border rounded"
          >
            <option value="day">Hoy</option>
            <option value="week">Esta semana</option>
            <option value="fortnight">Esta quincena</option>
            <option value="month">Este mes</option>
          </select>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <FinancialSummaryCard 
          type="income" 
          amount={financialData?.income || 0} 
          period={period}
        />
        <FinancialSummaryCard 
          type="expense" 
          amount={financialData?.expenses || 0} 
          period={period}
        />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <ExpensePieChart categories={categories} />
            <ExpenseSummaryCard categories={categories} />
          </div>
          
          <ExpenseHistoryCard expenses={categories.map(cat => ({
            category: cat.name,
            amount: cat.amount,
            date: new Date().toISOString().split('T')[0] // Fecha actual como ejemplo
          }))} />
        </div>
        
        <div>
          <AddTransactionForm onSubmit={handleAddTransaction} />
        </div>
      </div>
    </div>
  );
}

export default FinancialDashboard;