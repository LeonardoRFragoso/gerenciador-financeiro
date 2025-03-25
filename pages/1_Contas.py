import streamlit as st
import datetime
from utils import add_conta, update_conta, delete_conta, get_contas, rerun

st.set_page_config(page_title="Contas", layout="wide")

# Botão de retorno para a página inicial
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_conta_id" not in st.session_state:
    st.session_state.edit_conta_id = None

st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px #8A05BE;
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 0 25px #B5FF5A;
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

st.markdown("<h2 style='color:#F37529;'>🏦 Gerenciamento de Contas</h2>", unsafe_allow_html=True)

with st.container():
    with st.form("form_conta"):
        banco = st.text_input("Banco")
        saldo = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f")
        data = st.date_input("Data de Cadastro", datetime.date.today())
        submitted = st.form_submit_button("Adicionar Conta")
        if submitted:
            add_conta(banco, saldo, str(data))
            st.success("Conta registrada com sucesso!")
            rerun()

if st.session_state.edit_conta_id is not None:
    conta = next((c for c in get_contas() if c[0] == st.session_state.edit_conta_id), None)
    if conta:
        st.markdown("<h3 style='color:#8A05BE;'>✏️ Editar Conta</h3>", unsafe_allow_html=True)
        with st.form("edit_conta_form"):
            novo_banco = st.text_input("Banco", value=conta[1])
            novo_saldo = st.number_input("Saldo", min_value=0.0, value=conta[2], format="%.2f")
            nova_data = st.date_input("Data", value=datetime.datetime.strptime(conta[3], "%Y-%m-%d").date())
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_conta(conta[0], novo_banco, novo_saldo, str(nova_data))
                st.success("Conta atualizada com sucesso!")
                st.session_state.edit_conta_id = None
                rerun()

contas = get_contas()
if contas:
    st.markdown("<h3 style='color:#B5FF5A;'>📋 Contas Cadastradas</h3>", unsafe_allow_html=True)
    for conta in contas:
        with st.container():
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{conta[1]}</div>
                    <div class='metric-text'>Saldo: R$ {conta[2]:.2f} | Criada em: {conta[3]}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"edit_conta_{conta[0]}"):
                st.session_state.edit_conta_id = conta[0]
                rerun()
            if col2.button("🗑️ Excluir", key=f"delete_conta_{conta[0]}"):
                delete_conta(conta[0])
                st.success("Conta excluída com sucesso!")
                rerun()
