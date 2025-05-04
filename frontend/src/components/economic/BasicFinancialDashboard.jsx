import React, { useState, useEffect } from 'react';
import { financialService } from '../services/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const BasicFinancialDashboard = ({ patientId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [financialData, setFinancialData] = useState({
    expenses: 0,
    categories: []
  });
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  useEffect(() => {
    const fetchFinancialData = async () => {
      try {
        setLoading(true);
        const response = await financialService.getSummary(patientId, selectedPeriod);
        console.log('Financial data response:', response); // Para depuración
        
        setFinancialData({
          expenses: response.expenses || 0,
          categories: response.categories || []
        });
        setError(null);
      } catch (err) {
        console.error('Error fetching financial data:', err);
        setError('Error al cargar datos financieros');
      } finally {
        setLoading(false);
      }
    };

    fetchFinancialData();
  }, [patientId, selectedPeriod]);

  // Manejar cambio de período
  const handlePeriodChange = (period) => {
    setSelectedPeriod(period);
  };

  if (loading) {
    return <div className="text-center p-4">Cargando datos financieros...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
        <strong className="font-bold">Error: </strong>
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  // Definir los colores para las categorías
  const COLORS = ['#2563eb', '#16a34a', '#ef4444', '#f97316', '#22d3ee', '#a855f7'];
  
  // Formatear los datos para el gráfico
  const chartData = financialData.categories.map((category) => ({
    name: category.name,
    value: category.amount,
    color: category.color || '#6b7280'
  }));

  return (
    <div className="p-4">
      <div className="mb-4">
        <div className="bg-red-500 text-white rounded-md p-4 mb-4">
          <p className="text-sm font-medium">Gastos totales</p>
          <p className="text-3xl font-bold">${financialData.expenses.toLocaleString('es-ES')}</p>
        </div>
      </div>

      <div className="mb-4">
        <div className="flex space-x-2 border-b border-gray-200">
          <button 
            className={`py-2 px-4 text-sm font-medium ${selectedPeriod === 'day' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => handlePeriodChange('day')}
          >
            Día
          </button>
          <button 
            className={`py-2 px-4 text-sm font-medium ${selectedPeriod === 'week' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => handlePeriodChange('week')}
          >
            Últimos 7 días
          </button>
          <button 
            className={`py-2 px-4 text-sm font-medium ${selectedPeriod === 'fortnight' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => handlePeriodChange('fortnight')}
          >
            Últimos 15 días
          </button>
          <button 
            className={`py-2 px-4 text-sm font-medium ${selectedPeriod === 'month' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => handlePeriodChange('month')}
          >
            Último mes
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-4 mb-4">
        <h2 className="text-lg font-medium mb-4">Gastos por categoría</h2>
        
        {financialData.categories.length === 0 ? (
          <div className="text-center p-8 text-gray-500">
            No hay datos de categorías disponibles para este período
          </div>
        ) : (
          <div className="flex flex-col md:flex-row">
            <div className="w-full md:w-1/2 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    innerRadius={40}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `$${value.toLocaleString('es-ES')}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="w-full md:w-1/2">
              <div className="overflow-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Categoría
                      </th>
                      <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Monto gastado
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {financialData.categories.map((category, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div className="flex items-center">
                            <div 
                              className="w-3 h-3 rounded-full mr-2" 
                              style={{ backgroundColor: category.color || COLORS[index % COLORS.length] }}
                            />
                            <span>{category.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                          ${category.amount.toLocaleString('es-ES')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BasicFinancialDashboard;