import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils import get_receitas, get_gastos, get_contas, get_dividas, get_parcelas, add_meta, get_metas, configurar_pagina
from style import apply_style, theme_toggle, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Resumo Mensal")

# Seleção de tema
theme = theme_toggle()
apply_style(theme)

# Botão voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📅 Resumo Financeiro Mensal</h1>
    <p class="header-subtitle">Acompanhe e analise suas finanças mês a mês</p>
</div>
""", unsafe_allow_html=True)

# Carregar dados
receitas = get_receitas()
gastos = get_gastos()
dividas = get_dividas()
parcelas = get_parcelas()

# Converter para DataFrames
df_receitas = pd.DataFrame(receitas, columns=["id", "descricao", "valor", "data", "categoria"])
df_gastos = pd.DataFrame(gastos, columns=["id", "descricao", "valor", "data", "categoria"])
df_dividas = pd.DataFrame(dividas, columns=["id", "descricao", "valor", "data", "categoria"])
df_parcelas = pd.DataFrame(parcelas, columns=["id", "descricao", "valor", "data"])

# Converter colunas de data
for df in [df_receitas, df_gastos, df_dividas, df_parcelas]:
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors='coerce')

# Container de seleção de mês
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">📆 Período de Análise</h3>', unsafe_allow_html=True)
mes_ano = st.selectbox(
    "Selecione o mês de análise:",
    options=pd.date_range(start="2023-01-01", end=datetime.datetime.today(), freq='MS').strftime("%Y-%m").tolist()[::-1],
    format_func=lambda x: datetime.datetime.strptime(x, "%Y-%m").strftime("%B de %Y").title()
)
st.markdown('</div>', unsafe_allow_html=True)

filtro_data = lambda df: df[(df["data"].dt.strftime("%Y-%m") == mes_ano)] if not df.empty else pd.DataFrame()

# Filtrar por mês selecionado
r_mensal = filtro_data(df_receitas)
g_mensal = filtro_data(df_gastos)
d_mensal = filtro_data(df_dividas)
p_mensal = filtro_data(df_parcelas)

# Calcular totais
total_receitas = r_mensal["valor"].sum() if not r_mensal.empty else 0
total_gastos = g_mensal["valor"].sum() if not g_mensal.empty else 0
total_dividas = d_mensal["valor"].sum() if not d_mensal.empty else 0
total_parcelas = p_mensal["valor"].sum() if not p_mensal.empty else 0
saldo = total_receitas - total_gastos - total_dividas - total_parcelas

# Exibir métricas
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <p class="metric-label">Receitas</p>
        <h2 class="metric-value">{format_currency(total_receitas)}</h2>
        <span class="metric-subtitle">Total de entradas</span>
    </div>
    <div class="metric-card">
        <p class="metric-label">Gastos</p>
        <h2 class="metric-value">{format_currency(total_gastos)}</h2>
        <span class="metric-subtitle">Total de saídas</span>
    </div>
    <div class="metric-card">
        <p class="metric-label">Dívidas</p>
        <h2 class="metric-value">{format_currency(total_dividas)}</h2>
        <span class="metric-subtitle">Total de dívidas</span>
    </div>
    <div class="metric-card">
        <p class="metric-label">Parcelas</p>
        <h2 class="metric-value">{format_currency(total_parcelas)}</h2>
        <span class="metric-subtitle">Total de parcelas</span>
    </div>
    <div class="metric-card" style="border-color: {COLORS['success'] if saldo >= 0 else COLORS['error']}">
        <p class="metric-label">Saldo Mensal</p>
        <h2 class="metric-value" style="color: {COLORS['success'] if saldo >= 0 else COLORS['error']}">{format_currency(saldo)}</h2>
        <span class="metric-subtitle">Resultado do mês</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Gráficos de análise
col1, col2 = st.columns(2)

with col1:
    # Gráfico de composição mensal
    df_composicao = pd.DataFrame([
        {'Tipo': 'Receitas', 'Valor': total_receitas},
        {'Tipo': 'Gastos', 'Valor': total_gastos},
        {'Tipo': 'Dívidas', 'Valor': total_dividas},
        {'Tipo': 'Parcelas', 'Valor': total_parcelas}
    ])
    
    fig_composicao = px.bar(
        df_composicao,
        x='Tipo',
        y='Valor',
        title='Composição Financeira do Mês',
        color='Tipo',
        color_discrete_map={
            'Receitas': COLORS['success'],
            'Gastos': COLORS['warning'],
            'Dívidas': COLORS['error'],
            'Parcelas': COLORS['primary']
        }
    )
    fig_composicao.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_composicao, use_container_width=True)

with col2:
    # Gráfico de evolução diária
    df_evolucao = pd.concat([
        r_mensal.assign(tipo='Receitas'),
        g_mensal.assign(tipo='Gastos'),
        d_mensal.assign(tipo='Dívidas'),
        p_mensal.assign(tipo='Parcelas')
    ])
    
    if not df_evolucao.empty:
        df_evolucao = df_evolucao.groupby(['data', 'tipo'])['valor'].sum().reset_index()
        fig_evolucao = px.line(
            df_evolucao,
            x='data',
            y='valor',
            color='tipo',
            title='Evolução Diária',
            color_discrete_map={
                'Receitas': COLORS['success'],
                'Gastos': COLORS['warning'],
                'Dívidas': COLORS['error'],
                'Parcelas': COLORS['primary']
            }
        )
        fig_evolucao.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_evolucao, use_container_width=True)

# Detalhamento por categoria
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">🔍 Detalhamento por Categoria</h3>', unsafe_allow_html=True)

tabs = st.tabs(["📈 Receitas", "📉 Gastos", "💰 Dívidas", "📅 Parcelas"])

with tabs[0]:
    if not r_mensal.empty:
        # Gráfico de receitas por categoria
        receitas_categoria = r_mensal.groupby('categoria')['valor'].sum().reset_index()
        fig_receitas = px.pie(
            receitas_categoria,
            values='valor',
            names='categoria',
            title='Distribuição de Receitas por Categoria',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_receitas.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_receitas, use_container_width=True)
        
        # Tabela de receitas
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(
            r_mensal[["descricao", "valor", "data", "categoria"]]
            .assign(
                valor=lambda x: x["valor"].apply(lambda v: f"R$ {v:,.2f}"),
                data=lambda x: x["data"].dt.strftime("%d/%m/%Y")
            )
            .rename(columns={
                "descricao": "Descrição",
                "valor": "Valor",
                "data": "Data",
                "categoria": "Categoria"
            }),
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma receita registrada neste mês.")

with tabs[1]:
    if not g_mensal.empty:
        # Gráfico de gastos por categoria
        gastos_categoria = g_mensal.groupby('categoria')['valor'].sum().reset_index()
        fig_gastos = px.pie(
            gastos_categoria,
            values='valor',
            names='categoria',
            title='Distribuição de Gastos por Categoria',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_gastos.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_gastos, use_container_width=True)
        
        # Tabela de gastos
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(
            g_mensal[["descricao", "valor", "data", "categoria"]]
            .assign(
                valor=lambda x: x["valor"].apply(lambda v: f"R$ {v:,.2f}"),
                data=lambda x: x["data"].dt.strftime("%d/%m/%Y")
            )
            .rename(columns={
                "descricao": "Descrição",
                "valor": "Valor",
                "data": "Data",
                "categoria": "Categoria"
            }),
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhum gasto registrado neste mês.")

with tabs[2]:
    if not d_mensal.empty:
        # Gráfico de dívidas por categoria
        dividas_categoria = d_mensal.groupby('categoria')['valor'].sum().reset_index()
        fig_dividas = px.pie(
            dividas_categoria,
            values='valor',
            names='categoria',
            title='Distribuição de Dívidas por Categoria',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_dividas.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_dividas, use_container_width=True)
        
        # Tabela de dívidas
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(
            d_mensal[["descricao", "valor", "data", "categoria"]]
            .assign(
                valor=lambda x: x["valor"].apply(lambda v: f"R$ {v:,.2f}"),
                data=lambda x: x["data"].dt.strftime("%d/%m/%Y")
            )
            .rename(columns={
                "descricao": "Descrição",
                "valor": "Valor",
                "data": "Data",
                "categoria": "Categoria"
            }),
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma dívida registrada neste mês.")

with tabs[3]:
    if not p_mensal.empty:
        # Gráfico de parcelas ao longo do mês
        parcelas_dia = p_mensal.groupby('data')['valor'].sum().reset_index()
        fig_parcelas = go.Figure()
        fig_parcelas.add_trace(go.Scatter(
            x=parcelas_dia['data'],
            y=parcelas_dia['valor'],
            mode='lines+markers',
            name='Valor',
            line=dict(color=COLORS['primary'])
        ))
        fig_parcelas.update_layout(
            title='Distribuição de Parcelas ao Longo do Mês',
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_parcelas, use_container_width=True)
        
        # Tabela de parcelas
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(
            p_mensal[["descricao", "valor", "data"]]
            .assign(
                valor=lambda x: x["valor"].apply(lambda v: f"R$ {v:,.2f}"),
                data=lambda x: x["data"].dt.strftime("%d/%m/%Y")
            )
            .rename(columns={
                "descricao": "Descrição",
                "valor": "Valor",
                "data": "Data"
            }),
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma parcela registrada neste mês.")

st.markdown('</div>', unsafe_allow_html=True)
