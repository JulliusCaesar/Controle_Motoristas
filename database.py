import sqlite3

def conectar():
    conn = sqlite3.connect('controle.db')
    
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS motoristas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade_viagens INTEGER DEFAULT 0,
        valor_apresentado REAL DEFAULT 0.0,
        valor_deferido REAL DEFAULT 0.0,
        adiantamento REAL DEFAULT 2500.0,
        resultado REAL DEFAULT 0.0,
        status TEXT DEFAULT 'aguardando',
        banco TEXT NOT NULL,
        agencia TEXT NOT NULL,
        op TEXT NOT NULL,
        conta TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS viagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motorista_id INTEGER,
        nome TEXT,
        data TEXT NOT NULL,
        valor_apresentado REAL NOT NULL,
        valor_deferido REAL NOT NULL,
        FOREIGN KEY (motorista_id) REFERENCES motoristas(id)
    )
    ''')
    
    conn.commit()
    return conn
