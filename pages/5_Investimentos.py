import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import add_investimento, update_investimento, delete_investimento, get_investimentos, rerun, configurar_pagina
from style import apply_style, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Investimentos")

# Aplicar estilos
apply_style()

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_investimento_id" not in st.session_state:
    st.session_state.edit_investimento_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📈 Investimentos</h1>
    <p class="header-subtitle">Gerencie seus investimentos e acompanhe seu patrimônio financeiro</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar novo investimento
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Novo Investimento</h3>', unsafe_allow_html=True)
with st.form("form_investimento"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do Investimento")
        tipo = st.selectbox("Tipo", ["Renda Fixa", "Ações", "Fundos", "Criptomoedas", "Imóveis", "Outro"])
        valor_investido = st.number_input("Valor Investido", min_value=0.0, format="%.2f")
    with col2:
        valor_atual = st.number_input("Valor Atual", min_value=0.0, format="%.2f")
        data_inicio = st.date_input("Data de Início", datetime.date.today())
        instituicao = st.text_input("Instituição")
    
    # Calcular rendimento automaticamente
    if valor_investido > 0:
        rendimento_percentual = ((valor_atual / valor_investido) - 1) * 100
    else:
        rendimento_percentual = 0
    
    st.markdown(f"<p>Rendimento: <strong>{rendimento_percentual:.2f}%</strong></p>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("Registrar Investimento")
    if submitted:
        add_investimento(
            nome=nome,
            tipo=tipo,
            valor_investido=valor_investido,
            valor_atual=valor_atual,
            data_inicio=str(data_inicio),
            rendimento_percentual=rendimento_percentual,
            instituicao=instituicao
        )
        st.markdown("""
        <div class="alert success">
            ✅ Investimento registrado com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de investimento
if st.session_state.edit_investimento_id is not None:
    investimento = next((i for i in get_investimentos() if i[0] == st.session_state.edit_investimento_id), None)
    if investimento:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Investimento</h3>', unsafe_allow_html=True)
        with st.form("edit_investimento_form"):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", value=investimento[1])
                novo_tipo = st.selectbox("Tipo", ["Renda Fixa", "Ações", "Fundos", "Criptomoedas", "Imóveis", "Outro"], 
                                        index=["Renda Fixa", "Ações", "Fundos", "Criptomoedas", "Imóveis", "Outro"].index(investimento[2]))
                novo_valor_investido = st.number_input("Valor Investido", min_value=0.0, value=float(investimento[3]), format="%.2f")
            with col2:
                novo_valor_atual = st.number_input("Valor Atual", min_value=0.0, value=float(investimento[4]), format="%.2f")
                nova_data = st.date_input("Data de Início", 
                                         value=datetime.datetime.strptime(investimento[5], "%Y-%m-%d").date() 
                                         if investimento[5] else datetime.date.today())
                nova_instituicao = st.text_input("Instituição", value=investimento[7])
            
            # Calcular rendimento automaticamente
            if novo_valor_investido > 0:
                novo_rendimento_percentual = ((novo_valor_atual / novo_valor_investido) - 1) * 100
            else:
                novo_rendimento_percentual = 0
            
            st.markdown(f"<p>Rendimento: <strong>{novo_rendimento_percentual:.2f}%</strong></p>", unsafe_allow_html=True)
            
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_investimento(
                    record_id=investimento[0],
                    nome=novo_nome,
                    tipo=novo_tipo,
                    valor_investido=novo_valor_investido,
                    valor_atual=novo_valor_atual,
                    data_inicio=str(nova_data),
                    rendimento_percentual=novo_rendimento_percentual,
                    instituicao=nova_instituicao
                )
                st.markdown("""
                <div class="alert success">
                    ✅ Investimento atualizado com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_investimento_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista e análise de investimentos
investimentos = get_investimentos()
if investimentos:
    st.markdown('<h3 class="section-title">📊 Análise de Investimentos</h3>', unsafe_allow_html=True)
    
    # Métricas principais
    total_investido = sum(i[3] for i in investimentos)
    total_atual = sum(i[4] for i in investimentos)
    rendimento_total = ((total_atual / total_investido) - 1) * 100 if total_investido > 0 else 0
    
    # Investimento com maior rendimento
    melhor_investimento = max(investimentos, key=lambda i: i[6] if i[6] is not None else 0)
    
    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Investido</p>
            <h2 class="metric-value">{format_currency(total_investido)}</h2>
            <span class="metric-subtitle">Capital aplicado</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Valor Atual</p>
            <h2 class="metric-value">{format_currency(total_atual)}</h2>
            <span class="metric-subtitle">Patrimônio total</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rendimento_color = COLORS['success'] if rendimento_total >= 0 else COLORS['danger']
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Rendimento Total</p>
            <h2 class="metric-value" style="color: {rendimento_color};">{rendimento_total:.2f}%</h2>
            <span class="metric-subtitle">{format_currency(total_atual - total_investido)}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribuição por tipo
        df_tipo = pd.DataFrame([(i[2], i[4]) for i in investimentos], columns=['Tipo', 'Valor'])
        df_tipo = df_tipo.groupby('Tipo').sum().reset_index()
        
        fig_tipo = px.pie(
            df_tipo,
            values='Valor',
            names='Tipo',
            title='Distribuição de Investimentos por Tipo',
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['danger'], COLORS['warning']]
        )
        fig_tipo.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    with col2:
        # Gráfico de rendimento por investimento
        df_rendimento = pd.DataFrame([
            {
                'Nome': i[1],
                'Rendimento': i[6],
                'Valor': i[4]
            } for i in investimentos
        ])
        
        fig_rendimento = px.bar(
            df_rendimento,
            x='Nome',
            y='Rendimento',
            color='Rendimento',
            title='Rendimento por Investimento (%)',
            color_continuous_scale=['red', 'yellow', 'green'],
            text='Rendimento'
        )
        fig_rendimento.update_layout(**PLOTLY_LAYOUT)
        fig_rendimento.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig_rendimento, use_container_width=True)
    
    # Gráfico de evolução do patrimônio
    df_evolucao = pd.DataFrame([
        {
            'Data': pd.to_datetime(i[5]),
            'Valor Investido': i[3],
            'Valor Atual': i[4],
            'Nome': i[1]
        } for i in investimentos
    ]).sort_values('Data')
    
    fig_evolucao = go.Figure()
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao['Data'],
        y=df_evolucao['Valor Investido'].cumsum(),
        name='Capital Investido',
        line=dict(color=COLORS['secondary'])
    ))
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao['Data'],
        y=df_evolucao['Valor Atual'].cumsum(),
        name='Valor Atual',
        line=dict(color=COLORS['success'])
    ))
    fig_evolucao.update_layout(
        title='Evolução do Patrimônio ao Longo do Tempo',
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)
    
    # Lista de investimentos
    st.markdown('<h3 class="section-title">📋 Investimentos Registrados</h3>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_tipo = st.multiselect(
            "Filtrar por Tipo",
            options=list(set(i[2] for i in investimentos)),
            default=list(set(i[2] for i in investimentos))
        )
    with col2:
        ordenar_por = st.selectbox(
            "Ordenar por",
            options=["Valor Atual", "Rendimento", "Data de Início"]
        )
    
    # Aplicar filtros
    investimentos_filtrados = [i for i in investimentos if i[2] in filtro_tipo]
    
    # Aplicar ordenação
    if ordenar_por == "Valor Atual":
        investimentos_filtrados.sort(key=lambda i: i[4], reverse=True)
    elif ordenar_por == "Rendimento":
        investimentos_filtrados.sort(key=lambda i: i[6] if i[6] is not None else 0, reverse=True)
    elif ordenar_por == "Data de Início":
        investimentos_filtrados.sort(key=lambda i: i[5])
    
    # Lista de investimentos
    if investimentos_filtrados:
        st.markdown('<div class="grid">', unsafe_allow_html=True)
        for investimento in investimentos_filtrados:
            data_inicio = datetime.datetime.strptime(investimento[5], "%Y-%m-%d").date()
            dias_investidos = (datetime.date.today() - data_inicio).days
            
            rendimento_color = COLORS['success'] if investimento[6] >= 0 else COLORS['danger']
            
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h3 style="color: {COLORS['text']}; font-size: 1.2rem; margin: 0;">{investimento[1]}</h3>
                        <span style="background-color: {COLORS['surface']}; color: {COLORS['text']}; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{investimento[2]}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <p style="color: {COLORS['text']}; font-size: 1.5rem; margin: 0;">{format_currency(investimento[4])}</p>
                        <span style="color: {rendimento_color}; font-weight: bold;">{investimento[6]:.2f}%</span>
                    </div>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 10px;">
                        Investido: {format_currency(investimento[3])}
                    </p>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                        Instituição: {investimento[7]}<br>
                        Investido há {dias_investidos} dias ({investimento[5]})
                    </p>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button class="stButton" onclick="document.querySelector('#edit_investimento_{investimento[0]}').click()">✏️ Editar</button>
                        <button class="stButton" onclick="document.querySelector('#delete_investimento_{investimento[0]}').click()">🗑️ Excluir</button>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botões ocultos para funcionalidade
            if st.button("✏️", key=f"edit_investimento_{investimento[0]}", help="Editar investimento"):
                st.session_state.edit_investimento_id = investimento[0]
                rerun()
            if st.button("🗑️", key=f"delete_investimento_{investimento[0]}", help="Excluir investimento"):
                delete_investimento(investimento[0])
                st.markdown("""
                <div class="alert success">
                    ✅ Investimento excluído com sucesso!
                </div>
                """, unsafe_allow_html=True)
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert">
            ℹ️ Nenhum investimento encontrado com os filtros selecionados.
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhum investimento registrado. Adicione seus investimentos para acompanhar seu patrimônio.
    </div>
    """, unsafe_allow_html=True)
