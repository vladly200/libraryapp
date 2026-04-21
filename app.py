import os
import pymysql
from flask import Flask, render_template, request
from dotenv import load_dotenv

# 1. Загружаем переменные (для локальной разработки)
load_dotenv()

# 2. ИНИЦИАЛИЗАЦИЯ (Azure ищет именно эту строчку!)
app = Flask(__name__)

# 3. Функция подключения к базе
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
        ssl={'ssl': {}}  # Критично для Azure MySQL
    )

@app.route('/')
def home():
    return "Сайт работает! <a href='/booksrch'>Перейти к поиску</a>"

@app.route('/booksrch', methods=['GET'])
def search_books():
    query = request.args.get('search', '').strip()
    books = []
    error = None
    
    if query:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Ищем книгу по названию
                sql = "SELECT name, year_of_release, author FROM book WHERE name LIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)
            
    return render_template('booksrch.html', books=books, query=query, error=error)

if __name__ == "__main__":
    # Локальный запуск
    app.run(debug=True)