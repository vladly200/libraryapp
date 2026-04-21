from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymysql
import os

app = Flask(__name__)
load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,        # Чтобы не ждал вечно
        ssl={'ssl': {}}            # ВКЛЮЧАЕТ SSL ДЛЯ AZURE
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booksrch', methods=['GET'])
def search_books():
    query = request.args.get('search', '').strip()
    books = []
    if query:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT name, year_of_release, author, cover_image_url FROM book WHERE name LIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
            conn.close()
        except Exception as e:
            return f"Database Error: {e}", 500
    return render_template('booksrch.html', books=books, query=query)

if __name__ == "__main__":
    app.run()