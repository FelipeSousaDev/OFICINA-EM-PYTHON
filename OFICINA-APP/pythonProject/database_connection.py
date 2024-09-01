import pyodbc


import pyodbc

def get_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'  # Ou use o nome da instância, por exemplo, 'localhost\SQLEXPRESS'
            'DATABASE=PROJETO-OFICINA-SQL;'  # Nome do banco de dados
            'Trusted_Connection=yes;'  # Autenticação do Windows
        )
        return connection
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None









