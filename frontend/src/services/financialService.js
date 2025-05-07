/**
 * Servicio para interactuar con las APIs financieras del backend
 */

// URL base para las APIs financieras
const API_BASE_URL = '/api/financial';

/**
 * Obtiene el resumen financiero para un paciente y período
 * @param {number} patientId - ID del paciente
 * @param {string} period - Período ('day', 'week', 'month')
 * @returns {Promise<Object>} - Datos del resumen financiero
 */
export const getFinancialSummary = async (patientId, period = 'month') => {
  try {
    const url = `${API_BASE_URL}/summary?patient_id=${patientId}&period=${period}`;
    console.log(`Solicitando resumen financiero: ${url}`);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error obteniendo resumen financiero:', error);
    return { 
      error: true, 
      message: error.message || 'Error obteniendo datos financieros'
    };
  }
};

/**
 * Obtiene los gastos por categoría para un paciente y período
 * @param {number} patientId - ID del paciente
 * @param {string} period - Período ('day', 'week', 'month')
 * @returns {Promise<Array>} - Lista de categorías con sus montos
 */
export const getExpensesByCategory = async (patientId, period = 'month') => {
  try {
    const url = `${API_BASE_URL}/expenses/categories?patient_id=${patientId}&period=${period}`;
    console.log(`Solicitando gastos por categoría: ${url}`);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error obteniendo gastos por categoría:', error);
    return { 
      error: true, 
      message: error.message || 'Error obteniendo gastos por categoría'
    };
  }
};

/**
 * Obtiene el historial de mensajes con gastos para un paciente y período
 * @param {number} patientId - ID del paciente
 * @param {string} period - Período ('day', 'week', 'month')
 * @returns {Promise<Array>} - Lista de mensajes con gastos
 */
export const getTransactionsHistory = async (patientId, period = 'month') => {
  try {
    const url = `${API_BASE_URL}/messages-history?patient_id=${patientId}&period=${period}`;
    console.log(`Solicitando historial de transacciones: ${url}`);
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Formatear datos para adaptarlos a nuestro componente
    return data.map(item => ({
      id: item.id,                   // ID de ClassifiedData (importante para editar/eliminar)
      message_id: item.message_id,   // Mantenemos message_id también
      category: item.category.name,
      description: item.message,
      amount: item.amount,
      date: formatDate(new Date(item.date)),
      color: item.category.color,
      edited: item.edited || false
    }));
  } catch (error) {
    console.error('Error obteniendo historial de transacciones:', error);
    return { 
      error: true, 
      message: error.message || 'Error obteniendo historial de transacciones'
    };
  }
};

/**
 * Registra una nueva transacción financiera
 * @param {Object} transactionData - Datos de la transacción
 * @returns {Promise<Object>} - Respuesta del servidor
 */
export const registerTransaction = async (transactionData) => {
  try {
    console.log(`Registrando transacción:`, transactionData);
    
    const response = await fetch(`${API_BASE_URL}/transactions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(transactionData)
    });
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error registrando transacción:', error);
    return { 
      error: true, 
      message: error.message || 'Error registrando transacción'
    };
  }
};

/**
 * Actualiza una transacción existente
 * @param {Object} transactionData - Datos actualizados de la transacción
 * @returns {Promise<Object>} - Respuesta del servidor
 */
export const updateTransaction = async (transactionData) => {
  try {
    // Asegurarse de que tenemos el ID correcto
    const transactionId = transactionData.id;
    if (!transactionId) {
      throw new Error('ID de transacción no proporcionado');
    }
    
    console.log(`Actualizando transacción ID ${transactionId}:`, transactionData);
    
    const response = await fetch(`${API_BASE_URL}/transactions/${transactionId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        description: transactionData.description,
        amount: transactionData.amount,
        edited: true
      })
    });
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error actualizando transacción:', error);
    return { 
      error: true, 
      message: error.message || 'Error actualizando transacción'
    };
  }
};

/**
 * Elimina una transacción
 * @param {string|number} transactionId - ID de la transacción a eliminar
 * @returns {Promise<Object>} - Respuesta del servidor
 */
export const deleteTransaction = async (transactionId) => {
  try {
    if (!transactionId) {
      throw new Error('ID de transacción no proporcionado');
    }
    
    console.log(`Eliminando transacción con ID: ${transactionId}`);
    
    const response = await fetch(`${API_BASE_URL}/transactions/${transactionId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error eliminando transacción:', error);
    return { 
      error: true, 
      message: error.message || 'Error eliminando transacción'
    };
  }
};

/**
 * Formatea una fecha como DD/MM/YY
 * @param {Date} date - Objeto de fecha
 * @returns {string} - Fecha formateada
 */
const formatDate = (date) => {
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear().toString().slice(-2);
  
  return `${day}/${month}/${year}`;
};

export default {
  getFinancialSummary,
  getExpensesByCategory,
  getTransactionsHistory,
  registerTransaction,
  updateTransaction,
  deleteTransaction
};