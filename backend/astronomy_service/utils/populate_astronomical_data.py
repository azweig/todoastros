import sqlite3
from datetime import datetime, timedelta
import os
import sys
import time

# Asegurarse de que skyfield esté instalado
try:
    from skyfield.api import load
except ImportError:
    print("Instalando dependencias necesarias...")
    os.system("pip install skyfield")
    from skyfield.api import load

def init_db(db_path):
    """Crea la base de datos y las tablas necesarias."""
    print(f"Inicializando base de datos en {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabla para eventos astronómicos (fases lunares, posiciones planetarias)
    cursor.execute('''CREATE TABLE IF NOT EXISTS astronomical_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        event_type TEXT,
        ra REAL,
        dec REAL,
        magnitude REAL,
        details TEXT
    )''')
    
    # Tabla para posiciones planetarias específicas
    cursor.execute('''CREATE TABLE IF NOT EXISTS planetary_positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        planet TEXT NOT NULL,
        ra REAL,
        dec REAL,
        distance REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabla para fases lunares
    cursor.execute('''CREATE TABLE IF NOT EXISTS moon_phases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        phase TEXT NOT NULL,
        phase_angle REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

def fetch_moon_phases(db_path, start_year=1925, end_year=2025):
    """Obtiene las fases lunares para el rango de años especificado."""
    print(f"Obteniendo fases lunares desde {start_year} hasta {end_year}...")
    
    # Cargar datos necesarios
    ts = load.timescale()
    
    # Intentar cargar el archivo de efemérides, descargándolo si es necesario
    try:
        eph = load('de421.bsp')
    except Exception as e:
        print(f"Error al cargar efemérides: {e}")
        print("Descargando archivo de efemérides...")
        eph = load('de421.bsp')
    
    moon, sun, earth = eph['moon'], eph['sun'], eph['earth']

    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 1, 1)
    delta = timedelta(days=1)  # Podríamos usar un intervalo mayor para optimizar

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si ya existen datos para evitar duplicados
    cursor.execute("SELECT COUNT(*) FROM moon_phases")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Ya existen {count} registros de fases lunares. ¿Desea continuar? (s/n)")
        response = input().lower()
        if response != 's':
            conn.close()
            return
        
        # Limpiar tabla existente
        cursor.execute("DELETE FROM moon_phases")
        conn.commit()

    # Contador para mostrar progreso
    total_days = (end_date - start_date).days
    processed = 0
    start_time = time.time()

    current_date = start_date
    while current_date < end_date:
        t = ts.utc(current_date.year, current_date.month, current_date.day)
        astrometric_moon = earth.at(t).observe(moon)
        astrometric_sun = earth.at(t).observe(sun)
        moon_phase = astrometric_moon.separation_from(astrometric_sun)
        phase_angle = moon_phase.degrees
        phase = determine_moon_phase(phase_angle)

        cursor.execute('''INSERT INTO moon_phases (date, phase, phase_angle)
                          VALUES (?, ?, ?)''', (
            current_date.strftime('%Y-%m-%d'),
            phase,
            phase_angle
        ))

        # También guardar en la tabla general de eventos
        cursor.execute('''INSERT INTO astronomical_events (date, event_type, details)
                          VALUES (?, ?, ?)''', (
            current_date.strftime('%Y-%m-%d'),
            'Moon Phase',
            phase
        ))

        current_date += delta
        processed += 1
        
        # Mostrar progreso cada 1000 días
        if processed % 1000 == 0:
            elapsed = time.time() - start_time
            progress = (processed / total_days) * 100
            remaining = (elapsed / processed) * (total_days - processed) if processed > 0 else 0
            print(f"Progreso: {progress:.2f}% ({processed}/{total_days}) - Tiempo restante estimado: {remaining/60:.2f} minutos")
            conn.commit()  # Commit periódico para evitar pérdida de datos

    conn.commit()
    conn.close()
    print("Fases lunares cargadas correctamente.")

def determine_moon_phase(phase_angle):
    """Determina la fase lunar basada en el ángulo de fase."""
    if 0 <= phase_angle < 45:
        return "Luna Nueva"
    elif 45 <= phase_angle < 90:
        return "Cuarto Creciente"
    elif 90 <= phase_angle < 135:
        return "Luna Llena"
    elif 135 <= phase_angle < 180:
        return "Cuarto Menguante"
    else:
        return "Desconocido"

def fetch_planetary_positions(db_path, start_year=1925, end_year=2025):
    """Obtiene posiciones planetarias para el rango de años especificado."""
    print(f"Obteniendo posiciones planetarias desde {start_year} hasta {end_year}...")
    
    # Cargar datos necesarios
    ts = load.timescale()
    
    # Intentar cargar el archivo de efemérides, descargándolo si es necesario
    try:
        planets = load('de421.bsp')
    except Exception as e:
        print(f"Error al cargar efemérides: {e}")
        print("Descargando archivo de efemérides...")
        planets = load('de421.bsp')
    
    earth = planets['earth']
    planetary_bodies = {
        'mercury': 'Mercurio',
        'venus': 'Venus',
        'mars': 'Marte',
        'jupiter barycenter': 'Júpiter',
        'saturn barycenter': 'Saturno',
        'uranus barycenter': 'Urano',
        'neptune barycenter': 'Neptuno',
        'pluto barycenter': 'Plutón'
    }

    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 1, 1)
    delta = timedelta(days=1)  # Podríamos usar un intervalo mayor para optimizar

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si ya existen datos para evitar duplicados
    cursor.execute("SELECT COUNT(*) FROM planetary_positions")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Ya existen {count} registros de posiciones planetarias. ¿Desea continuar? (s/n)")
        response = input().lower()
        if response != 's':
            conn.close()
            return
        
        # Limpiar tabla existente
        cursor.execute("DELETE FROM planetary_positions")
        conn.commit()

    # Contador para mostrar progreso
    total_days = (end_date - start_date).days
    total_calculations = total_days * len(planetary_bodies)
    processed = 0
    start_time = time.time()

    current_date = start_date
    while current_date < end_date:
        t = ts.utc(current_date.year, current_date.month, current_date.day)
        date_str = current_date.strftime('%Y-%m-%d')

        for body_key, body_name in planetary_bodies.items():
            try:
                planet = planets[body_key]
                astrometric = earth.at(t).observe(planet)
                ra, dec, distance = astrometric.radec()

                # Guardar en la tabla específica de posiciones planetarias
                cursor.execute('''INSERT INTO planetary_positions (date, planet, ra, dec, distance)
                                VALUES (?, ?, ?, ?, ?)''', (
                    date_str,
                    body_name,
                    ra.hours,
                    dec.degrees,
                    distance.au
                ))

                # También guardar en la tabla general de eventos
                cursor.execute('''INSERT INTO astronomical_events (date, event_type, ra, dec, details)
                                VALUES (?, ?, ?, ?, ?)''', (
                    date_str,
                    f'Posición Planetaria',
                    ra.hours,
                    dec.degrees,
                    f"Posición de {body_name} el {date_str}"
                ))
            except Exception as e:
                print(f"Error al procesar {body_key} para {date_str}: {e}")

            processed += 1
            
            # Mostrar progreso cada 1000 cálculos
            if processed % 1000 == 0:
                elapsed = time.time() - start_time
                progress = (processed / total_calculations) * 100
                remaining = (elapsed / processed) * (total_calculations - processed) if processed > 0 else 0
                print(f"Progreso: {progress:.2f}% ({processed}/{total_calculations}) - Tiempo restante estimado: {remaining/60:.2f} minutos")
                conn.commit()  # Commit periódico para evitar pérdida de datos

        current_date += delta

    conn.commit()
    conn.close()
    print("Posiciones planetarias cargadas correctamente.")

