import { useState } from 'react';
import EditModal from './EditModal';
import './TransactionItem.css';

/**
 * Componente para mostrar un ítem de transacción
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.transaction - Datos de la transacción
 * @param {Function} props.onEdit - Función para manejar edición
 * @param {Function} props.onDelete - Función para manejar eliminación
 */
function TransactionItem({ transaction, onEdit, onDelete }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Destacar el monto de la transacción en la descripción
  const highlightAmountInDescription = (description, amount) => {
    if (!description) return '';
    
    // Convertir el monto a diferentes formatos para buscar
    const amountStr = String(amount);
    const amountWithComma = amount.toLocaleString().replace(',', '.');
    const amountWithDot = amount.toLocaleString().replace('.', ',');
    
    // Patrones a buscar
    const patterns = [
      amountStr,
      amountWithComma,
      amountWithDot,
      '$' + amountStr,
      '$' + amountWithComma,
      '$' + amountWithDot
    ];
    
    // Crear una expresión regular para buscar cualquiera de los patrones
    const regex = new RegExp(`(${patterns.join('|')})`, 'g');
    
    // Dividir la descripción basada en el regex
    const parts = description.split(regex);
    
    // Si no hay coincidencias, devolver la descripción original
    if (parts.length === 1) return description;
    
    // Renderizar cada parte, destacando las que coinciden con el regex
    return parts.map((part, index) => {
      if (patterns.includes(part) || patterns.some(p => p === part)) {
        return <span key={index} className="highlighted-amount">{part}</span>;
      }
      return part;
    });
  };
  
  // Asegurarse de tener una ID válida para editar/eliminar
  const transactionId = transaction.id || transaction.message_id;
  
  return (
    <>
      <div className="transaction-item">
        <div className="transaction-header">
          <div className="transaction-category">
            <div 
              className="category-dot" 
              style={{ backgroundColor: transaction.color || '#6b7280' }}
            ></div>
            <span>{transaction.category}</span>
            {transaction.edited && (
              <span className="edited-indicator" title="Transacción editada">
                ✎
              </span>
            )}
          </div>
          <div className="transaction-date">{transaction.date}</div>
        </div>
        
        <div className="transaction-description">
          "{highlightAmountInDescription(transaction.description, transaction.amount)}"
        </div>
        
        <div className="transaction-details">
          <span className="transaction-amount">${transaction.amount.toLocaleString()}</span>
          <button 
            className="edit-btn"
            onClick={() => setIsModalOpen(true)}
          >
            editar
          </button>
        </div>
      </div>
      
      <EditModal
        transaction={{...transaction, id: transactionId}}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={onEdit}
        onDelete={onDelete}
      />
    </>
  );
}

export default TransactionItem;