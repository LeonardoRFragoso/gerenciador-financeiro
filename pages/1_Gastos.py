import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils import add_gasto, update_gasto, delete_gasto, get_gastos, rerun, configurar_pagina
from style import apply_style, theme_toggle, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Gastos")

# Seleção de tema
theme = theme_toggle()
apply_style(theme)

# Botão de retorno
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_gasto_id" not in st.session_state:
    st.session_state.edit_gasto_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">💸 Registro de Gastos</h1>
    <p class="header-subtitle">Monitore e categorize suas despesas para um melhor controle financeiro</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar novo gasto
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Novo Gasto</h3>', unsafe_allow_html=True)
with st.form("form_gasto"):
    col1, col2 = st.columns(2)
    with col1:
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor do Gasto", min_value=0.0, format="%.2f")
    with col2:
        data = st.date_input("Data", datetime.date.today())
        categoria = st.text_input("Categoria")
    submitted = st.form_submit_button("Adicionar Gasto")
    if submitted:
        add_gasto(descricao, valor, str(data), categoria)
        st.markdown("""
        <div class="alert success">
            ✅ Gasto registrado com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de gasto
if st.session_state.edit_gasto_id is not None:
    gasto = next((g for g in get_gastos() if g[0] == st.session_state.edit_gasto_id), None)
    if gasto:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Gasto</h3>', unsafe_allow_html=True)
        with st.form("edit_gasto_form"):
            col1, col2 = st.columns(2)
            with col1:
                nova_descricao = st.text_input("Descrição", value=gasto[1])
                novo_valor = st.number_input("Valor do Gasto", min_value=0.0, value=gasto[2], format="%.2f")
            with col2:
                nova_data = st.date_input("Data", value=datetime.datetime.strptime(gasto[3], "%Y-%m-%d").date())
                nova_categoria = st.text_input("Categoria", value=gasto[4])
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_gasto(gasto[0], nova_descricao, novo_valor, str(nova_data), nova_categoria)
                st.markdown("""
                <div class="alert success">
                    ✅ Gasto atualizado com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_gasto_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista e análise de gastos
gastos = get_gastos()
if gastos:
    st.markdown('<h3 class="section-title">📊 Análise de Gastos</h3>', unsafe_allow_html=True)
    
    # Métricas principais
    total_gastos = sum(gasto[2] for gasto in gastos)
    gastos_por_categoria = {}
    for gasto in gastos:
        categoria = gasto[4]
        if categoria in gastos_por_categoria:
            gastos_por_categoria[categoria] += gasto[2]
        else:
            gastos_por_categoria[categoria] = gasto[2]
    
    categoria_maior_gasto = max(gastos_por_categoria.items(), key=lambda x: x[1])
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Total de Gastos</p>
            <h2 class="metric-value">{format_currency(total_gastos)}</h2>
            <span class="metric-subtitle">Soma de todas as despesas</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Maior Categoria</p>
            <h2 class="metric-value">{categoria_maior_gasto[0]}</h2>
            <span class="metric-subtitle">{format_currency(categoria_maior_gasto[1])}</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Média por Gasto</p>
            <h2 class="metric-value">{format_currency(total_gastos/len(gastos))}</h2>
            <span class="metric-subtitle">Valor médio por registro</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de gastos por categoria
        df_categoria = pd.DataFrame(list(gastos_por_categoria.items()), columns=['Categoria', 'Valor'])
        fig_categoria = px.pie(
            df_categoria,
            values='Valor',
            names='Categoria',
            title='Distribuição de Gastos por Categoria'
        )
        fig_categoria.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    with col2:
        # Gráfico de evolução temporal
        df_temporal = pd.DataFrame([(g[3], g[2]) for g in gastos], columns=['Data', 'Valor'])
        df_temporal['Data'] = pd.to_datetime(df_temporal['Data'])
        df_temporal = df_temporal.sort_values('Data')
        fig_temporal = px.line(
            df_temporal,
            x='Data',
            y='Valor',
            title='Evolução dos Gastos ao Longo do Tempo'
        )
        fig_temporal.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Lista de gastos
    st.markdown('<h3 class="section-title">📋 Gastos Registrados</h3>', unsafe_allow_html=True)
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for gasto in gastos:
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['secondary']}; font-size: 1.2rem; margin-bottom: 10px;">{gasto[1]}</h3>
                <p style="color: {COLORS['text']}; font-size: 1.5rem; margin-bottom: 5px;">{format_currency(gasto[2])}</p>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                    Data: {gasto[3]}<br>
                    Categoria: {gasto[4]}
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="stButton" onclick="document.querySelector('#edit_gasto_{gasto[0]}').click()">✏️ Editar</button>
                    <button class="stButton" onclick="document.querySelector('#delete_gasto_{gasto[0]}').click()">🗑️ Excluir</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões ocultos para funcionalidade
        if st.button("✏️", key=f"edit_gasto_{gasto[0]}", help="Editar gasto"):
            st.session_state.edit_gasto_id = gasto[0]
            rerun()
        if st.button("🗑️", key=f"delete_gasto_{gasto[0]}", help="Excluir gasto"):
            delete_gasto(gasto[0])
            st.markdown("""
            <div class="alert success">
                ✅ Gasto excluído com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhum gasto registrado. Comece adicionando suas despesas para ter um melhor controle financeiro.
    </div>
    """, unsafe_allow_html=True)