def main():
    """Función principal para ejecutar el script."""
    # Determinar la ruta de la base de datos
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'astronomical_data.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Usando base de datos: {db_path}")
    
    # Inicializar la base de datos
    init_db(db_path)
    
    # Menú de opciones
    while True:
        print("\nSeleccione una opción:")
        print("1. Cargar fases lunares")
        print("2. Cargar posiciones planetarias")
        print("3. Cargar todos los datos astronómicos")
        print("4. Salir")
        
        option = input("Opción: ")
        
        if option == '1':
            start_year = int(input("Año de inicio (por defecto 1925): ") or "1925")
            end_year = int(input("Año de fin (por defecto 2025): ") or "2025")
            fetch_moon_phases(db_path, start_year, end_year)
        elif option == '2':
            start_year = int(input("Año de inicio (por defecto 1925): ") or "1925")
            end_year = int(input("Año de fin (por defecto 2025): ") or "2025")
            fetch_planetary_positions(db_path, start_year, end_year)
        elif option == '3':
            start_year = int(input("Año de inicio (por defecto 1925): ") or "1925")
            end_year = int(input("Año de fin (por defecto 2025): ") or "2025")
            fetch_moon_phases(db_path, start_year, end_year)
            fetch_planetary_positions(db_path, start_year, end_year)
            print("Todos los datos astronómicos han sido cargados.")
        elif option == '4':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
