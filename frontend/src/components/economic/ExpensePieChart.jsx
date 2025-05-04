import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

// Componente personalizado para renderizar etiquetas dentro del gráfico
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, name }) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  // Solo mostrar nombre si el porcentaje es significativo
  if (percent < 0.05) return null;

  return (
    <text 
      x={x} 
      y={y} 
      fill="#fff" 
      textAnchor="middle" 
      dominantBaseline="central"
      fontSize={12}
      fontWeight="bold"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

// Componente personalizado para el tooltip
const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip" style={{ 
        backgroundColor: '#fff', 
        padding: '10px', 
        border: '1px solid #ccc',
        borderRadius: '4px',
        boxShadow: '0 2px 5px rgba(0,0,0,0.15)'
      }}>
        <p className="tooltip-category" style={{ fontWeight: 'bold', marginBottom: '5px' }}>
          {data.name}
        </p>
        <p className="tooltip-amount">
          <span style={{ fontWeight: 'bold' }}>Monto:</span> ${data.amount.toLocaleString()}
        </p>
        <p className="tooltip-percent">
          <span style={{ fontWeight: 'bold' }}>Porcentaje:</span> {(payload[0].percent * 100).toFixed(1)}%
        </p>
      </div>
    );
  }
  return null;
};

// Componente de leyenda personalizada
const CustomLegend = ({ payload }) => {
  return (
    <ul style={{ 
      listStyle: 'none', 
      padding: 0, 
      display: 'flex', 
      flexWrap: 'wrap', 
      justifyContent: 'center',
      marginTop: '15px'
    }}>
      {payload.map((entry, index) => (
        <li key={`legend-item-${index}`} style={{ 
          display: 'flex', 
          alignItems: 'center', 
          marginRight: '15px',
          marginBottom: '8px'
        }}>
          <div style={{ 
            width: '12px', 
            height: '12px', 
            backgroundColor: entry.color, 
            marginRight: '5px', 
            borderRadius: '2px' 
          }} />
          <span style={{ fontSize: '12px' }}>{entry.value}</span>
        </li>
      ))}
    </ul>
  );
};

function ExpensePieChart({ categories }) {
  // Si no hay categorías o están vacías, mostrar mensaje
  if (!categories || categories.length === 0) {
    return (
      <div className="expense-pie-chart-container" style={{ 
        textAlign: 'center', 
        padding: '20px', 
        background: 'white', 
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '10px' }}>
          Distribución de Gastos
        </h3>
        <p style={{ color: '#6b7280' }}>No hay datos de gastos disponibles</p>
      </div>
    );
  }

  // Calcular el total para obtener porcentajes
  const total = categories.reduce((sum, category) => sum + category.amount, 0);

  // Preparar datos para el gráfico, ordenando de mayor a menor
  const chartData = [...categories]
    .sort((a, b) => b.amount - a.amount)
    .map(category => ({
      ...category,
      percentage: (category.amount / total) * 100
    }));

  return (
    <div className="expense-pie-chart-container" style={{ 
      background: 'white', 
      padding: '20px', 
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '15px', textAlign: 'center' }}>
        Distribución de Gastos
      </h3>
      <div style={{ height: '300px', width: '100%' }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={120}
              innerRadius={60}
              paddingAngle={4}
              dataKey="amount"
              nameKey="name"
              animationDuration={800}
              animationBegin={0}
              animationEasing="ease"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.color} 
                  stroke="#fff"
                  strokeWidth={2}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              content={<CustomLegend />}
              verticalAlign="bottom"
              height={50}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div style={{ 
        textAlign: 'center', 
        marginTop: '10px',
        padding: '8px',
        background: '#f9fafb',
        borderRadius: '4px',
        fontWeight: 'bold'
      }}>
        Total: ${total.toLocaleString()}
      </div>
    </div>
  );
}

export default ExpensePieChart;