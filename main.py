import streamlit as st
import datetime

# Configurações da página
st.set_page_config(
    page_title="Gerenciador Financeiro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === ESTILO VISUAL CHAMATIVO E NAVEGAÇÃO POR CARDS ===
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #F5F5F5;
    font-family: 'Poppins', sans-serif;
}

/* Esconder menu e sidebar */
#MainMenu, header, footer {visibility: hidden;}
section[data-testid="stSidebar"] { display: none !important; }

.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
    margin-top: 40px;
    padding: 0 10px;
}

.card-container {
    background-color: #1e1e1e;
    border: 2px solid #8A05BE;
    border-radius: 15px;
    padding: 25px;
    width: 100%;
    max-width: 260px;
    text-align: center;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 0 12px #8A05BE;
    color: #F5F5F5;
}
.card-container:hover {
    box-shadow: 0 0 20px #B5FF5A;
    transform: translateY(-5px);
    cursor: pointer;
}
.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}
.card-desc {
    font-size: 14px;
    color: #B0B0B0;
}
@media (max-width: 768px) {
    .card-grid {
        flex-direction: column;
        align-items: center;
    }
}
</style>
""", unsafe_allow_html=True)

# === CONTEÚDO PRINCIPAL ===
st.markdown("""
    <h1 style='text-align:center;'>🚀 Bem-vindo ao Gerenciador Financeiro</h1>
    <p style='text-align:center; color:#B0B0B0;'>Organize suas finanças, acompanhe receitas, gastos, metas e conquiste o controle da sua vida financeira.</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class='card-grid'>
    <a href='?page=Dashboard' target='_self'><div class='card-container'>
        <div class='card-title'>📊 Dashboard</div>
        <div class='card-desc'>Visão geral das finanças com análise 50/30/20.</div>
    </div></a>
    <a href='?page=Contas' target='_self'><div class='card-container'>
        <div class='card-title'>🏦 Contas</div>
        <div class='card-desc'>Gerencie saldos em diferentes contas.</div>
    </div></a>
    <a href='?page=Receitas' target='_self'><div class='card-container'>
        <div class='card-title'>💰 Receitas</div>
        <div class='card-desc'>Cadastre e visualize todas as entradas financeiras.</div>
    </div></a>
    <a href='?page=Gastos' target='_self'><div class='card-container'>
        <div class='card-title'>💸 Gastos</div>
        <div class='card-desc'>Controle completo das despesas mensais.</div>
    </div></a>
    <a href='?page=Metas' target='_self'><div class='card-container'>
        <div class='card-title'>🎯 Metas</div>
        <div class='card-desc'>Defina objetivos financeiros e acompanhe seu progresso.</div>
    </div></a>
    <a href='?page=Dividas' target='_self'><div class='card-container'>
        <div class='card-title'>📉 Dívidas</div>
        <div class='card-desc'>Gerencie dívidas e parcelas com clareza.</div>
    </div></a>
    <a href='?page=Parcelas' target='_self'><div class='card-container'>
        <div class='card-title'>📆 Parcelas</div>
        <div class='card-desc'>Controle de pagamentos recorrentes.</div>
    </div></a>
    <a href='?page=Insights' target='_self'><div class='card-container'>
        <div class='card-title'>🤖 Insights</div>
        <div class='card-desc'>Receba sugestões automáticas com IA.</div>
    </div></a>
</div>
""", unsafe_allow_html=True)

# === REDIRECIONAMENTO PARA AS PÁGINAS ===
import urllib.parse
page = st.query_params.get("page")

if page == "Dashboard":
    st.switch_page("pages/0_Dashboard.py")
elif page == "Contas":
    st.switch_page("pages/1_Contas.py")
elif page == "Receitas":
    st.switch_page("pages/6_Receitas.py")
elif page == "Gastos":
    st.switch_page("pages/2_Gastos.py")
elif page == "Metas":
    st.switch_page("pages/3_Metas.py")
elif page == "Dividas":
    st.switch_page("pages/4_Dividas.py")
elif page == "Parcelas":
    st.switch_page("pages/5_Parcelas.py")
elif page == "Insights":
    st.switch_page("pages/7_Insights.py")

# Rodapé
st.markdown("""
<hr style='border: none; border-top: 1px solid #333;'>
<p style='text-align:center; font-size: 13px; color: #888;'>© 2025 - Seu Gerenciador Financeiro com Streamlit</p>
""", unsafe_allow_html=True)
