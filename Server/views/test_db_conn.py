from peewee import *
from flask import Blueprint, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


test_db_bp = Blueprint('test_db', __name__)


@test_db_bp.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Try to execute a simple query to test the database connection
        db.connect()
        db.execute_sql('SELECT 1;')  # A simple test query


        return jsonify({'message': 'Database connection is successful'}), 200
    except Exception as e:
        return jsonify({'error': f'Database connection error: {str(e)}'}), 500
    finally:
        db.close()  # Always close the database connection




