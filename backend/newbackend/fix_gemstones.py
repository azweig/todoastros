#!/usr/bin/env python3
import os

# Ruta al archivo del servicio de gemas
gemstones_file = "gemstones_service/gemstones_service.py"

# Verificar si el archivo existe
if not os.path.exists(gemstones_file):
    print(f"Error: No se encontró el archivo {gemstones_file}")
    exit(1)

# Leer el contenido del archivo
with open(gemstones_file, 'r') as f:
    content = f.read()

# Crear una copia de seguridad
with open(f"{gemstones_file}.bak", 'w') as f:
    f.write(content)
print(f"Copia de seguridad creada en {gemstones_file}.bak")

# Buscar la función gemstones
start = content.find('@app.route(\'/gemstones\', methods=[\'POST\'])')
end = content.find('if __name__ == "__main__":', start)

if start == -1 or end == -1:
    print("No se pudo encontrar la función gemstones en el archivo")
    exit(1)

# Nueva implementación de la función gemstones
new_function = '''@app.route('/gemstones', methods=['POST'])
def gemstones():
    """Endpoint para obtener información sobre gemas y cristales para un signo zodiacal."""
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        sign = data.get('sign', '')
        name = data.get('name', '')
        birth_date = data.get('birth_date', '')
        chinese_sign = data.get('chinese_sign', '')
        vedic_sign = data.get('vedic_sign', '')

        # Validar datos requeridos
        if not sign:
            logger.warning("Solicitud con datos incompletos")
            return jsonify({"error": "Falta el signo zodiacal"}), 400

        # Generar hash para la consulta
        query_data = {
            "sign": sign,
            "name": name,
            "birth_date": birth_date,
            "chinese_sign": chinese_sign,
            "vedic_sign": vedic_sign
        }
        query_hash = get_query_hash(query_data)

        # Verificar si ya existe una respuesta almacenada
        stored_response = get_stored_response(query_hash)
        if stored_response:
            logger.info(f"Usando respuesta almacenada para signo {sign}")
            return jsonify(stored_response)

        # Usar siempre datos simulados
        logger.info(f"Usando datos simulados para signo {sign}")
        
        # Respuesta simulada para todos los signos
        gemstones_text = f"""
# Gemas y Cristales para {sign}

## 1. Cuarzo Transparente
- **Propiedades**: Claridad, amplificación, equilibrio
- **Beneficios**: Ayuda a clarificar pensamientos y amplifica la energía de otras piedras
- **Uso recomendado**: Meditación, joyería o decoración
- **Combinaciones**: Funciona bien con todas las demás piedras

## 2. Amatista
- **Propiedades**: Calma, intuición, protección
- **Beneficios**: Equilibra emociones y mejora la conexión espiritual
- **Uso recomendado**: Cerca de la cabeza durante el descanso o meditación
- **Combinaciones**: Con cuarzo rosa para amor y compasión

## 3. Turmalina Negra
- **Propiedades**: Protección, enraizamiento, purificación
- **Beneficios**: Absorbe y transforma energías negativas
- **Uso recomendado**: En entradas de hogares u oficinas
- **Combinaciones**: Con cuarzo transparente para amplificar su protección

## 4. Lapislázuli
- **Propiedades**: Sabiduría, verdad, comunicación
- **Beneficios**: Mejora la expresión personal y la búsqueda de conocimiento
- **Uso recomendado**: Colgante cerca de la garganta
- **Combinaciones**: Con amatista para mayor intuición

## 5. Citrino
- **Propiedades**: Abundancia, confianza, energía positiva
- **Beneficios**: Atrae prosperidad y mantiene un estado de ánimo positivo
- **Uso recomendado**: En espacios de trabajo o bolsillos
- **Combinaciones**: Con cuarzo ahumado para manifestación práctica
"""
        
        # Personalizar con el nombre si está disponible
        if name:
            gemstones_text = f"# Gemas y Cristales para {name} ({sign})\\n" + gemstones_text.split('\\n', 1)[1]
        
        # Preparar respuesta
        response_data = {
            "gemstones_info": gemstones_text,
            "sign": sign,
            "name": name if name else "No especificado",
            "birth_date": birth_date if birth_date else "No especificado",
            "chinese_sign": chinese_sign if chinese_sign else "No especificado",
            "vedic_sign": vedic_sign if vedic_sign else "No especificado",
            "is_mock": True
        }
        
        # Almacenar en la base de datos
        store_response(query_hash, response_data)
        
        logger.info(f"Información simulada sobre gemas generada para {sign}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
'''

# Reemplazar la función en el contenido
modified_content = content[:start] + new_function + content[end:]

# Guardar el archivo modificado
with open(gemstones_file, 'w') as f:
    f.write(modified_content)

print("Servicio de gemas modificado para usar siempre datos simulados")
