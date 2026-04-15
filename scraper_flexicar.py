import os
import requests
import psycopg2
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re  # Importamos expresiones regulares

load_dotenv()

def scrapear_ocasionplus():
    url = "https://www.ocasionplus.com/coches-segunda-mano"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # --- NUEVA ESTRATEGIA DE BÚSQUEDA ---
    # Buscamos divs que tengan una clase que CONTENGA "containerCard"
    coches = soup.find_all('div', class_=re.compile(r'containerCard'))
    
    if not coches:
        # Plan C: Buscar por el nombre del coche (que suele ser un H2) y subir al contenedor
        print("Probando plan alternativo por etiquetas H2...")
        coches = [h2.find_parent('div') for h2 in soup.find_all('h2') if h2.find_parent('div')]

    print(f"Procesando {len(coches)} anuncios encontrados...")

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    # Buscamos todas las tarjetas de vehículos usando la clase base que me pasaste
    coches = soup.find_all('div', class_=re.compile(r'cardVehicle_card'))

    print(f"Procesando {len(coches)} anuncios reales encontrados...")

    for i, coche in enumerate(coches):
        try:
            # 1. Nombre (Marca y Modelo)
            nombre_tag = coche.find('span', {'data-test': 'span-brand-model'})
            version_tag = coche.find('span', {'data-test': 'span-version'})
            
            if not nombre_tag: continue
            nombre_completo = f"{nombre_tag.text.strip()} {version_tag.text.strip() if version_tag else ''}"

            # 2. Precio (El primero que es el precio al contado)
            precio_tag = coche.find('span', {'data-test': 'span-price'})
            if not precio_tag: continue
            
            # Limpiamos puntos y símbolo de euro (ej: 16.450€ -> 16450)
            precio_limpio = int(''.join(filter(str.isdigit, precio_tag.text)))

            # 3. Enlace (Está en el <a> que envuelve todo)
            link_tag = coche.find('a', href=True)
            link = "https://www.ocasionplus.com" + link_tag['href']

            # 4. Inserción en Neon
            cur.execute('''
                INSERT INTO coches (marca, modelo, precio, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET precio = EXCLUDED.precio;
            ''', (nombre_tag.text.strip(), nombre_completo, precio_limpio, link))

            
            print(f"  ✅ {nombre_completo}: {precio_limpio}€")

        except Exception as e:
            print(f"  ❌ Error en coche {i}: {e}")
            continue

    conn.commit()
    cur.close()
    conn.close()
    print("¡Scraping y guardado completados!")

if __name__ == "__main__":
    scrapear_ocasionplus()