from flask import Flask, request, jsonify, send_file
import logging
import os
import requests
import sqlite3
import json
import tempfile
from fpdf import FPDF
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pdf_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Diccionario de traducciones para los elementos del reporte
translations = {
    'es': {
        'title': 'Reporte Astrológico',
        'name': 'Nombre',
        'dob': 'Fecha de Nacimiento',
        'tob': 'Hora de Nacimiento',
        'pob': 'Lugar de Nacimiento',
        'zodiac_sign': 'Signo Zodiacal',
        'chinese_sign': 'Signo Chino',
        'music': 'Música Popular',
        'astronomy': 'Astronomía',
        'weather': 'Clima Histórico',
        'compatibility': 'Compatibilidad',
        'locations': 'Lugares Recomendados',
        'generated': 'Generado el',
        'page': 'Página',
        'of': 'de',
        'free_report': 'Reporte Gratuito',
        'premium_report': 'Reporte Premium'
    },
    'en': {
        'title': 'Astrological Report',
        'name': 'Name',
        'dob': 'Date of Birth',
        'tob': 'Time of Birth',
        'pob': 'Place of Birth',
        'zodiac_sign': 'Zodiac Sign',
        'chinese_sign': 'Chinese Sign',
        'music': 'Popular Music',
        'astronomy': 'Astronomy',
        'weather': 'Historical Weather',
        'compatibility': 'Compatibility',
        'locations': 'Recommended Locations',
        'generated': 'Generated on',
        'page': 'Page',
        'of': 'of',
        'free_report': 'Free Report',
        'premium_report': 'Premium Report'
    },
    'pt': {
        'title': 'Relatório Astrológico',
        'name': 'Nome',
        'dob': 'Data de Nascimento',
        'tob': 'Hora de Nascimento',
        'pob': 'Local de Nascimento',
        'zodiac_sign': 'Signo do Zodíaco',
        'chinese_sign': 'Signo Chinês',
        'music': 'Música Popular',
        'astronomy': 'Astronomia',
        'weather': 'Clima Histórico',
        'compatibility': 'Compatibilidade',
        'locations': 'Locais Recomendados',
        'generated': 'Gerado em',
        'page': 'Página',
        'of': 'de',
        'free_report': 'Relatório Gratuito',
        'premium_report': 'Relatório Premium'
    },
    'fr': {
        'title': 'Rapport Astrologique',
        'name': 'Nom',
        'dob': 'Date de Naissance',
        'tob': 'Heure de Naissance',
        'pob': 'Lieu de Naissance',
        'zodiac_sign': 'Signe du Zodiaque',
        'chinese_sign': 'Signe Chinois',
        'music': 'Musique Populaire',
        'astronomy': 'Astronomie',
        'weather': 'Météo Historique',
        'compatibility': 'Compatibilité',
        'locations': 'Lieux Recommandés',
        'generated': 'Généré le',
        'page': 'Page',
        'of': 'sur',
        'free_report': 'Rapport Gratuit',
        'premium_report': 'Rapport Premium'
    },
    'de': {
        'title': 'Astrologischer Bericht',
        'name': 'Name',
        'dob': 'Geburtsdatum',
        'tob': 'Geburtszeit',
        'pob': 'Geburtsort',
        'zodiac_sign': 'Sternzeichen',
        'chinese_sign': 'Chinesisches Zeichen',
        'music': 'Populäre Musik',
        'astronomy': 'Astronomie',
        'weather': 'Historisches Wetter',
        'compatibility': 'Kompatibilität',
        'locations': 'Empfohlene Orte',
        'generated': 'Erstellt am',
        'page': 'Seite',
        'of': 'von',
        'free_report': 'Kostenloser Bericht',
        'premium-Bericht': 'Premium-Bericht'
    }
}

def get_translation(key, language='es'):
    """Obtiene la traducción de una clave en el idioma especificado"""
    if language not in translations:
        language = 'es'  # Idioma por defecto
    
    return translations[language].get(key, key)

