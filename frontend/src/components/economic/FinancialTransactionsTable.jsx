import React, { useState, useEffect } from 'react';
import { financialService } from '../../services/api';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';
import { FaReceipt, FaCalendarAlt } from 'react-icons/fa';
import { MdError, MdInfo } from 'react-icons/md';

const FinancialTransactionsTable = ({ patientId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setLoading(true);
        const response = await financialService.getFinancialTransactions(patientId);
        setTransactions(response.data || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching transactions:', err);
        setError('No se pudieron cargar las transacciones');
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
    // Actualizar cada 5 minutos
    const interval = setInterval(fetchTransactions, 300000);
    return () => clearInterval(interval);
  }, [patientId]);

  // Formatear fecha para mostrar
  const formatDate = (dateString) => {
    if (!dateString) return 'No disponible';
    try {
      const date = parseISO(dateString);
      return format(date, 'dd/MM/yyyy HH:mm', { locale: es });
    } catch (e) {
      return 'Fecha inválida';
    }
  };

  // Colores para categorías
  const getCategoryColor = (category) => {
    const categoryColors = {
      'Medicamentos': 'bg-blue-100 text-blue-800',
      'Servicios básicos': 'bg-cyan-100 text-cyan-800',
      'Cuidados': 'bg-red-100 text-red-800',
      'Salud': 'bg-orange-100 text-orange-800',
      'Supermercado': 'bg-green-100 text-green-800',
      'Transporte': 'bg-purple-100 text-purple-800',
      'Vivienda': 'bg-indigo-100 text-indigo-800',
      'Recreación': 'bg-amber-100 text-amber-800',
      'Varios': 'bg-gray-100 text-gray-800',
      'Otros': 'bg-gray-100 text-gray-800'
    };
    
    return categoryColors[category] || 'bg-gray-100 text-gray-800';
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

  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-6 flex-grow">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Últimas Transacciones</h2>
          <FaReceipt className="text-blue-500 text-xl" />
        </div>
        
        <div className="border-t border-gray-200 my-4"></div>
        
        {transactions.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 flex flex-col items-center justify-center h-64">
            <MdInfo className="text-blue-400 text-5xl mb-4 opacity-50" />
            <p className="text-gray-600 text-center">No hay transacciones disponibles</p>
            <p className="text-gray-500 text-sm text-center mt-2">Las transacciones registradas aparecerán aquí</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Categoría
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Monto
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Descripción
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {transactions.map((transaction) => (
                  <tr key={transaction.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center">
                        <FaCalendarAlt className="text-gray-400 mr-2" />
                        {formatDate(transaction.date)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getCategoryColor(transaction.category)}`}>
                        {transaction.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-gray-900">
                      ${transaction.amount.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 truncate max-w-xs">
                      {transaction.description}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialTransactionsTable;