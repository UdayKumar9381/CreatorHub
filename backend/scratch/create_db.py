import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='[PASSWORD]'
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ideaflow")
    print("Database 'ideaflow' created or already exists.")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
