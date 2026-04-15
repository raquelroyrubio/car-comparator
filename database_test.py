import os
import psycopg2
from dotenv import load_dotenv

# Cargamos la configuración del archivo .env
load_dotenv()

def conectar_y_probar():
    try:
        # Conexión a Neon
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        print("✅ Conexión exitosa a Neon")

        # 1. Crear la tabla (por si no la creaste en el SQL Editor)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS coches (
                id SERIAL PRIMARY KEY,
                marca TEXT,
                modelo TEXT,
                precio INT,
                url TEXT UNIQUE
            );
        ''')
        
        # 2. Insertar un coche de prueba
        print("Guardando coche de prueba...")
        cur.execute('''
            INSERT INTO coches (marca, modelo, precio, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        ''', ('Audi', 'A3', 15000, 'https://ejemplo.com/audi-a3'))

        conn.commit()
        print("✅ ¡Coche guardado correctamente!")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    conectar_y_probar()