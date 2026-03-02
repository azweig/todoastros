#!/bin/bash

echo "📦 Organizando estructura del proyecto todoastros..."

# Crear nuevas carpetas
mkdir -p backend frontend scripts nginx logs

# ========================
# FRONTEND
# ========================
mv app frontend/
mv public frontend/ 2>/dev/null
mv *.json frontend/ 2>/dev/null
mv *.mjs frontend/ 2>/dev/null
mv *.ts frontend/ 2>/dev/null
mv tsconfig.json frontend/ 2>/dev/null
mv node_modules frontend/ 2>/dev/null
mv styles frontend/ 2>/dev/null
mv .next frontend/ 2>/dev/null

# ========================
# BACKEND
# ========================
mv *_service.py backend/
mv base_service.py backend/
mv requirements.txt backend/ 2>/dev/null
mv __pycache__ backend/ 2>/dev/null
mv backend.old backend/ 2>/dev/null
mv backend.zip backend/ 2>/dev/null
mv newbackend backend/ 2>/dev/null

# ========================
# SCRIPTS
# ========================
mv *.sh scripts/
mv *.bat scripts/ 2>/dev/null

# ========================
# NGINX CONFIG
# ========================
mv *nginx*.conf nginx/
mv nginx_config.conf nginx/

# ========================
# EXTRA
# ========================
mv logs logs_old_$(date +%s) 2>/dev/null

# ========================
# ACTUALIZAR nginx config
# ========================
sed -i 's|/var/html/todoastros|/var/html/todoastros/frontend|g' nginx/nginx_astrofuturo.conf

echo "✅ Proyecto reorganizado."

echo "📄 ATENCIÓN: revisá el archivo nginx/nginx_astrofuturo.conf para confirmar que los paths sean correctos."
echo "👉 También recordá reiniciar nginx con: sudo systemctl reload nginx"

