import React, { useState, useEffect } from 'react';
import { financialService } from '../../services/api';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer 
} from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';
import { FaChartLine } from 'react-icons/fa';
import { MdError, MdInfo } from 'react-icons/md';

const FinancialHistoryChart = ({ patientId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [historyData, setHistoryData] = useState({
    daily: [],
    weekly: [],
    monthly: []
  });
  const [selectedView, setSelectedView] = useState('monthly');

  useEffect(() => {
    const fetchHistoryData = async () => {
      try {
        setLoading(true);
        const response = await financialService.getFinancialHistory(patientId);
        
        if (response.status === 'success' && response.data) {
          setHistoryData(response.data);
        } else {
          setHistoryData({
            daily: [],
            weekly: [],
            monthly: []
          });
        }
        
        setError(null);
      } catch (err) {
        console.error('Error fetching financial history:', err);
        setError('No se pudo cargar el historial financiero');
      } finally {
        setLoading(false);
      }
    };

    fetchHistoryData();
  }, [patientId]);

  // Formateadores para las etiquetas de los ejes
  const formatXAxis = (value) => {
    try {
      switch (selectedView) {
        case 'daily':
          return format(parseISO(value), 'dd/MM', { locale: es });
        case 'weekly':
          return value.replace(/^\d{4}-W/, 'Sem ');
        case 'monthly':
          return format(parseISO(`${value}-01`), 'MMM yyyy', { locale: es });
        default:
          return value;
      }
    } catch (e) {
      return value;
    }
  };

  const formatYAxis = (value) => {
    return `$${value.toLocaleString('es-ES', { maximumFractionDigits: 0 })}`;
  };

  // Formatear tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      let formattedLabel;
      
      try {
        switch (selectedView) {
          case 'daily':
            formattedLabel = format(parseISO(label), 'dd MMM yyyy', { locale: es });
            break;
          case 'weekly':
            formattedLabel = `Semana ${label.replace(/^\d{4}-W/, '')} de ${label.substring(0, 4)}`;
            break;
          case 'monthly':
            formattedLabel = format(parseISO(`${label}-01`), 'MMMM yyyy', { locale: es });
            break;
          default:
            formattedLabel = label;
        }
      } catch (e) {
        formattedLabel = label;
      }
      
      return (
        <div className="bg-white p-2 border border-gray-200 shadow-md rounded">
          <p className="font-medium text-sm text-gray-700">{formattedLabel}</p>
          <p className="text-sm text-gray-900 font-bold">
            ${payload[0].value.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
          </p>
        </div>
      );
    }
    
    return null;
  };

  // Cambia entre las diferentes vistas
  const handleViewChange = (view) => {
    setSelectedView(view);
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md h-full flex justify-center items-center p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md h-full flex flex-col justify-center items-center p-6">
        <MdError className="text-red-500 text-5xl mb-4" />
        <h3 className="text-lg font-semibold text-red-600">Error</h3>
        <p className="text-gray-600">{error}</p>
      </div>
    );
  }

  // Determinar qué datos mostrar según la vista seleccionada
  const getViewData = () => {
    switch (selectedView) {
      case 'daily':
        return historyData.daily.map(d => ({
          date: d.date,
          amount: d.amount
        }));
      case 'weekly':
        return historyData.weekly.map(w => ({
          date: w.week,
          amount: w.amount
        }));
      case 'monthly':
        return historyData.monthly.map(m => ({
          date: m.month,
          amount: m.amount
        }));
      default:
        return [];
    }
  };

  const chartData = getViewData();
  const hasNoData = chartData.length === 0;

  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-6 flex-grow">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Historial de Gastos</h2>
          <FaChartLine className="text-blue-500 text-xl" />
        </div>
        
        <div className="flex space-x-2 mb-4">
          <button
            className={`px-3 py-1 text-sm font-medium rounded-md ${
              selectedView === 'daily' 
                ? 'bg-blue-100 text-blue-800 border border-blue-200' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={() => handleViewChange('daily')}
          >
            Diario
          </button>
          <button
            className={`px-3 py-1 text-sm font-medium rounded-md ${
              selectedView === 'weekly' 
                ? 'bg-blue-100 text-blue-800 border border-blue-200' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={() => handleViewChange('weekly')}
          >
            Semanal
          </button>
          <button
            className={`px-3 py-1 text-sm font-medium rounded-md ${
              selectedView === 'monthly' 
                ? 'bg-blue-100 text-blue-800 border border-blue-200' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={() => handleViewChange('monthly')}
          >
            Mensual
          </button>
        </div>
        
        <div className="border-t border-gray-200 my-4"></div>
        
        {hasNoData ? (
          <div className="bg-gray-50 rounded-lg p-8 flex flex-col items-center justify-center h-64">
            <MdInfo className="text-blue-400 text-5xl mb-4 opacity-50" />
            <p className="text-gray-600 text-center">No hay datos históricos disponibles</p>
            <p className="text-gray-500 text-sm text-center mt-2">
              El historial de gastos aparecerá aquí cuando haya datos
            </p>
          </div>
        ) : (
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={formatXAxis}
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  tickFormatter={formatYAxis}
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="amount"
                  name="Gastos"
                  stroke="#3b82f6"
                  activeDot={{ r: 8 }}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialHistoryChart;