# backend/app/services/whatsapp_service.py
def extract_message_from_whatsapp(data):
    """
    Extrae el texto del mensaje, ID y número de teléfono de la estructura de datos de WhatsApp.
    
    Args:
        data (dict): Datos del webhook de WhatsApp
        
    Returns:
        tuple: (texto_mensaje, id_mensaje, numero_telefono) o (None, None, None) si hay error
    """
    try:
        # Ejemplo de estructura (ajustar según documentación actual de WhatsApp):
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [{}])[0]
        
        # Extraer texto del mensaje
        text = messages.get('text', {}).get('body', '')
        
        # Extraer ID del mensaje
        message_id = messages.get('id', '')
        
        # Extraer número de teléfono
        from_obj = messages.get('from', '')
        
        return text, message_id, from_obj
    except (IndexError, KeyError, TypeError) as e:
        print(f"Error extrayendo mensaje: {e}")
        return None, None, None