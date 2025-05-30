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
    
    // Verificar si hay datos válidos para signos vitales
    // Ahora verificamos basándonos en el campo 'available' de cada signo vital
    if (!data.physicalVars || 
        (!data.physicalVars.bloodPressure.available && 
         !data.physicalVars.temperature.available && 
         !data.physicalVars.oxygenSaturation.available)) {
      // No hay datos disponibles de signos vitales
      return {
        hasData: false,
        currentStatus: null,
        vitalSigns: null,
        normalValues: data.normalValues || {
          bloodPressure: { systolic: 130, diastolic: 80 },
          temperature: 36.5,
          oxygenation: 98
        },
        weeklySummary: null
      };
    }
    
    // Procesar valores de signos vitales 
    const vitalSigns = {
      bloodPressure: data.physicalVars.bloodPressure,
      temperature: data.physicalVars.temperature,
      oxygenation: data.physicalVars.oxygenSaturation
    };
    
    // Si algún signo vital está disponible, intentamos procesarlo para mantener retrocompatibilidad
    if (data.physicalVars.bloodPressure.available) {
      try {
        const [systolic, diastolic] = data.physicalVars.bloodPressure.value.split('/');
        vitalSigns.bloodPressure.systolic = parseInt(systolic);
        vitalSigns.bloodPressure.diastolic = parseInt(diastolic);
      } catch (e) {
        console.error('Error al parsear presión arterial:', e);
      }
    }
    
    if (data.physicalVars.temperature.available) {
      try {
        vitalSigns.temperature.value = parseFloat(data.physicalVars.temperature.value.replace(',', '.'));
      } catch (e) {
        console.error('Error al parsear temperatura:', e);
      }
    }
    
    if (data.physicalVars.oxygenSaturation.available) {
      try {
        vitalSigns.oxygenation.value = parseInt(data.physicalVars.oxygenSaturation.value);
      } catch (e) {
        console.error('Error al parsear oxigenación:', e);
      }
    }
    
    // Transformar los datos del backend al formato que espera el frontend
    return {
      hasData: true,
      currentStatus: {
        status: getStatusFromConclusion(data.generalConclusion),
        score: getScoreFromConclusion(data.generalConclusion),
        emoji: getEmojiFromConclusion(data.generalConclusion)
      },
      vitalSigns: vitalSigns,
      normalValues: data.normalValues,
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
 * @param {string} category - Categoría de salud ('all', 'physical', 'cognitive', 'emotional', 'medication', 'autonomy')
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
        'medication': 'medication',  // NUEVO: Soporte directo para medicación
        'autonomy': 'autonomy'       // ACTUALIZADO: Mapeo directo para autonomía
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
      category: item.category, // Ya viene en formato correcto del backend
      categoryName: item.categoryName, // Nombre completo de la categoría
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
      category: data.category,
      categoryName: data.categoryName,
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
      return '5'
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
  // ACTUALIZADO: Mapeo simplificado ya que el backend ahora envía las categorías correctamente
  const categoryMap = {
    'physical': 'physical',
    'cognitive': 'cognitive', 
    'emotional': 'emotional',
    'medication': 'medication',  // NUEVO: Soporte para medicación
    'autonomy': 'autonomy'
  };
  
  return categoryMap[backendCategory] || 'physical';
}

function mapFrontendToBackendCategory(frontendCategory) {
  // ACTUALIZADO: Mapeo simplificado para compatibilidad con nueva estructura
  const categoryMap = {
    'physical': 'Salud Física',
    'cognitive': 'Salud Cognitiva',
    'emotional': 'Estado Emocional',
    'medication': 'Medicación',  // NUEVO: Mapeo para medicación
    'autonomy': 'Autonomía'
  };
  
  return categoryMap[frontendCategory] || 'Salud Física';
}

function formatDate(date, time) {
  // Convertir fecha DD/MM/YYYY y hora HH:MM a formato ISO
  const [day, month, year] = date.split('/');
  const [hour, minute] = time.split(':');
  return new Date(year, month - 1, day, hour, minute).toISOString();
}