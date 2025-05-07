import { useState, useEffect } from 'react';
import './EditModal.css';

/**
 * Modal para editar o eliminar una transacción
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.transaction - Datos de la transacción a editar
 * @param {boolean} props.isOpen - Si el modal está abierto
 * @param {Function} props.onClose - Función para cerrar el modal
 * @param {Function} props.onSave - Función para guardar cambios
 * @param {Function} props.onDelete - Función para eliminar la transacción
 */
function EditModal({ transaction, isOpen, onClose, onSave, onDelete }) {
  const [formData, setFormData] = useState({
    amount: '',
    description: ''
  });
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);
  
  // Actualizar formulario cuando cambia la transacción
  useEffect(() => {
    if (transaction) {
      setFormData({
        amount: transaction.amount,
        description: transaction.description || ''
      });
    }
  }, [transaction]);

  // Manejar cambios en los campos
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Guardar cambios
  const handleSave = () => {
    // Validar que los campos obligatorios estén llenos
    if (!formData.amount) {
      alert('El monto es obligatorio');
      return;
    }

    // Llamar a la función onSave con los datos actualizados
    onSave({
      ...transaction,
      amount: parseFloat(formData.amount),
      description: formData.description,
      edited: true // Marcar como editado
    });

    // Cerrar modal y resetear estado
    handleClose();
  };

  // Solicitar confirmación para eliminar
  const handleDeleteClick = () => {
    setShowConfirmDelete(true);
  };

  // Confirmar eliminación
  const handleConfirmDelete = () => {
    onDelete(transaction.id);
    handleClose();
  };

  // Cerrar modal y resetear estado
  const handleClose = () => {
    setShowConfirmDelete(false);
    onClose();
  };

  // Si el modal no está abierto, no renderizar nada
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-header">
          <h3>Editar Transacción</h3>
          <button className="close-modal-btn" onClick={handleClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="form-group">
            <label htmlFor="modal-category">Categoría</label>
            <input 
              type="text" 
              id="modal-category" 
              value={transaction?.category || ''} 
              disabled 
              className="form-control"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="modal-amount">Monto</label>
            <input 
              type="number" 
              id="modal-amount" 
              name="amount"
              value={formData.amount} 
              onChange={handleChange}
              className="form-control"
              min="0"
              step="0.01"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="modal-description">Descripción</label>
            <textarea 
              id="modal-description" 
              name="description"
              value={formData.description} 
              onChange={handleChange}
              className="form-control description-textarea"
              rows="3"
            ></textarea>
          </div>
          
          {showConfirmDelete ? (
            <div className="confirm-delete-container">
              <p className="confirm-message">¿Está seguro que desea eliminar esta transacción?</p>
              <div className="confirm-buttons">
                <button 
                  className="cancel-btn"
                  onClick={() => setShowConfirmDelete(false)}
                >
                  Cancelar
                </button>
                <button 
                  className="confirm-delete-btn"
                  onClick={handleConfirmDelete}
                >
                  Sí, eliminar
                </button>
              </div>
            </div>
          ) : (
            <div className="modal-actions">
              <button 
                className="delete-btn"
                onClick={handleDeleteClick}
              >
                Eliminar
              </button>
              <button 
                className="save-btn"
                onClick={handleSave}
              >
                Guardar cambios
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default EditModal;