# backend/app/services/classification_service.py
import logging
import json
from datetime import datetime
from app.extensions import db
from app.models.message import Message
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.classified_value import ClassifiedValue
from app.services.gemini_service import GeminiService

# Configuración de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClassificationService:
    """
    Servicio para gestionar la clasificación de mensajes y 
    almacenamiento de datos clasificados usando la estructura normalizada
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
                content=message_text,
                caregiver_id=1,  # Esto se debería obtener del teléfono
                patient_id=patient_id or 1  # Fallback a ID 1 si no se proporciona
            )
            db.session.add(message)
            db.session.commit()
            logger.info(f"Mensaje guardado con ID: {message.id}")
            
            # 2. Clasificar mensaje
            classification_result = self.gemini_service.classify_message(message_text)
            logger.info(f"Mensaje clasificado: {len(classification_result.get('categorias', []))} categorías detectadas")
            
            # 3. Guardar datos clasificados en estructura normalizada
            if "error" not in classification_result:
                saved_values = self._save_normalized_classification(message.id, classification_result, patient_id or 1)
                logger.info(f"Datos clasificados guardados: {saved_values} valores para mensaje ID: {message.id}")
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
    
    def _save_normalized_classification(self, message_id, classification_data, patient_id):
        """
        Guarda los datos clasificados en la estructura normalizada
        
        Args:
            message_id (int): ID del mensaje original
            classification_data (dict): Datos clasificados
            patient_id (int): ID del paciente
            
        Returns:
            int: Número de valores guardados
        """
        saved_count = 0
        
        try:
            # Procesar cada categoría en la respuesta
            for categoria in classification_data.get('categorias', []):
                if not categoria.get('detectada', False):
                    continue
                    
                # Buscar la categoría en la BD por nombre (case-insensitive)
                category_name = categoria.get('nombre')
                category = Category.query.filter(
                    db.func.lower(Category.name) == db.func.lower(category_name)
                ).first()
                
                if not category:
                    # Registrar que no se encontró la categoría y continuar
                    logger.warning(f"Categoría no encontrada: {category_name}")
                    continue
                    
                # Procesar subcategorías
                for subcategoria in categoria.get('subcategorias', []):
                    if not subcategoria.get('detectada', False):
                        continue
                        
                    # Buscar la subcategoría por nombre dentro de la categoría (case-insensitive)
                    subcategory_name = subcategoria.get('nombre')
                    subcategory = Subcategory.query.filter(
                        db.func.lower(Subcategory.name) == db.func.lower(subcategory_name),
                        Subcategory.category_id == category.id
                    ).first()
                    
                    if not subcategory:
                        # Registrar que no se encontró la subcategoría y continuar
                        logger.warning(
                            f"Subcategoría no encontrada: {subcategory_name} en categoría {category_name}"
                        )
                        continue
                    
                    # Solo crear el valor clasificado si hay un valor no vacío
                    valor = subcategoria.get('valor')
                    if valor and valor.strip():
                        # Crear el valor clasificado
                        classified_value = ClassifiedValue(
                            message_id=message_id,
                            subcategory_id=subcategory.id,
                            value=valor,
                            confidence=subcategoria.get('confianza', 0.0)
                        )
                        db.session.add(classified_value)
                        saved_count += 1
                        logger.info(f"Valor clasificado guardado: {category_name} > {subcategory_name}: {valor}")
            
            # Confirmar cambios
            db.session.commit()
            logger.info(f"Total de valores clasificados guardados: {saved_count}")
            
            return saved_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error guardando valores clasificados: {str(e)}")
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
        from datetime import datetime, timedelta
        
        try:
            # Calcular fecha de inicio
            start_date = datetime.now() - timedelta(days=days)
            
            # Obtener valores clasificados para el paciente en el período
            values = ClassifiedValue.query.join(
                Message, ClassifiedValue.message_id == Message.id
            ).join(
                Subcategory, ClassifiedValue.subcategory_id == Subcategory.id
            ).join(
                Category, Subcategory.category_id == Category.id
            ).filter(
                Message.patient_id == patient_id,
                Message.created_at >= start_date
            ).order_by(Message.created_at.desc()).all()
            
            # Agrupar por categoría
            summary = {}
            for value in values:
                category_name = value.subcategory.category.name
                subcategory_name = value.subcategory.name
                
                if category_name not in summary:
                    summary[category_name] = {}
                
                if subcategory_name not in summary[category_name]:
                    summary[category_name][subcategory_name] = []
                
                summary[category_name][subcategory_name].append({
                    'value': value.value,
                    'confidence': value.confidence,
                    'date': value.created_at.isoformat(),
                    'message_id': value.message_id
                })
            
            return {
                'patient_id': patient_id,
                'period_days': days,
                'summary': summary,
                'total_values': len(values)
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo resumen para paciente {patient_id}: {str(e)}")
            return {
                'error': str(e),
                'patient_id': patient_id,
                'period_days': days
            }