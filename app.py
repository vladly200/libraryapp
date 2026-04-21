import os
import pymysql
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    # Azure MySQL Flexible Server требует SSL. 
    # Эти настройки — самый надежный вариант.
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
        ssl={'ssl': {}} 
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
                sql = "SELECT name, year_of_release, author FROM book WHERE name LIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
            conn.close()
        except Exception as e:
            error = str(e) # Если база не подключится, мы увидим причину
            
    return render_template('booksrch.html', books=books, query=query, error=error)

if __name__ == "__main__":
    app.run()