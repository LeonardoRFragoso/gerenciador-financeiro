import streamlit as st
import datetime
from utils import add_gasto, update_gasto, delete_gasto, get_gastos, rerun

st.set_page_config(page_title="Gastos", layout="wide")

# Botão de retorno
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_gasto_id" not in st.session_state:
    st.session_state.edit_gasto_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #F37529;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #FF8800;
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

st.markdown("<h2 style='color:#F37529;'>💸 Registro de Gastos</h2>", unsafe_allow_html=True)

with st.container():
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
    gasto = next((g for g in get_gastos() if g[0] == st.session_state.edit_gasto_id), None)
    if gasto:
        st.markdown("<h3 style='color:#F37529;'>✏️ Editar Gasto</h3>", unsafe_allow_html=True)
        with st.form("edit_gasto_form"):
            nova_descricao = st.text_input("Descrição", value=gasto[1])
            novo_valor = st.number_input("Valor do Gasto", min_value=0.0, value=gasto[2], format="%.2f")
            nova_data = st.date_input("Data", value=datetime.datetime.strptime(gasto[3], "%Y-%m-%d").date())
            nova_categoria = st.text_input("Categoria", value=gasto[4])
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_gasto(gasto[0], nova_descricao, novo_valor, str(nova_data), nova_categoria)
                st.success("Gasto atualizado com sucesso!")
                st.session_state.edit_gasto_id = None
                rerun()

gastos = get_gastos()
if gastos:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Gastos Registrados</h3>", unsafe_allow_html=True)
    for gasto in gastos:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{gasto[1]}</div>
                    <div class='metric-text'>Valor: R$ {gasto[2]:.2f} | Data: {gasto[3]} | Categoria: {gasto[4]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_gasto_{gasto[0]}"):
                st.session_state.edit_gasto_id = gasto[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_gasto_{gasto[0]}"):
                delete_gasto(gasto[0])
                st.success("Gasto excluído com sucesso!")
                rerun()
