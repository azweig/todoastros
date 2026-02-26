from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import ephem
import pytz
from geopy.geocoders import Nominatim
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import boto3
from typing import Optional

app = FastAPI()
s3 = boto3.client('s3')

class ChartRequest(BaseModel):
    name: str
    birth_date: str
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None
    plan: str

def calculate_planetary_positions(date: datetime, lat: float = 0, lon: float = 0):
    # Initialize dictionary for planetary positions
    positions = {}
    
    # Calculate positions for each planet
    planets = [
        ephem.Sun(), ephem.Moon(), ephem.Mercury(),
        ephem.Venus(), ephem.Mars(), ephem.Jupiter(),
        ephem.Saturn(), ephem.Uranus(), ephem.Neptune()
    ]
    
    # Create observer location
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = date
    
    # Calculate position for each planet
    for planet in planets:
        planet.compute(observer)
        positions[planet.name] = {
            'longitude': float(planet.hlong),
            'latitude': float(planet.hlat),
            'constellation': ephem.constellation(planet)[1]
        }
    
    return positions

def generate_pdf(name: str, positions: dict, plan: str):
    # Create PDF
    c = canvas.Canvas(f"/tmp/{name}_chart.pdf", pagesize=letter)
    
    # Add header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, 750, f"Astral Chart for {name}")
    
    # Add planetary positions
    y = 700
    c.setFont("Helvetica", 12)
    for planet, pos in positions.items():
        c.drawString(72, y, f"{planet}: {pos['constellation']}")
        if plan == 'premium':
            c.drawString(72, y-15, f"Long: {pos['longitude']:.2f}° Lat: {pos['latitude']:.2f}°")
            y -= 40
        else:
            y -= 25
    
    c.save()
    
    # Upload to S3
    bucket_name = 'astrofuturo-charts'
    key = f"charts/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    s3.upload_file(
        f"/tmp/{name}_chart.pdf",
        bucket_name,
        key,
        ExtraArgs={'ContentType': 'application/pdf'}
    )
    
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"

@app.post("/generate-chart")
async def generate_chart(request: ChartRequest):
    try:
        # Parse birth date
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        
        # If premium plan, get exact location and time
        lat, lon = 0, 0
        if request.plan == 'premium' and request.birth_place:
            geolocator = Nominatim(user_agent="astrofuturo")
            location = geolocator.geocode(request.birth_place)
            if location:
                lat, lon = location.latitude, location.longitude
            
            if request.birth_time:
                time_parts = request.birth_time.split(':')
                birth_date = birth_date.replace(
                    hour=int(time_parts[0]),
                    minute=int(time_parts[1])
                )
        
        # Calculate planetary positions
        positions = calculate_planetary_positions(birth_date, lat, lon)
        
        # Generate and upload PDF
        chart_url = generate_pdf(request.name, positions, request.plan)
        
        return {"status": "success", "chart_url": chart_url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

