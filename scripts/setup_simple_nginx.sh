#!/bin/bash

echo "Copiando configuración simple de nginx..."
cp simple_nginx.conf /etc/nginx/sites-available/astrofuturo

echo "Creando enlace simbólico..."
ln -sf /etc/nginx/sites-available/astrofuturo /etc/nginx/sites-enabled/

# Eliminar el default si existe
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo "Eliminando configuración default de nginx..."
    rm /etc/nginx/sites-enabled/default
fi

echo "Verificando configuración de nginx..."
nginx -t

echo "Reiniciando nginx..."
systemctl restart nginx

echo "Verificando estado de nginx..."
systemctl status nginx | grep Active


