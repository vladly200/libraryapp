@app.route('/booksrch', methods=['GET'])
def search_books():
    query = request.args.get('search', '').strip()
    books = []
    if query:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT name, year_of_release, author FROM book WHERE name LIKE %s"
                cursor.execute(sql, ('%' + query + '%',))
                books = cursor.fetchall()
            conn.close()
        except Exception as e:
            # Если база не пустит, ты увидишь причину прямо на сайте!
            return f"""
            <div style="color: red; border: 1px solid red; padding: 20px;">
                <h1>Ошибка подключения к базе:</h1>
                <p>{str(e)}</p>
                <p>Проверь DB_USER и DB_PASSWORD в настройках Azure!</p>
            </div>
            """
    return render_template('booksrch.html', books=books, query=query)