#!/bin/bash

# Script para actualizar los archivos requirements.txt con versiones compatibles

# Definir las versiones compatibles
FLASK_VERSION="2.0.1"
WERKZEUG_VERSION="2.0.1"
REQUESTS_VERSION="2.26.0"
PYJWT_VERSION="2.1.0"
MATPLOTLIB_VERSION="3.4.3"
FPDF_VERSION="1.7.2"

# Función para actualizar un archivo requirements.txt
update_requirements() {
    local file=$1
    echo "Actualizando $file..."
    
    # Crear copia de seguridad
    cp "$file" "${file}.bak"
    
    # Actualizar versiones
    sed -i "s/flask==.*/flask==$FLASK_VERSION/" "$file"
    
    # Añadir werkzeug si no existe
    if ! grep -q "werkzeug" "$file"; then
        echo "werkzeug==$WERKZEUG_VERSION" >> "$file"
    else
        sed -i "s/werkzeug==.*/werkzeug==$WERKZEUG_VERSION/" "$file"
    fi
    
    # Actualizar otras dependencias si existen
    if grep -q "requests" "$file"; then
        sed -i "s/requests==.*/requests==$REQUESTS_VERSION/" "$file"
    fi
    
    if grep -q "pyjwt" "$file"; then
        sed -i "s/pyjwt==.*/pyjwt==$PYJWT_VERSION/" "$file"
    fi
    
    if grep -q "matplotlib" "$file"; then
        sed -i "s/matplotlib==.*/matplotlib==$MATPLOTLIB_VERSION/" "$file"
    fi
    
    if grep -q "fpdf" "$file"; then
        sed -i "s/fpdf==.*/fpdf==$FPDF_VERSION/" "$file"
    fi
    
    echo "✅ $file actualizado"
}

# Actualizar el archivo requirements.txt.template
update_requirements "requirements.txt.template"

# Actualizar los archivos requirements.txt de cada servicio
for service_dir in */; do
    if [ -f "${service_dir}requirements.txt" ]; then
        update_requirements "${service_dir}requirements.txt"
    fi
done

echo "Todos los archivos requirements.txt han sido actualizados."
