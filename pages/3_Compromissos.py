import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import add_compromisso, update_compromisso, delete_compromisso, get_compromissos, rerun, configurar_pagina
from style import apply_style, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Compromissos Financeiros")

# Aplicar estilos
apply_style()

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_compromisso_id" not in st.session_state:
    st.session_state.edit_compromisso_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">💼 Compromissos Financeiros</h1>
    <p class="header-subtitle">Gerencie suas dívidas, parcelas e compromissos financeiros em um só lugar</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar novo compromisso
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Novo Compromisso</h3>', unsafe_allow_html=True)
with st.form("form_compromisso"):
    col1, col2 = st.columns(2)
    with col1:
        descricao = st.text_input("Descrição")
        tipo = st.selectbox("Tipo", ["Dívida", "Parcela", "Financiamento", "Empréstimo", "Outro"])
        valor_total = st.number_input("Valor Total", min_value=0.0, format="%.2f")
    with col2:
        data_vencimento = st.date_input("Data de Vencimento", datetime.date.today())
        status = st.selectbox("Status", ["Pendente", "Pago", "Atrasado", "Parcial"])
        
        # Campos condicionais baseados no tipo
        if tipo in ["Financiamento", "Empréstimo", "Dívida"]:
            taxa_juros = st.number_input("Taxa de Juros (%)", min_value=0.0, max_value=100.0, format="%.2f")
        else:
            taxa_juros = 0.0
            
        # Opção de parcelamento
        is_parcelado = st.checkbox("Parcelado")
        
    # Campos de parcelamento (aparecem se a opção de parcelamento estiver marcada)
    if is_parcelado:
        col1, col2 = st.columns(2)
        with col1:
            total_parcelas = st.number_input("Total de Parcelas", min_value=1, value=1)
        with col2:
            parcela_atual = st.number_input("Parcela Atual", min_value=1, max_value=total_parcelas, value=1)
        
        # Calcular valor da parcela automaticamente
        valor_parcela = valor_total / total_parcelas if total_parcelas > 0 else valor_total
        st.markdown(f"<p>Valor da Parcela: <strong>{format_currency(valor_parcela)}</strong></p>", unsafe_allow_html=True)
    else:
        total_parcelas = 1
        parcela_atual = 1
        valor_parcela = valor_total
    
    submitted = st.form_submit_button("Registrar Compromisso")
    if submitted:
        add_compromisso(
            descricao=descricao,
            valor_total=valor_total,
            valor_parcela=valor_parcela,
            data_vencimento=str(data_vencimento),
            status=status,
            tipo=tipo,
            taxa_juros=taxa_juros,
            total_parcelas=total_parcelas,
            parcela_atual=parcela_atual
        )
        st.markdown("""
        <div class="alert success">
            ✅ Compromisso registrado com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de compromisso
if st.session_state.edit_compromisso_id is not None:
    compromisso = next((c for c in get_compromissos() if c[0] == st.session_state.edit_compromisso_id), None)
    if compromisso:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Compromisso</h3>', unsafe_allow_html=True)
        with st.form("edit_compromisso_form"):
            col1, col2 = st.columns(2)
            with col1:
                nova_descricao = st.text_input("Descrição", value=compromisso[1])
                novo_tipo = st.selectbox("Tipo", ["Dívida", "Parcela", "Financiamento", "Empréstimo", "Outro"], 
                                         index=["Dívida", "Parcela", "Financiamento", "Empréstimo", "Outro"].index(compromisso[6]))
                novo_valor_total = st.number_input("Valor Total", min_value=0.0, value=float(compromisso[2]), format="%.2f")
            with col2:
                nova_data = st.date_input("Data de Vencimento", 
                                         value=datetime.datetime.strptime(compromisso[4], "%Y-%m-%d").date() 
                                         if compromisso[4] else datetime.date.today())
                novo_status = st.selectbox("Status", ["Pendente", "Pago", "Atrasado", "Parcial"], 
                                          index=["Pendente", "Pago", "Atrasado", "Parcial"].index(compromisso[5]) 
                                          if compromisso[5] in ["Pendente", "Pago", "Atrasado", "Parcial"] else 0)
                
                # Campos condicionais baseados no tipo
                if novo_tipo in ["Financiamento", "Empréstimo", "Dívida"]:
                    nova_taxa_juros = st.number_input("Taxa de Juros (%)", min_value=0.0, max_value=100.0, 
                                                     value=float(compromisso[7]), format="%.2f")
                else:
                    nova_taxa_juros = 0.0
                
                # Opção de parcelamento
                is_parcelado = st.checkbox("Parcelado", value=compromisso[8] > 1)
            
            # Campos de parcelamento (aparecem se a opção de parcelamento estiver marcada)
            if is_parcelado:
                col1, col2 = st.columns(2)
                with col1:
                    novo_total_parcelas = st.number_input("Total de Parcelas", min_value=1, value=int(compromisso[8]))
                with col2:
                    novo_parcela_atual = st.number_input("Parcela Atual", min_value=1, max_value=novo_total_parcelas, 
                                                        value=int(compromisso[9]))
                
                # Calcular valor da parcela automaticamente
                novo_valor_parcela = novo_valor_total / novo_total_parcelas if novo_total_parcelas > 0 else novo_valor_total
                st.markdown(f"<p>Valor da Parcela: <strong>{format_currency(novo_valor_parcela)}</strong></p>", unsafe_allow_html=True)
            else:
                novo_total_parcelas = 1
                novo_parcela_atual = 1
                novo_valor_parcela = novo_valor_total
            
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_compromisso(
                    record_id=compromisso[0],
                    descricao=nova_descricao,
                    valor_total=novo_valor_total,
                    valor_parcela=novo_valor_parcela,
                    data_vencimento=str(nova_data),
                    status=novo_status,
                    tipo=novo_tipo,
                    taxa_juros=nova_taxa_juros,
                    total_parcelas=novo_total_parcelas,
                    parcela_atual=novo_parcela_atual
                )
                st.markdown("""
                <div class="alert success">
                    ✅ Compromisso atualizado com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_compromisso_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista e análise de compromissos
compromissos = get_compromissos()
if compromissos:
    st.markdown('<h3 class="section-title">📊 Análise de Compromissos</h3>', unsafe_allow_html=True)
    
    # Métricas principais
    total_compromissos = sum(c[2] for c in compromissos)  # Soma do valor total
    total_parcelas_pendentes = sum(c[3] for c in compromissos if c[5] in ["Pendente", "Atrasado"])  # Soma das parcelas pendentes
    
    # Contagem por tipo
    tipos_count = {}
    for c in compromissos:
        tipo = c[6]
        if tipo in tipos_count:
            tipos_count[tipo] += 1
        else:
            tipos_count[tipo] = 1
    
    # Contagem por status
    status_count = {}
    for c in compromissos:
        status = c[5]
        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1
    
    # Calcular próximo vencimento
    proximos_vencimentos = sorted([
        (c, datetime.datetime.strptime(c[4], "%Y-%m-%d").date()) 
        for c in compromissos 
        if c[5] in ["Pendente", "Atrasado"]
    ], key=lambda x: x[1])
    
    proximo_vencimento = proximos_vencimentos[0] if proximos_vencimentos else None
    
    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total em Compromissos</p>
            <h2 class="metric-value">{format_currency(total_compromissos)}</h2>
            <span class="metric-subtitle">Soma de todos os compromissos</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Parcelas Pendentes</p>
            <h2 class="metric-value">{format_currency(total_parcelas_pendentes)}</h2>
            <span class="metric-subtitle">Valor a pagar</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if proximo_vencimento:
            dias_ate_vencimento = (proximo_vencimento[1] - datetime.date.today()).days
            status_color = {
                'Pendente': COLORS['warning'],
                'Atrasado': COLORS['danger'],
                'Pago': COLORS['success'],
                'Parcial': COLORS['secondary']
            }[proximo_vencimento[0][5]]
            
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Próximo Vencimento</p>
                <h2 class="metric-value" style="color: {status_color};">{proximo_vencimento[0][1]}</h2>
                <span class="metric-subtitle">
                    {format_currency(proximo_vencimento[0][3])} - 
                    {"Vence" if dias_ate_vencimento >= 0 else "Venceu"} {f"em {dias_ate_vencimento} dias" if dias_ate_vencimento >= 0 else f"há {abs(dias_ate_vencimento)} dias"}
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Próximo Vencimento</p>
                <h2 class="metric-value">Nenhum</h2>
                <span class="metric-subtitle">Não há compromissos pendentes</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de compromissos por tipo
        df_tipo = pd.DataFrame([(c[6], c[2]) for c in compromissos], columns=['Tipo', 'Valor'])
        df_tipo = df_tipo.groupby('Tipo').sum().reset_index()
        
        fig_tipo = px.pie(
            df_tipo,
            values='Valor',
            names='Tipo',
            title='Distribuição de Compromissos por Tipo',
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['danger'], COLORS['warning']]
        )
        fig_tipo.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    with col2:
        # Gráfico de compromissos por status
        df_status = pd.DataFrame([(c[5], c[3]) for c in compromissos], columns=['Status', 'Valor'])
        df_status = df_status.groupby('Status').sum().reset_index()
        
        fig_status = px.pie(
            df_status,
            values='Valor',
            names='Status',
            title='Distribuição de Compromissos por Status',
            color_discrete_map={
                'Pendente': COLORS['warning'],
                'Atrasado': COLORS['danger'],
                'Pago': COLORS['success'],
                'Parcial': COLORS['secondary']
            }
        )
        fig_status.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Gráfico de linha temporal
    df_temporal = pd.DataFrame([
        {
            'Data': pd.to_datetime(c[4]),
            'Valor': c[3],
            'Tipo': c[6],
            'Status': c[5]
        } for c in compromissos
    ]).sort_values('Data')
    
    fig_temporal = px.line(
        df_temporal,
        x='Data',
        y='Valor',
        color='Tipo',
        title='Evolução dos Compromissos ao Longo do Tempo',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['danger'], COLORS['warning']]
    )
    fig_temporal.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Filtros para a lista de compromissos
    st.markdown('<h3 class="section-title">📋 Compromissos Registrados</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_tipo = st.multiselect(
            "Filtrar por Tipo",
            options=list(tipos_count.keys()),
            default=list(tipos_count.keys())
        )
    with col2:
        filtro_status = st.multiselect(
            "Filtrar por Status",
            options=list(status_count.keys()),
            default=list(status_count.keys())
        )
    with col3:
        ordenar_por = st.selectbox(
            "Ordenar por",
            options=["Data de Vencimento", "Valor", "Tipo", "Status"]
        )
    
    # Aplicar filtros
    compromissos_filtrados = [
        c for c in compromissos 
        if c[6] in filtro_tipo and c[5] in filtro_status
    ]
    
    # Aplicar ordenação
    if ordenar_por == "Data de Vencimento":
        compromissos_filtrados.sort(key=lambda c: datetime.datetime.strptime(c[4], "%Y-%m-%d").date())
    elif ordenar_por == "Valor":
        compromissos_filtrados.sort(key=lambda c: c[2], reverse=True)
    elif ordenar_por == "Tipo":
        compromissos_filtrados.sort(key=lambda c: c[6])
    elif ordenar_por == "Status":
        compromissos_filtrados.sort(key=lambda c: c[5])
    
    # Lista de compromissos
    if compromissos_filtrados:
        st.markdown('<div class="grid">', unsafe_allow_html=True)
        for compromisso in compromissos_filtrados:
            data_vencimento = datetime.datetime.strptime(compromisso[4], "%Y-%m-%d").date()
            dias_vencimento = (data_vencimento - datetime.date.today()).days
            
            status_color = {
                'Pendente': COLORS['warning'],
                'Atrasado': COLORS['danger'],
                'Pago': COLORS['success'],
                'Parcial': COLORS['secondary']
            }[compromisso[5]]
            
            # Informações de parcelamento
            info_parcela = ""
            if compromisso[8] > 1:
                info_parcela = f"Parcela {compromisso[9]} de {compromisso[8]}"
            
            # Informações de juros
            info_juros = ""
            if compromisso[7] > 0:
                info_juros = f"Taxa de Juros: {compromisso[7]}%"
            
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h3 style="color: {COLORS['text']}; font-size: 1.2rem; margin: 0;">{compromisso[1]}</h3>
                        <span style="background-color: {status_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{compromisso[5]}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <p style="color: {COLORS['text']}; font-size: 1.5rem; margin: 0;">{format_currency(compromisso[3])}</p>
                        <span style="background-color: {COLORS['surface']}; color: {COLORS['text']}; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{compromisso[6]}</span>
                    </div>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 10px;">
                        {"Vence" if dias_vencimento >= 0 else "Venceu"} {f"em {dias_vencimento} dias" if dias_vencimento >= 0 else f"há {abs(dias_vencimento)} dias"} ({compromisso[4]})
                    </p>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                        {info_parcela}
                        {f"<br>{info_juros}" if info_juros else ""}
                    </p>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button class="stButton" onclick="document.querySelector('#edit_compromisso_{compromisso[0]}').click()">✏️ Editar</button>
                        <button class="stButton" onclick="document.querySelector('#delete_compromisso_{compromisso[0]}').click()">🗑️ Excluir</button>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botões ocultos para funcionalidade
            if st.button("✏️", key=f"edit_compromisso_{compromisso[0]}", help="Editar compromisso"):
                st.session_state.edit_compromisso_id = compromisso[0]
                rerun()
            if st.button("🗑️", key=f"delete_compromisso_{compromisso[0]}", help="Excluir compromisso"):
                delete_compromisso(compromisso[0])
                st.markdown("""
                <div class="alert success">
                    ✅ Compromisso excluído com sucesso!
                </div>
                """, unsafe_allow_html=True)
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert">
            ℹ️ Nenhum compromisso encontrado com os filtros selecionados.
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhum compromisso registrado. Adicione seus compromissos financeiros para melhor controle.
    </div>
    """, unsafe_allow_html=True)
