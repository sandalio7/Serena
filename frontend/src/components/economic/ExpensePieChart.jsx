import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './ExpensePieChart.css';

/**
 * Componente de gráfico circular para mostrar gastos por categoría
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.data - Array de objetos con datos de categorías (category, amount, color)
 */
function ExpensePieChart({ data }) {
  // Si no hay datos, mostramos un mensaje
  if (!data || data.length === 0) {
    return <div className="no-data">No hay datos disponibles para el gráfico</div>;
  }

  return (
    <div className="pie-chart-container">
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
              <Cell key={`cell-${index}`} fill={entry.color || '#' + ((Math.random() * 0xffffff) << 0).toString(16)} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ExpensePieChart;