import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-H50EB6O\\SQLEXPRESS;'
        'DATABASE=UserInfoDB;'
        'Trusted_Connection=yes;'
    )
    print("Connection Successful!")
except pyodbc.InterfaceError as e:
    print(f"Interface Error: {e}")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")
