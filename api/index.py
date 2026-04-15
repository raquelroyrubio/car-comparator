from flask import Flask, render_template_string
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

HTML_TEMPLATE = """
<html>
    <head>
        <title>Car Comparator Pro</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 p-8">
        <h1 class="text-3xl font-bold mb-6 text-center">🚗 Chollos Ocasion Plus</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {% for coche in coches %}
            <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-500">
                <h2 class="text-xl font-semibold">{{ coche[1] }}</h2>
                <p class="text-2xl font-bold text-blue-600 my-2">{{ "{:,}".format(coche[2]) }}€</p>
                <a href="{{ coche[3] }}" target="_blank" class="block text-center bg-blue-500 text-white py-2 rounded mt-4 hover:bg-blue-600">Ver Oferta</a>
            </div>
            {% endfor %}
        </div>
    </body>
</html>
"""

@app.route('/')
def index():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    cur.execute("SELECT marca, modelo, precio, url FROM coches ORDER BY precio ASC")
    coches = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, coches=coches)
