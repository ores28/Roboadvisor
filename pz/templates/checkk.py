import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-H50EB6O\SQLEXPRESS;'  # Change this to your server name
        'DATABASE=UserInfoDB;'
        'Trusted_Connection=yes;'
    )
    print("Connection Successful!")
    conn.close()
except Exception as e:
    print("Error:", e)
