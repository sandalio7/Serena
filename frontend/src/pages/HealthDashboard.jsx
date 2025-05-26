import { useState, useEffect, useRef } from 'react';
import MainLayout from '../components/layout/MainLayout';
import VitalSignsCard from '../components/health/VitalSignsCard';
import WeeklySummaryCard from '../components/health/WeeklySummaryCard';
import HealthHistorySection from '../components/health/HealthHistorySection';
import { 
  getHealthSummary, 
  getHealthHistory,
  getHealthDataMock,
  updateHealthEvent
} from '../services/healthService';
import './HealthDashboard.css';

function HealthDashboard() {
  // ID del paciente (en una aplicación real podría venir de un contexto o prop)
  const patientId = 1;
  
  // Estados para almacenar los datos de salud
  const [healthData, setHealthData] = useState(null);
  const [historyEvents, setHistoryEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(Date.now());
  const [refreshing, setRefreshing] = useState(false);
  
  // Estados para los filtros del historial
  const [activePeriod, setActivePeriod] = useState('day');
  const [activeCategory, setActiveCategory] = useState('all');
  
  // Ref para el intervalo de polling
  const intervalRef = useRef(null);
  
  // Función para cargar datos
  const loadHealthData = async () => {
    try {
      if (healthData) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      
      // Intentar cargar datos reales del backend
      const summary = await getHealthSummary(patientId, activePeriod);
      
      if (summary.hasData) {
        setHealthData(summary);
      } else {
        // No hay datos nuevos, mantener los actuales o mostrar vacío
        setHealthData(prevData => prevData || null);
      }
      
    } catch (error) {
      console.error('Error cargando datos de salud:', error);
      
      // Si hay error y no tenemos datos previos, usar datos mock para desarrollo
      if (process.env.NODE_ENV === 'development' && !healthData) {
        console.log('Usando datos mock por error en el backend');
        const mockData = getHealthDataMock();
        setHealthData(mockData);
      } else if (!healthData) {
        setError('No se pudieron cargar los datos de salud');
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  // Función para cargar historial
  const loadHistory = async () => {
    try {
      const history = await getHealthHistory(patientId, activePeriod, activeCategory);
      setHistoryEvents(history);
    } catch (error) {
      console.error('Error cargando historial:', error);
      
      // Si hay error, usar datos mock para el historial
      if (process.env.NODE_ENV === 'development') {
        const mockData = getHealthDataMock();
        setHistoryEvents(mockData.historyEvents);
      }
    }
  };
  
  // Cargar datos iniciales
  useEffect(() => {
    loadHealthData();
  }, [patientId, activePeriod]);
  
  // Cargar historial cuando cambian los filtros
  useEffect(() => {
    if (healthData) {
      loadHistory();
    }
  }, [patientId, activePeriod, activeCategory]);
  
  // Configurar polling automático cada 30 segundos
  useEffect(() => {
    // Iniciar polling
    intervalRef.current = setInterval(() => {
      loadHealthData();
      if (healthData) {
        loadHistory();
      }
    }, 30000); // 30 segundos
    
    // Limpiar intervalo al desmontar
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [healthData]);
  
  // Refrescar cuando la página vuelve a estar visible
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        loadHealthData();
        if (healthData) {
          loadHistory();
        }
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [healthData]);
  
  // Función para manejar la edición de un evento
  const handleEditEvent = async (event) => {
    try {
      console.log('Editando evento:', event);
      // Por ahora, solo mostrar en consola
    } catch (error) {
      console.error('Error actualizando evento:', error);
    }
  };
  
  if (loading) {
    return (
      <MainLayout>
        <div className="health-dashboard">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading">Cargando datos de salud...</div>
          </div>
        </div>
      </MainLayout>
    );
  }
  
  if (error && !healthData) {
    return (
      <MainLayout>
        <div className="health-dashboard">
          <div className="error">Error: {error}</div>
          <button 
            onClick={() => window.location.reload()} 
            className="retry-button"
          >
            Reintentar
          </button>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="health-dashboard">
        <div className="dashboard-header">
          <h1 className="main-title">Último día</h1>
          {refreshing && (
            <div className="refreshing-indicator">
              <div className="refreshing-spinner"></div>
              <span>Actualizando...</span>
            </div>
          )}
        </div>
        
        <VitalSignsCard 
          vitalSigns={healthData?.vitalSigns}
          normalValues={healthData?.normalValues}
          hasData={healthData?.vitalSigns !== null}
        />
        
        <h2 className="section-title">Resumen Semanal</h2>
        <WeeklySummaryCard 
          summaryData={healthData?.weeklySummary}
          hasData={healthData?.weeklySummary !== null}
        />
        
        <h2 className="section-title">Historial</h2>
        <HealthHistorySection 
          events={historyEvents}
          onEditEvent={handleEditEvent}
          activePeriod={activePeriod}
          setActivePeriod={setActivePeriod}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
        />
        
        <div className="last-update">
          Última actualización: {new Date(lastUpdate).toLocaleTimeString()}
        </div>
      </div>
    </MainLayout>
  );
}

export default HealthDashboard;