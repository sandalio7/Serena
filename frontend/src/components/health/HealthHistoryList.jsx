// src/components/health/HealthHistoryList.jsx
import React, { useState, useEffect } from 'react';
import { healthService } from '../../services/api';

const HealthHistoryList = ({ patientId, period }) => {
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState('');

  useEffect(() => {
    const fetchHealthHistory = async () => {
      setLoading(true);
      try {
        // Obtener todos los datos de historial
        const data = await healthService.getHealthHistory(patientId, period, '');
        setHistory(data);
        setError(null);
      } catch (err) {
        console.error('Error al obtener historial de salud:', err);
        setError('No se pudo cargar el historial. Intente nuevamente.');
      } finally {
        setLoading(false);
      }
    };

    fetchHealthHistory();
  }, [patientId, period]);

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Salud Física':
        return '🏃';
      case 'Estado Cognitivo':
        return '🧠';
      case 'Estado Emocional':
        return '😊';
      case 'Medicación':
        return '💊';
      default:
        return '📋';
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'Salud Física':
        return 'text-blue-500';
      case 'Estado Cognitivo':
        return 'text-purple-500';
      case 'Estado Emocional':
        return 'text-yellow-500';
      case 'Medicación':
        return 'text-green-500';
      default:
        return 'text-gray-500';
    }
  };

  const getRatingColor = (rating) => {
    if (rating >= 8) return 'text-green-500';
    if (rating >= 5) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Filtrar los items según la categoría seleccionada
  const filteredHistory = activeCategory ? history.filter(item => {
    switch (activeCategory) {
      case 'physical':
        return item.category === 'Salud Física';
      case 'cognitive':
        return item.category === 'Estado Cognitivo';
      case 'emotional':
        return item.category === 'Estado Emocional';
      case 'medication':
        return item.category === 'Medicación';
      default:
        return true;
    }
  }) : history;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h2 className="text-xl font-bold mb-4">Historial de Salud</h2>
      
      {/* Botones de categoría */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button 
          className={`px-3 py-1 rounded text-sm ${activeCategory === '' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveCategory('')}
        >
          Todos
        </button>
        <button 
          className={`px-3 py-1 rounded text-sm ${activeCategory === 'physical' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveCategory('physical')}
        >
          Salud Física
        </button>
        <button 
          className={`px-3 py-1 rounded text-sm ${activeCategory === 'cognitive' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveCategory('cognitive')}
        >
          Estado Cognitivo
        </button>
        <button 
          className={`px-3 py-1 rounded text-sm ${activeCategory === 'emotional' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveCategory('emotional')}
        >
          Estado Emocional
        </button>
        <button 
          className={`px-3 py-1 rounded text-sm ${activeCategory === 'medication' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveCategory('medication')}
        >
          Medicación
        </button>
      </div>

      {loading ? (
        <div className="text-center py-6">
          <span className="text-gray-500">Cargando datos...</span>
        </div>
      ) : error ? (
        <div className="text-center py-6">
          <span className="text-red-500">{error}</span>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="text-center py-6">
          <span className="text-gray-500">No hay registros para mostrar en este período</span>
        </div>
      ) : (
        <div className="max-h-96 overflow-y-auto">
          {filteredHistory.map((item, index) => (
            <div key={`health-item-${index}`} className="border-b border-gray-200 py-4 px-2">
              <div className="flex justify-between items-start">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">{getCategoryIcon(item.category)}</span>
                  <div>
                    <div className="font-medium text-gray-800">{item.category}</div>
                    <div className="text-sm text-gray-600">{item.subcategory}</div>
                  </div>
                </div>
                
                <div className="text-2xl font-bold">
                  <span className={getRatingColor(item.rating)}>
                    {item.rating}/10
                  </span>
                </div>
              </div>
              
              <div className="mt-2 ml-10">
                <div className="text-md font-medium text-gray-700">{item.value}</div>
                <div className="text-xs text-gray-500 mt-1">
                  {item.date} - {item.time}
                </div>
                <div className="text-xs text-gray-500 mt-1 italic">
                  "{item.original_text}"
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HealthHistoryList;