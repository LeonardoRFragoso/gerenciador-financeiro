import streamlit as st
import datetime
from utils import add_receita, update_receita, delete_receita, get_receitas, rerun

st.set_page_config(page_title="Receitas", layout="wide")

# Botão voltar para home
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_receita_id" not in st.session_state:
    st.session_state.edit_receita_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #43A047;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #66BB6A;
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

st.markdown("<h2 style='color:#F37529;'>💰 Registro de Receitas</h2>", unsafe_allow_html=True)

with st.container():
    with st.form("form_receita"):
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor da Receita", min_value=0.0, format="%.2f")
        data = st.date_input("Data", datetime.date.today())
        categoria = st.text_input("Categoria")
        submitted = st.form_submit_button("Adicionar Receita")
        if submitted:
            add_receita(descricao, valor, str(data), categoria)
            st.success("Receita registrada com sucesso!")
            rerun()

if st.session_state.edit_receita_id is not None:
    receita = next((r for r in get_receitas() if r[0] == st.session_state.edit_receita_id), None)
    if receita:
        st.markdown("<h3 style='color:#43A047;'>✏️ Editar Receita</h3>", unsafe_allow_html=True)
        with st.form("edit_receita_form"):
            nova_descricao = st.text_input("Descrição", value=receita[1])
            novo_valor = st.number_input("Valor da Receita", min_value=0.0, value=receita[2], format="%.2f")
            nova_data = st.date_input("Data", value=datetime.datetime.strptime(receita[3], "%Y-%m-%d").date())
            nova_categoria = st.text_input("Categoria", value=receita[4])
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_receita(receita[0], nova_descricao, novo_valor, str(nova_data), nova_categoria)
                st.success("Receita atualizada com sucesso!")
                st.session_state.edit_receita_id = None
                rerun()

receitas = get_receitas()
if receitas:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Receitas Registradas</h3>", unsafe_allow_html=True)
    for receita in receitas:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{receita[1]}</div>
                    <div class='metric-text'>Valor: R$ {receita[2]:.2f} | Data: {receita[3]} | Categoria: {receita[4]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_receita_{receita[0]}"):
                st.session_state.edit_receita_id = receita[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_receita_{receita[0]}"):
                delete_receita(receita[0])
                st.success("Receita excluída com sucesso!")
                rerun()