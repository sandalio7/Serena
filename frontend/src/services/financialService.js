/**
 * Servicio para interactuar con las APIs financieras del backend
 */

// URL base para las APIs financieras
const API_BASE_URL = '/api/financial';

/**
 * Verifica si la respuesta es JSON válido o muestra un error detallado
 * @param {Response} response - Respuesta fetch
 * @returns {Promise<any>} - Datos JSON o error
 */
const handleResponse = async (response) => {
  // Primero verificamos si la respuesta es exitosa
  if (!response.ok) {
    // Intentamos obtener detalles del error
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      // Si el error está en formato JSON, lo extraemos
      const errorData = await response.json();
      throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
    } else {
      // Si no es JSON, mostramos el texto del error
      const errorText = await response.text();
      console.error('Respuesta no JSON:', errorText.substring(0, 150) + '...');
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
  }

  // Si la respuesta es exitosa, verificamos que sea JSON
  const contentType = response.headers.get('content-type');
  if (!contentType || !contentType.includes('application/json')) {
    // Si no es JSON, es un problema en el servidor
    const text = await response.text();
    console.error('Respuesta no JSON:', text.substring(0, 150) + '...');
    throw new Error('La respuesta del servidor no es JSON válido');
  }

  // Parece ser JSON válido, lo devolvemos
  return await response.json();
};

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
    return await handleResponse(response);
  } catch (error) {
    console.error('Error obteniendo resumen financiero:', error);
    // Devolvemos un objeto de error para manejarlo en el componente
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
    return await handleResponse(response);
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
    const data = await handleResponse(response);
    
    // Formatear datos para adaptarlos a nuestro componente
    return data.map(item => ({
      id: item.message_id,
      category: item.category.name,
      description: item.message,
      amount: item.amount,
      date: formatDate(new Date(item.date)),
      color: item.category.color
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
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error registrando transacción:', error);
    return { 
      error: true, 
      message: error.message || 'Error registrando transacción'
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
  registerTransaction
};