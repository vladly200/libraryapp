from flask import Flask, render_template, request
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)
load_dotenv()

# Универсальная функция подключения к PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        sslmode='require'  # Azure PostgreSQL требует SSL
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pl')
def indexPL():
    return render_template('indexPL.html')

@app.route('/ua')
def indexUA():
    return render_template('indexUA.html')

@app.route('/myBooks')
def my_books():
    return render_template('MyBooks.html')

@app.route('/booksrch', methods=['GET'])
def search_books():
    query = request.args.get('search', '').strip()
    books = []

    if query:
        try:
            # Используем новую функцию подключения
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # В PostgreSQL LIKE чувствителен к регистру, ILIKE — нет (лучше для поиска)
                sql = "SELECT name, year_of_release, author, cover_image_url FROM book WHERE name ILIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error: {e}") # Это отобразится в логах Azure
            return f"Database Error: {e}", 500

    return render_template('booksrch.html', books=books, query=query)

if __name__ == "__main__":
    app.run()