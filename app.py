import os
import pymysql  # <--- ВОТ ЭТОЙ СТРОЧКИ У ТЕБЯ СЕЙЧАС НЕТ
from flask import Flask, render_template, request
from dotenv import load_dotenv
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5, # Не ждем дольше 5 секунд
        ssl={'ssl': {}}    # Обязательно для Azure Flexible Server
    )