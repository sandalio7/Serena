import React, { useState } from 'react';

const HealthRecordsList = ({ records, activeType, onTypeChange }) => {
  // Función para obtener emoji según el estado
  const getStatusEmoji = (status) => {
    if (status === "Bueno" || status === "Normal") return "😊";
    if (status === "Moderado") return "😐";
    if (status === "Regular" || status === "Bajo") return "😕";
    if (status === "Alerta") return "⚠️";
    return "❓";
  };

  // Formatear fecha relativamente
  const formatRelativeDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 60) {
      return `Hace ${diffMins} minutos`;
    } else if (diffMins < 1440) { // menos de un día
      const hours = Math.floor(diffMins / 60);
      return `Hace ${hours} horas`;
    } else {
      const days = Math.floor(diffMins / 1440);
      return `Hace ${days} días`;
    }
  };

  // Mock data para desarrollo
  const mockRecords = [
    { 
      id: 1,
      type: "cognitive", 
      value: "8/10", 
      status: "Bueno", 
      notes: "Confusión", 
      details: "Estuvo un poco confundida últimamente",
      timestamp: "2025-05-03T20:11:00"
    },
    { 
      id: 2,
      type: "physical", 
      value: "7/10", 
      status: "Moderado", 
      notes: "Caminó solo dentro de la casa sin asistencia", 
      timestamp: "2025-05-03T20:11:00"
    },
    { 
      id: 3,
      type: "physical", 
      value: "6/10", 
      status: "Moderado", 
      notes: "Dolor en el pecho", 
      timestamp: "2025-05-03T20:11:00"
    },
    { 
      id: 4,
      type: "emotional", 
      value: "5/10", 
      status: "Regular", 
      notes: "Irritabilidad", 
      timestamp: "2025-05-03T20:11:00"
    }
  ];

  // Usar datos reales o mock
  const healthRecords = records && records.length > 0 ? records : mockRecords;

  return (
    <div className="health-records-container">
      {/* Filtros de tipo */}
      <div className="type-filter">
        <button 
          className={`type-filter-btn ${activeType === 'all' ? 'type-active' : ''}`}
          onClick={() => onTypeChange('all')}
        >
          Todos
        </button>
        <button 
          className={`type-filter-btn ${activeType === 'cognitive' ? 'type-active' : ''}`}
          onClick={() => onTypeChange('cognitive')}
        >
          Cognitivo
        </button>
        <button 
          className={`type-filter-btn ${activeType === 'physical' ? 'type-active' : ''}`}
          onClick={() => onTypeChange('physical')}
        >
          Físico
        </button>
        <button 
          className={`type-filter-btn ${activeType === 'emotional' ? 'type-active' : ''}`}
          onClick={() => onTypeChange('emotional')}
        >
          Emocional
        </button>
      </div>
      
      {/* Lista de registros de salud */}
      <div className="records-list">
        <h3>Registros de salud ({healthRecords.length})</h3>
        
        {healthRecords.length === 0 ? (
          <p className="no-records">No hay registros para el período seleccionado</p>
        ) : (
          <ul className="records-items">
            {healthRecords.map((record) => (
              <li key={record.id} className="record-item">
                <div className="record-content">
                  <div className={`record-icon ${record.type}`}>
                    {record.type === 'cognitive' && '🧠'}
                    {record.type === 'physical' && '❤️'}
                    {record.type === 'emotional' && '😊'}
                  </div>
                  <div className="record-details">
                    <div className="record-header">
                      <h4>
                        {record.type === 'cognitive' && 'Estado Cognitivo'}
                        {record.type === 'physical' && 'Estado Físico'}
                        {record.type === 'emotional' && 'Estado Emocional'}
                      </h4>
                      <span className="record-time">{formatRelativeDate(record.timestamp)}</span>
                    </div>
                    <p className="record-notes">"{record.notes}"</p>
                    <div className="record-status">
                      <span className="record-value">
                        Valoración: {record.value} {getStatusEmoji(record.status)}
                      </span>
                      {record.details && (
                        <span className="record-details-text">{record.details}</span>
                      )}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default HealthRecordsList;