import psycopg2

# Conectar a la base de datos postgres por defecto para comprobar si la base de datos 'usuarios' existe
default_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="bdproyecto",  # Tu contraseña de postgres
    host="database-2.c7w6ds5r8lrc.us-east-1.rds.amazonaws.com"
)
default_conn.autocommit = True  # Necesario para crear una base de datos fuera de una transacción
default_cursor = default_conn.cursor()

# Comprobar si la base de datos 'usuarios' existe
default_cursor.execute("SELECT 1 FROM pg_database WHERE datname='usuarios'")
db_exists = default_cursor.fetchone()

# Crear la base de datos 'usuarios' si no existe
if not db_exists:
    default_cursor.execute("CREATE DATABASE usuarios")

# Cerrar la conexión inicial
default_cursor.close()
default_conn.close()

# Conectar a la base de datos 'usuarios'
conn = psycopg2.connect(
    dbname="usuarios",
    user="postgres",
    password="bdproyecto",  # Tu contraseña de postgres
    host="database-2.c7w6ds5r8lrc.us-east-1.rds.amazonaws.com"
)
cursor = conn.cursor()

cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
table_exists = cursor.fetchone()[0]

if not table_exists:
    sql_query = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            firstname varchar(100) NOT NULL,
            lastname varchar(100) NOT NULL,
            gender varchar(100) NOT NULL,
            age SMALLINT,
            phone varchar(100) NOT NULL,
            address varchar(100) NOT NULL
        )
    """
    cursor.execute(sql_query)

    conn.commit()

def commit():
    conn.commit()

