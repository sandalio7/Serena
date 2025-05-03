import React, { useEffect, useState } from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Legend, Tooltip } from 'recharts';

function ExpensePieChart({ categories }) {
  // Si no hay categorías o están vacías, mostrar mensaje
  if (!categories || categories.length === 0) {
    return (
      <div className="expense-pie-chart-container text-center p-4 bg-white rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-2">Distribución de Gastos</h3>
        <p className="text-gray-500">No hay datos de gastos disponibles</p>
      </div>
    );
  }

  return (
    <div className="expense-pie-chart-container bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">Distribución de Gastos</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={categories}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="amount"
              nameKey="name"
              label={({ name, percent }) => 
                `${name}: ${(percent * 100).toFixed(0)}%`
              }
            >
              {categories.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => [`$${value.toLocaleString()}`, 'Gasto']}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default ExpensePieChart;