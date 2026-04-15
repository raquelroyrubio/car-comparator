@app.route('/')
def home():
    try:
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            return "❌ Error: No se encuentra la DATABASE_URL en Vercel."
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT marca, modelo, precio, url FROM coches ORDER BY precio ASC")
        coches = cur.fetchall()
        cur.close()
        conn.close()
        
        if not coches:
            return "⚠️ Conectado a Neon, pero la tabla de coches está vacía."
            
        return render_template_string(HTML_TEMPLATE, coches=coches)
    except Exception as e:
        return f"❌ Error de conexión o consulta: {str(e)}"