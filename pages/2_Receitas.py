import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils import add_receita, update_receita, delete_receita, get_receitas, rerun, configurar_pagina
from style import apply_style, theme_toggle, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Receitas")

# Seleção de tema
theme = theme_toggle()
apply_style(theme)

# Botão voltar para home
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_receita_id" not in st.session_state:
    st.session_state.edit_receita_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">💰 Registro de Receitas</h1>
    <p class="header-subtitle">Acompanhe e analise suas fontes de renda</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar nova receita
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Nova Receita</h3>', unsafe_allow_html=True)
with st.form("form_receita"):
    col1, col2 = st.columns(2)
    with col1:
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor da Receita", min_value=0.0, format="%.2f")
    with col2:
        data = st.date_input("Data", datetime.date.today())
        categoria = st.selectbox("Categoria", [
            "Salário",
            "Investimentos",
            "Freelance",
            "Vendas",
            "Aluguel",
            "Outros"
        ])
    submitted = st.form_submit_button("Adicionar Receita")
    if submitted:
        add_receita(descricao, valor, str(data), categoria)
        st.markdown("""
        <div class="alert success">
            ✅ Receita registrada com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de receita
if st.session_state.edit_receita_id is not None:
    receita = next((r for r in get_receitas() if r[0] == st.session_state.edit_receita_id), None)
    if receita:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Receita</h3>', unsafe_allow_html=True)
        with st.form("edit_receita_form"):
            col1, col2 = st.columns(2)
            with col1:
                nova_descricao = st.text_input("Descrição", value=receita[1])
                novo_valor = st.number_input("Valor da Receita", min_value=0.0, value=receita[2], format="%.2f")
            with col2:
                nova_data = st.date_input("Data", value=datetime.datetime.strptime(receita[3], "%Y-%m-%d").date())
                nova_categoria = st.selectbox("Categoria", [
                    "Salário",
                    "Investimentos",
                    "Freelance",
                    "Vendas",
                    "Aluguel",
                    "Outros"
                ], index=["Salário", "Investimentos", "Freelance", "Vendas", "Aluguel", "Outros"].index(receita[4]))
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_receita(receita[0], nova_descricao, novo_valor, str(nova_data), nova_categoria)
                st.markdown("""
                <div class="alert success">
                    ✅ Receita atualizada com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_receita_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista e análise de receitas
receitas = get_receitas()
if receitas:
    st.markdown('<h3 class="section-title">📊 Análise de Receitas</h3>', unsafe_allow_html=True)
    
    # Métricas principais
    total_receitas = sum(receita[2] for receita in receitas)
    receitas_por_categoria = {}
    for r in receitas:
        receitas_por_categoria[r[4]] = receitas_por_categoria.get(r[4], 0) + r[2]
    
    # Calcular média mensal
    datas = [datetime.datetime.strptime(r[3], "%Y-%m-%d").date() for r in receitas]
    if len(datas) > 1:
        dias_total = (max(datas) - min(datas)).days
        media_mensal = total_receitas / (dias_total / 30) if dias_total > 0 else total_receitas
    else:
        media_mensal = total_receitas
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Total em Receitas</p>
            <h2 class="metric-value">{format_currency(total_receitas)}</h2>
            <span class="metric-subtitle">Total acumulado</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Média Mensal</p>
            <h2 class="metric-value">{format_currency(media_mensal)}</h2>
            <span class="metric-subtitle">Receita média por mês</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Principal Fonte</p>
            <h2 class="metric-value">{max(receitas_por_categoria.items(), key=lambda x: x[1])[0]}</h2>
            <span class="metric-subtitle">{format_currency(max(receitas_por_categoria.items(), key=lambda x: x[1])[1])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de receitas por categoria
        df_categorias = pd.DataFrame([
            {
                'Categoria': categoria,
                'Valor': valor
            } for categoria, valor in receitas_por_categoria.items()
        ])
        
        fig_categorias = px.pie(
            df_categorias,
            values='Valor',
            names='Categoria',
            title='Distribuição de Receitas por Categoria',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_categorias.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_categorias, use_container_width=True)
    
    with col2:
        # Gráfico de evolução temporal
        df_temporal = pd.DataFrame([
            {
                'Data': pd.to_datetime(r[3]),
                'Valor': r[2],
                'Categoria': r[4]
            } for r in receitas
        ]).sort_values('Data')
        
        fig_temporal = px.line(
            df_temporal,
            x='Data',
            y='Valor',
            color='Categoria',
            title='Evolução das Receitas ao Longo do Tempo',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_temporal.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Lista de receitas
    st.markdown('<h3 class="section-title">📋 Receitas Registradas</h3>', unsafe_allow_html=True)
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for receita in receitas:
        data_receita = datetime.datetime.strptime(receita[3], "%Y-%m-%d").date()
        dias_atras = (datetime.date.today() - data_receita).days
        
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['success']}; font-size: 1.2rem; margin-bottom: 10px;">{receita[1]}</h3>
                <p style="color: {COLORS['text']}; font-size: 1.5rem; margin-bottom: 5px;">{format_currency(receita[2])}</p>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                    Categoria: <span style="color: {COLORS['success']}">{receita[4]}</span><br>
                    {f"Há {dias_atras} dias" if dias_atras > 0 else "Hoje"} ({receita[3]})
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="stButton" onclick="document.querySelector('#edit_receita_{receita[0]}').click()">✏️ Editar</button>
                    <button class="stButton" onclick="document.querySelector('#delete_receita_{receita[0]}').click()">🗑️ Excluir</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões ocultos para funcionalidade
        if st.button("✏️", key=f"edit_receita_{receita[0]}", help="Editar receita"):
            st.session_state.edit_receita_id = receita[0]
            rerun()
        if st.button("🗑️", key=f"delete_receita_{receita[0]}", help="Excluir receita"):
            delete_receita(receita[0])
            st.markdown("""
            <div class="alert success">
                ✅ Receita excluída com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhuma receita registrada. Adicione suas receitas para começar a análise financeira.
    </div>
    """, unsafe_allow_html=True)