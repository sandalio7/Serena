import { useState, useEffect } from 'react'
import './App.css'
import './index.css'
import FinancialSummaryCard from './components/economic/FinancialSummaryCard'
import ExpensePieChart from './components/economic/ExpensePieChart'
import PhysicalVarsCard from './components/health/PhysicalVarsCard'
import SleepCard from './components/health/SleepCard'
import QualitativeStateCard from './components/health/QualitativeStateCard'
import ConclusionCard from './components/health/ConclusionCard'
import PatientSelector from './components/PatientSelector'
import { financialService, healthService } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('economic')
  const [selectedPatientId, setSelectedPatientId] = useState(1)  // Default a paciente con ID 1
  const [activePeriod, setActivePeriod] = useState('month')
  const [activeHealthPeriod, setActiveHealthPeriod] = useState('month')
  
  // Estados para almacenar datos de la API
  const [financialData, setFinancialData] = useState({
    income: 0,
    expenses: 0,
    categories: []
  })
  
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
  
  // Estado para el formulario
  const [formData, setFormData] = useState({
    type: 'expense',
    category: '',
    amount: '',
    date: new Date().toISOString().split('T')[0]
  })

  // Cargar datos financieros cuando cambia el período o el paciente
  useEffect(() => {
    if (!selectedPatientId) return;
    
    async function loadFinancialData() {
      setLoading(prev => ({ ...prev, financial: true }))
      setError(prev => ({ ...prev, financial: null }))
      
      try {
        // En un entorno real, descomentar estas líneas
        // const summary = await financialService.getSummary(selectedPatientId, activePeriod);
        // const categories = await financialService.getExpensesByCategory(selectedPatientId, activePeriod);
        
        // Para pruebas, usamos datos de ejemplo
        const mockData = {
          income: 145200,
          expenses: 172850,
          categories: [
            { name: 'Vivienda', amount: 45000, color: '#1e40af' },
            { name: 'Servicios básicos', amount: 22500, color: '#3b82f6' },
            { name: 'Cuidados', amount: 40000, color: '#ef4444' },
            { name: 'Salud', amount: 35000, color: '#f97316' },
            { name: 'Supermercado', amount: 21000, color: '#22c55e' },
            { name: 'Transporte', amount: 5350, color: '#a855f7' },
            { name: 'Varios', amount: 4000, color: '#6b7280' },
          ]
        }
        
        setFinancialData(mockData)
      } catch (err) {
        console.error('Error loading financial data:', err)
        setError(prev => ({ ...prev, financial: 'Error al cargar datos financieros' }))
      } finally {
        setLoading(prev => ({ ...prev, financial: false }))
      }
    }
    
    loadFinancialData()
  }, [selectedPatientId, activePeriod])
  
  // Cargar datos de salud cuando cambia el período o el paciente
  useEffect(() => {
    if (!selectedPatientId) return;
    
    async function loadHealthData() {
      setLoading(prev => ({ ...prev, health: true }))
      setError(prev => ({ ...prev, health: null }))
      
      try {
        
         const data = await healthService.getHealthData(selectedPatientId, activeHealthPeriod);
        
        // Para pruebas, usamos datos de ejemplo
        
        
        setHealthData(mockData)
      } catch (err) {
        console.error('Error loading health data:', err)
        setError(prev => ({ ...prev, health: 'Error al cargar datos de salud' }))
      } finally {
        setLoading(prev => ({ ...prev, health: false }))
      }
    }
    
    loadHealthData()
  }, [selectedPatientId, activeHealthPeriod])
  
  // Manejar cambios en el formulario
  const handleFormChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }
  
  // Manejar envío del formulario
  // En la función handleSubmit
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Validar datos del formulario
      if (!formData.category || !formData.amount) {
        alert('Por favor complete todos los campos');
        return;
      }
      
      // Preparar datos para enviar
      const transactionData = {
        patient_id: selectedPatientId,
        type: formData.type,
        category: formData.category,
        amount: parseFloat(formData.amount.replace(/[\$,]/g, '')),
        date: formData.date
      };
      
      // Enviar datos a la API
      await financialService.registerTransaction(transactionData);
      
      // Mostrar confirmación
      alert('Transacción registrada correctamente');
      
      // Limpiar formulario
      setFormData({
        type: 'expense',
        category: '',
        amount: '',
        date: new Date().toISOString().split('T')[0]
      });
      
      // Recargar datos
      loadFinancialData();
    } catch (err) {
      console.error('Error registering transaction:', err);
      alert('Error al registrar la transacción');
    }
  };

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
        
        <PatientSelector 
          onSelectPatient={setSelectedPatientId}
          selectedPatientId={selectedPatientId}
        />
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
                
                <div className="card">
                  <h3>Gastos por categoría</h3>
                  <ExpensePieChart categories={financialData.categories} />
                  
                  <table className="expenses-table">
                    <thead>
                      <tr>
                        <th>Categoría</th>
                        <th>Monto gastado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {financialData.categories.map((category) => (
                        <tr key={category.name}>
                          <td>
                            <span 
                              className="color-indicator" 
                              style={{ backgroundColor: category.color }}
                            ></span>
                            {category.name}
                          </td>
                          <td>${category.amount.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                
                <div className="card">
                  <h3>Registrar nuevo movimiento</h3>
                  <form className="expense-form" onSubmit={handleSubmit}>
                    <div className="form-group">
                      <label htmlFor="type">Tipo</label>
                      <select 
                        id="type" 
                        name="type" 
                        value={formData.type}
                        onChange={handleFormChange}
                      >
                        <option value="income">Ingreso</option>
                        <option value="expense">Gasto</option>
                      </select>
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="category">Subcategoría</label>
                      <select 
                        id="category" 
                        name="category"
                        value={formData.category}
                        onChange={handleFormChange}
                      >
                        <option value="">Seleccionar...</option>
                        {financialData.categories.map((category) => (
                          <option key={category.name} value={category.name}>
                            {category.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="amount">Monto</label>
                      <input 
                        type="text" 
                        id="amount" 
                        name="amount" 
                        placeholder="$7.800"
                        value={formData.amount}
                        onChange={handleFormChange}
                      />
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="date">Fecha</label>
                      <input 
                        type="date" 
                        id="date" 
                        name="date"
                        value={formData.date}
                        onChange={handleFormChange}
                      />
                    </div>
                    
                    <button type="submit" className="btn-primary">
                      Registrar
                    </button>
                  </form>
                </div>
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
                
                <div className="qualitative-states">
                  <QualitativeStateCard 
                    title="Estado Cognitivo"
                    rating={healthData.cognitiveState.rating}
                    description={healthData.cognitiveState.description}
                  />
                  
                  <QualitativeStateCard 
                    title="Estado Físico"
                    rating={healthData.physicalState.rating}
                    description={healthData.physicalState.description}
                  />
                  
                  <QualitativeStateCard 
                    title="Estado Emocional"
                    rating={healthData.emotionalState.rating}
                    description={healthData.emotionalState.description}
                  />
                </div>
                
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