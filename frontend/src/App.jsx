import { useState, useEffect } from 'react'
import './App.css'
import './index.css'
import FinancialSummaryCard from './components/economic/FinancialSummaryCard'
import ExpensePieChart from './components/economic/ExpensePieChart'
import ExpenseHistoryList from './components/economic/ExpenseHistoryList'
import PhysicalVarsCard from './components/health/PhysicalVarsCard'
import SleepCard from './components/health/SleepCard'
import HealthHistoryList from './components/health/HealthHistoryList' // Nuevo componente importado
import ConclusionCard from './components/health/ConclusionCard'

import { financialService, healthService } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('economic')
  const [selectedPatientId] = useState(1)  // Fijo en 1, no editable
  const [activePeriod, setActivePeriod] = useState('month')
  const [activeHealthPeriod, setActiveHealthPeriod] = useState('month')
  const [activeHealthCategory, setActiveHealthCategory] = useState('') // Nuevo estado para filtrar por categoría
  
  // Estados para almacenar datos de la API
  const [financialData, setFinancialData] = useState({
    income: 0,
    expenses: 0,
    categories: []
  })
  
  // Nuevo estado para el historial de gastos
  const [expenseHistory, setExpenseHistory] = useState([])
  
  const [healthData, setHealthData] = useState({
    physicalVars: {
      bloodPressure: { value: '', status: '' },
      temperature: { value: '', status: '' },
      oxygenSaturation: { value: '', status: '' },
      weight: { value: '', status: '', bmi: '' }
    },
    sleep: { hours: '', status: '' },
    cognitiveState: {
      rating: 0,
      description: ''
    },
    physicalState: {
      rating: 0,
      description: ''
    },
    emotionalState: {
      rating: 0,
      description: ''
    },
    generalConclusion: ''
  })
  
  const [loading, setLoading] = useState({
    financial: false,
    health: false
  })
  
  const [error, setError] = useState({
    financial: null,
    health: null
  })
  
  // Cargar datos financieros cuando cambia el período
  useEffect(() => {
    async function loadFinancialData() {
      setLoading(prev => ({ ...prev, financial: true }))
      setError(prev => ({ ...prev, financial: null }))
      
      try {
        // Obtener datos reales del backend
        const summary = await financialService.getSummary(selectedPatientId, activePeriod);
        const categories = await financialService.getExpensesByCategory(selectedPatientId, activePeriod);
        const history = await financialService.getExpenseHistory(selectedPatientId, activePeriod);
        
        setFinancialData({
          income: summary.income,
          expenses: summary.expenses,
          categories: categories
        })
        
        setExpenseHistory(history);
        
        console.log('Datos financieros cargados:', { summary, categories, history })
      } catch (err) {
        console.error('Error loading financial data:', err)
        setError(prev => ({ ...prev, financial: 'Error al cargar datos financieros' }))
      } finally {
        setLoading(prev => ({ ...prev, financial: false }))
      }
    }
    
    loadFinancialData()
  }, [selectedPatientId, activePeriod])
  
  // Cargar datos de salud cuando cambia el período
  useEffect(() => {
    async function loadHealthData() {
      setLoading(prev => ({ ...prev, health: true }));
      setError(prev => ({ ...prev, health: null }));
      
      try {
        // Llamar al servicio API con el ID del paciente y el período
        const data = await healthService.getHealthData(selectedPatientId, activeHealthPeriod);
        console.log('Datos de salud recibidos:', data);
        
        // Verificar si hay datos disponibles
        if (data && !data.error) {
          setHealthData(data);
        } else {
          // Si el backend devuelve un error, mostrar mensaje
          setError(prev => ({ 
            ...prev, 
            health: data.error || 'No se pudieron cargar los datos de salud' 
          }));
        }
      } catch (err) {
        console.error('Error loading health data:', err);
        setError(prev => ({ 
          ...prev, 
          health: 'Error al cargar datos de salud. Por favor intente nuevamente.' 
        }));
      } finally {
        setLoading(prev => ({ ...prev, health: false }));
      }
    }
    
    loadHealthData();
  }, [selectedPatientId, activeHealthPeriod]);

  return (
    <div className="container">
      <header>
        <div className="tabs">
          <button 
            className={`tab tab-economic ${activeTab === 'economic' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('economic')}
          >
            Dashboard Económico
          </button>
          <button 
            className={`tab tab-health ${activeTab === 'health' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('health')}
          >
            Dashboard de Salud
          </button>
        </div>
        
        <div className="patient-info">
          <h2>Dashboard - Paciente ID: {selectedPatientId}</h2>
        </div>
      </header>

      <main>
        {activeTab === 'economic' ? (
          <div className="economic-dashboard">
            {loading.financial ? (
              <p className="loading-message">Cargando datos financieros...</p>
            ) : error.financial ? (
              <p className="error-message">{error.financial}</p>
            ) : (
              <>
                <FinancialSummaryCard type="income" amount={financialData.income} />
                <FinancialSummaryCard type="expense" amount={financialData.expenses} />
                
                <div className="period-filter">
                  <button 
                    className={activePeriod === 'day' ? 'period-active' : ''}
                    onClick={() => setActivePeriod('day')}
                  >
                    Día
                  </button>
                  <button 
                    className={activePeriod === 'week' ? 'period-active' : ''}
                    onClick={() => setActivePeriod('week')}
                  >
                    Últimos 7 días
                  </button>
                  <button 
                    className={activePeriod === 'fortnight' ? 'period-active' : ''}
                    onClick={() => setActivePeriod('fortnight')}
                  >
                    Últimos 15 días
                  </button>
                  <button 
                    className={activePeriod === 'month' ? 'period-active' : ''}
                    onClick={() => setActivePeriod('month')}
                  >
                    Último mes
                  </button>
                </div>
                
                <ExpensePieChart categories={financialData.categories} />
                
                {/* Nuevo componente para historial de gastos */}
                <ExpenseHistoryList expenseHistory={expenseHistory} />
              </>
            )}
          </div>
        ) : (
          <div className="health-dashboard">
            {loading.health ? (
              <p className="loading-message">Cargando datos de salud...</p>
            ) : error.health ? (
              <p className="error-message">{error.health}</p>
            ) : (
              <>
                <PhysicalVarsCard data={healthData.physicalVars} />
                <SleepCard data={healthData.sleep} />
                
                <div className="filter-container">
                  <div className="period-filter">
                    <button 
                      className={activeHealthPeriod === 'day' ? 'period-active' : ''}
                      onClick={() => setActiveHealthPeriod('day')}
                    >
                      Día
                    </button>
                    <button 
                      className={activeHealthPeriod === 'week' ? 'period-active' : ''}
                      onClick={() => setActiveHealthPeriod('week')}
                    >
                      Semana
                    </button>
                    <button 
                      className={activeHealthPeriod === 'month' ? 'period-active' : ''}
                      onClick={() => setActiveHealthPeriod('month')}
                    >
                      Mes
                    </button>
                  </div>
                  
                  <div className="category-filter">
                    <select 
                      value={activeHealthCategory}
                      onChange={(e) => setActiveHealthCategory(e.target.value)}
                      className="category-select"
                    >
                      <option value="">Todas las categorías</option>
                      <option value="physical">Salud Física</option>
                      <option value="cognitive">Estado Cognitivo</option>
                      <option value="emotional">Estado Emocional</option>
                      <option value="medication">Medicación</option>
                    </select>
                  </div>
                </div>
                
                {/* Reemplazamos las tarjetas de estados por el historial */}
                <HealthHistoryList patientId={selectedPatientId} period={activeHealthPeriod} />
                
                <ConclusionCard status={healthData.generalConclusion} />
              </>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App