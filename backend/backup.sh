#!/bin/bash

# Script para realizar copias de seguridad de Astrofuturo

# Directorio de backup
BACKUP_DIR="/var/backups/astrofuturo"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio de backup si no existe
mkdir -p $BACKUP_DIR

echo "Iniciando copia de seguridad de Astrofuturo..."

# Backup de los volúmenes de Docker
echo "Realizando copia de seguridad de los volúmenes..."
docker-compose down

# Crear un directorio temporal
TEMP_DIR=$(mktemp -d)

# Copiar los datos de los volúmenes
for volume in auth_data zodiac_data music_data astronomy_data weather_data astro_report_data news_data pdf_data openai_data compatibility_data location_data email_data whatsapp_data payment_data; do
    echo "Copiando volumen $volume..."
    VOLUME_PATH=$(docker volume inspect astrofuturo_$volume -f '{{ .Mountpoint }}')
    mkdir -p $TEMP_DIR/$volume
    cp -r $VOLUME_PATH/* $TEMP_DIR/$volume/ 2>/dev/null || true
done

# Comprimir los datos
echo "Comprimiendo datos..."
tar -czf $BACKUP_DIR/astrofuturo_data_$DATE.tar.gz -C $TEMP_DIR .

# Limpiar directorio temporal
rm -rf $TEMP_DIR

# Reiniciar servicios
docker-compose up -d

echo "Copia de seguridad completada: $BACKUP_DIR/astrofuturo_data_$DATE.tar.gz"

# Mantener solo las últimas 10 copias de seguridad
echo "Limpiando copias de seguridad antiguas..."
ls -t $BACKUP_DIR/astrofuturo_data_*.tar.gz | tail -n +11 | xargs rm -f

echo "Proceso de copia de seguridad finalizado."
