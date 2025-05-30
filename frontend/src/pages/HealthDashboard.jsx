// HealthDashboard.jsx - ACTUALIZADO CON SOPORTE COMPLETO PARA MEDICACIÓN
import { useState, useEffect, useRef } from 'react';
import MainLayout from '../components/layout/MainLayout';
import VitalSignsCard from '../components/health/VitalSignsCard';
import WeeklySummaryCard from '../components/health/WeeklySummaryCard';
import HealthHistorySection from '../components/health/HealthHistorySection';
import { 
  getHealthSummary, 
  getHealthHistory,
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
  // ACTUALIZADO: 'all' sigue siendo el valor por defecto, pero ahora incluye soporte para 'medication'
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
      setError('No se pudieron cargar los datos de salud');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  // Función para cargar historial
  // ACTUALIZADO: Ahora maneja correctamente todas las categorías incluyendo 'medication'
  const loadHistory = async () => {
    try {
      // El servicio ya maneja correctamente el filtro de medicación y excluye gastos
      const history = await getHealthHistory(patientId, activePeriod, activeCategory);
      setHistoryEvents(history);
      
      // Debug: Log para verificar que no hay items de gastos
      const expenseItems = history.filter(item => 
        item.categoryName && item.categoryName.toLowerCase().includes('gasto')
      );
      if (expenseItems.length > 0) {
        console.warn('⚠️  Se encontraron items de gastos en el dashboard de salud:', expenseItems);
      }
      
    } catch (error) {
      console.error('Error cargando historial:', error);
      setHistoryEvents([]); // En caso de error, simplemente mostrar lista vacía
    }
  };
  
  // Cargar datos iniciales
  useEffect(() => {
    loadHealthData();
  }, [patientId, activePeriod]);
  
  // Cargar historial cuando cambian los filtros
  // ACTUALIZADO: Ahora reacciona correctamente a cambios en activeCategory (incluyendo 'medication')
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
  // ACTUALIZADA: Ahora maneja correctamente eventos de medicación
  const handleEditEvent = async (event) => {
    try {
      console.log('Editando evento:', event);
      
      // Verificación adicional: asegurar que no estamos editando un item de gastos
      if (event.categoryName && event.categoryName.toLowerCase().includes('gasto')) {
        console.error('❌ Intento de editar item de gastos en dashboard de salud');
        alert('Los items de gastos no pueden editarse desde el dashboard de salud. Use el dashboard económico.');
        return;
      }
      
      await updateHealthEvent(event.id, event);
      // Recargar historial después de editar
      loadHistory();
    } catch (error) {
      console.error('Error actualizando evento:', error);
      alert('Error al actualizar el evento. Por favor, inténtelo de nuevo.');
    }
  };
  
  // Función auxiliar para validar filtros
  // NUEVA: Validar que los filtros sean válidos para el dashboard de salud
  const validateCategoryFilter = (category) => {
    const validCategories = ['all', 'physical', 'cognitive', 'emotional', 'medication', 'autonomy'];
    return validCategories.includes(category);
  };
  
  // Handler para cambio de categoría con validación
  // NUEVO: Wrapper para setActiveCategory con validación
  const handleCategoryChange = (newCategory) => {
    if (validateCategoryFilter(newCategory)) {
      setActiveCategory(newCategory);
    } else {
      console.error('Categoría no válida para dashboard de salud:', newCategory);
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
          <h1 className="main-title">Dashboard de Salud</h1>
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
        
        <WeeklySummaryCard 
          summaryData={healthData?.weeklySummary}
          hasData={healthData?.weeklySummary !== null}
        />
        
        {/* ACTUALIZADO: Ahora usa handleCategoryChange para validación */}
        <HealthHistorySection 
          events={historyEvents}
          onEditEvent={handleEditEvent}
          activePeriod={activePeriod}
          setActivePeriod={setActivePeriod}
          activeCategory={activeCategory}
          setActiveCategory={handleCategoryChange}
        />
        
        <div className="last-update">
          Última actualización: {new Date(lastUpdate).toLocaleTimeString()}
        </div>
        
        
      </div>
    </MainLayout>
  );
}

export default HealthDashboard;