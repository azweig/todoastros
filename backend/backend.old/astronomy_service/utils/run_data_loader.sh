#!/bin/bash

# Crear volumen para datos si no existe
docker volume create astronomical_data

# Construir la imagen
docker build -f utils/Dockerfile.data_loader -t astronomical_data_loader .

# Ejecutar el contenedor
docker run -it --rm \
  -v astronomical_data:/data \
  astronomical_data_loader
