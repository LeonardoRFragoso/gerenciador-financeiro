import streamlit as st
import datetime
from utils import add_meta, update_meta, delete_meta, get_metas, rerun

st.set_page_config(page_title="Metas", layout="wide")

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_meta_id" not in st.session_state:
    st.session_state.edit_meta_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #A020F0;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #DA70D6;
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

st.markdown("<h2 style='color:#F37529;'>🎯 Controle de Metas Financeiras</h2>", unsafe_allow_html=True)

with st.container():
    with st.form("form_meta"):
        descricao = st.text_input("Descrição da Meta")
        valor = st.number_input("Valor da Meta", min_value=0.0, format="%.2f")
        data_limite = st.date_input("Data Limite", datetime.date.today())
        submitted = st.form_submit_button("Criar Meta")
        if submitted:
            add_meta(descricao, valor, str(data_limite))
            st.success("Meta criada com sucesso!")
            rerun()

if st.session_state.edit_meta_id is not None:
    meta = next((m for m in get_metas() if m[0] == st.session_state.edit_meta_id), None)
    if meta:
        st.markdown("<h3 style='color:#A020F0;'>✏️ Editar Meta</h3>", unsafe_allow_html=True)
        with st.form("edit_meta_form"):
            nova_descricao = st.text_input("Descrição", value=meta[1])
            novo_valor = st.number_input("Valor da Meta", min_value=0.0, value=meta[2], format="%.2f")
            nova_data = st.date_input("Data Limite", value=datetime.datetime.strptime(meta[3], "%Y-%m-%d").date())
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_meta(meta[0], nova_descricao, novo_valor, str(nova_data))
                st.success("Meta atualizada com sucesso!")
                st.session_state.edit_meta_id = None
                rerun()

metas = get_metas()
if metas:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Metas Cadastradas</h3>", unsafe_allow_html=True)
    for meta in metas:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{meta[1]}</div>
                    <div class='metric-text'>Valor: R$ {meta[2]:.2f} | Até: {meta[3]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_meta_{meta[0]}"):
                st.session_state.edit_meta_id = meta[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_meta_{meta[0]}"):
                delete_meta(meta[0])
                st.success("Meta excluída com sucesso!")
                rerun()