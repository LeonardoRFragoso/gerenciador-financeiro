import sqlite3
import datetime
import streamlit as st
import pandas as pd
import os
import json
from pathlib import Path

# Conexão com o banco SQLite
conn = sqlite3.connect('financas.db', check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            saldo REAL,
            tipo TEXT DEFAULT 'Corrente',
            instituicao TEXT DEFAULT 'Outro'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data TEXT,
            categoria TEXT,
            recorrente INTEGER DEFAULT 0,
            dedutivel_ir INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data_limite TEXT,
            valor_atual REAL DEFAULT 0,
            categoria TEXT DEFAULT 'Outro'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS compromissos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor_total REAL,
            valor_parcela REAL,
            data_vencimento TEXT,
            status TEXT DEFAULT 'Pendente',
            tipo TEXT DEFAULT 'Dívida',
            taxa_juros REAL DEFAULT 0,
            total_parcelas INTEGER DEFAULT 1,
            parcela_atual INTEGER DEFAULT 1
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data TEXT,
            categoria TEXT,
            recorrente INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS investimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            valor_investido REAL,
            valor_atual REAL,
            data_inicio TEXT,
            rendimento_percentual REAL,
            instituicao TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            valor_planejado REAL,
            mes TEXT,
            ano INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            cor TEXT,
            icone TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            mensagem TEXT,
            data TEXT,
            lida INTEGER DEFAULT 0,
            tipo TEXT
        )
    ''')
    
    conn.commit()

    # Migrar dados das tabelas antigas para as novas
    try:
        # Verificar se existem tabelas antigas
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dividas'")
        if c.fetchone():
            # Migrar dívidas para compromissos
            c.execute("SELECT * FROM dividas")
            dividas = c.fetchall()
            for divida in dividas:
                c.execute("""
                    INSERT INTO compromissos 
                    (descricao, valor_total, valor_parcela, data_vencimento, tipo, taxa_juros) 
                    VALUES (?, ?, ?, ?, 'Dívida', ?)
                """, (divida[1], divida[2], divida[2]/divida[4] if divida[4] > 0 else divida[2], 
                      datetime.datetime.now().strftime("%Y-%m-%d"), divida[3]))
            
            # Migrar parcelas para compromissos
            c.execute("SELECT * FROM parcelas")
            parcelas = c.fetchall()
            for parcela in parcelas:
                c.execute("""
                    INSERT INTO compromissos 
                    (descricao, valor_total, valor_parcela, data_vencimento, status, tipo) 
                    VALUES (?, ?, ?, ?, ?, 'Parcela')
                """, (parcela[1], parcela[2], parcela[2], parcela[3], parcela[4] if len(parcela) > 4 else 'Pendente'))
            
            conn.commit()
    except Exception as e:
        st.error(f"Erro na migração de dados: {e}")
    
    # Inserir categorias padrão se não existirem
    c.execute("SELECT COUNT(*) FROM categorias")
    if c.fetchone()[0] == 0:
        categorias_padrao = [
            # Categorias de gastos
            ('Moradia', 'gasto', '#FF5733', 'house'),
            ('Alimentação', 'gasto', '#33FF57', 'utensils'),
            ('Transporte', 'gasto', '#3357FF', 'car'),
            ('Saúde', 'gasto', '#FF33A8', 'heart'),
            ('Educação', 'gasto', '#33A8FF', 'book'),
            ('Lazer', 'gasto', '#A833FF', 'smile'),
            ('Vestuário', 'gasto', '#FFA833', 'tshirt'),
            ('Serviços', 'gasto', '#33FFA8', 'tools'),
            # Categorias de receitas
            ('Salário', 'receita', '#33FF57', 'money-bill'),
            ('Freelance', 'receita', '#33A8FF', 'laptop'),
            ('Investimentos', 'receita', '#A833FF', 'chart-line'),
            ('Presente', 'receita', '#FF33A8', 'gift'),
            ('Outros', 'receita', '#FFA833', 'ellipsis-h'),
            # Categorias de investimentos
            ('Renda Fixa', 'investimento', '#33FF57', 'piggy-bank'),
            ('Ações', 'investimento', '#FF5733', 'chart-line'),
            ('Fundos', 'investimento', '#3357FF', 'chart-pie'),
            ('Criptomoedas', 'investimento', '#A833FF', 'coins')
        ]
        
        for cat in categorias_padrao:
            c.execute("INSERT INTO categorias (nome, tipo, cor, icone) VALUES (?, ?, ?, ?)", cat)
        
        conn.commit()

init_db()

# Função para reiniciar a página
def rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.query_params(updated=str(datetime.datetime.now()))

# Função para configuração padrão da página sem sidebar
def configurar_pagina(titulo):
    """
    Configura a página com as configurações padrão e remove a sidebar.
    
    Args:
        titulo (str): Título da página a ser exibido na aba do navegador
    """
    st.set_page_config(
        page_title=titulo,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS adicional para garantir que a sidebar seja completamente removida
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { 
        display: none !important; 
        width: 0px !important;
        height: 0px !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: -1 !important;
    }
    div[data-testid="collapsedControl"] { display: none !important; }
    .css-18e3th9 {padding-top: 0 !important;}
    .css-1d391kg {padding-top: 3.5rem !important;}
    </style>
    """, unsafe_allow_html=True)

# Funções CRUD para "Contas"
def add_conta(nome, saldo, tipo="Corrente", instituicao="Outro"):
    c.execute("INSERT INTO contas (nome, saldo, tipo, instituicao) VALUES (?, ?, ?, ?)", 
              (nome, saldo, tipo, instituicao))
    conn.commit()

def update_conta(record_id, nome, saldo, tipo="Corrente", instituicao="Outro"):
    c.execute("UPDATE contas SET nome=?, saldo=?, tipo=?, instituicao=? WHERE id=?", 
              (nome, saldo, tipo, instituicao, record_id))
    conn.commit()

def delete_conta(record_id):
    c.execute("DELETE FROM contas WHERE id=?", (record_id,))
    conn.commit()

def get_contas():
    c.execute("SELECT * FROM contas")
    return c.fetchall()

# Funções CRUD para "Gastos"
def add_gasto(descricao, valor, data, categoria, recorrente=0, dedutivel_ir=0):
    c.execute("""
        INSERT INTO gastos (descricao, valor, data, categoria, recorrente, dedutivel_ir) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (descricao, valor, data, categoria, recorrente, dedutivel_ir))
    conn.commit()

def update_gasto(record_id, descricao, valor, data, categoria, recorrente=0, dedutivel_ir=0):
    c.execute("""
        UPDATE gastos 
        SET descricao=?, valor=?, data=?, categoria=?, recorrente=?, dedutivel_ir=? 
        WHERE id=?
    """, (descricao, valor, data, categoria, recorrente, dedutivel_ir, record_id))
    conn.commit()

def delete_gasto(record_id):
    c.execute("DELETE FROM gastos WHERE id=?", (record_id,))
    conn.commit()

def get_gastos():
    c.execute("SELECT * FROM gastos")
    return c.fetchall()

# Funções CRUD para "Metas"
def add_meta(descricao, valor, data_limite, valor_atual=0, categoria="Outro"):
    c.execute("""
        INSERT INTO metas (descricao, valor, data_limite, valor_atual, categoria) 
        VALUES (?, ?, ?, ?, ?)
    """, (descricao, valor, data_limite, valor_atual, categoria))
    conn.commit()

def update_meta(record_id, descricao, valor, data_limite, valor_atual=0, categoria="Outro"):
    c.execute("""
        UPDATE metas 
        SET descricao=?, valor=?, data_limite=?, valor_atual=?, categoria=? 
        WHERE id=?
    """, (descricao, valor, data_limite, valor_atual, categoria, record_id))
    conn.commit()

def delete_meta(record_id):
    c.execute("DELETE FROM metas WHERE id=?", (record_id,))
    conn.commit()

def get_metas():
    c.execute("SELECT * FROM metas")
    return c.fetchall()

# Funções CRUD para "Compromissos" (unificando Dívidas e Parcelas)
def add_compromisso(descricao, valor_total, valor_parcela, data_vencimento, 
                   status="Pendente", tipo="Dívida", taxa_juros=0, 
                   total_parcelas=1, parcela_atual=1):
    c.execute("""
        INSERT INTO compromissos 
        (descricao, valor_total, valor_parcela, data_vencimento, status, tipo, 
         taxa_juros, total_parcelas, parcela_atual) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (descricao, valor_total, valor_parcela, data_vencimento, status, tipo, 
          taxa_juros, total_parcelas, parcela_atual))
    conn.commit()

def update_compromisso(record_id, descricao, valor_total, valor_parcela, data_vencimento, 
                      status="Pendente", tipo="Dívida", taxa_juros=0, 
                      total_parcelas=1, parcela_atual=1):
    c.execute("""
        UPDATE compromissos 
        SET descricao=?, valor_total=?, valor_parcela=?, data_vencimento=?, status=?, tipo=?, 
            taxa_juros=?, total_parcelas=?, parcela_atual=? 
        WHERE id=?
    """, (descricao, valor_total, valor_parcela, data_vencimento, status, tipo, 
          taxa_juros, total_parcelas, parcela_atual, record_id))
    conn.commit()

def delete_compromisso(record_id):
    c.execute("DELETE FROM compromissos WHERE id=?", (record_id,))
    conn.commit()

def get_compromissos():
    c.execute("SELECT * FROM compromissos")
    return c.fetchall()

# Funções para manter compatibilidade com código existente
def get_dividas():
    c.execute("SELECT * FROM compromissos WHERE tipo='Dívida'")
    result = c.fetchall()
    # Converter para o formato antigo: id, descricao, valor, taxa_juros, prazo
    return [(r[0], r[1], r[2], r[7], r[8]) for r in result]

def get_parcelas():
    c.execute("SELECT * FROM compromissos WHERE tipo='Parcela'")
    result = c.fetchall()
    # Converter para o formato antigo: id, descricao, valor, data_vencimento, status
    return [(r[0], r[1], r[3], r[4], r[5]) for r in result]

def add_divida(descricao, valor, data, categoria):
    # Adiciona uma dívida como um compromisso do tipo 'Dívida'
    add_compromisso(
        descricao=descricao,
        valor_total=valor,
        valor_parcela=valor,
        data_vencimento=data,
        status="Pendente",
        tipo="Dívida",
        taxa_juros=0,
        total_parcelas=1,
        parcela_atual=1
    )

def update_divida(record_id, descricao, valor, data, categoria):
    # Atualiza uma dívida existente
    c.execute("SELECT * FROM compromissos WHERE id=?", (record_id,))
    compromisso = c.fetchone()
    if compromisso:
        update_compromisso(
            record_id=record_id,
            descricao=descricao,
            valor_total=valor,
            valor_parcela=valor,
            data_vencimento=data,
            status=compromisso[5],  # Mantém o status atual
            tipo="Dívida",
            taxa_juros=compromisso[7],  # Mantém a taxa de juros atual
            total_parcelas=compromisso[8],  # Mantém o total de parcelas atual
            parcela_atual=compromisso[9]  # Mantém a parcela atual
        )

def delete_divida(record_id):
    # Exclui uma dívida
    delete_compromisso(record_id)

def add_parcela(descricao, valor, data_vencimento, status="Pendente"):
    # Adiciona uma parcela como um compromisso do tipo 'Parcela'
    add_compromisso(
        descricao=descricao,
        valor_total=valor,
        valor_parcela=valor,
        data_vencimento=data_vencimento,
        status=status,
        tipo="Parcela",
        taxa_juros=0,
        total_parcelas=1,
        parcela_atual=1
    )

def update_parcela(record_id, descricao, valor, data_vencimento, status):
    # Atualiza uma parcela existente
    update_compromisso(
        record_id=record_id,
        descricao=descricao,
        valor_total=valor,
        valor_parcela=valor,
        data_vencimento=data_vencimento,
        status=status,
        tipo="Parcela",
        taxa_juros=0,
        total_parcelas=1,
        parcela_atual=1
    )

def delete_parcela(record_id):
    # Exclui uma parcela
    delete_compromisso(record_id)

# Funções CRUD para "Receitas"
def add_receita(descricao, valor, data, categoria, recorrente=0):
    c.execute("""
        INSERT INTO receitas (descricao, valor, data, categoria, recorrente) 
        VALUES (?, ?, ?, ?, ?)
    """, (descricao, valor, data, categoria, recorrente))
    conn.commit()

def update_receita(record_id, descricao, valor, data, categoria, recorrente=0):
    c.execute("""
        UPDATE receitas 
        SET descricao=?, valor=?, data=?, categoria=?, recorrente=? 
        WHERE id=?
    """, (descricao, valor, data, categoria, recorrente, record_id))
    conn.commit()

def delete_receita(record_id):
    c.execute("DELETE FROM receitas WHERE id=?", (record_id,))
    conn.commit()

def get_receitas():
    c.execute("SELECT * FROM receitas")
    return c.fetchall()

# Funções CRUD para "Investimentos"
def add_investimento(nome, tipo, valor_investido, valor_atual, data_inicio, rendimento_percentual, instituicao):
    c.execute("""
        INSERT INTO investimentos 
        (nome, tipo, valor_investido, valor_atual, data_inicio, rendimento_percentual, instituicao) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nome, tipo, valor_investido, valor_atual, data_inicio, rendimento_percentual, instituicao))
    conn.commit()

def update_investimento(record_id, nome, tipo, valor_investido, valor_atual, data_inicio, rendimento_percentual, instituicao):
    c.execute("""
        UPDATE investimentos 
        SET nome=?, tipo=?, valor_investido=?, valor_atual=?, data_inicio=?, rendimento_percentual=?, instituicao=? 
        WHERE id=?
    """, (nome, tipo, valor_investido, valor_atual, data_inicio, rendimento_percentual, instituicao, record_id))
    conn.commit()

def delete_investimento(record_id):
    c.execute("DELETE FROM investimentos WHERE id=?", (record_id,))
    conn.commit()

def get_investimentos():
    c.execute("SELECT * FROM investimentos")
    return c.fetchall()

# Funções CRUD para "Orçamentos"
def add_orcamento(categoria, valor_planejado, mes, ano):
    c.execute("""
        INSERT INTO orcamentos (categoria, valor_planejado, mes, ano) 
        VALUES (?, ?, ?, ?)
    """, (categoria, valor_planejado, mes, ano))
    conn.commit()

def update_orcamento(record_id, categoria, valor_planejado, mes, ano):
    c.execute("""
        UPDATE orcamentos 
        SET categoria=?, valor_planejado=?, mes=?, ano=? 
        WHERE id=?
    """, (categoria, valor_planejado, mes, ano, record_id))
    conn.commit()

def delete_orcamento(record_id):
    c.execute("DELETE FROM orcamentos WHERE id=?", (record_id,))
    conn.commit()

def get_orcamentos(mes=None, ano=None):
    if mes and ano:
        c.execute("SELECT * FROM orcamentos WHERE mes=? AND ano=?", (mes, ano))
    else:
        c.execute("SELECT * FROM orcamentos")
    return c.fetchall()

# Funções CRUD para "Categorias"
def add_categoria(nome, tipo, cor="#33A8FF", icone="tag"):
    c.execute("""
        INSERT INTO categorias (nome, tipo, cor, icone) 
        VALUES (?, ?, ?, ?)
    """, (nome, tipo, cor, icone))
    conn.commit()

def update_categoria(record_id, nome, tipo, cor, icone):
    c.execute("""
        UPDATE categorias 
        SET nome=?, tipo=?, cor=?, icone=? 
        WHERE id=?
    """, (nome, tipo, cor, icone, record_id))
    conn.commit()

def delete_categoria(record_id):
    c.execute("DELETE FROM categorias WHERE id=?", (record_id,))
    conn.commit()

def get_categorias(tipo=None):
    if tipo:
        c.execute("SELECT * FROM categorias WHERE tipo=?", (tipo,))
    else:
        c.execute("SELECT * FROM categorias")
    return c.fetchall()

# Funções CRUD para "Notificações"
def add_notificacao(titulo, mensagem, data, tipo="info"):
    c.execute("""
        INSERT INTO notificacoes (titulo, mensagem, data, tipo) 
        VALUES (?, ?, ?, ?)
    """, (titulo, mensagem, data, tipo))
    conn.commit()

def update_notificacao(record_id, lida=1):
    c.execute("UPDATE notificacoes SET lida=? WHERE id=?", (lida, record_id))
    conn.commit()

def delete_notificacao(record_id):
    c.execute("DELETE FROM notificacoes WHERE id=?", (record_id,))
    conn.commit()

def get_notificacoes(apenas_nao_lidas=False):
    if apenas_nao_lidas:
        c.execute("SELECT * FROM notificacoes WHERE lida=0 ORDER BY data DESC")
    else:
        c.execute("SELECT * FROM notificacoes ORDER BY data DESC")
    return c.fetchall()

# Funções para análise e previsão financeira
def calcular_fluxo_caixa_mensal(mes, ano):
    # Formato do mês: YYYY-MM
    mes_str = f"{ano}-{mes:02d}"
    
    # Obter receitas do mês
    c.execute("SELECT SUM(valor) FROM receitas WHERE strftime('%Y-%m', data) = ?", (mes_str,))
    total_receitas = c.fetchone()[0] or 0
    
    # Obter gastos do mês
    c.execute("SELECT SUM(valor) FROM gastos WHERE strftime('%Y-%m', data) = ?", (mes_str,))
    total_gastos = c.fetchone()[0] or 0
    
    # Obter compromissos do mês
    c.execute("SELECT SUM(valor_parcela) FROM compromissos WHERE strftime('%Y-%m', data_vencimento) = ?", (mes_str,))
    total_compromissos = c.fetchone()[0] or 0
    
    return {
        'receitas': total_receitas,
        'gastos': total_gastos,
        'compromissos': total_compromissos,
        'saldo': total_receitas - total_gastos - total_compromissos
    }

def prever_fluxo_caixa(meses=3):
    hoje = datetime.datetime.now()
    previsao = []
    
    for i in range(meses):
        mes_futuro = hoje.month + i
        ano_futuro = hoje.year + (mes_futuro - 1) // 12
        mes_futuro = ((mes_futuro - 1) % 12) + 1
        
        # Obter receitas recorrentes
        c.execute("SELECT SUM(valor) FROM receitas WHERE recorrente=1")
        receitas_recorrentes = c.fetchone()[0] or 0
        
        # Obter média de receitas dos últimos 3 meses
        c.execute("""
            SELECT AVG(total) FROM (
                SELECT strftime('%Y-%m', data) as mes, SUM(valor) as total 
                FROM receitas 
                GROUP BY mes 
                ORDER BY mes DESC LIMIT 3
            )
        """)
        media_receitas = c.fetchone()[0] or 0
        
        # Obter gastos recorrentes
        c.execute("SELECT SUM(valor) FROM gastos WHERE recorrente=1")
        gastos_recorrentes = c.fetchone()[0] or 0
        
        # Obter média de gastos dos últimos 3 meses
        c.execute("""
            SELECT AVG(total) FROM (
                SELECT strftime('%Y-%m', data) as mes, SUM(valor) as total 
                FROM gastos 
                GROUP BY mes 
                ORDER BY mes DESC LIMIT 3
            )
        """)
        media_gastos = c.fetchone()[0] or 0
        
        # Obter compromissos futuros
        mes_str = f"{ano_futuro}-{mes_futuro:02d}"
        c.execute("SELECT SUM(valor_parcela) FROM compromissos WHERE strftime('%Y-%m', data_vencimento) = ?", (mes_str,))
        compromissos_futuros = c.fetchone()[0] or 0
        
        # Calcular previsão
        receitas_previstas = max(receitas_recorrentes, media_receitas * 0.9)  # Estimativa conservadora
        gastos_previstos = max(gastos_recorrentes, media_gastos * 1.1)  # Estimativa conservadora
        
        previsao.append({
            'mes': mes_str,
            'receitas': receitas_previstas,
            'gastos': gastos_previstos,
            'compromissos': compromissos_futuros,
            'saldo_previsto': receitas_previstas - gastos_previstos - compromissos_futuros
        })
    
    return previsao

# Funções para importação e exportação de dados
def exportar_dados(diretorio):
    """Exporta todos os dados para arquivos JSON"""
    os.makedirs(diretorio, exist_ok=True)
    
    # Tabelas para exportar
    tabelas = ['contas', 'gastos', 'metas', 'compromissos', 'receitas', 
               'investimentos', 'orcamentos', 'categorias', 'notificacoes']
    
    for tabela in tabelas:
        c.execute(f"SELECT * FROM {tabela}")
        colunas = [desc[0] for desc in c.description]
        dados = []
        
        for row in c.fetchall():
            dados.append(dict(zip(colunas, row)))
        
        with open(os.path.join(diretorio, f"{tabela}.json"), 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    
    return True

def importar_dados(diretorio):
    """Importa dados de arquivos JSON"""
    if not os.path.exists(diretorio):
        return False
    
    # Tabelas para importar
    tabelas = ['contas', 'gastos', 'metas', 'compromissos', 'receitas', 
               'investimentos', 'orcamentos', 'categorias', 'notificacoes']
    
    for tabela in tabelas:
        arquivo = os.path.join(diretorio, f"{tabela}.json")
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            if dados:
                # Limpar tabela existente
                c.execute(f"DELETE FROM {tabela}")
                
                # Obter colunas da tabela
                c.execute(f"PRAGMA table_info({tabela})")
                colunas = [info[1] for info in c.fetchall()]
                colunas.remove('id')  # Remover coluna ID que é autoincrement
                
                # Preparar query de inserção
                placeholders = ', '.join(['?'] * len(colunas))
                colunas_str = ', '.join(colunas)
                
                # Inserir dados
                for item in dados:
                    valores = [item.get(col) for col in colunas]
                    c.execute(f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})", valores)
                
                conn.commit()
    
    return True

# Função para categorização automática de transações
def categorizar_transacao(descricao):
    """Categoriza automaticamente uma transação com base em palavras-chave"""
    descricao = descricao.lower()
    
    # Mapeamento de palavras-chave para categorias
    categorias_gastos = {
        'moradia': ['aluguel', 'condomínio', 'iptu', 'água', 'luz', 'gás', 'internet', 'telefone'],
        'alimentação': ['mercado', 'supermercado', 'restaurante', 'lanche', 'delivery', 'ifood'],
        'transporte': ['uber', '99', 'taxi', 'combustível', 'gasolina', 'estacionamento', 'metrô', 'ônibus'],
        'saúde': ['farmácia', 'remédio', 'consulta', 'médico', 'dentista', 'exame', 'plano de saúde'],
        'educação': ['escola', 'faculdade', 'curso', 'livro', 'material escolar'],
        'lazer': ['cinema', 'teatro', 'show', 'viagem', 'hotel', 'passeio', 'netflix', 'spotify'],
        'vestuário': ['roupa', 'calçado', 'tênis', 'acessório']
    }
    
    categorias_receitas = {
        'salário': ['salário', 'pagamento', 'contracheque', 'folha'],
        'freelance': ['freela', 'projeto', 'consultoria'],
        'investimentos': ['dividendo', 'juros', 'rendimento', 'aluguel']
    }
    
    # Verificar categorias de gastos
    for categoria, palavras in categorias_gastos.items():
        if any(palavra in descricao for palavra in palavras):
            return categoria
    
    # Verificar categorias de receitas
    for categoria, palavras in categorias_receitas.items():
        if any(palavra in descricao for palavra in palavras):
            return categoria
    
    # Categoria padrão
    return 'outros'

# Função para análise de IR
def calcular_dedutiveis_ir(ano):
    """Calcula o total de despesas dedutíveis do IR para um determinado ano"""
    c.execute("""
        SELECT SUM(valor) FROM gastos 
        WHERE dedutivel_ir=1 AND strftime('%Y', data) = ?
    """, (str(ano),))
    
    total_dedutiveis = c.fetchone()[0] or 0
    return total_dedutiveis
