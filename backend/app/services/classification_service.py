import logging
from datetime import datetime
from app.extensions import db
from app.models.message import Message
from app.models.classified_data import ClassifiedData
from app.services.gemini_service import GeminiService

# Configuración de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClassificationService:
    """
    Servicio para gestionar la clasificación de mensajes y 
    almacenamiento de datos clasificados
    """
    
    def __init__(self):
        """Inicializa el servicio de clasificación"""
        self.gemini_service = GeminiService()
    
    def process_message(self, message_text, phone_number, patient_id=None):
        """
        Procesa un mensaje recibido: lo guarda, clasifica y almacena resultados
        
        Args:
            message_text (str): Texto del mensaje
            phone_number (str): Número de teléfono del remitente
            patient_id (int, optional): ID del paciente asociado
            
        Returns:
            dict: Datos procesados y resultados de la clasificación
        """
        try:
            # 1. Guardar mensaje original
            message = Message(
                text=message_text,
                phone_number=phone_number,
                patient_id=patient_id,
                received_at=datetime.utcnow()
            )
            db.session.add(message)
            db.session.commit()
            logger.info(f"Mensaje guardado con ID: {message.id}")
            
            # 2. Clasificar mensaje
            classification_result = self.gemini_service.classify_message(message_text)
            logger.info(f"Mensaje clasificado: {len(classification_result.get('categorias', []))} categorías detectadas")
            
            # 3. Guardar datos clasificados
            if "error" not in classification_result:
                self._save_classification_data(message.id, classification_result)
                logger.info(f"Datos clasificados guardados para el mensaje ID: {message.id}")
            else:
                logger.error(f"Error en clasificación para mensaje ID {message.id}: {classification_result.get('error')}")
            
            return {
                "message_id": message.id,
                "classification": classification_result,
                "status": "error" if "error" in classification_result else "success"
            }
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def _save_classification_data(self, message_id, classification_data):
        """
        Guarda los datos clasificados en la base de datos
        
        Args:
            message_id (int): ID del mensaje original
            classification_data (dict): Datos clasificados
        """
        try:
            # Obtener resumen
            resumen = classification_data.get("resumen", "")
            
            # Procesar cada categoría detectada
            for categoria in classification_data.get("categorias", []):
                if not categoria.get("detectada", False):
                    continue
                    
                categoria_nombre = categoria.get("nombre", "")
                
                # Procesar subcategorías
                for subcategoria in categoria.get("subcategorias", []):
                    if not subcategoria.get("detectada", False):
                        continue
                        
                    subcategoria_nombre = subcategoria.get("nombre", "")
                    valor = subcategoria.get("valor", "")
                    confianza = subcategoria.get("confianza", 0.0)
                    
                    # Crear registro de datos clasificados
                    classified_data = ClassifiedData(
                        message_id=message_id,
                        category=categoria_nombre,
                        subcategory=subcategoria_nombre,
                        value=valor,
                        confidence=confianza,
                        summary=resumen
                    )
                    db.session.add(classified_data)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error guardando datos clasificados: {str(e)}")
            raise
    
    def get_patient_classification_summary(self, patient_id, days=7):
        """
        Obtiene un resumen de los datos clasificados de un paciente
        
        Args:
            patient_id (int): ID del paciente
            days (int): Número de días para el resumen
            
        Returns:
            dict: Resumen de los datos clasificados
        """
        # Este método se implementará en el futuro para obtener datos para el dashboard
        pass