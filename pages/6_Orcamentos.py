import streamlit as st
import datetime
import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import add_orcamento, update_orcamento, delete_orcamento, get_orcamentos, get_gastos, get_categorias, calcular_fluxo_caixa_mensal, rerun, configurar_pagina
from style import apply_style, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Orçamentos")

# Aplicar estilos
apply_style()

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_orcamento_id" not in st.session_state:
    st.session_state.edit_orcamento_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📝 Orçamentos</h1>
    <p class="header-subtitle">Planeje seus gastos e mantenha o controle financeiro com orçamentos mensais</p>
</div>
""", unsafe_allow_html=True)

# Obter mês e ano atual para filtros
hoje = datetime.date.today()
mes_atual = hoje.month
ano_atual = hoje.year

# Seletor de mês e ano
col1, col2 = st.columns(2)
with col1:
    mes_selecionado = st.selectbox(
        "Mês", 
        options=list(range(1, 13)),
        format_func=lambda x: calendar.month_name[x],
        index=mes_atual - 1
    )
with col2:
    ano_selecionado = st.selectbox(
        "Ano",
        options=list(range(ano_atual - 2, ano_atual + 3)),
        index=2
    )

# Obter categorias para gastos
categorias = [cat[1] for cat in get_categorias("gasto")]
if not categorias:
    categorias = ["Moradia", "Alimentação", "Transporte", "Saúde", "Educação", "Lazer", "Vestuário", "Serviços", "Outros"]

# Container para adicionar novo orçamento
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Novo Orçamento</h3>', unsafe_allow_html=True)
with st.form("form_orcamento"):
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Categoria", options=categorias)
        valor_planejado = st.number_input("Valor Planejado", min_value=0.0, format="%.2f")
    with col2:
        mes = st.selectbox(
            "Mês", 
            options=list(range(1, 13)),
            format_func=lambda x: calendar.month_name[x],
            index=mes_atual - 1,
            key="form_mes"
        )
        ano = st.selectbox(
            "Ano",
            options=list(range(ano_atual - 2, ano_atual + 3)),
            index=2,
            key="form_ano"
        )
    
    submitted = st.form_submit_button("Registrar Orçamento")
    if submitted:
        # Verificar se já existe orçamento para esta categoria neste mês/ano
        mes_str = f"{ano}-{mes:02d}"
        orcamentos_existentes = get_orcamentos(mes, ano)
        categoria_existente = next((o for o in orcamentos_existentes if o[1] == categoria), None)
        
        if categoria_existente:
            st.markdown(f"""
            <div class="alert warning">
                ⚠️ Já existe um orçamento para a categoria {categoria} no período {calendar.month_name[mes]}/{ano}.
            </div>
            """, unsafe_allow_html=True)
        else:
            add_orcamento(
                categoria=categoria,
                valor_planejado=valor_planejado,
                mes=mes_str,
                ano=ano
            )
            st.markdown("""
            <div class="alert success">
                ✅ Orçamento registrado com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de orçamento
