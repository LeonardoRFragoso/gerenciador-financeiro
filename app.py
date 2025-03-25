import streamlit as st
import datetime
import sqlite3
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ========================
# Custom CSS para Dark Mode
# ========================
st.markdown(
    """
    <style>
    /* Configura o fundo e cores do texto para um dark mode elegante */
    .reportview-container {
        background-color: #121212;
        color: #E1E1E1;
    }
    .sidebar .sidebar-content {
        background-color: #1A1A1A;
        color: #E1E1E1;
    }
    .stButton button {
        background-color: #6A0DAD;
        color: #ffffff;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input {
        background-color: #333333;
        color: #E1E1E1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========================
# Conexão e inicialização do SQLite
# ========================
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
    conn.commit()

init_db()

# ========================
# Funções CRUD para cada tabela
# ========================
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

# ========================
# Variáveis de controle para edição
# ========================
if "edit_conta_id" not in st.session_state:
    st.session_state.edit_conta_id = None
if "edit_gasto_id" not in st.session_state:
    st.session_state.edit_gasto_id = None
if "edit_meta_id" not in st.session_state:
    st.session_state.edit_meta_id = None
if "edit_divida_id" not in st.session_state:
    st.session_state.edit_divida_id = None
if "edit_parcela_id" not in st.session_state:
    st.session_state.edit_parcela_id = None

# ========================
# Função para "forçar" recarregamento da página
# ========================
def rerun():
    """Tenta usar st.experimental_rerun() (disponível a partir da v1.12.0).
    Se não estiver disponível, usa st.experimental_set_query_params() como fallback."""
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.experimental_set_query_params(updated=str(datetime.datetime.now()))

# ========================
# Configura a chave da API do OpenAI (usando st.secrets)
# ========================
openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
if not openai_api_key:
    st.error("Defina sua chave da API do OpenAI em st.secrets ou via variável de ambiente.")

# ========================
# Função para obter insights financeiros via LangChain
# ========================
def obter_insights_financeiros():
    contas = get_contas()
    gastos = get_gastos()
    metas = get_metas()
    dividas = get_dividas()
    parcelas = get_parcelas()
    
    resumo = "Contas: " + str(contas) + "\n"
    resumo += "Gastos: " + str(gastos) + "\n"
    resumo += "Metas: " + str(metas) + "\n"
    resumo += "Dívidas: " + str(dividas) + "\n"
    resumo += "Parcelas: " + str(parcelas) + "\n"
    
    prompt_template = (
        "Baseado nos dados financeiros abaixo, quais estratégias e dicas você recomenda "
        "para organizar melhor as finanças, reduzir gastos desnecessários e alcançar uma reserva de emergência?\n\n"
        "{dados}"
    )
    prompt = PromptTemplate(input_variables=["dados"], template=prompt_template)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    resposta = chain.run({"dados": resumo})
    return resposta

# ========================
# Barra lateral de navegação
# ========================
pagina = st.sidebar.selectbox("Selecione a página", 
                              ["Contas", "Gastos", "Metas", "Dívidas", "Parcelas", "Insights"])

st.title("Gerenciador Financeiro com Streamlit e LangChain")

# ========================
# Página de Contas
# ========================
if pagina == "Contas":
    st.header("Cadastro de Contas")
    with st.form("form_conta"):
        nome_conta = st.text_input("Nome da Conta")
        saldo = st.number_input("Saldo Atual", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Adicionar Conta")
        if submitted:
            add_conta(nome_conta, saldo)
            st.success("Conta adicionada com sucesso!")
            rerun()
    
    if st.session_state.edit_conta_id is not None:
        record_id = st.session_state.edit_conta_id
        c.execute("SELECT nome, saldo FROM contas WHERE id=?", (record_id,))
        conta = c.fetchone()
        if conta:
            st.subheader("Editar Conta")
            with st.form("edit_conta_form"):
                novo_nome = st.text_input("Nome da Conta", value=conta[0])
                novo_saldo = st.number_input("Saldo Atual", min_value=0.0, value=conta[1], format="%.2f")
                edit_submitted = st.form_submit_button("Salvar Alterações")
                if edit_submitted:
                    update_conta(record_id, novo_nome, novo_saldo)
                    st.success("Conta atualizada com sucesso!")
                    st.session_state.edit_conta_id = None
                    rerun()
    
    contas = get_contas()
    if contas:
        st.subheader("Contas cadastradas:")
        for conta in contas:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**Nome:** {conta[1]} | **Saldo:** {conta[2]:.2f}")
            if col2.button("Editar", key=f"edit_conta_{conta[0]}"):
                st.session_state.edit_conta_id = conta[0]
                rerun()
            if col3.button("Excluir", key=f"delete_conta_{conta[0]}"):
                delete_conta(conta[0])
                st.success("Conta excluída com sucesso!")
                rerun()

# ========================
# Página de Gastos
# ========================
elif pagina == "Gastos":
    st.header("Registro de Gastos")
    with st.form("form_gasto"):
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor do Gasto", min_value=0.0, format="%.2f")
        data = st.date_input("Data", datetime.date.today())
        categoria = st.text_input("Categoria")
        submitted = st.form_submit_button("Adicionar Gasto")
        if submitted:
            add_gasto(descricao, valor, str(data), categoria)
            st.success("Gasto registrado com sucesso!")
            rerun()
    
    if st.session_state.edit_gasto_id is not None:
        record_id = st.session_state.edit_gasto_id
        c.execute("SELECT descricao, valor, data, categoria FROM gastos WHERE id=?", (record_id,))
        gasto = c.fetchone()
        if gasto:
            st.subheader("Editar Gasto")
            with st.form("edit_gasto_form"):
                nova_descricao = st.text_input("Descrição", value=gasto[0])
                novo_valor = st.number_input("Valor do Gasto", min_value=0.0, value=gasto[1], format="%.2f")
                nova_data = st.date_input("Data", value=datetime.datetime.strptime(gasto[2], "%Y-%m-%d").date())
                nova_categoria = st.text_input("Categoria", value=gasto[3])
                edit_submitted = st.form_submit_button("Salvar Alterações")
                if edit_submitted:
                    update_gasto(record_id, nova_descricao, novo_valor, str(nova_data), nova_categoria)
                    st.success("Gasto atualizado com sucesso!")
                    st.session_state.edit_gasto_id = None
                    rerun()
    
    gastos = get_gastos()
    if gastos:
        st.subheader("Gastos registrados:")
        for gasto in gastos:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**Descrição:** {gasto[1]} | **Valor:** {gasto[2]:.2f} | **Data:** {gasto[3]} | **Categoria:** {gasto[4]}")
            if col2.button("Editar", key=f"edit_gasto_{gasto[0]}"):
                st.session_state.edit_gasto_id = gasto[0]
                rerun()
            if col3.button("Excluir", key=f"delete_gasto_{gasto[0]}"):
                delete_gasto(gasto[0])
                st.success("Gasto excluído com sucesso!")
                rerun()

# ========================
# Página de Metas
# ========================
elif pagina == "Metas":
    st.header("Cadastro de Metas")
    with st.form("form_meta"):
        descricao = st.text_input("Descrição da Meta")
        valor_meta = st.number_input("Valor da Meta", min_value=0.0, format="%.2f")
        data_limite = st.date_input("Data Limite", datetime.date.today())
        submitted = st.form_submit_button("Adicionar Meta")
        if submitted:
            add_meta(descricao, valor_meta, str(data_limite))
            st.success("Meta cadastrada com sucesso!")
            rerun()
    
    if st.session_state.edit_meta_id is not None:
        record_id = st.session_state.edit_meta_id
        c.execute("SELECT descricao, valor, data_limite FROM metas WHERE id=?", (record_id,))
        meta = c.fetchone()
        if meta:
            st.subheader("Editar Meta")
            with st.form("edit_meta_form"):
                nova_descricao = st.text_input("Descrição da Meta", value=meta[0])
                novo_valor = st.number_input("Valor da Meta", min_value=0.0, value=meta[1], format="%.2f")
                nova_data_limite = st.date_input("Data Limite", value=datetime.datetime.strptime(meta[2], "%Y-%m-%d").date())
                edit_submitted = st.form_submit_button("Salvar Alterações")
                if edit_submitted:
                    update_meta(record_id, nova_descricao, novo_valor, str(nova_data_limite))
                    st.success("Meta atualizada com sucesso!")
                    st.session_state.edit_meta_id = None
                    rerun()
    
    metas = get_metas()
    if metas:
        st.subheader("Metas cadastradas:")
        for meta in metas:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**Descrição:** {meta[1]} | **Valor:** {meta[2]:.2f} | **Data Limite:** {meta[3]}")
            if col2.button("Editar", key=f"edit_meta_{meta[0]}"):
                st.session_state.edit_meta_id = meta[0]
                rerun()
            if col3.button("Excluir", key=f"delete_meta_{meta[0]}"):
                delete_meta(meta[0])
                st.success("Meta excluída com sucesso!")
                rerun()

# ========================
# Página de Dívidas
# ========================
elif pagina == "Dívidas":
    st.header("Cadastro de Dívidas")
    with st.form("form_divida"):
        descricao = st.text_input("Descrição da Dívida")
        valor = st.number_input("Valor da Dívida", min_value=0.0, format="%.2f")
        taxa_juros = st.number_input("Taxa de Juros (%)", min_value=0.0, format="%.2f")
        prazo = st.number_input("Prazo (meses)", min_value=1)
        submitted = st.form_submit_button("Adicionar Dívida")
        if submitted:
            add_divida(descricao, valor, taxa_juros, prazo)
            st.success("Dívida cadastrada com sucesso!")
            rerun()
    
    if st.session_state.edit_divida_id is not None:
        record_id = st.session_state.edit_divida_id
        c.execute("SELECT descricao, valor, taxa_juros, prazo FROM dividas WHERE id=?", (record_id,))
        divida = c.fetchone()
        if divida:
            st.subheader("Editar Dívida")
            with st.form("edit_divida_form"):
                nova_descricao = st.text_input("Descrição da Dívida", value=divida[0])
                novo_valor = st.number_input("Valor da Dívida", min_value=0.0, value=divida[1], format="%.2f")
                nova_taxa = st.number_input("Taxa de Juros (%)", min_value=0.0, value=divida[2], format="%.2f")
                novo_prazo = st.number_input("Prazo (meses)", min_value=1, value=divida[3])
                edit_submitted = st.form_submit_button("Salvar Alterações")
                if edit_submitted:
                    update_divida(record_id, nova_descricao, novo_valor, nova_taxa, novo_prazo)
                    st.success("Dívida atualizada com sucesso!")
                    st.session_state.edit_divida_id = None
                    rerun()
    
    dividas = get_dividas()
    if dividas:
        st.subheader("Dívidas registradas:")
        for divida in dividas:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**Descrição:** {divida[1]} | **Valor:** {divida[2]:.2f} | **Taxa de Juros:** {divida[3]:.2f}% | **Prazo:** {divida[4]} meses")
            if col2.button("Editar", key=f"edit_divida_{divida[0]}"):
                st.session_state.edit_divida_id = divida[0]
                rerun()
            if col3.button("Excluir", key=f"delete_divida_{divida[0]}"):
                delete_divida(divida[0])
                st.success("Dívida excluída com sucesso!")
                rerun()

# ========================
# Página de Parcelas
# ========================
elif pagina == "Parcelas":
    st.header("Registro de Parcelas")
    with st.form("form_parcela"):
        descricao = st.text_input("Descrição da Parcela")
        valor = st.number_input("Valor da Parcela", min_value=0.0, format="%.2f")
        data_vencimento = st.date_input("Data de Vencimento", datetime.date.today())
        submitted = st.form_submit_button("Adicionar Parcela")
        if submitted:
            add_parcela(descricao, valor, str(data_vencimento))
            st.success("Parcela registrada com sucesso!")
            rerun()
    
    if st.session_state.edit_parcela_id is not None:
        record_id = st.session_state.edit_parcela_id
        c.execute("SELECT descricao, valor, data_vencimento FROM parcelas WHERE id=?", (record_id,))
        parcela = c.fetchone()
        if parcela:
            st.subheader("Editar Parcela")
            with st.form("edit_parcela_form"):
                nova_descricao = st.text_input("Descrição da Parcela", value=parcela[0])
                novo_valor = st.number_input("Valor da Parcela", min_value=0.0, value=parcela[1], format="%.2f")
                nova_data = st.date_input("Data de Vencimento", value=datetime.datetime.strptime(parcela[2], "%Y-%m-%d").date())
                edit_submitted = st.form_submit_button("Salvar Alterações")
                if edit_submitted:
                    update_parcela(record_id, nova_descricao, novo_valor, str(nova_data))
                    st.success("Parcela atualizada com sucesso!")
                    st.session_state.edit_parcela_id = None
                    rerun()
    
    parcelas = get_parcelas()
    if parcelas:
        st.subheader("Parcelas registradas:")
        for parcela in parcelas:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**Descrição:** {parcela[1]} | **Valor:** {parcela[2]:.2f} | **Data de Vencimento:** {parcela[3]}")
            if col2.button("Editar", key=f"edit_parcela_{parcela[0]}"):
                st.session_state.edit_parcela_id = parcela[0]
                rerun()
            if col3.button("Excluir", key=f"delete_parcela_{parcela[0]}"):
                delete_parcela(parcela[0])
                st.success("Parcela excluída com sucesso!")
                rerun()

# ========================
# Página de Insights
# ========================
elif pagina == "Insights":
    st.header("Insights Financeiros com Assistente AI")
    st.write("Clique no botão abaixo para obter sugestões personalizadas com base nos seus dados financeiros.")
    if st.button("Obter Insights"):
        with st.spinner("Processando insights..."):
            resposta = obter_insights_financeiros()
            st.success("Insights obtidos!")
            st.write(resposta)
