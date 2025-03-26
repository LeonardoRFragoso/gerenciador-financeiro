import streamlit as st
import pandas as pd
from utils import configurar_pagina

# Configuração da página
configurar_pagina("Gerenciador Financeiro")

# Estilos CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset e Estilos Base */
body {
    background-color: #0A0A0F;
    color: #F5F5F5;
    font-family: 'Inter', sans-serif;
}

#MainMenu, header, footer {visibility: hidden;}
.css-18e3th9 {padding-top: 0 !important;}
.css-1d391kg {padding-top: 3.5rem !important;}
section[data-testid="stSidebar"] { 
    display: none !important; 
    width: 0px !important;
}
div[data-testid="collapsedControl"] { display: none !important; }

/* Glassmorphism Effect */
.glass-container {
    background: rgba(138, 5, 190, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
    padding: 20px;
}

.card-container {
    background: linear-gradient(135deg, rgba(138, 5, 190, 0.1) 0%, rgba(181, 255, 90, 0.05) 100%);
    border: 1px solid rgba(138, 5, 190, 0.3);
    border-radius: 15px;
    padding: 25px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.card-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8A05BE, #B5FF5A);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.card-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(138, 5, 190, 0.2);
    border-color: rgba(138, 5, 190, 0.5);
}

.card-container:hover::before {
    transform: scaleX(1);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #B5FF5A;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-desc {
    font-size: 0.9rem;
    color: rgba(245, 245, 245, 0.7);
    line-height: 1.5;
}

/* Animação de brilho */
@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(138, 5, 190, 0.2); }
    50% { box-shadow: 0 0 20px rgba(138, 5, 190, 0.4); }
    100% { box-shadow: 0 0 5px rgba(138, 5, 190, 0.2); }
}

/* Header Estilizado */
.header-container {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(180deg, rgba(138, 5, 190, 0.1) 0%, rgba(10, 10, 15, 0) 100%);
    border-radius: 0 0 30px 30px;
    margin-bottom: 40px;
}

.header-title {
    background: linear-gradient(90deg, #8A05BE, #B5FF5A);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 15px;
}

.header-subtitle {
    color: rgba(245, 245, 245, 0.7);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}

/* Footer Estilizado */
.footer {
    text-align: center;
    padding: 30px;
    background: linear-gradient(0deg, rgba(138, 5, 190, 0.1) 0%, rgba(10, 10, 15, 0) 100%);
    margin-top: 60px;
}

.footer-text {
    color: rgba(245, 245, 245, 0.5);
    font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
    .card-grid {
        grid-template-columns: 1fr;
    }
    .header-title {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚀 Gerenciador Financeiro</h1>
    <p class="header-subtitle">Transforme suas finanças com uma experiência moderna e intuitiva de gestão financeira</p>
</div>
""", unsafe_allow_html=True)

# Cards Grid
st.markdown("""
<div class='card-grid'>
    <a href='?page=Dashboard' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>📊 Dashboard</div>
            <div class='card-desc'>Visualize sua situação financeira com análises detalhadas e gráficos interativos</div>
        </div>
    </a>
    <a href='?page=Contas' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>🏦 Contas</div>
            <div class='card-desc'>Gerencie suas contas bancárias e acompanhe seus saldos em tempo real</div>
        </div>
    </a>
    <a href='?page=Receitas' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>💰 Receitas</div>
            <div class='card-desc'>Registre e categorize suas fontes de renda para melhor controle</div>
        </div>
    </a>
    <a href='?page=Gastos' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>💸 Gastos</div>
            <div class='card-desc'>Monitore suas despesas e identifique oportunidades de economia</div>
        </div>
    </a>
    <a href='?page=Metas' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>🎯 Metas</div>
            <div class='card-desc'>Estabeleça objetivos financeiros e acompanhe seu progresso</div>
        </div>
    </a>
    <a href='?page=Compromissos' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>💼 Compromissos</div>
            <div class='card-desc'>Gerencie suas dívidas, parcelas e outros compromissos financeiros</div>
        </div>
    </a>
    <a href='?page=Investimentos' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>📈 Investimentos</div>
            <div class='card-desc'>Acompanhe seus investimentos e monitore seu patrimônio financeiro</div>
        </div>
    </a>
    <a href='?page=Orcamentos' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>📝 Orçamentos</div>
            <div class='card-desc'>Planeje seus gastos e mantenha o controle financeiro com orçamentos mensais</div>
        </div>
    </a>
    <a href='?page=ResumoMensal' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>📅 Resumo Mensal</div>
            <div class='card-desc'>Visualize o panorama completo das suas finanças mensais</div>
        </div>
    </a>
    <a href='?page=Insights' target="_self" style='text-decoration: none;'>
        <div class='card-container'>
            <div class='card-title'>🤖 Insights</div>
            <div class='card-desc'>Receba recomendações personalizadas baseadas em IA para otimizar suas finanças</div>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# Redirecionamento
page = st.query_params.get("page")

if page == "Dashboard":
    st.switch_page("pages/0_Dashboard.py")
elif page == "Contas":
    st.switch_page("pages/4_Contas.py")
elif page == "Receitas":
    st.switch_page("pages/2_Receitas.py")
elif page == "Gastos":
    st.switch_page("pages/1_Gastos.py")
elif page == "Metas":
    st.switch_page("pages/7_Metas.py")
elif page == "Compromissos":
    st.switch_page("pages/3_Compromissos.py")
elif page == "Investimentos":
    st.switch_page("pages/5_Investimentos.py")
elif page == "Orcamentos":
    st.switch_page("pages/6_Orcamentos.py")
elif page == "ResumoMensal":
    st.switch_page("pages/8_Resumo_mensal.py")
elif page == "Insights":
    st.switch_page("pages/9_Insights.py")

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">&copy; 2025 Gerenciador Financeiro - Desenvolvido com &hearts; e tecnologia de ponta</p>
</div>
""", unsafe_allow_html=True)
