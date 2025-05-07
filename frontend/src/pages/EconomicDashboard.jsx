import { useState, useEffect } from 'react';
import PeriodSelector from '../components/common/PeriodSelector';
import ExpenseCard from '../components/economic/ExpenseCard';
import ExpensesByCategorySection from '../components/economic/ExpensesByCategorySection';
import TransactionHistory from '../components/economic/TransactionHistory';
import FormularioRegistro from '../components/economic/FormularioRegistro';
import { 
  getFinancialSummary, 
  getExpensesByCategory, 
  getTransactionsHistory,
  registerTransaction,
  updateTransaction,
  deleteTransaction
} from '../services/financialService';
import './EconomicDashboard.css';

/**
 * Dashboard económico principal
 */
function EconomicDashboard() {
  // ID del paciente (en una aplicación real podría venir de un contexto o prop)
  const patientId = 1;
  
  // Estado para el período seleccionado
  const [selectedPeriod, setSelectedPeriod] = useState('day');
  
  // Estados independientes para cada sección
  const [expenseTotalData, setExpenseTotalData] = useState({
    totalExpense: 0,
    loading: true,
    error: null
  });
  
  const [expensesData, setExpensesData] = useState({
    categories: [],
    loading: true,
    error: null
  });
  
  const [transactionsData, setTransactionsData] = useState({
    items: [],
    loading: true,
    error: null
  });
  
  // Manejar cambio de período - solo afecta a gastos por categoría y transacciones
  const handlePeriodChange = (period) => {
    setSelectedPeriod(period);
    // Solo activamos carga para los componentes que se actualizarán
    setExpensesData(prev => ({ ...prev, loading: true, error: null }));
    setTransactionsData(prev => ({ ...prev, loading: true, error: null }));
  };
  
  // Cargar datos de gastos totales (independiente del período)
  useEffect(() => {
    const loadExpenseTotalData = async () => {
      try {
        console.log('Cargando datos de gastos totales...');
        // Obtener datos del resumen financiero
        const summaryData = await getFinancialSummary(patientId, 'month');
        
        if (summaryData.error) {
          console.error('Error en resumen financiero:', summaryData.message);
          setExpenseTotalData({
            totalExpense: 0,
            loading: false,
            error: summaryData.message
          });
          return;
        }
        
        setExpenseTotalData({
          totalExpense: summaryData.expenses || 0,
          loading: false,
          error: null
        });
      } catch (error) {
        console.error('Error inesperado cargando gastos totales:', error);
        setExpenseTotalData({
          totalExpense: 0,
          loading: false,
          error: 'Error al cargar los gastos totales'
        });
      }
    };
    
    loadExpenseTotalData();
  }, []); // Solo se ejecuta una vez al montar el componente
  
  // Cargar datos de gastos por categoría (depende del período)
  useEffect(() => {
    const loadExpensesData = async () => {
      try {
        console.log(`Cargando gastos por categoría para período: ${selectedPeriod}...`);
        // Obtener datos de gastos por categoría
        const categoriesData = await getExpensesByCategory(patientId, selectedPeriod);
        
        if (categoriesData.error) {
          console.error('Error en gastos por categoría:', categoriesData.message);
          setExpensesData({
            categories: [],
            loading: false,
            error: categoriesData.message
          });
          return;
        }
        
        // Adaptar formato de los datos si es necesario
        const formattedCategories = Array.isArray(categoriesData) 
          ? categoriesData.map(cat => ({
              category: cat.name,
              amount: cat.amount,
              color: cat.color
            }))
          : [];
        
        setExpensesData({
          categories: formattedCategories,
          loading: false,
          error: null
        });
      } catch (error) {
        console.error('Error inesperado cargando gastos por categoría:', error);
        setExpensesData({
          categories: [],
          loading: false,
          error: 'Error al cargar los gastos por categoría'
        });
      }
    };
    
    loadExpensesData();
  }, [selectedPeriod, patientId]); // Se ejecuta cada vez que cambia el período
  
  // Cargar datos de transacciones (depende del período)
  useEffect(() => {
    const loadTransactionsData = async () => {
      try {
        console.log(`Cargando historial de transacciones para período: ${selectedPeriod}...`);
        // Obtener datos de transacciones
        const transactionsHistory = await getTransactionsHistory(patientId, selectedPeriod);
        
        if (transactionsHistory.error) {
          console.error('Error en historial de transacciones:', transactionsHistory.message);
          setTransactionsData({
            items: [],
            loading: false,
            error: transactionsHistory.message
          });
          return;
        }
        
        setTransactionsData({
          items: Array.isArray(transactionsHistory) ? transactionsHistory : [],
          loading: false,
          error: null
        });
      } catch (error) {
        console.error('Error inesperado cargando historial de transacciones:', error);
        setTransactionsData({
          items: [],
          loading: false,
          error: 'Error al cargar el historial de transacciones'
        });
      }
    };
    
    loadTransactionsData();
  }, [selectedPeriod, patientId]); // Se ejecuta cada vez que cambia el período
  
  // Manejar el registro de una nueva transacción
  const handleRegisterTransaction = async (formData) => {
    try {
      // Preparar datos para el backend
      const transactionData = {
        patient_id: patientId,
        type: 'expense', // Por ahora solo manejamos gastos
        category: formData.category,
        amount: formData.amount,
        date: new Date().toISOString().split('T')[0], // Formato YYYY-MM-DD
        description: `Registro manual: ${formData.description || 'Sin descripción'}`
      };
      
      console.log('Registrando transacción:', transactionData);
      
      // Llamar al servicio para registrar la transacción
      const result = await registerTransaction(transactionData);
      
      if (result.error) {
        alert(`Error al registrar la transacción: ${result.message}`);
        return;
      }
      
      // Recargar los datos
      setExpensesData(prev => ({ ...prev, loading: true }));
      setTransactionsData(prev => ({ ...prev, loading: true }));
      setExpenseTotalData(prev => ({ ...prev, loading: true }));
      
      // Mostrar mensaje de éxito
      alert('Transacción registrada exitosamente');
    } catch (error) {
      console.error('Error al registrar la transacción:', error);
      alert('Error al registrar la transacción. Inténtelo nuevamente.');
    }
  };
  
  // Manejar la actualización de una transacción
  const handleTransactionUpdate = async (updatedTransaction) => {
    try {
      console.log('Actualizando transacción:', updatedTransaction);
      
      // Llamar al servicio para actualizar la transacción
      const result = await updateTransaction(updatedTransaction);
      
      if (result.error) {
        alert(`Error al actualizar la transacción: ${result.message}`);
        return;
      }
      
      // Recargar los datos
      setExpensesData(prev => ({ ...prev, loading: true }));
      setTransactionsData(prev => ({ ...prev, loading: true }));
      setExpenseTotalData(prev => ({ ...prev, loading: true }));
      
      // Mostrar mensaje de éxito
      alert('Transacción actualizada exitosamente');
    } catch (error) {
      console.error('Error al actualizar la transacción:', error);
      alert('Error al actualizar la transacción. Inténtelo nuevamente.');
    }
  };
  
  // Manejar la eliminación de una transacción
  const handleTransactionDelete = async (transactionId) => {
    try {
      console.log('Eliminando transacción:', transactionId);
      
      // Llamar al servicio para eliminar la transacción
      const result = await deleteTransaction(transactionId);
      
      if (result.error) {
        alert(`Error al eliminar la transacción: ${result.message}`);
        return;
      }
      
      // Recargar los datos
      setExpensesData(prev => ({ ...prev, loading: true }));
      setTransactionsData(prev => ({ ...prev, loading: true }));
      setExpenseTotalData(prev => ({ ...prev, loading: true }));
      
      // Mostrar mensaje de éxito
      alert('Transacción eliminada exitosamente');
    } catch (error) {
      console.error('Error al eliminar la transacción:', error);
      alert('Error al eliminar la transacción. Inténtelo nuevamente.');
    }
  };
  
  return (
    <div className="economic-dashboard">
      <h1>Dashboard Económico</h1>
      
      {/* Gastos totales (no se actualiza con el período) */}
      <ExpenseCard 
        amount={expenseTotalData.totalExpense} 
        loading={expenseTotalData.loading}
        error={expenseTotalData.error}
      />
      
      {/* Selector de período - afecta solo a gastos por categoría y transacciones */}
      <PeriodSelector 
        selectedPeriod={selectedPeriod}
        onPeriodChange={handlePeriodChange}
      />
      
      <div className="dashboard-content">
        {/* Gastos por categoría (se actualiza con el período) */}
        <ExpensesByCategorySection 
          categories={expensesData.categories} 
          loading={expensesData.loading}
          error={expensesData.error}
        />
        
        {/* Formulario de registro con campo de descripción */}
        <FormularioRegistro onRegister={handleRegisterTransaction} />
        
        {/* Historial de transacciones (se actualiza con el período) */}
        <TransactionHistory 
          transactions={transactionsData.items} 
          loading={transactionsData.loading}
          error={transactionsData.error}
          onTransactionUpdate={handleTransactionUpdate}
          onTransactionDelete={handleTransactionDelete}
        />
      </div>
    </div>
  );
}

export default EconomicDashboard;