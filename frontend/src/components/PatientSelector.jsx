import { useState, useEffect } from 'react';
import { patientService } from '../services/api';

function PatientSelector({ onSelectPatient, selectedPatientId }) {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadPatients() {
      setLoading(true);
      setError(null);
      
      try {
        // En un entorno real, descomentar esta línea
        // const data = await patientService.getPatients();
        
        // Para pruebas, usamos datos de ejemplo
        const mockData = [
          { id: 1, name: 'Juan Pérez' },
          { id: 2, name: 'María López' },
          { id: 3, name: 'Carlos Rodríguez' }
        ];
        
        setPatients(mockData);
      } catch (err) {
        console.error('Error loading patients:', err);
        setError('Error al cargar la lista de pacientes');
      } finally {
        setLoading(false);
      }
    }
    
    loadPatients();
  }, []);

  return (
    <div className="patient-selector">
      <label htmlFor="patient" className="selector-label">Seleccionar Paciente:</label>
      
      {loading ? (
        <p className="loading-text">Cargando pacientes...</p>
      ) : error ? (
        <p className="error-text">{error}</p>
      ) : (
        <select 
          id="patient"
          value={selectedPatientId || ''}
          onChange={(e) => onSelectPatient(Number(e.target.value))}
          className="patient-select"
        >
          <option value="">Seleccionar paciente</option>
          {patients.map((patient) => (
            <option key={patient.id} value={patient.id}>
              {patient.name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}

export default PatientSelector;