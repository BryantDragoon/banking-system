import sqlite3
from kivy.utils import platform
import os


DB_NAME = "MyBankingDB.db"

# Instruccion especial para solo ejecutarse en android, creando db en un espacio con permiso para escribir
if platform == "android":
    from android.storage import app_storage_path # type: ignore
    DB_NAME = os.path.join(app_storage_path(), "MyBankingDB.db")


def create_table_users():
    """Crea en la base de datos la tabla users."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    last_name TEXT,
                    telephone TEXT,
                    date_of_birth TEXT,
                    country TEXT,
                    marital_status TEXT,
                    login_id TEXT UNIQUE,
                    password TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    connection.commit()
    connection.close()


def create_table_accounts():
    """Crea en la base de datos la tabla accounts."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    balance NUMERIC(12,2) DEFAULT 0.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    connection.commit()
    connection.close()


def create_table_transactions():
    """Crea en la base de datos la tabla transactions."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_account_id INTEGER,
                    to_account_id INTEGER,
                    type TEXT,
                    amount NUMERIC(12,2),
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    connection.commit()
    connection.close()


def insert_user(name, last_name, telephone, date_of_birth, country, marital_status, login_id, password):
    """Inserta un nuevo usuario en la base de datos. Regresa su id en tabla users"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO users (name, last_name, telephone, date_of_birth, country, marital_status, login_id, password)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", 
                   (name, last_name, telephone, date_of_birth, country, marital_status, login_id, password)
                )
    user_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return user_id


def insert_account(user_id):
    """Crea un nueva cuenta bancaria para un usuario en la base de datos."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO accounts (user_id)
                   VALUES (?);""", 
                   (user_id,)
                )
    connection.commit()
    connection.close()


def is_id_used(login_id):
    """Funcion para revisar si ya existe un usuario con el mismo login_id"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM users
                    WHERE login_id = ?;""", 
                    (login_id,)
                    )
    exist = cursor.fetchone()
    connection.close()
    
    return True if exist else False
        

def validate_credentials(login_id, password):
    """Funcion para verificar que ID y contraseña coinciden con un usuario valido.
    Regresa el registro del usuario si lo encuentra"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM users
                    WHERE login_id = ? AND password = ?;""", 
                    (login_id, password)
                    )
    exist = cursor.fetchone()
    connection.close()

    return exist if exist else False
    

def get_user_account(user_id):
    """Funcion para extraer datos de la cuenta de banco de un id de usuario"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM accounts
                    WHERE user_id = ?;""", 
                    (user_id,)
                    )
    account = cursor.fetchone()
    connection.close()
    return account


def update_balance(account_id, amount):
    """Funcion que actualiza el saldo de la cuenta tras movimiento"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?;""", 
                    (amount, account_id)
                )
    connection.commit()
    connection.close()


def insert_transaction(from_user_id, to_user_id, type, amount, description):
    """Inserta registro de trasaccion bancaria realizada."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO transactions (from_account_id, to_account_id, type, amount, description)
                   VALUES (?,?,?,?,?);""", (from_user_id, to_user_id, type, amount, description)
                )
    connection.commit()
    connection.close()


def get_transactions(account_id):
    """Regresa todos los registros de trasacciones de un user id. Regresa de mas reciente a mas antiguo"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT *
                   FROM transactions
                   WHERE from_account_id = ? OR to_account_id = ?
                   ORDER BY created_at DESC;""",
                   (account_id,account_id)
                    )
    transactions = cursor.fetchall()
    connection.close()
    return transactions


def get_users_accounts(user_id):
    """Regresa nombre y numero de cuenta de todos los demas usuarios no vinculados al user id dado"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT account_id, name, last_name
                   FROM users LEFT JOIN accounts
                   ON users.user_id = accounts.user_id
                   WHERE users.user_id != ?
                   ORDER BY last_name ASC;""",
                   (user_id,)
                    )
    users = cursor.fetchall()
    connection.close()
    return users


def get_table_users():
    """ Funcion para obtener todos los registros de usuarios capturados en tabla users."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM users;"""
                    )
    users = cursor.fetchall()
    connection.close()
    return users


def get_table_accounts():
    """ Funcion para obtener todos los registros de cuentas capturadas en tabla accounts."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM accounts;"""
                    )
    accounts = cursor.fetchall()
    connection.close()
    return accounts


def get_table_transactions():
    """Funcion para obtener todos los registros de transacciones en tabla transactions."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT *
                    FROM transactions;"""
                    )
    transactions = cursor.fetchall()
    connection.close()
    return transactions


def reset_db():
    """Funcion que borra registros en las tres tablas, y sus indices, para comenzar de cero"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM users;""") # Borra registros de tabla
    cursor.execute("""UPDATE sqlite_sequence SET seq=0 WHERE name=?;""", ("users",)) # Resetea el contador autoincremental 
    cursor.execute("""DELETE FROM accounts;""")
    cursor.execute("""UPDATE sqlite_sequence SET seq=0 WHERE name=?;""",("accounts",))
    cursor.execute("""DELETE FROM transactions;""")
    cursor.execute("""UPDATE sqlite_sequence SET seq=0 WHERE name=?;""", ("transactions",))
    connection.commit()
    connection.close()
