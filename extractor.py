import requests
from bs4 import BeautifulSoup

def buscar_coches(url):
    # Simulamos que somos un navegador para que no nos bloqueen
    headers = {'User-Agent': 'Mozilla/5.0'}
    respuesta = requests.get(url, headers=headers)
    
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Aquí buscaríamos las etiquetas HTML de los coches
        # Ejemplo: soup.find_all('div', class_='anuncio-coche')
        print("¡Web leída correctamente!")
    else:
        print(f"Error al acceder: {respuesta.status_code}")

# Prueba con una URL de ejemplo (usa una real de un concesionario local)
buscar_coches("https://www.ocasionplus.com")