import { useState } from 'react';
import MainLayout from '../components/layout/MainLayout';
import HealthStatusCard from '../components/health/HealthStatusCard';
import VitalSignsCard from '../components/health/VitalSignsCard';
import WeeklySummaryCard from '../components/health/WeeklySummaryCard';
import HealthHistorySection from '../components/health/HealthHistorySection';
import './HealthDashboard.css';

function HealthDashboard() {
  // Estado para almacenar los datos de salud (en una implementación real vendría de una API)
  const [healthData, setHealthData] = useState({
    currentStatus: {
      status: "Regular",
      score: "6",
      emoji: "🙂"
    },
    vitalSigns: {
      bloodPressure: { systolic: 130, diastolic: 80 },
      temperature: 35.5,
      oxygenation: 80
    },
    normalValues: {
      bloodPressure: { systolic: 130, diastolic: 80 },
      temperature: 36.5,
      oxygenation: 98
    },
    weeklySummary: {
      physical: {
        score: 8,
        description: "Camino 100 metros, dimos una vuelta a la plaza"
      },
      cognitive: {
        score: 6,
        description: "Estuvo desorientado durante el día, no encontraba su guitarra"
      },
      emotional: {
        score: 10,
        description: "Hoy nos saludo a todos cuando se despertó, está contento"
      },
      autonomy: {
        score: 4,
        description: "Tuvimos que ayudarlo a sentarse y levantarse del sillón"
      }
    },
    historyEvents: [
      {
        id: 1,
        category: 'physical',
        description: "El cuidador cobró $5.000 este mes",
        date: '2025-04-12T10:30:00'
      },
      {
        id: 2,
        category: 'physical',
        description: "El cuidador cobró $5.000 este mes",
        date: '2025-04-12T14:45:00'
      },
      {
        id: 3,
        category: 'cognitive',
        description: "Gasté $8.000 en el servicio de cuidador",
        date: '2025-04-12T16:20:00'
      }
    ]
  });

  // Función para manejar la edición de un evento
  const handleEditEvent = (event) => {
    console.log('Editando evento:', event);
    // Aquí iría la lógica para abrir un modal de edición
  };

  return (
    <MainLayout>
      <div className="health-dashboard">
        <h1>Estado de Salud</h1>
        
        <HealthStatusCard 
          status={healthData.currentStatus.status}
          score={healthData.currentStatus.score}
          emoji={healthData.currentStatus.emoji}
        />
        
        <VitalSignsCard 
          vitalSigns={healthData.vitalSigns}
          normalValues={healthData.normalValues}
        />
        
        <WeeklySummaryCard 
          summaryData={healthData.weeklySummary}
        />
        
        <HealthHistorySection 
          events={healthData.historyEvents}
          onEditEvent={handleEditEvent}
        />
      </div>
    </MainLayout>
  );
}

export default HealthDashboard;