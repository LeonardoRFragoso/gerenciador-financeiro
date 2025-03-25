import sqlite3
import datetime
import streamlit as st

# Conexão com o banco SQLite
conn = sqlite3.connect('financas.db', check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            saldo REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data TEXT,
            categoria TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data_limite TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dividas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            taxa_juros REAL,
            prazo INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS parcelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data_vencimento TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data TEXT,
            categoria TEXT
        )
    ''')
    conn.commit()

init_db()

# Função para reiniciar a página
def rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.query_params(updated=str(datetime.datetime.now()))

# Funções CRUD para "Contas"
def add_conta(nome, saldo):
    c.execute("INSERT INTO contas (nome, saldo) VALUES (?, ?)", (nome, saldo))
    conn.commit()

def update_conta(record_id, nome, saldo):
    c.execute("UPDATE contas SET nome=?, saldo=? WHERE id=?", (nome, saldo, record_id))
    conn.commit()

def delete_conta(record_id):
    c.execute("DELETE FROM contas WHERE id=?", (record_id,))
    conn.commit()

def get_contas():
    c.execute("SELECT * FROM contas")
    return c.fetchall()

# Funções CRUD para "Gastos"
def add_gasto(descricao, valor, data, categoria):
    c.execute("INSERT INTO gastos (descricao, valor, data, categoria) VALUES (?, ?, ?, ?)", (descricao, valor, data, categoria))
    conn.commit()

def update_gasto(record_id, descricao, valor, data, categoria):
    c.execute("UPDATE gastos SET descricao=?, valor=?, data=?, categoria=? WHERE id=?", (descricao, valor, data, categoria, record_id))
    conn.commit()

def delete_gasto(record_id):
    c.execute("DELETE FROM gastos WHERE id=?", (record_id,))
    conn.commit()

def get_gastos():
    c.execute("SELECT * FROM gastos")
    return c.fetchall()

# Funções CRUD para "Metas"
def add_meta(descricao, valor, data_limite):
    c.execute("INSERT INTO metas (descricao, valor, data_limite) VALUES (?, ?, ?)", (descricao, valor, data_limite))
    conn.commit()

def update_meta(record_id, descricao, valor, data_limite):
    c.execute("UPDATE metas SET descricao=?, valor=?, data_limite=? WHERE id=?", (descricao, valor, data_limite, record_id))
    conn.commit()

def delete_meta(record_id):
    c.execute("DELETE FROM metas WHERE id=?", (record_id,))
    conn.commit()

def get_metas():
    c.execute("SELECT * FROM metas")
    return c.fetchall()

# Funções CRUD para "Dívidas"
def add_divida(descricao, valor, taxa_juros, prazo):
    c.execute("INSERT INTO dividas (descricao, valor, taxa_juros, prazo) VALUES (?, ?, ?, ?)", (descricao, valor, taxa_juros, prazo))
    conn.commit()

def update_divida(record_id, descricao, valor, taxa_juros, prazo):
    c.execute("UPDATE dividas SET descricao=?, valor=?, taxa_juros=?, prazo=? WHERE id=?", (descricao, valor, taxa_juros, prazo, record_id))
    conn.commit()

def delete_divida(record_id):
    c.execute("DELETE FROM dividas WHERE id=?", (record_id,))
    conn.commit()

def get_dividas():
    c.execute("SELECT * FROM dividas")
    return c.fetchall()

# Funções CRUD para "Parcelas"
def add_parcela(descricao, valor, data_vencimento):
    c.execute("INSERT INTO parcelas (descricao, valor, data_vencimento) VALUES (?, ?, ?)", (descricao, valor, data_vencimento))
    conn.commit()

def update_parcela(record_id, descricao, valor, data_vencimento):
    c.execute("UPDATE parcelas SET descricao=?, valor=?, data_vencimento=? WHERE id=?", (descricao, valor, data_vencimento, record_id))
    conn.commit()

def delete_parcela(record_id):
    c.execute("DELETE FROM parcelas WHERE id=?", (record_id,))
    conn.commit()

def get_parcelas():
    c.execute("SELECT * FROM parcelas")
    return c.fetchall()

# Funções CRUD para "Receitas"
def add_receita(descricao, valor, data, categoria):
    c.execute("INSERT INTO receitas (descricao, valor, data, categoria) VALUES (?, ?, ?, ?)", (descricao, valor, data, categoria))
    conn.commit()

def update_receita(record_id, descricao, valor, data, categoria):
    c.execute("UPDATE receitas SET descricao=?, valor=?, data=?, categoria=? WHERE id=?", (descricao, valor, data, categoria, record_id))
    conn.commit()

def delete_receita(record_id):
    c.execute("DELETE FROM receitas WHERE id=?", (record_id,))
    conn.commit()

def get_receitas():
    c.execute("SELECT * FROM receitas")
    return c.fetchall()
