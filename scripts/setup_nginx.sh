#!/bin/bash

echo "Copiando configuración de nginx..."
cp nginx_astrofuturo.conf /etc/nginx/sites-available/astrofuturo

echo "Creando enlace simbólico..."
ln -sf /etc/nginx/sites-available/astrofuturo /etc/nginx/sites-enabled/

echo "Verificando configuración de nginx..."
nginx -t

echo "Reiniciando nginx..."
systemctl restart nginx

echo "Verificando estado de nginx..."
systemctl status nginx

