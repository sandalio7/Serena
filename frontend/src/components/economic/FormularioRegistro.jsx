import { useState } from 'react';
import './FormularioRegistro.css';

/**
 * Componente de formulario para registrar nuevas transacciones
 * @param {Object} props - Propiedades del componente
 * @param {Function} props.onRegister - Función a llamar cuando se registra una transacción
 */
function FormularioRegistro({ onRegister }) {
  const [formData, setFormData] = useState({
    category: '',
    amount: '',
    description: ''
  });

  // Maneja cambios en los campos del formulario
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [id]: value
    }));
  };

  // Maneja el envío del formulario
  const handleSubmit = () => {
    // Validar que los campos obligatorios estén llenos
    if (!formData.category || !formData.amount) {
      alert('Por favor, complete los campos de categoría y monto');
      return;
    }

    // Crear objeto de transacción
    const transactionData = {
      category: formData.category,
      amount: parseFloat(formData.amount),
      description: formData.description || 'Sin descripción'
    };

    // Llamar a la función proporcionada por el padre
    onRegister(transactionData);

    // Limpiar formulario
    setFormData({
      category: '',
      amount: '',
      description: ''
    });
  };

  return (
    <div className="register-form">
      <div className="form-controls">
        <div className="form-group">
          <select 
            className="form-control" 
            id="category"
            value={formData.category}
            onChange={handleChange}
          >
            <option value="">Seleccione categoría</option>
            <option value="Vivienda">Vivienda</option>
            <option value="Servicios básicos">Servicios básicos</option>
            <option value="Cuidados">Cuidados</option>
            <option value="Salud">Salud</option>
            <option value="Supermercado">Supermercado</option>
            <option value="Transporte">Transporte</option>
            <option value="Medicamentos">Medicamentos</option>
            <option value="Recreación">Recreación</option>
            <option value="Otros">Otros</option>
          </select>
        </div>
        
        <div className="form-group">
          <input 
            type="number" 
            className="form-control" 
            id="amount"
            placeholder="Monto" 
            min="0" 
            step="0.01"
            value={formData.amount}
            onChange={handleChange}
          />
        </div>
      </div>
      
      <div className="form-group description-group">
        <input 
          type="text" 
          className="form-control description-input" 
          id="description"
          placeholder="Descripción (opcional)"
          value={formData.description}
          onChange={handleChange}
        />
      </div>
      
      <button 
        className="register-btn"
        onClick={handleSubmit}
      >
        Registrar
      </button>
    </div>
  );
}

export default FormularioRegistro;