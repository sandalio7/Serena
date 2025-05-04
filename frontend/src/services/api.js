// src/services/api.js
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

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
      const error = await response.json();
      throw new Error(error.error || `Error: ${response.status}`);
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
    return fetchApi('/api/patient/list');
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
  
  // Registrar nueva transacción
  registerTransaction: async (transactionData) => {
    return fetchApi('/api/financial/transactions', {
      method: 'POST',
      body: JSON.stringify(transactionData),
    });
  },
  
  // Obtener historial de mensajes con gastos (nueva función)
  getExpenseHistory: async (patientId, period = 'month') => {
    return fetchApi(`/api/financial/messages-history?patient_id=${patientId}&period=${period}`);
  }
};

// Funciones para datos de salud (pendiente de implementar en backend)
export const healthService = {
  // Obtener datos de salud
  getHealthData: async (patientId, period = 'month') => {
    try {
      return await fetchApi(`/api/health/summary?patient_id=${patientId}&period=${period}`);
    } catch (error) {
      console.error('Error fetching health data:', error);
      // Si hay un error, devolver un objeto con datos vacíos y un mensaje
      return {
        data_available: false,
        message: 'No se pudieron cargar los datos de salud',
        physicalVars: {
          bloodPressure: { value: '', status: '' },
          temperature: { value: '', status: '' },
          oxygenSaturation: { value: '', status: '' },
          weight: { value: '', status: '', bmi: '' }
        },
        sleep: { hours: '', status: '' },
        cognitiveState: { rating: 0, description: '' },
        physicalState: { rating: 0, description: '' },
        emotionalState: { rating: 0, description: '' },
        generalConclusion: ''
      };
    }
  },
  
  // Obtener historial de métricas
  getMetricsHistory: async (patientId, metricType, period = 'month') => {
    try {
      return await fetchApi(`/api/health/metrics/${metricType}?patient_id=${patientId}&period=${period}`);
    } catch (error) {
      console.error('Error fetching metrics history:', error);
      return [];
    }
  },
  
  // Nueva función para obtener el historial de salud
  getHealthHistory: async (patientId, period = 'day', category = '') => {
    try {
      let url = `/api/health/history?patient_id=${patientId}&period=${period}`;
      if (category) {
        url += `&category=${category}`;
      }
      
      const response = await fetchApi(url);
      return response.history || [];
    } catch (error) {
      console.error('Error fetching health history:', error);
      return [];
    }
  }
};

export const api = {
  get: (endpoint, options) => fetchApi(endpoint, { method: 'GET', ...options }),
  post: (endpoint, data, options) => fetchApi(endpoint, { 
    method: 'POST', 
    body: JSON.stringify(data), 
    ...options 
  }),
  put: (endpoint, data, options) => fetchApi(endpoint, { 
    method: 'PUT', 
    body: JSON.stringify(data), 
    ...options 
  }),
  delete: (endpoint, options) => fetchApi(endpoint, { method: 'DELETE', ...options }),
};

export default {
  patient: patientService,
  financial: financialService,
  health: healthService
};