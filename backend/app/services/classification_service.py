#backend/app/services/classification_service.py
import logging
import json
from datetime import datetime
from app.extensions import db
from app.models.message import Message
from app.models.classified_data import ClassifiedData
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
            
            # 3. Guardar datos clasificados
            if "error" not in classification_result:
                self._save_classification_data(message.id, classification_result, patient_id or 1)
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
    
    def _save_classification_data(self, message_id, classification_data, patient_id):
        """
        Guarda los datos clasificados en la base de datos
        
        Args:
            message_id (int): ID del mensaje original
            classification_data (dict): Datos clasificados
            patient_id (int): ID del paciente
        """
        try:
            # Convertir datos a JSON
            raw_data_json = json.dumps(classification_data, ensure_ascii=False)
            
            # Extraer datos por categoría para mantener compatibilidad con la estructura anterior
            physical_health = self._extract_category_data(classification_data, "Salud Física")
            cognitive_health = self._extract_category_data(classification_data, "Salud Cognitiva")
            emotional_state = self._extract_category_data(classification_data, "Estado Emocional")
            medication = self._extract_category_data(classification_data, "Medicación")
            expenses = self._extract_category_data(classification_data, "Gastos")
            
            # Obtener resumen
            summary = classification_data.get("resumen", "")
            
            # Crear registro de datos clasificados (estructura antigua para compatibilidad)
            classified_data = ClassifiedData(
                raw_data=raw_data_json,
                physical_health=physical_health,
                cognitive_health=cognitive_health,
                emotional_state=emotional_state,
                medication=medication,
                expenses=expenses,
                summary=summary,
                message_id=message_id,
                patient_id=patient_id
            )
            
            db.session.add(classified_data)
            
            # NUEVO: Guardar en la estructura normalizada
            self._save_normalized_classification(message_id, classification_data, patient_id)
            
            db.session.commit()
            
            logger.info(f"Datos clasificados guardados para mensaje ID: {message_id}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error guardando datos clasificados: {str(e)}")
            raise

    def _extract_category_data(self, classification_data, category_name):
        """
        Extrae datos de una categoría específica y los devuelve como JSON
        
        Args:
            classification_data (dict): Datos clasificados
            category_name (str): Nombre de la categoría a extraer
            
        Returns:
            str: JSON con los datos de la categoría
        """
        import json
        
        for category in classification_data.get("categorias", []):
            if category.get("nombre") == category_name and category.get("detectada", False):
                # Extraer solo las subcategorías detectadas
                subcategories = []
                for subcategory in category.get("subcategorias", []):
                    if subcategory.get("detectada", False):
                        subcategories.append({
                            "nombre": subcategory.get("nombre", ""),
                            "valor": subcategory.get("valor", ""),
                            "confianza": subcategory.get("confianza", 0.0)
                        })
                
                # Devolver como JSON
                return json.dumps(subcategories, ensure_ascii=False)
        
        # Si no se encuentra la categoría o no está detectada, devolver lista vacía
        return json.dumps([], ensure_ascii=False)
    
    # NUEVO: Método para guardar datos en la estructura normalizada
    def _save_normalized_classification(self, message_id, classification_data, patient_id):
        """
        Guarda los datos clasificados en la estructura normalizada
        
        Args:
            message_id (int): ID del mensaje original
            classification_data (dict): Datos clasificados
            patient_id (int): ID del paciente
        """
        try:
            # Procesar cada categoría en la respuesta
            for categoria in classification_data.get('categorias', []):
                if not categoria.get('detectada', False):
                    continue
                    
                # Buscar la categoría en la BD por nombre
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
                        
                    # Buscar la subcategoría por nombre dentro de la categoría
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
                        logger.info(f"Valor clasificado guardado para subcategoría: {subcategory_name}")
            
        except Exception as e:
            logger.error(f"Error guardando valores clasificados en estructura normalizada: {str(e)}")
            # No hacer raise aquí, para permitir que siga el flujo principal si hay error
    
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