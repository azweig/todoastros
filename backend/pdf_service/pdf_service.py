"""
TodoAstros Premium PDF Generator
Generates comprehensive natal chart PDFs with:
- Zodiac wheel visualization
- Detailed sun/moon/ascendant descriptions
- Numerology analysis (name breakdown, life path, etc.)
- Family numerology and compatibility
- Planetary positions table
- Elemental distribution
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Circle, Line, String, Wedge, Polygon
from reportlab.graphics import renderPDF
from io import BytesIO
import math
from datetime import datetime
from flask import Flask, request, jsonify, send_file
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdf_service_premium")

app = Flask(__name__)

# Color palette
COLORS = {
    'primary': HexColor('#1a1a2e'),      # Dark blue
    'secondary': HexColor('#16213e'),    # Navy
    'accent': HexColor('#e94560'),       # Coral red
    'gold': HexColor('#d4af37'),         # Gold
    'text': HexColor('#2d2d2d'),         # Dark gray
    'light': HexColor('#f5f5f5'),        # Light gray
    'fire': HexColor('#ff6b6b'),         # Fire element
    'earth': HexColor('#4ecdc4'),        # Earth element  
    'air': HexColor('#95e1d3'),          # Air element
    'water': HexColor('#6c5ce7'),        # Water element
}

# Zodiac signs data
ZODIAC_SIGNS = {
    'Aries': {'symbol': '♈', 'element': 'Fuego', 'ruler': 'Marte', 'quality': 'Cardinal'},
    'Tauro': {'symbol': '♉', 'element': 'Tierra', 'ruler': 'Venus', 'quality': 'Fijo'},
    'Géminis': {'symbol': '♊', 'element': 'Aire', 'ruler': 'Mercurio', 'quality': 'Mutable'},
    'Cáncer': {'symbol': '♋', 'element': 'Agua', 'ruler': 'Luna', 'quality': 'Cardinal'},
    'Leo': {'symbol': '♌', 'element': 'Fuego', 'ruler': 'Sol', 'quality': 'Fijo'},
    'Virgo': {'symbol': '♍', 'element': 'Tierra', 'ruler': 'Mercurio', 'quality': 'Mutable'},
    'Libra': {'symbol': '♎', 'element': 'Aire', 'ruler': 'Venus', 'quality': 'Cardinal'},
    'Escorpio': {'symbol': '♏', 'element': 'Agua', 'ruler': 'Plutón', 'quality': 'Fijo'},
    'Sagitario': {'symbol': '♐', 'element': 'Fuego', 'ruler': 'Júpiter', 'quality': 'Mutable'},
    'Capricornio': {'symbol': '♑', 'element': 'Tierra', 'ruler': 'Saturno', 'quality': 'Cardinal'},
    'Acuario': {'symbol': '♒', 'element': 'Aire', 'ruler': 'Urano', 'quality': 'Fijo'},
    'Piscis': {'symbol': '♓', 'element': 'Agua', 'ruler': 'Neptuno', 'quality': 'Mutable'},
}

# Numerology letter values
NUMEROLOGY_VALUES = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
    'Ñ': 5,  # Spanish Ñ
}

VOWELS = set('AEIOU')


def reduce_number(n):
    """Reduce a number to a single digit or master number (11, 22, 33)"""
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n


def calculate_name_numerology(name):
    """Calculate numerology values for a name"""
    name = name.upper().replace(' ', '')
    total = 0
    vowel_total = 0
    consonant_total = 0
    breakdown = []
    
    for letter in name:
        if letter in NUMEROLOGY_VALUES:
            value = NUMEROLOGY_VALUES[letter]
            breakdown.append(f"{letter}={value}")
            total += value
            if letter in VOWELS:
                vowel_total += value
            else:
                consonant_total += value
    
    return {
        'total': total,
        'reduced': reduce_number(total),
        'vowels': reduce_number(vowel_total),
        'consonants': reduce_number(consonant_total),
        'breakdown': ' + '.join(breakdown)
    }


def calculate_life_path(birth_date):
    """Calculate life path number from birth date (DD/MM/YYYY)"""
    day, month, year = birth_date.split('/')
    total = sum(int(d) for d in day) + sum(int(d) for d in month) + sum(int(d) for d in year)
    return reduce_number(total)


class PremiumPDFGenerator:
    """Generate premium natal chart PDFs"""
    
    def __init__(self, data):
        self.data = data
        self.buffer = BytesIO()
        self.width, self.height = A4
        self.styles = self._create_styles()
        
    def _create_styles(self):
        """Create custom paragraph styles"""
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='CoverTitle',
            fontName='Helvetica-Bold',
            fontSize=28,
            textColor=COLORS['primary'],
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='CoverSubtitle',
            fontName='Helvetica',
            fontSize=14,
            textColor=COLORS['text'],
            alignment=TA_CENTER,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=COLORS['primary'],
            spaceBefore=20,
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='SubsectionTitle',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=COLORS['accent'],
            spaceBefore=14,
            spaceAfter=8
        ))
        
        styles.add(ParagraphStyle(
            name='BodyText',
            fontName='Helvetica',
            fontSize=11,
            textColor=COLORS['text'],
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        ))
        
        styles.add(ParagraphStyle(
            name='Quote',
            fontName='Helvetica-Oblique',
            fontSize=11,
            textColor=COLORS['text'],
            alignment=TA_CENTER,
            spaceBefore=20,
            spaceAfter=20
        ))
        
        styles.add(ParagraphStyle(
            name='TableHeader',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=white,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='Footer',
            fontName='Helvetica',
            fontSize=9,
            textColor=COLORS['text'],
            alignment=TA_CENTER
        ))
        
        return styles
    
    def _draw_zodiac_wheel(self, canvas, x, y, radius=100):
        """Draw the natal chart zodiac wheel"""
        # Outer circle
        canvas.setStrokeColor(COLORS['primary'])
        canvas.setLineWidth(2)
        canvas.circle(x, y, radius)
        
        # Inner circles
        canvas.setLineWidth(1)
        canvas.circle(x, y, radius * 0.85)
        canvas.circle(x, y, radius * 0.6)
        canvas.circle(x, y, radius * 0.2)
        
        # Draw 12 house divisions
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = x + radius * 0.6 * math.cos(angle)
            y1 = y + radius * 0.6 * math.sin(angle)
            x2 = x + radius * math.cos(angle)
            y2 = y + radius * math.sin(angle)
            canvas.line(x1, y1, x2, y2)
        
        # Draw zodiac symbols
        canvas.setFont('Helvetica', 10)
        signs = list(ZODIAC_SIGNS.keys())
        for i, sign in enumerate(signs):
            angle = math.radians(i * 30 + 15 - 90)
            sx = x + radius * 0.92 * math.cos(angle)
            sy = y + radius * 0.92 * math.sin(angle)
            canvas.drawCentredString(sx, sy - 4, ZODIAC_SIGNS[sign]['symbol'])
        
        # Draw cardinal points
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawCentredString(x, y + radius + 15, "MC")
        canvas.drawCentredString(x, y - radius - 15, "IC")
        canvas.drawCentredString(x + radius + 15, y, "DSC")
        canvas.drawCentredString(x - radius - 18, y, "ASC")
        
        # Draw planet positions (simplified - actual positions would come from data)
        planets = self.data.get('planets', [])
        canvas.setFont('Helvetica', 8)
        for planet in planets:
            # Calculate position based on sign and degree
            # This is simplified - real implementation would use actual positions
            pass
    
    def _add_cover_page(self, story):
        """Add the cover page with zodiac wheel"""
        name = self.data.get('name', 'Nombre')
        location = self.data.get('location', 'Ubicación')
        birth_date = self.data.get('birth_date', '01/01/1990')
        birth_time = self.data.get('birth_time', '12:00')
        
        sun_sign = self.data.get('sun_sign', 'Aries')
        moon_sign = self.data.get('moon_sign', 'Tauro')
        ascendant = self.data.get('ascendant', 'Géminis')
        
        # Title
        story.append(Spacer(1, 30*mm))
        story.append(Paragraph("COSMOGRAMA NATAL COMPLETO", self.styles['CoverTitle']))
        story.append(Spacer(1, 15*mm))
        
        # Name
        story.append(Paragraph(f"<b>{name}</b>", self.styles['CoverTitle']))
        story.append(Spacer(1, 5*mm))
        
        # Birth info
        story.append(Paragraph(
            f"{location.upper()} • {birth_date} • {birth_time}",
            self.styles['CoverSubtitle']
        ))
        story.append(Spacer(1, 40*mm))
        
        # Key placements
        placements = f"""
        <b>■ SOL EN {sun_sign.upper()}</b><br/>
        <b>■ LUNA EN {moon_sign.upper()}</b><br/>
        <b>AC {ascendant.upper()}</b>
        """
        story.append(Paragraph(placements, self.styles['CoverSubtitle']))
        story.append(Spacer(1, 20*mm))
        
        # Personal info
        spouse = self.data.get('spouse_name', '')
        children = self.data.get('children_count', 0)
        profession = self.data.get('profession', '')
        
        if spouse or children or profession:
            personal_info = []
            if spouse:
                personal_info.append(f"Casado/a con {spouse}")
            if children:
                personal_info.append(f"{children} hijos")
            if profession:
                personal_info.append(profession)
            story.append(Paragraph(" • ".join(personal_info), self.styles['CoverSubtitle']))
        
        story.append(Spacer(1, 30*mm))
        story.append(Paragraph("TODOASTROS • EDICIÓN COMPLETA", self.styles['Footer']))
        story.append(PageBreak())
    
    def _add_soul_map_section(self, story):
        """Add the 'El Mapa del Alma' narrative section"""
        story.append(Paragraph("El Mapa del Alma", self.styles['SectionTitle']))
        
        name = self.data.get('name', 'Nombre')
        birth_date = self.data.get('birth_date', '01/01/1990')
        location = self.data.get('location', 'Ubicación')
        sun_sign = self.data.get('sun_sign', 'Aries')
        
        # Generate personalized narrative
        narrative = self.data.get('soul_narrative', f"""
        Cuando el sol atravesaba el signo de {sun_sign}, en aquel luminoso día de tu nacimiento, 
        el universo conspiró para traer al mundo un alma única y especial. En las tierras de {location}, 
        nacía {name.split()[0]} — y su nombre mismo era ya una profecía de lo que vendría.
        """)
        
        story.append(Paragraph(narrative, self.styles['BodyText']))
        story.append(Spacer(1, 10*mm))
    
    def _add_sun_section(self, story):
        """Add detailed Sun sign analysis"""
        sun_sign = self.data.get('sun_sign', 'Aries')
        sun_description = self.data.get('sun_description', '')
        
        story.append(Paragraph(
            f"■ SOL EN {sun_sign.upper()} — {self._get_sun_archetype(sun_sign)}",
            self.styles['SubsectionTitle']
        ))
        
        if sun_description:
            story.append(Paragraph(sun_description, self.styles['BodyText']))
        else:
            story.append(Paragraph(
                self._get_default_sun_description(sun_sign),
                self.styles['BodyText']
            ))
    
    def _add_moon_section(self, story):
        """Add detailed Moon sign analysis"""
        moon_sign = self.data.get('moon_sign', 'Tauro')
        moon_description = self.data.get('moon_description', '')
        
        story.append(Paragraph(
            f"■ LUNA EN {moon_sign.upper()} — {self._get_moon_archetype(moon_sign)}",
            self.styles['SubsectionTitle']
        ))
        
        if moon_description:
            story.append(Paragraph(moon_description, self.styles['BodyText']))
        else:
            story.append(Paragraph(
                self._get_default_moon_description(moon_sign),
                self.styles['BodyText']
            ))
    
    def _add_numerology_section(self, story):
        """Add comprehensive numerology analysis"""
        story.append(PageBreak())
        story.append(Paragraph("Numerología Completa", self.styles['SectionTitle']))
        
        name = self.data.get('name', '')
        birth_date = self.data.get('birth_date', '01/01/1990')
        
        # Name breakdown
        if name:
            story.append(Paragraph("DESGLOSE DEL NOMBRE", self.styles['SubsectionTitle']))
            
            name_parts = name.split()
            total_sum = 0
            
            for part in name_parts:
                num_data = calculate_name_numerology(part)
                total_sum += num_data['total']
                story.append(Paragraph(
                    f"<b>{part.upper()}:</b> {num_data['breakdown']} = {num_data['total']} → {num_data['reduced']}",
                    self.styles['BodyText']
                ))
            
            final_reduced = reduce_number(total_sum)
            story.append(Paragraph(
                f"<b>TOTAL:</b> {total_sum} → {final_reduced}",
                self.styles['BodyText']
            ))
        
        story.append(Spacer(1, 10*mm))
        
        # Life path
        life_path = calculate_life_path(birth_date)
        
        # Numerology table
        num_data = [
            ['NÚMERO', 'VALOR', 'SIGNIFICADO'],
            ['CAMINO DE VIDA', str(life_path), self._get_number_meaning(life_path)],
            ['NÚMERO DESTINO', str(reduce_number(total_sum) if name else '—'), 
             self._get_destiny_meaning(reduce_number(total_sum)) if name else '—'],
        ]
        
        if name:
            full_num = calculate_name_numerology(name)
            num_data.append(['NÚMERO DEL ALMA', str(full_num['vowels']), 
                           self._get_soul_meaning(full_num['vowels'])])
            num_data.append(['PERSONALIDAD', str(full_num['consonants']), 
                           self._get_personality_meaning(full_num['consonants'])])
        
        table = Table(num_data, colWidths=[100, 60, 280])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['text']),
            ('ROWHEIGHT', (0, 0), (-1, -1), 25),
        ]))
        story.append(table)
    
    def _add_planetary_table(self, story):
        """Add planetary positions table"""
        story.append(PageBreak())
        story.append(Paragraph("Configuración Planetaria", self.styles['SectionTitle']))
        
        planets = self.data.get('planets', [
            {'name': 'Sol', 'sign': 'Libra', 'degree': '22°', 'house': 'Casa X', 'element': 'Aire', 'status': 'Directo'},
            {'name': 'Luna', 'sign': 'Piscis', 'degree': '24°', 'house': 'Casa III', 'element': 'Agua', 'status': 'Directo'},
            {'name': 'Mercurio', 'sign': 'Escorpio', 'degree': '15°', 'house': 'Casa XI', 'element': 'Agua', 'status': 'Directo'},
            {'name': 'Venus', 'sign': 'Escorpio', 'degree': '20°', 'house': 'Casa XI', 'element': 'Agua', 'status': 'Directo'},
            {'name': 'Marte', 'sign': 'Acuario', 'degree': '3°', 'house': 'Casa II', 'element': 'Aire', 'status': 'Directo'},
            {'name': 'Júpiter', 'sign': 'Piscis', 'degree': '14°', 'house': 'Casa III', 'element': 'Agua', 'status': 'Directo'},
            {'name': 'Saturno', 'sign': 'Sagitario', 'degree': '6°', 'house': 'Casa XII', 'element': 'Fuego', 'status': 'Directo'},
            {'name': 'Urano', 'sign': 'Sagitario', 'degree': '19°', 'house': 'Casa XII', 'element': 'Fuego', 'status': 'Directo'},
            {'name': 'Neptuno', 'sign': 'Capricornio', 'degree': '3°', 'house': 'Casa I', 'element': 'Tierra', 'status': 'Directo'},
            {'name': 'Plutón', 'sign': 'Escorpio', 'degree': '6°', 'house': 'Casa X', 'element': 'Agua', 'status': 'Directo'},
        ])
        
        # Build table data
        table_data = [['ASTRO', 'POSICIÓN', 'CASA', 'ELEM.', 'ESTADO']]
        
        for planet in planets:
            position = f"{planet['sign']} {planet['degree']}"
            table_data.append([
                f"■ {planet['name']}",
                position,
                planet['house'],
                planet['element'],
                planet['status']
            ])
        
        table = Table(table_data, colWidths=[80, 100, 80, 60, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['text']),
            ('ROWHEIGHT', (0, 0), (-1, -1), 22),
            ('BACKGROUND', (0, 1), (-1, -1), COLORS['light']),
        ]))
        story.append(table)
        
        # Add elemental distribution
        story.append(Spacer(1, 15*mm))
        story.append(Paragraph("Distribución Elemental", self.styles['SubsectionTitle']))
        
        elements = self.data.get('element_distribution', {
            'Agua': 50, 'Aire': 20, 'Fuego': 20, 'Tierra': 10
        })
        
        elem_data = [['■ AGUA', '■ AIRE', '■ FUEGO', '■ TIERRA']]
        elem_data.append([f"{elements.get('Agua', 0)}%", f"{elements.get('Aire', 0)}%", 
                         f"{elements.get('Fuego', 0)}%", f"{elements.get('Tierra', 0)}%"])
        
        elem_table = Table(elem_data, colWidths=[95, 95, 95, 95])
        elem_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (0, 0), COLORS['water']),
            ('TEXTCOLOR', (1, 0), (1, 0), COLORS['air']),
            ('TEXTCOLOR', (2, 0), (2, 0), COLORS['fire']),
            ('TEXTCOLOR', (3, 0), (3, 0), COLORS['earth']),
        ]))
        story.append(elem_table)
        
        # Footer quote
        story.append(Spacer(1, 20*mm))
        story.append(Paragraph(
            '"Los astros no obligan, pero sí inclinan. Tu voluntad es el timón."',
            self.styles['Quote']
        ))
        story.append(Paragraph("TODOASTROS • EDICIÓN COMPLETA", self.styles['Footer']))
    
    def _get_sun_archetype(self, sign):
        """Get the archetype title for each sun sign"""
        archetypes = {
            'Aries': 'El Guerrero Cósmico',
            'Tauro': 'El Constructor de Mundos',
            'Géminis': 'El Mensajero Divino',
            'Cáncer': 'El Guardián del Hogar',
            'Leo': 'El Rey del Zodíaco',
            'Virgo': 'El Sanador Perfeccionista',
            'Libra': 'La Diplomática Celestial',
            'Escorpio': 'El Transformador Profundo',
            'Sagitario': 'El Buscador de Verdad',
            'Capricornio': 'El Arquitecto del Destino',
            'Acuario': 'El Revolucionario Visionario',
            'Piscis': 'El Místico Soñador'
        }
        return archetypes.get(sign, 'El Ser Único')
    
    def _get_moon_archetype(self, sign):
        """Get the archetype title for each moon sign"""
        archetypes = {
            'Aries': 'El Impulso Emocional',
            'Tauro': 'La Seguridad Terrenal',
            'Géminis': 'La Mente Inquieta',
            'Cáncer': 'El Refugio del Alma',
            'Leo': 'El Corazón Radiante',
            'Virgo': 'El Orden Interior',
            'Libra': 'La Armonía Emocional',
            'Escorpio': 'El Abismo Transformador',
            'Sagitario': 'El Espíritu Libre',
            'Capricornio': 'La Fortaleza Emocional',
            'Acuario': 'La Libertad Interior',
            'Piscis': 'El Océano Emocional'
        }
        return archetypes.get(sign, 'El Mundo Interior')
    
    def _get_default_sun_description(self, sign):
        """Get default sun sign description"""
        descriptions = {
            'Libra': """Tu esencia solar vibra en el signo de la balanza. No viniste a este mundo a tomar partido, 
            sino a encontrar el punto donde los opuestos se reconcilian. Posees un sentido innato de la justicia 
            que te convierte en mediadora natural en cualquier conflicto. La belleza no es para ti un lujo, 
            sino una necesidad del alma.""",
            # Add more signs as needed
        }
        return descriptions.get(sign, f"Tu Sol en {sign} te otorga características únicas y especiales.")
    
    def _get_default_moon_description(self, sign):
        """Get default moon sign description"""
        descriptions = {
            'Piscis': """Tu Luna es el místico invisible. Piscis como sede de tu mundo emocional te convierte 
            en una esponja psíquica de extraordinaria sensibilidad. Sientes lo que otros no pueden ver. 
            Percibes el dolor ajeno antes de que sea expresado, anticipas las necesidades emocionales de 
            quienes te rodean.""",
            # Add more signs as needed
        }
        return descriptions.get(sign, f"Tu Luna en {sign} define tu mundo emocional interior.")
    
    def _get_number_meaning(self, num):
        """Get life path number meaning"""
        meanings = {
            1: 'El Líder. Viniste a iniciar y crear.',
            2: 'El Cooperador. Tu don es la diplomacia.',
            3: 'El Comunicador. La expresión es tu camino.',
            4: 'El Constructor. Viniste a edificar bases sólidas.',
            5: 'El Aventurero. La libertad es tu esencia.',
            6: 'El Protector. El hogar es tu santuario.',
            7: 'El Buscador. Tu mente busca verdades ocultas.',
            8: 'El Manifestador. El éxito material es tu dominio.',
            9: 'El Humanitario. Viniste a servir al mundo.',
            11: 'El Iluminador. Número maestro de intuición.',
            22: 'El Arquitecto. Número maestro de manifestación.',
            33: 'El Sanador. Número maestro del amor universal.',
        }
        return meanings.get(num, 'Número único con propósito especial.')
    
    def _get_destiny_meaning(self, num):
        """Get destiny number meaning"""
        return self._get_number_meaning(num)
    
    def _get_soul_meaning(self, num):
        """Get soul urge number meaning"""
        meanings = {
            1: 'En tu interior arde el pionero.',
            2: 'Buscas paz y armonía interior.',
            3: 'Tu alma anhela expresión creativa.',
            4: 'Deseas seguridad y estabilidad.',
            5: 'Tu espíritu busca aventura.',
            6: 'Anhelas amor y familia.',
            7: 'Buscas conocimiento profundo.',
            8: 'Deseas logro y reconocimiento.',
            9: 'Tu alma sirve a la humanidad.',
        }
        return meanings.get(num, 'Propósito interior único.')
    
    def _get_personality_meaning(self, num):
        """Get personality number meaning"""
        meanings = {
            1: 'El mundo ve un líder en ti.',
            2: 'Proyectas diplomacia y gentileza.',
            3: 'Tu imagen es creativa y expresiva.',
            4: 'El mundo ve confiabilidad en ti.',
            5: 'Proyectas dinamismo y versatilidad.',
            6: 'La protectora. El mundo ve refugio en ti.',
            7: 'Proyectas misterio y profundidad.',
            8: 'El mundo ve poder y autoridad.',
            9: 'Proyectas sabiduría y compasión.',
        }
        return meanings.get(num, 'Imagen única ante el mundo.')
    
    def generate(self):
        """Generate the complete PDF"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        story = []
        
        # Add all sections
        self._add_cover_page(story)
        self._add_soul_map_section(story)
        self._add_sun_section(story)
        self._add_moon_section(story)
        self._add_numerology_section(story)
        self._add_planetary_table(story)
        
        # Build PDF
        doc.build(story)
        
        self.buffer.seek(0)
        return self.buffer.getvalue()


# Flask routes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up", "service": "pdf_service_premium"}), 200


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """Generate a premium PDF from the provided data"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        report_type = data.get('report_type', 'premium')
        
        if report_type == 'premium':
            generator = PremiumPDFGenerator(data)
            pdf_bytes = generator.generate()
            
            return send_file(
                BytesIO(pdf_bytes),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"carta_astral_{data.get('name', 'cliente').replace(' ', '_')}.pdf"
            )
        else:
            # For free/basic reports, use simpler generation
            return jsonify({"error": "Basic report generation not implemented in premium service"}), 400
            
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500


@app.route('/generate_pdf/preview', methods=['POST'])
def preview_pdf():
    """Generate a preview (first page only) of the premium PDF"""
    try:
        data = request.json
        data['preview_only'] = True
        
        generator = PremiumPDFGenerator(data)
        pdf_bytes = generator.generate()
        
        return send_file(
            BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=False
        )
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return jsonify({"error": f"Failed to generate preview: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5008)
