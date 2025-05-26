import sqlite3
import uuid
from datetime import datetime

# Quantidade de chaves para gerar
NUM_MONTHLY_KEYS = 10
NUM_YEARLY_KEYS = 5

# Nome do arquivo do banco de dados
DB_FILE = "redeem_keys.db"

# Cria a conexão com o banco
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        type TEXT CHECK(type IN ('monthly', 'yearly')) NOT NULL,
        is_redeemed INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
''')

# Função para gerar uma chave única
def generate_key():
    return str(uuid.uuid4()).replace('-', '').upper()[:16]

# Inserir chaves no banco
def insert_keys(amount, key_type):
    for _ in range(amount):
        key = generate_key()
        created_at = datetime.utcnow().isoformat()
        try:
            cursor.execute('''
                INSERT INTO keys (key, type, created_at)
                VALUES (?, ?, ?)
            ''', (key, key_type, created_at))
        except sqlite3.IntegrityError:
            print(f"Chave duplicada ignorada: {key}")

# Gerar e inserir chaves
insert_keys(NUM_MONTHLY_KEYS, 'monthly')
insert_keys(NUM_YEARLY_KEYS, 'yearly')

# Confirmar e fechar
conn.commit()
conn.close()

print("Chaves geradas e salvas em 'redeem_keys.db'.")
