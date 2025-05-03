import React, { useState } from 'react';

function AddTransactionForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    type: 'expense',
    category: '',
    amount: '',
    date: new Date().toISOString().split('T')[0],
    description: ''
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const categories = [
    'Vivienda',
    'Servicios básicos',
    'Cuidados',
    'Salud',
    'Supermercado',
    'Transporte',
    'Medicamentos',
    'Recreación',
    'Varios',
    'Otros'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Validación básica
    if (!formData.category || !formData.amount || !formData.date) {
      setError('Por favor complete todos los campos requeridos');
      return;
    }
    
    try {
      setLoading(true);
      await onSubmit(formData);
      // Resetear el formulario después de enviar
      setFormData({
        type: 'expense',
        category: '',
        amount: '',
        date: new Date().toISOString().split('T')[0],
        description: ''
      });
    } catch (err) {
      setError(err.message || 'Error al registrar la transacción');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-transaction-form bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-3">Registrar Transacción</h3>
      
      {error && (
        <div className="bg-red-100 text-red-700 p-2 rounded mb-3">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1">Tipo de transacción</label>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="expense">Gasto</option>
            <option value="income">Ingreso</option>
          </select>
        </div>
        
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1">Categoría</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Seleccione una categoría</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
        
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1">Monto</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            min="0"
            step="0.01"
            className="w-full p-2 border rounded"
            placeholder="0.00"
          />
        </div>
        
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1">Fecha</label>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1">Descripción (opcional)</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            rows="2"
            placeholder="Descripción opcional de la transacción"
          ></textarea>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded font-medium hover:bg-blue-700 disabled:bg-blue-300"
        >
          {loading ? 'Guardando...' : 'Guardar Transacción'}
        </button>
      </form>
    </div>
  );
}

export default AddTransactionForm;