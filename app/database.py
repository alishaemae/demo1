# app/database.py
import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',        
    'db': 'masterpol_partners',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    'autocommit': True
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)
