import { useState } from 'react'
import './App.css'
import './index.css'
import FinancialSummaryCard from './components/economic/FinancialSummaryCard'
import ExpensePieChart from './components/economic/ExpensePieChart'
import PhysicalVarsCard from './components/health/PhysicalVarsCard'
import SleepCard from './components/health/SleepCard'
import QualitativeStateCard from './components/health/QualitativeStateCard'
import ConclusionCard from './components/health/ConclusionCard'

function App() {
  const [activeTab, setActiveTab] = useState('economic')
  const [activePeriod, setActivePeriod] = useState('month')
  const [activeHealthPeriod, setActiveHealthPeriod] = useState('month')

  // Datos de ejemplo - Dashboard Económico
  const financialData = {
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

  // Datos de ejemplo - Dashboard de Salud
  const healthData = {
    physicalVars: {
      bloodPressure: { value: '130/85', status: 'Normal' },
      temperature: { value: '36,8', status: 'Normal' },
      oxygenSaturation: { value: '95', status: 'Moderado' },
      weight: { value: '71', status: 'Moderado', bmi: '27' }
    },
    sleep: { hours: '5,5', status: 'Bajo' },
    cognitiveState: {
      rating: 4,
      description: 'Se lo notó desorientado durante toda la tarde'
    },
    physicalState: {
      rating: 7,
      description: 'Caminó solo dentro de la casa sin asistencia'
    },
    emotionalState: {
      rating: 6,
      description: 'Participó con desgano en actividades'
    },
    generalConclusion: 'Regular'
  }

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
      </header>

      <main>
        {activeTab === 'economic' ? (
          <div className="economic-dashboard">
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
              <form className="expense-form">
                <div className="form-group">
                  <label htmlFor="type">Tipo</label>
                  <select id="type" name="type">
                    <option value="income">Ingreso</option>
                    <option value="expense">Gasto</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="category">Subcategoría</label>
                  <select id="category" name="category">
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
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="date">Fecha</label>
                  <input type="date" id="date" name="date" />
                </div>
                
                <button type="submit" className="btn-primary">
                  Registrar
                </button>
              </form>
            </div>
          </div>
        ) : (
          <div className="health-dashboard">
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
          </div>
        )}
      </main>
    </div>
  )
}

export default App