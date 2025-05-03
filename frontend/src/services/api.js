// src/services/api.js
const API_URL = 'http://localhost:5000'; // Ajusta esta URL según la configuración de tu backend

// Función genérica para hacer peticiones a la API
async function fetchApi(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Funciones para obtener pacientes
export const patientService = {
  getPatients: async () => {
    return fetchApi('/api/list');
  }
};

// Funciones para datos financieros
export const financialService = {
  // Obtener resumen financiero
  getSummary: async (patientId, period = 'month') => {
    return fetchApi(`/api/financial/summary?patient_id=${patientId}&period=${period}`);
  },
  
  // Obtener gastos por categoría
  getExpensesByCategory: async (patientId, period = 'month') => {
    return fetchApi(`/api/financial/expenses/categories?patient_id=${patientId}&period=${period}`);
  },
  
  // Registrar nuevo movimiento
  registerTransaction: async (transactionData) => {
    return fetchApi('/api/financial/transactions', {
      method: 'POST',
      body: JSON.stringify(transactionData),
    });
  }
};

// Funciones para datos de salud
export const healthService = {
  // Obtener datos de salud
  getHealthData: async (patientId, period = 'month') => {
    return fetchApi(`/api/health/summary?patient_id=${patientId}&period=${period}`);
  },
  
  // Obtener historial de métricas
  getMetricsHistory: async (patientId, metricType, period = 'month') => {
    return fetchApi(`/api/health/metrics/${metricType}?patient_id=${patientId}&period=${period}`);
  }
};

export default {
  patient: patientService,
  financial: financialService,
  health: healthService
};