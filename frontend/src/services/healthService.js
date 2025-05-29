// services/healthService.js - ACTUALIZADO

/**
 * API de endpoints para el dashboard de salud
 */
const API_ENDPOINTS = {
  HEALTH_SUMMARY: '/api/health/summary',
  HEALTH_HISTORY: '/api/health/history',
  HEALTH_METRICS: '/api/health/metrics',
};

/**
 * Obtiene el resumen general de salud del paciente
 * @param {number} patientId - ID del paciente
 * @param {string} period - Período de tiempo ('day', 'week', 'month')
 * @returns {Promise<Object>} Resumen de salud completo
 */
export const getHealthSummary = async (patientId, period = 'day') => {
  try {
    const response = await fetch(`${API_ENDPOINTS.HEALTH_SUMMARY}?patient_id=${patientId}&period=${period}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Error al obtener resumen de salud');
    }
    
    // Verificar si hay datos válidos
    if (!data.physicalVars || !data.physicalVars.bloodPressure || 
        !data.physicalVars.temperature || !data.physicalVars.oxygenSaturation ||
        (data.physicalVars.bloodPressure.value === '120/80' && 
         data.physicalVars.temperature.value === '36.5' && 
         data.physicalVars.oxygenSaturation.value === '98')) {
      // Estos son valores por defecto del backend, probablemente no hay datos nuevos
      return {
        hasData: false,
        currentStatus: null,
        vitalSigns: null,
        normalValues: {
          bloodPressure: { systolic: 130, diastolic: 80 },
          temperature: 36.5,
          oxygenation: 98
        },
        weeklySummary: null
      };
    }
    
    // Transformar los datos del backend al formato que espera el frontend
    return {
      hasData: true,
      currentStatus: {
        status: getStatusFromConclusion(data.generalConclusion),
        score: getScoreFromConclusion(data.generalConclusion),
        emoji: getEmojiFromConclusion(data.generalConclusion)
      },
      vitalSigns: {
        bloodPressure: {
          systolic: parseInt(data.physicalVars.bloodPressure.value.split('/')[0]),
          diastolic: parseInt(data.physicalVars.bloodPressure.value.split('/')[1])
        },
        temperature: parseFloat(data.physicalVars.temperature.value.replace(',', '.')),
        oxygenation: parseInt(data.physicalVars.oxygenSaturation.value)
      },
      normalValues: {
        bloodPressure: { systolic: 130, diastolic: 80 },
        temperature: 36.5,
        oxygenation: 98
      },
      weeklySummary: {
        physical: {
          score: data.physicalState.rating,
          description: data.physicalState.description
        },
        cognitive: {
          score: data.cognitiveState.rating,
          description: data.cognitiveState.description
        },
        emotional: {
          score: data.emotionalState.rating,
          description: data.emotionalState.description
        },
        autonomy: {
          score: Math.max(6, data.physicalState.rating - 1), // Derivar autonomía de estado físico
          description: "Se deriva de los datos de estado físico"
        }
      }
    };
  } catch (error) {
    console.error('Error en getHealthSummary:', error);
    throw error;
  }
};

/**
 * Obtiene el historial de eventos de salud con filtros
 * @param {number} patientId - ID del paciente
 * @param {string} period - Período de tiempo ('day', 'week', 'month')
 * @param {string} category - Categoría de salud (opcional)
 * @returns {Promise<Array>} Lista de eventos de salud
 */
export const getHealthHistory = async (patientId, period = 'day', category = 'all') => {
  try {
    let params = `patient_id=${patientId}&period=${period}`;
    
    // Solo agregar categoría si no es 'all'
    if (category !== 'all') {
      // Mapear las categorías del frontend a las del backend
      const categoryMap = {
        'physical': 'physical',
        'cognitive': 'cognitive',
        'emotional': 'emotional',
        'autonomy': 'physical' // Autonomía está dentro de salud física
      };
      
      const backendCategory = categoryMap[category];
      if (backendCategory) {
        params += `&category=${backendCategory}`;
      }
    }
    
    const response = await fetch(`${API_ENDPOINTS.HEALTH_HISTORY}?${params}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Error al obtener historial de salud');
    }
    
    // Transformar los datos del backend al formato que espera el frontend
    return data.history.map(item => ({
      id: item.id,
      category: mapBackendToFrontendCategory(item.category), // 'physical', 'cognitive', etc.
      categoryName: item.category, // Nombre completo como "Estado Físico"
      description: item.value,
      date: formatDate(item.date, item.time),
      score: item.rating
    }));
  } catch (error) {
    console.error('Error en getHealthHistory:', error);
    throw error;
  }
};

/**
 * Actualiza un evento de salud
 * @param {number} eventId - ID del evento
 * @param {Object} eventData - Datos actualizados del evento
 * @returns {Promise<Object>} Evento actualizado
 */
export const updateHealthEvent = async (eventId, eventData) => {
  try {
    const response = await fetch(`${API_ENDPOINTS.HEALTH_HISTORY}/${eventId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        value: eventData.description,
        category: mapFrontendToBackendCategory(eventData.category),
        rating: eventData.score || 5
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Error al actualizar evento de salud');
    }
    
    return {
      id: data.id,
      category: mapBackendToFrontendCategory(data.category),
      categoryName: data.category,
      description: data.value,
      date: formatDate(data.date, data.time),
      score: data.rating
    };
  } catch (error) {
    console.error('Error en updateHealthEvent:', error);
    throw error;
  }
};

/**
 * Funciones auxiliares
 */
function getStatusFromConclusion(conclusion) {
  switch (conclusion) {
    case 'Bueno':
      return 'Bueno';
    case 'Regular':
      return 'Regular';
    case 'Malo':
      return 'Malo';
    default:
      return 'Regular';
  }
}

function getScoreFromConclusion(conclusion) {
  switch (conclusion) {
    case 'Bueno':
      return '8';
    case 'Regular':
      return '6';
    case 'Malo':
      return '4';
    default:
      return '5';
  }
}

function getEmojiFromConclusion(conclusion) {
  switch (conclusion) {
    case 'Bueno':
      return '😊';
    case 'Regular':
      return '🙂';
    case 'Malo':
      return '☹️';
    default:
      return '😐';
  }
}

function mapBackendToFrontendCategory(backendCategory) {
  const categoryMap = {
    'Estado Físico': 'physical',
    'Salud Física': 'physical',
    'Estado cognitivo': 'cognitive',
    'Estado Cognitivo': 'cognitive',
    'Estado emocional': 'emotional',
    'Estado Emocional': 'emotional',
    'Medicación': 'autonomy', // Tratamos medicación como parte de autonomía
    'Autonomía': 'autonomy'
  };
  
  return categoryMap[backendCategory] || 'physical';
}

function mapFrontendToBackendCategory(frontendCategory) {
  const categoryMap = {
    'physical': 'Estado Físico',
    'cognitive': 'Estado Cognitivo',
    'emotional': 'Estado Emocional',
    'autonomy': 'Autonomía'
  };
  
  return categoryMap[frontendCategory] || 'Estado Físico';
}

function formatDate(date, time) {
  // Convertir fecha DD/MM/YYYY y hora HH:MM a formato ISO
  const [day, month, year] = date.split('/');
  const [hour, minute] = time.split(':');
  return new Date(year, month - 1, day, hour, minute).toISOString();
}