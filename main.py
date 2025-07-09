import streamlit as st
import pandas as pd
from utils import configurar_pagina
from style import apply_style, theme_toggle, COLORS

# Configuração da página
configurar_pagina("Gerenciador Financeiro")


# Seleção de tema e aplicação de estilos
theme = theme_toggle()
apply_style(theme)

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
