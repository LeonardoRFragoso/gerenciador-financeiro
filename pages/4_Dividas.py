import streamlit as st
import datetime
from utils import add_divida, update_divida, delete_divida, get_dividas, rerun

st.set_page_config(page_title="Dívidas", layout="wide")

# Botão voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_divida_id" not in st.session_state:
    st.session_state.edit_divida_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #C62828;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #FF5252;
    transform: scale(1.02);
}
.metric-title {
    font-size: 18px;
    font-weight: bold;
    color: #F5F5F5;
    margin-bottom: 5px;
}
.metric-text {
    font-size: 14px;
    color: #B0B0B0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#F37529;'>📉 Controle de Dívidas</h2>", unsafe_allow_html=True)

with st.container():
    with st.form("form_divida"):
        descricao = st.text_input("Descrição da Dívida")
        valor = st.number_input("Valor da Dívida", min_value=0.0, format="%.2f")
        data = st.date_input("Data de Registro", datetime.date.today())
        categoria = st.text_input("Categoria")
        submitted = st.form_submit_button("Registrar Dívida")
        if submitted:
            add_divida(descricao, valor, str(data), categoria)
            st.success("Dívida registrada com sucesso!")
            rerun()

if st.session_state.edit_divida_id is not None:
    divida = next((d for d in get_dividas() if d[0] == st.session_state.edit_divida_id), None)
    if divida:
        st.markdown("<h3 style='color:#C62828;'>✏️ Editar Dívida</h3>", unsafe_allow_html=True)
        with st.form("edit_divida_form"):
            nova_descricao = st.text_input("Descrição", value=divida[1])
            novo_valor = st.number_input("Valor da Dívida", min_value=0.0, value=divida[2], format="%.2f")
            nova_data = st.date_input("Data", value=datetime.datetime.strptime(divida[3], "%Y-%m-%d").date())
            nova_categoria = st.text_input("Categoria", value=divida[4])
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_divida(divida[0], nova_descricao, novo_valor, str(nova_data), nova_categoria)
                st.success("Dívida atualizada com sucesso!")
                st.session_state.edit_divida_id = None
                rerun()

dividas = get_dividas()
if dividas:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Dívidas Registradas</h3>", unsafe_allow_html=True)
    for divida in dividas:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{divida[1]}</div>
                    <div class='metric-text'>Valor: R$ {divida[2]:.2f} | Data: {divida[3]} | Categoria: {divida[4]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_divida_{divida[0]}"):
                st.session_state.edit_divida_id = divida[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_divida_{divida[0]}"):
                delete_divida(divida[0])
                st.success("Dívida excluída com sucesso!")
                rerun()
