from flask import Flask, render_template,request
from dotenv import load_dotenv
import pymysql
import tempfile
import os

app = Flask(__name__)
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'youruser'),
    'password': os.getenv('DB_PASSWORD', 'yourpassword'),
    'database': os.getenv('DB_NAME', 'yourdatabase'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'ssl': {'ca': os.getenv('SSL_CA')} if os.getenv('SSL_CA') else None
}

@app.route('/')
def home():
    return render_template('index.html')
    

@app.route('/pl')
def indexPL():
    return render_template('indexPL.html')

@app.route('/ua')
def indexUA():
    return render_template('indexUA.html')

@app.route('/booksrch',methods=['GET'])
def search_books():
    query = request.args.get('search', '').strip()
    books = []

    if query:
        conn = pymysql.connect(**{k: v for k, v in DB_CONFIG.items() if v is not None})
        try:
            with conn.cursor() as cursor:
                sql = "SELECT name, year_of_release, author, cover_image_url FROM book WHERE name LIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
        finally:
            conn.close()

    return render_template('booksrch.html', books=books, query=query)

if __name__ == "__main__":
    app.run()

