from flask import Flask, render_template,request
from dotenv import load_dotenv
import pymysql
import os

app = Flask(__name__)
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'ssl': {'ca': os.getenv('DB_SSL_CA')} if os.getenv('DB_SSL_CA') else None
}

@app.route('/')
def home():
    return render_template('index.html')
    
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
    app.run(debug=True)