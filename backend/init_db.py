#!/usr/bin/env python3
import sqlite3
import os
import hashlib
import uuid
import logging
from datetime import datetime, timedelta

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("init_db")

def init_db(db_path):
    logger.info(f"Inicializando base de datos en {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        api_key TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL DEFAULT 'free',
        subscription_end_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_name TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(user_id, service_name)
    )
    ''')

    # Crear usuario admin por defecto
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "astrofuturo2023")

    cursor.execute("SELECT id FROM users WHERE username = ?", (admin_username,))
    if not cursor.fetchone():
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        api_key = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (username, password_hash, api_key, user_type) VALUES (?, ?, ?, ?)",
            (admin_username, password_hash, api_key, "admin")
        )
        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)",
            (api_key, user_id)
        )
        logger.info(f"Usuario admin creado con API key: {api_key}")
        
        # Asignar todos los servicios al admin
        all_services = ['zodiac', 'basic_report', 'music', 'astronomy', 'weather', 
                        'astro_report', 'news', 'compatibility', 'location_recommendation']
        for service in all_services:
            cursor.execute(
                "INSERT INTO user_services (user_id, service_name) VALUES (?, ?)",
                (user_id, service)
            )
        logger.info(f"Servicios asignados al usuario admin")

    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada correctamente")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = 'auth.db'
    init_db(db_path)
