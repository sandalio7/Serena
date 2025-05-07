import { useState } from 'react';
import TransactionItem from './TransactionItem';
import './TransactionHistory.css';

/**
 * Componente para mostrar el historial de transacciones
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.transactions - Array de objetos con datos de transacciones
 * @param {boolean} props.loading - Indica si los datos están cargando
 * @param {string} props.error - Mensaje de error, si existe
 * @param {Function} props.onTransactionUpdate - Función para actualizar una transacción
 * @param {Function} props.onTransactionDelete - Función para eliminar una transacción
 */
function TransactionHistory({ 
  transactions, 
  loading, 
  error, 
  onTransactionUpdate,
  onTransactionDelete 
}) {
  // Verificamos que transactions sea un array y tenga elementos
  const hasTransactions = Array.isArray(transactions) && transactions.length > 0;

  // Manejar la edición de una transacción
  const handleEdit = (updatedTransaction) => {
    if (onTransactionUpdate) {
      onTransactionUpdate(updatedTransaction);
    }
  };

  // Manejar la eliminación de una transacción
  const handleDelete = (transactionId) => {
    if (onTransactionDelete) {
      onTransactionDelete(transactionId);
    }
  };

  if (loading) {
    return (
      <div className="transactions-history">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">Cargando transacciones...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="transactions-history">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <h3 className="error-title">Error al cargar transacciones</h3>
          <p className="error-message">{error}</p>
          <p className="error-help">Intente de nuevo más tarde o contacte al soporte técnico.</p>
        </div>
      </div>
    );
  }

  if (!hasTransactions) {
    return (
      <div className="transactions-history">
        <div className="empty-container">
          <div className="empty-icon">📋</div>
          <h3 className="empty-title">No hay transacciones</h3>
          <p className="empty-message">No se encontraron transacciones para mostrar en el período seleccionado.</p>
          <div className="empty-actions">
            <p className="empty-suggestion">Intente seleccionar un período diferente o registre nuevas transacciones.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="transactions-history">
      <h3 className="section-title">Historial de Transacciones</h3>
      
      {/* Iteramos a través de las transacciones para mostrarlas */}
      {transactions.map(transaction => (
        <TransactionItem
          key={transaction.id}
          transaction={transaction}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}

export default TransactionHistory;