if st.session_state.edit_orcamento_id is not None:
    orcamento = next((o for o in get_orcamentos() if o[0] == st.session_state.edit_orcamento_id), None)
    if orcamento:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Orçamento</h3>', unsafe_allow_html=True)
        with st.form("edit_orcamento_form"):
            col1, col2 = st.columns(2)
            with col1:
                nova_categoria = st.selectbox("Categoria", options=categorias, index=categorias.index(orcamento[1]) if orcamento[1] in categorias else 0)
                novo_valor = st.number_input("Valor Planejado", min_value=0.0, value=float(orcamento[2]), format="%.2f")
            with col2:
                mes_ano = orcamento[3].split("-")
                novo_mes = st.selectbox(
                    "Mês", 
                    options=list(range(1, 13)),
                    format_func=lambda x: calendar.month_name[x],
                    index=int(mes_ano[1]) - 1,
                    key="edit_mes"
                )
                novo_ano = st.selectbox(
                    "Ano",
                    options=list(range(ano_atual - 2, ano_atual + 3)),
                    index=list(range(ano_atual - 2, ano_atual + 3)).index(orcamento[4]),
                    key="edit_ano"
                )
            
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                novo_mes_str = f"{novo_ano}-{novo_mes:02d}"
                update_orcamento(
                    record_id=orcamento[0],
                    categoria=nova_categoria,
                    valor_planejado=novo_valor,
                    mes=novo_mes_str,
                    ano=novo_ano
                )
                st.markdown("""
                <div class="alert success">
                    ✅ Orçamento atualizado com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_orcamento_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Obter orçamentos para o mês/ano selecionado
orcamentos = get_orcamentos(mes_selecionado, ano_selecionado)

# Obter gastos para o mês/ano selecionado
mes_str = f"{ano_selecionado}-{mes_selecionado:02d}"
gastos = [g for g in get_gastos() if g[3].startswith(mes_str)]

# Calcular gastos por categoria
gastos_por_categoria = {}
for gasto in gastos:
    categoria = gasto[4]
    if categoria in gastos_por_categoria:
        gastos_por_categoria[categoria] += gasto[2]
    else:
        gastos_por_categoria[categoria] = gasto[2]

# Análise de orçamentos
if orcamentos:
    st.markdown('<h3 class="section-title">📊 Análise de Orçamentos</h3>', unsafe_allow_html=True)
    
    # Calcular métricas
    total_orcado = sum(o[2] for o in orcamentos)
    total_gasto = sum(gastos_por_categoria.values())
    percentual_utilizado = (total_gasto / total_orcado) * 100 if total_orcado > 0 else 0
    
    # Fluxo de caixa do mês
    fluxo_caixa = calcular_fluxo_caixa_mensal(mes_selecionado, ano_selecionado)
    saldo_mes = fluxo_caixa['saldo']
    
    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Orçado</p>
            <h2 class="metric-value">{format_currency(total_orcado)}</h2>
            <span class="metric-subtitle">Planejamento mensal</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Gasto</p>
            <h2 class="metric-value">{format_currency(total_gasto)}</h2>
            <span class="metric-subtitle">{percentual_utilizado:.1f}% do orçamento</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        saldo_color = COLORS['success'] if saldo_mes >= 0 else COLORS['danger']
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Saldo do Mês</p>
            <h2 class="metric-value" style="color: {saldo_color};">{format_currency(saldo_mes)}</h2>
            <span class="metric-subtitle">Receitas - Gastos - Compromissos</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Preparar dados para gráficos
    dados_orcamento = []
    for orcamento in orcamentos:
        categoria = orcamento[1]
        valor_orcado = orcamento[2]
        valor_gasto = gastos_por_categoria.get(categoria, 0)
        percentual = (valor_gasto / valor_orcado) * 100 if valor_orcado > 0 else 0
        
        status = "Dentro do orçamento"
        if percentual >= 100:
            status = "Acima do orçamento"
        elif percentual >= 80:
            status = "Próximo do limite"
        
        dados_orcamento.append({
            'Categoria': categoria,
            'Valor Orçado': valor_orcado,
            'Valor Gasto': valor_gasto,
            'Percentual': percentual,
            'Status': status
        })
    
    df_orcamento = pd.DataFrame(dados_orcamento)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras comparando orçado vs gasto
        fig_comparativo = go.Figure()
        fig_comparativo.add_trace(go.Bar(
            x=df_orcamento['Categoria'],
            y=df_orcamento['Valor Orçado'],
            name='Orçado',
            marker_color=COLORS['primary']
        ))
        fig_comparativo.add_trace(go.Bar(
            x=df_orcamento['Categoria'],
            y=df_orcamento['Valor Gasto'],
            name='Gasto',
            marker_color=COLORS['secondary']
        ))
        fig_comparativo.update_layout(
            title='Orçado vs Gasto por Categoria',
            barmode='group',
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_comparativo, use_container_width=True)
    
    with col2:
        # Gráfico de percentual utilizado
        df_orcamento_sorted = df_orcamento.sort_values('Percentual', ascending=False)
        
        fig_percentual = px.bar(
            df_orcamento_sorted,
            x='Categoria',
            y='Percentual',
            color='Status',
            title='Percentual do Orçamento Utilizado',
            color_discrete_map={
                'Dentro do orçamento': COLORS['success'],
                'Próximo do limite': COLORS['warning'],
                'Acima do orçamento': COLORS['danger']
            },
            text='Percentual'
        )
        fig_percentual.update_layout(**PLOTLY_LAYOUT)
        fig_percentual.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_percentual, use_container_width=True)
    
    # Gráfico de pizza com distribuição do orçamento
    fig_distribuicao = px.pie(
        df_orcamento,
        values='Valor Orçado',
        names='Categoria',
        title='Distribuição do Orçamento por Categoria',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning'], COLORS['danger']]
    )
    fig_distribuicao.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_distribuicao, use_container_width=True)
    
    # Lista de orçamentos
    st.markdown('<h3 class="section-title">📋 Orçamentos do Mês</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for orcamento in orcamentos:
        categoria = orcamento[1]
        valor_orcado = orcamento[2]
        valor_gasto = gastos_por_categoria.get(categoria, 0)
        percentual = (valor_gasto / valor_orcado) * 100 if valor_orcado > 0 else 0
        
        # Definir cor com base no percentual
        if percentual >= 100:
            status_color = COLORS['danger']
        elif percentual >= 80:
            status_color = COLORS['warning']
        else:
            status_color = COLORS['success']
        
        st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="color: {COLORS['text']}; font-size: 1.2rem; margin: 0;">{categoria}</h3>
                    <span style="background-color: {status_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{percentual:.1f}%</span>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="background-color: {COLORS['surface']}; border-radius: 8px; height: 10px; width: 100%;">
                        <div style="background-color: {status_color}; border-radius: 8px; height: 10px; width: {min(percentual, 100)}%;"></div>
                    </div>
                </div>
                <p style="color: {COLORS['text']}; font-size: 1.1rem; margin-bottom: 5px;">
                    {format_currency(valor_gasto)} / {format_currency(valor_orcado)}
                </p>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                    Restante: {format_currency(max(0, valor_orcado - valor_gasto))}
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="stButton" onclick="document.querySelector('#edit_orcamento_{orcamento[0]}').click()">✏️ Editar</button>
                    <button class="stButton" onclick="document.querySelector('#delete_orcamento_{orcamento[0]}').click()">🗑️ Excluir</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões ocultos para funcionalidade
        if st.button("✏️", key=f"edit_orcamento_{orcamento[0]}", help="Editar orçamento"):
            st.session_state.edit_orcamento_id = orcamento[0]
            rerun()
        if st.button("🗑️", key=f"delete_orcamento_{orcamento[0]}", help="Excluir orçamento"):
            delete_orcamento(orcamento[0])
            st.markdown("""
            <div class="alert success">
                ✅ Orçamento excluído com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert">
        ℹ️ Nenhum orçamento definido para {calendar.month_name[mes_selecionado]}/{ano_selecionado}. 
        Adicione orçamentos para melhor controle financeiro.
    </div>
    """, unsafe_allow_html=True)