def verify_api_key(api_key):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            json={"api_key": api_key}
        )
        return response.status_code == 200 and response.json().get("valid", False)
    except Exception as e:
        logger.error(f"Error al verificar API key: {str(e)}")
        return False

def init_db():
    conn = sqlite3.connect('pdf.db')
    cursor = conn.cursor()
    
    # Tabla para caché de PDFs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdf_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        city_of_birth TEXT NOT NULL,
        report_type TEXT NOT NULL DEFAULT 'free',
        pdf_path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(name, date_of_birth, city_of_birth, report_type)
    )
    ''')
    
    conn.commit()
    conn.close()

class AstroPDF(FPDF):
    def __init__(self, report_type='free'):
        super().__init__()
        self.report_type = report_type
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Logo
        # self.image('logo.png', 10, 8, 33)
        # Título
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(50, 50, 50)
        
        if self.report_type == 'premium':
            self.cell(0, 10, 'Informe Astrológico Premium', align='C', ln=1)
        else:
            self.cell(0, 10, 'Informe Astrológico Básico', align='C', ln=1)
            
        self.ln(10)

    def footer(self):
        # Posición a 1.5 cm del final
        self.set_y(-15)
        # Fuente
        self.set_font('Helvetica', 'I', 8)
        # Número de página
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

    def add_title_page(self, name, birth_date, location):
        self.add_page()
        self.set_font('Helvetica', 'B', 20)
        
        if self.report_type == 'premium':
            self.set_text_color(128, 0, 128)  # Púrpura para premium
        else:
            self.set_text_color(0, 102, 204)  # Azul para básico
            
        self.cell(0, 20, f"Carta Astral de {name}", ln=1, align='C')
        self.ln(10)
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Fecha de Nacimiento: {birth_date}", ln=1, align='C')
        self.cell(0, 10, f"Lugar de Nacimiento: {location}", ln=1, align='C')
        
        if self.report_type == 'premium':
            self.ln(5)
            self.set_font('Helvetica', 'B', 12)
            self.set_text_color(128, 0, 128)
            self.cell(0, 10, "REPORTE PREMIUM", ln=1, align='C')
            
        self.ln(20)

    def add_chart(self, chart_path):
        if os.path.exists(chart_path):
            self.image(chart_path, x=10, y=self.get_y(), w=190)
            self.ln(150)
        else:
            self.set_font('Helvetica', 'I', 12)
            self.cell(0, 10, "Imagen de carta astral no disponible", ln=1, align='C')
            self.ln(10)

    def add_section(self, title, content):
        self.set_font('Helvetica', 'B', 16)
        
        if self.report_type == 'premium':
            self.set_text_color(128, 0, 128)  # Púrpura para premium
        else:
            self.set_text_color(0, 102, 204)  # Azul para básico
            
        self.cell(0, 10, title, ln=1)
        self.ln(5)
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, content)
        self.ln(10)
        
    def add_zodiac_section(self, zodiac_data):
        if not zodiac_data:
            return
            
        self.add_section("Información Zodiacal", 
            f"Signo Zodiacal Occidental: {zodiac_data.get('western_zodiac', 'No disponible')}\n"
            f"Signo Zodiacal Chino: {zodiac_data.get('chinese_zodiac', 'No disponible')}"
        )
        
    def add_compatibility_section(self, compatibility_data):
        if not compatibility_data:
            return
            
        self.add_section("Compatibilidad", compatibility_data.get('compatibility_report', 'No disponible'))
        
    def add_location_section(self, location_data):
        if not location_data or 'recommended_places' not in location_data:
            return
            
        self.add_section("Lugares Recomendados", "")
        
        for place in location_data.get('recommended_places', []):
            self.set_font('Helvetica', 'B', 14)
            self.cell(0, 10, place.get('name', 'Lugar desconocido'), ln=1)
            
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 8, place.get('description', 'Sin descripción'))
            
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, "Para trabajo:", ln=1)
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 8, place.get('work_compatibility', 'No disponible'))
            
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, "Para relaciones:", ln=1)
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 8, place.get('relationship_compatibility', 'No disponible'))
            
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, "Mejor época:", ln=1)
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 8, place.get('best_time', 'No disponible'))
            
            self.ln(10)
            
    def add_music_section(self, music_data):
        if not music_data or 'top_songs' not in music_data:
            return
            
        self.add_section("Música Popular en tu Fecha de Nacimiento", "")
        
        for song in music_data.get('top_songs', [])[:5]:  # Limitamos a 5 canciones
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, f"{song.get('song', 'Canción desconocida')} - {song.get('artist', 'Artista desconocido')}", ln=1)
            self.set_font('Helvetica', 'I', 10)
            self.cell(0, 8, f"Posición #{song.get('rank', 'N/A')} el {song.get('date', 'fecha desconocida')}", ln=1)
            self.ln(5)
            
    def add_astronomy_section(self, astronomy_data):
        if not astronomy_data:
            return
            
        content = f"Fase Lunar: {astronomy_data.get('moon_phase', 'No disponible')}\n\n"
        
        if 'planetary_positions' in astronomy_data:
            content += "Posiciones Planetarias:\n"
            for planet in astronomy_data.get('planetary_positions', []):
                content += f"- {planet.get('planet', 'Planeta desconocido')}: RA {planet.get('ra', 'N/A')}, DEC {planet.get('dec', 'N/A')}\n"
                
        self.add_section("Información Astronómica", content)
        
    def add_weather_section(self, weather_data):
        if not weather_data:
            return
            
        content = f"Temperatura: {weather_data.get('temperature', 'No disponible')}°C\n"
        content += f"Condiciones: {weather_data.get('description', 'No disponible')}"
                
        self.add_section("Condiciones Climáticas en tu Nacimiento", content)

def create_pie_chart(values, labels, output_path, title="Distribución de Elementos"):
    """Create a pie chart with given values and labels."""
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, 
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
            wedgeprops={'edgecolor': 'black'})
    plt.title(title, fontsize=14, color='darkblue')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.savefig(output_path, format='png', bbox_inches='tight')
    plt.close()

def create_bar_chart(values, labels, output_path, title="Compatibilidad por Elemento"):
    """Create a bar chart with given values and labels."""
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    
    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.title(title, fontsize=14, color='darkblue')
    plt.ylim(0, 100)  # Establecer límite de 0 a 100%
    plt.savefig(output_path, format='png', bbox_inches='tight')
    plt.close()

def generate_astrological_pdf(name, birth_date, location, report_type, summary_data, text_content, 
                             zodiac_data=None, astronomy_data=None, music_data=None, weather_data=None,
                             compatibility_data=None, location_data=None, output_file=None):
    """Generate a complete astrological report PDF."""
    if not output_file:
        temp_dir = tempfile.mkdtemp()
        output_file = os.path.join(temp_dir, f"{name.replace(' ', '_')}_astrological_report.pdf")
    
    # Crear directorio temporal para gráficos
    temp_dir = os.path.dirname(output_file)
    chart_path = os.path.join(temp_dir, 'chart.png')
    
    # Crear gráfico de elementos
    if zodiac_data and 'western_zodiac' in zodiac_data:
        # Asignar valores según el signo zodiacal
        zodiac_sign = zodiac_data.get('western_zodiac')
        
        # Valores de ejemplo para los elementos (fuego, tierra, aire, agua)
        element_values = {
            'Aries': [70, 10, 15, 5],
            'Leo': [75, 5, 15, 5],
            'Sagitario': [65, 10, 20, 5],
            'Tauro': [5, 70, 15, 10],
            'Virgo': [10, 65, 20, 5],
            'Capricornio': [5, 75, 10, 10],
            'Géminis': [15, 10, 70, 5],
            'Libra': [10, 5, 75, 10],
            'Acuario': [15, 5, 70, 10],
            'Cáncer': [5, 15, 10, 70],
            'Escorpio': [10, 10, 5, 75],
            'Piscis': [5, 10, 15, 70]
        }
        
        values = element_values.get(zodiac_sign, [25, 25, 25, 25])  # Valores por defecto si no se encuentra el signo
        create_pie_chart(values, ['Fuego', 'Tierra', 'Aire', 'Agua'], chart_path)
    else:
        # Crear gráfico genérico si no hay datos zodiacales
        create_pie_chart([25, 25, 25, 25], ['Fuego', 'Tierra', 'Aire', 'Agua'], chart_path)
    
    # Crear PDF
    pdf = AstroPDF(report_type)
    pdf.alias_nb_pages()
    pdf.add_title_page(name, birth_date, location)
    
    # Añadir gráfico
    pdf.add_chart(chart_path)
    
    # Añadir resumen
    if summary_data:
        summary_text = '\n'.join(summary_data)
        pdf.add_section("Resumen", summary_text)
    
    # Añadir información zodiacal
    if zodiac_data:
        pdf.add_zodiac_section(zodiac_data)
    
    # Añadir contenido principal
    if text_content:
        pdf.add_section("Análisis Detallado", text_content)
    
    # Añadir secciones adicionales para reportes premium
    if report_type == 'premium':
        # Compatibilidad
        if compatibility_data:
            pdf.add_compatibility_section(compatibility_data)
            
        # Lugares recomendados
        if location_data:
            pdf.add_location_section(location_data)
            
        # Música
        if music_data:
            pdf.add_music_section(music_data)
            
        # Astronomía
        if astronomy_data:
            pdf.add_astronomy_section(astronomy_data)
            
        # Clima
        if weather_data:
            pdf.add_weather_section(weather_data)
    
    # Guardar el PDF
    pdf.output(output_file)
    return output_file

class PDFGenerator:
    def __init__(self, report_data, report_type="free", language="es"):
        self.report_data = report_data
        self.report_type = report_type
        self.language = language
        self.buffer = io.BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.styles = getSampleStyleSheet()
        self.elements = []
        
        # Añadir estilo personalizado para títulos
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        ))
        
        # Añadir estilo personalizado para subtítulos
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        ))
        
        # Añadir estilo personalizado para información personal
        self.styles.add(ParagraphStyle(
            name='Info',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6
        ))
    
    def add_title(self):
        title = get_translation('title', self.language)
        report_type = get_translation('premium_report' if self.report_type == 'premium' else 'free_report', self.language)
        self.elements.append(Paragraph(f"{title} - {report_type}", self.styles['Title']))
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_personal_info(self):
        name = self.report_data.get('name', '')
        dob = self.report_data.get('date_of_birth', '')
        tob = self.report_data.get('time_of_birth', '')
        pob = self.report_data.get('city_of_birth', '')
        
        # Crear tabla para información personal
        data = [
            [f"{get_translation('name', self.language)}:", name],
            [f"{get_translation('dob', self.language)}:", dob],
            [f"{get_translation('tob', self.language)}:", tob],
            [f"{get_translation('pob', self.language)}:", pob]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.white)
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_zodiac_info(self):
        zodiac_info = self.report_data.get('zodiac_info', {})
        if not zodiac_info:
            return
        
        self.elements.append(Paragraph(get_translation('zodiac_sign', self.language), self.styles['Subtitle']))
        
        western_zodiac = zodiac_info.get('western_zodiac', '')
        chinese_zodiac = zodiac_info.get('chinese_zodiac', '')
        
        # Añadir información zodiacal
        self.elements.append(Paragraph(f"{get_translation('zodiac_sign', self.language)}: {western_zodiac}", self.styles['Info']))
        self.elements.append(Paragraph(f"{get_translation('chinese_sign', self.language)}: {chinese_zodiac}", self.styles['Info']))
        
        # Añadir descripción del signo zodiacal
        if 'description' in zodiac_info:
            self.elements.append(Paragraph(zodiac_info['description'], self.styles['Normal']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_music_info(self):
        music_data = self.report_data.get('music_data', {})
        if not music_data:
            return
        
        self.elements.append(Paragraph(get_translation('music', self.language), self.styles['Subtitle']))
        
        # Añadir canciones populares
        if 'songs' in music_data:
            for song in music_data['songs']:
                self.elements.append(Paragraph(f"{song['title']} - {song['artist']}", self.styles['Info']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_astronomy_info(self):
        astronomy_data = self.report_data.get('astronomy_data', {})
        if not astronomy_data:
            return
        
        self.elements.append(Paragraph(get_translation('astronomy', self.language), self.styles['Subtitle']))
        
        # Añadir información astronómica
        if 'moon_phase' in astronomy_data:
            self.elements.append(Paragraph(f"Fase lunar: {astronomy_data['moon_phase']}", self.styles['Info']))
        
        if 'planets' in astronomy_data:
            for planet, position in astronomy_data['planets'].items():
                self.elements.append(Paragraph(f"{planet}: {position}", self.styles['Info']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_weather_info(self):
        weather_data = self.report_data.get('weather_data', {})
        if not weather_data:
            return
        
        self.elements.append(Paragraph(get_translation('weather', self.language), self.styles['Subtitle']))
        
        # Añadir información climática
        if 'conditions' in weather_data:
            self.elements.append(Paragraph(f"Condiciones: {weather_data['conditions']}", self.styles['Info']))
        
        if 'temperature' in weather_data:
            self.elements.append(Paragraph(f"Temperatura: {weather_data['temperature']}°C", self.styles['Info']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_compatibility_info(self):
        compatibility_data = self.report_data.get('compatibility_data', {})
        if not compatibility_data:
            return
        
        self.elements.append(Paragraph(get_translation('compatibility', self.language), self.styles['Subtitle']))
        
        # Añadir información de compatibilidad
        if 'partner_name' in compatibility_data and 'compatibility_score' in compatibility_data:
            self.elements.append(Paragraph(
                f"Compatibilidad con {compatibility_data['partner_name']}: {compatibility_data['compatibility_score']}%",
                self.styles['Info']
            ))
        
        if 'description' in compatibility_data:
            self.elements.append(Paragraph(compatibility_data['description'], self.styles['Normal']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_location_info(self):
        location_data = self.report_data.get('location_data', {})
        if not location_data:
            return
        
        self.elements.append(Paragraph(get_translation('locations', self.language), self.styles['Subtitle']))
        
        # Añadir lugares recomendados
        if 'recommended_locations' in location_data:
            for location in location_data['recommended_locations']:
                self.elements.append(Paragraph(f"{location['name']}: {location['description']}", self.styles['Info']))
        
        self.elements.append(Spacer(1, 0.25*inch))
    
    def add_footer(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        footer_text = f"{get_translation('generated', self.language)}: {now}"
        self.elements.append(Spacer(1, 0.5*inch))
        self.elements.append(Paragraph(footer_text, self.styles['Normal']))
    
    def generate(self):
        self.add_title()
        self.add_personal_info()
        self.add_zodiac_info()
        
        # Añadir información adicional para reportes premium
        if self.report_type == 'premium':
            if 'music_data' in self.report_data:
                self.add_music_info()
            
            if 'astronomy_data' in self.report_data:
                self.add_astronomy_info()
            
            if 'weather_data' in self.report_data:
                self.add_weather_info()
            
            if 'compatibility_data' in self.report_data:
                self.add_compatibility_info()
            
            if 'location_data' in self.report_data:
                self.add_location_info()
        
        self.add_footer()
        
        # Construir el PDF
        self.doc.build(self.elements)
        
        # Obtener el contenido del buffer
        pdf = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    report_data = data.get('report_data', {})
    report_type = data.get('report_type', 'free')
    language = data.get('language', 'es')
    
    if not report_data:
        return jsonify({"error": "Report data is required"}), 400
    
    try:
        pdf_generator = PDFGenerator(report_data, report_type, language)
        pdf = pdf_generator.generate()
        
        return pdf, 200, {'Content-Type': 'application/pdf'}
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5008)

