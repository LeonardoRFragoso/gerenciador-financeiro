import streamlit as st
import datetime
from utils import add_parcela, update_parcela, delete_parcela, get_parcelas, rerun

st.set_page_config(page_title="Parcelas", layout="wide")

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_parcela_id" not in st.session_state:
    st.session_state.edit_parcela_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #00BFA6;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #1DE9B6;
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

st.markdown("<h2 style='color:#F37529;'>📆 Gerenciamento de Parcelas</h2>", unsafe_allow_html=True)

with st.container():
    with st.form("form_parcela"):
        descricao = st.text_input("Descrição da Parcela")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        vencimento = st.date_input("Data de Vencimento", datetime.date.today())
        submitted = st.form_submit_button("Adicionar Parcela")
        if submitted:
            add_parcela(descricao, valor, str(vencimento))
            st.success("Parcela registrada com sucesso!")
            rerun()

if st.session_state.edit_parcela_id is not None:
    parcela = next((p for p in get_parcelas() if p[0] == st.session_state.edit_parcela_id), None)
    if parcela:
        st.markdown("<h3 style='color:#00BFA6;'>✏️ Editar Parcela</h3>", unsafe_allow_html=True)
        with st.form("edit_parcela_form"):
            nova_descricao = st.text_input("Descrição", value=parcela[1])
            novo_valor = st.number_input("Valor", min_value=0.0, value=parcela[2], format="%.2f")
            nova_data = st.date_input("Data de Vencimento", value=datetime.datetime.strptime(parcela[3], "%Y-%m-%d").date())
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_parcela(parcela[0], nova_descricao, novo_valor, str(nova_data))
                st.success("Parcela atualizada com sucesso!")
                st.session_state.edit_parcela_id = None
                rerun()

parcelas = get_parcelas()
if parcelas:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Parcelas Cadastradas</h3>", unsafe_allow_html=True)
    for parcela in parcelas:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{parcela[1]}</div>
                    <div class='metric-text'>Valor: R$ {parcela[2]:.2f} | Vencimento: {parcela[3]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_parcela_{parcela[0]}"):
                st.session_state.edit_parcela_id = parcela[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_parcela_{parcela[0]}"):
                delete_parcela(parcela[0])
                st.success("Parcela excluída com sucesso!")
                rerun()