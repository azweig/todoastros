#!/bin/bash

# Script para configurar Nginx

# Directorio donde se guardan las configuraciones de Nginx
NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"

# Copiar archivos de configuración
sudo cp nginx/*.conf $NGINX_CONF_DIR/

# Habilitar los sitios
for conf_file in nginx/*.conf; do
    site_name=$(basename $conf_file)
    sudo ln -sf $NGINX_CONF_DIR/$site_name $NGINX_ENABLED_DIR/$site_name
done

# Verificar la configuración de Nginx
sudo nginx -t

# Si la configuración es correcta, reiniciar Nginx
if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
    echo "Nginx se ha configurado correctamente."
else
    echo "Error en la configuración de Nginx. Por favor revisa los archivos de configuración."
fi
