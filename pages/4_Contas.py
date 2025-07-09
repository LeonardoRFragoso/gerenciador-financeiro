import streamlit as st
import datetime
from utils import add_conta, update_conta, delete_conta, get_contas, rerun, configurar_pagina
from style import apply_style, theme_toggle, format_currency, COLORS

configurar_pagina("Contas")

# Seleção de tema
theme = theme_toggle()
apply_style(theme)

# Botão de retorno para a página inicial
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_conta_id" not in st.session_state:
    st.session_state.edit_conta_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏦 Gerenciamento de Contas</h1>
    <p class="header-subtitle">Gerencie suas contas bancárias e acompanhe seus saldos em tempo real</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar nova conta
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Nova Conta</h3>', unsafe_allow_html=True)
with st.form("form_conta"):
    col1, col2 = st.columns(2)
    with col1:
        banco = st.text_input("Banco")
    with col2:
        saldo = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f")
    data = st.date_input("Data de Cadastro", datetime.date.today())
    submitted = st.form_submit_button("Adicionar Conta")
    if submitted:
        add_conta(banco, saldo, str(data))
        st.markdown("""
        <div class="alert success">
            ✅ Conta registrada com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de conta
if st.session_state.edit_conta_id is not None:
    conta = next((c for c in get_contas() if c[0] == st.session_state.edit_conta_id), None)
    if conta:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Conta</h3>', unsafe_allow_html=True)
        with st.form("edit_conta_form"):
            col1, col2 = st.columns(2)
            with col1:
                novo_banco = st.text_input("Banco", value=conta[1])
            with col2:
                novo_saldo = st.number_input("Saldo", min_value=0.0, value=conta[2], format="%.2f")
            nova_data = st.date_input("Data", value=datetime.datetime.strptime(conta[3], "%Y-%m-%d").date())
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_conta(conta[0], novo_banco, novo_saldo, str(nova_data))
                st.markdown("""
                <div class="alert success">
                    ✅ Conta atualizada com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_conta_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista de contas
contas = get_contas()
if contas:
    st.markdown('<h3 class="section-title">📋 Contas Cadastradas</h3>', unsafe_allow_html=True)
    
    # Cálculo do saldo total
    saldo_total = sum(conta[2] for conta in contas)
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Saldo Total</p>
            <h2 class="metric-value">{format_currency(saldo_total)}</h2>
            <span class="metric-subtitle">Em todas as contas</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Total de Contas</p>
            <h2 class="metric-value">{len(contas)}</h2>
            <span class="metric-subtitle">Contas ativas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de contas
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for conta in contas:
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['secondary']}; font-size: 1.2rem; margin-bottom: 10px;">{conta[1]}</h3>
                <p style="color: {COLORS['text']}; font-size: 1.5rem; margin-bottom: 5px;">{format_currency(conta[2])}</p>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">Criada em: {conta[3]}</p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="stButton" onclick="document.querySelector('#edit_conta_{conta[0]}').click()">✏️ Editar</button>
                    <button class="stButton" onclick="document.querySelector('#delete_conta_{conta[0]}').click()">🗑️ Excluir</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões ocultos para funcionalidade
        if st.button("✏️", key=f"edit_conta_{conta[0]}", help="Editar conta"):
            st.session_state.edit_conta_id = conta[0]
            rerun()
        if st.button("🗑️", key=f"delete_conta_{conta[0]}", help="Excluir conta"):
            delete_conta(conta[0])
            st.markdown("""
            <div class="alert success">
                ✅ Conta excluída com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhuma conta cadastrada. Comece adicionando sua primeira conta bancária.
    </div>
    """, unsafe_allow_html=True)
