import { PieChart, Pie, Cell, ResponsiveContainer, Label } from 'recharts';
import './ExpensePieChart.css';

/**
 * Componente de gráfico circular para mostrar gastos por categoría
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.data - Array de objetos con datos de categorías (category, amount, color)
 * @param {boolean} props.isEmpty - Indica si realmente no hay datos
 */
function ExpensePieChart({ data, isEmpty = false }) {
  // Si no hay datos, mostramos un mensaje
  if (!data || data.length === 0) {
    return <div className="no-data">No hay datos disponibles para el gráfico</div>;
  }

  return (
    <div className={`pie-chart-container ${isEmpty ? 'empty-data' : ''}`}>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            innerRadius={40}
            paddingAngle={2}
            dataKey="amount"
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.color || '#' + ((Math.random() * 0xffffff) << 0).toString(16)} 
              />
            ))}
            {isEmpty && (
              <Label
                position="center"
                value="Sin datos"
                fill="#6b7280"
                style={{ fontSize: '14px', fontWeight: 'bold' }}
              />
            )}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      
      {isEmpty && (
        <div className="empty-data-overlay">
          <span className="empty-data-message">No hay datos para el período seleccionado</span>
        </div>
      )}
    </div>
  );
}

export default ExpensePieChart;