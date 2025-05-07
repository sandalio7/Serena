import './PeriodSelector.css';

/**
 * Componente para seleccionar el período de tiempo
 * @param {Object} props - Propiedades del componente
 * @param {string} props.selectedPeriod - Período seleccionado actualmente (day, week, month)
 * @param {Function} props.onPeriodChange - Función para manejar el cambio de período
 */
function PeriodSelector({ selectedPeriod, onPeriodChange }) {
  const periods = [
    { id: 'day', label: 'Último Día' },
    { id: 'week', label: 'Última Semana' },
    { id: 'month', label: 'Último Mes' },
    { id: 'custom', label: 'Elegir' }
  ];

  return (
    <div className="period-selector">
      {periods.map(period => (
        <button
          key={period.id}
          className={`period-btn ${selectedPeriod === period.id ? 'active' : ''}`}
          onClick={() => onPeriodChange(period.id)}
        >
          {period.label}
        </button>
      ))}
    </div>
  );
}

export default PeriodSelector;