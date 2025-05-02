import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

function ExpensePieChart({ categories }) {
  // Calculamos el total para los porcentajes
  const total = categories.reduce((sum, category) => sum + category.amount, 0);
  
  // Formateamos los datos para el gráfico
  const data = categories.map(category => ({
    name: category.name,
    value: category.amount,
    color: category.color,
    percentage: ((category.amount / total) * 100).toFixed(1)
  }));

  // Renderizador personalizado para las etiquetas
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, name, percentage }) => {
    // Solo mostramos etiquetas para categorías con porcentaje significativo
    if (parseFloat(percentage) < 5) return null;
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor="middle" 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${percentage}%`}
      </text>
    );
  };

  return (
    <div className="pie-chart-container">
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={100}
            innerRadius={60}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value) => [`$${value.toLocaleString()}`, 'Monto']}
            labelFormatter={(name) => `${name}`}
          />
          {/* Eliminamos el componente Legend que estaba aquí */}
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ExpensePieChart;