import sqlite3

conn = sqlite3.connect('auth.db')
cursor = conn.cursor()

# Verificar los servicios actuales
cursor.execute('SELECT service_name FROM user_services WHERE user_id = 1')
current_services = [row[0] for row in cursor.fetchall()]
print('Servicios actuales:', current_services)

# Lista de todos los servicios que debería tener el admin
all_services = [
    'zodiac', 'basic_report', 'music', 'astronomy', 'weather', 
    'astro_report', 'news', 'compatibility', 'location', 'location_recommendation',
    'geographic', 'houses', 'gemstones', 'astro_chart', 'email', 'whatsapp', 'movies'
]

# Añadir los servicios faltantes
for service in all_services:
    if service not in current_services:
        try:
            cursor.execute('INSERT INTO user_services (user_id, service_name) VALUES (?, ?)', (1, service))
            print(f'Servicio {service} añadido')
        except sqlite3.IntegrityError:
            print(f'El servicio {service} ya existe para el usuario 1')

conn.commit()
conn.close()
print('Operación completada')
