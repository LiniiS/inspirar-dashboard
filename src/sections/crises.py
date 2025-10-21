import streamlit as st
import pandas as pd
from dateutil import parser
from collections import Counter
import plotly.express as px
import numpy as np
from utils.colors import CHART_COLORS

def mostrar_crises(pacientes_recorte):
    st.info('Análise abrangente das crises de asma: períodos de duração, medicamentos utilizados durante as crises e distribuição por sexo.')
    
    # Análise geral de crises
    total_crises = sum([len(p.get('crisis', [])) for p in pacientes_recorte])
    total_pacientes = len(pacientes_recorte)
    total_pacientes_com_crise = sum([1 for p in pacientes_recorte if len(p.get('crisis', [])) > 0])
    taxa_pacientes_crise = (total_pacientes_com_crise / total_pacientes * 100) if total_pacientes > 0 else 0
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Crises", total_crises)
    col2.metric("Pacientes com Crise", total_pacientes_com_crise)
    col3.metric("Taxa de Incidência", f"{taxa_pacientes_crise:.1f}%")
    
    if total_pacientes_com_crise > 0:
        media_crises_por_paciente = total_crises / total_pacientes_com_crise
        col4.metric("Média Crises/Paciente", f"{media_crises_por_paciente:.1f}")
    else:
        col4.metric("Média Crises/Paciente", "0")
    
    if total_crises == 0:
        st.warning("Não há dados de crises registradas no período analisado.")
        st.markdown('---')
        return
    
    # Processamento detalhado das crises
    dados_crises = []
    medicamentos_crises = []
    
    for paciente in pacientes_recorte:
        sexo_paciente = paciente.get('sex', 'I')
        idade_paciente = paciente.get('age', 0)
        
        for crise in paciente.get('crisis', []):
            try:
                # Calcular duração da crise
                ini = parser.parse(crise.get('initialUsageDate'))
                fim = parser.parse(crise.get('finalUsageDate'))
                duracao = (fim - ini).days
                
                # Dados da crise
                dados_crises.append({
                    'paciente_id': paciente.get('id', 'N/A'),
                    'sexo': sexo_paciente,
                    'idade': idade_paciente,
                    'duracao': duracao,
                    'data_inicio': ini,
                    'data_fim': fim
                })
                
                # Medicamentos utilizados durante a crise
                medicamentos = crise.get('medications', [])
                for med in medicamentos:
                    nome_med = med.get('name', 'Medicamento não especificado')
                    medicamentos_crises.append({
                        'paciente_id': paciente.get('id', 'N/A'),
                        'sexo': sexo_paciente,
                        'duracao_crise': duracao,
                        'medicamento': nome_med
                    })
            except Exception as e:
                continue
    
    if not dados_crises:
        st.warning("Não foi possível processar os dados de crises.")
        st.markdown('---')
        return
    
    df_crises = pd.DataFrame(dados_crises)
    df_medicamentos = pd.DataFrame(medicamentos_crises) if medicamentos_crises else pd.DataFrame()
    
    # --- SEÇÃO 1: Distribuição por Duração ---
    st.markdown("---")
    st.subheader('Distribuição de Crises por Duração')
    
    # Definir faixas de duração
    bins = [-1, 2, 5, 10, 15, 30, float('inf')]
    labels = ['1-2 dias', '3-5 dias', '6-10 dias', '11-15 dias', '16-30 dias', 'Mais de 30 dias']
    df_crises['faixa_duracao'] = pd.cut(df_crises['duracao'], bins=bins, labels=labels)
    
    col_grafico1, col_stats1 = st.columns([2, 1])
    
    with col_grafico1:
        # Gráfico de distribuição por duração
        faixas_count = df_crises['faixa_duracao'].value_counts().reindex(labels, fill_value=0)
        
        fig_duracao = px.bar(
            x=faixas_count.values,
            y=faixas_count.index,
            orientation='h',
            title='Número de Crises por Faixa de Duração',
            labels={'x': 'Número de Crises', 'y': 'Duração'},
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_duracao.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Número de Crises",
            yaxis_title="Faixa de Duração"
        )
        st.plotly_chart(fig_duracao, use_container_width=True, height=400)
    
    with col_stats1:
        st.markdown("**Estatísticas de Duração:**")
        
        duracao_media = df_crises['duracao'].mean()
        duracao_mediana = df_crises['duracao'].median()
        duracao_max = df_crises['duracao'].max()
        duracao_min = df_crises['duracao'].min()
        
        st.metric("Duração Média", f"{duracao_media:.1f} dias")
        st.metric("Mediana", f"{duracao_mediana:.0f} dias")
        st.metric("Duração Máxima", f"{duracao_max} dias")
        st.metric("Duração Mínima", f"{duracao_min} dias")
        
        st.markdown("**Distribuição por Faixa:**")
        for faixa, count in faixas_count.items():
            perc = (count / len(df_crises)) * 100
            st.markdown(f"• **{faixa}:** {count} ({perc:.1f}%)")
    
    # --- SEÇÃO 2: Análise por Sexo ---
    st.markdown("---")
    st.subheader('Análise de Crises por Sexo')
    
    # Filtrar dados para excluir sexo indefinido
    df_crises_sexo = df_crises[df_crises['sexo'].isin(['M', 'F'])].copy()
    
    if not df_crises_sexo.empty:
        # Mapear códigos para nomes
        df_crises_sexo['Sexo'] = df_crises_sexo['sexo'].map({
            'M': 'Masculino',
            'F': 'Feminino'
        })
        
        col_sexo_grafico, col_sexo_stats = st.columns([2, 1])
        
        with col_sexo_grafico:
            # Gráfico de crises por sexo e faixa de duração
            crises_sexo_duracao = df_crises_sexo.groupby(['Sexo', 'faixa_duracao'], observed=True).size().reset_index(name='count')
            
            fig_sexo_duracao = px.bar(
                crises_sexo_duracao,
                x='faixa_duracao',
                y='count',
                color='Sexo',
                title='Distribuição de Crises por Sexo e Duração',
                labels={'count': 'Número de Crises', 'faixa_duracao': 'Faixa de Duração'},
                color_discrete_sequence=[CHART_COLORS[2], CHART_COLORS[3]],
                barmode='group'
            )
            fig_sexo_duracao.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Faixa de Duração",
                yaxis_title="Número de Crises",
                legend_title="Sexo",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_sexo_duracao, use_container_width=True, height=400)
        
        with col_sexo_stats:
            st.markdown("**Estatísticas por Sexo:**")
            
            # Análise por sexo
            for sexo in ['Masculino', 'Feminino']:
                dados_sexo = df_crises_sexo[df_crises_sexo['Sexo'] == sexo]
                
                if not dados_sexo.empty:
                    num_crises = len(dados_sexo)
                    duracao_media_sexo = dados_sexo['duracao'].mean()
                    
                    st.markdown(f"**{sexo}:**")
                    st.markdown(f"• Crises: {num_crises}")
                    st.markdown(f"• Duração média: {duracao_media_sexo:.1f} dias")
                    
                    # Pacientes únicos por sexo
                    pacientes_unicos = dados_sexo['paciente_id'].nunique()
                    st.markdown(f"• Pacientes: {pacientes_unicos}")
                    st.markdown("---")
            
            # Comparação geral
            st.markdown("**Comparação:**")
            crises_masc = len(df_crises_sexo[df_crises_sexo['Sexo'] == 'Masculino'])
            crises_fem = len(df_crises_sexo[df_crises_sexo['Sexo'] == 'Feminino'])
            total_crises_sexo = crises_masc + crises_fem
            
            if total_crises_sexo > 0:
                perc_masc = (crises_masc / total_crises_sexo) * 100
                perc_fem = (crises_fem / total_crises_sexo) * 100
                st.markdown(f"• **M/F:** {perc_masc:.1f}% / {perc_fem:.1f}%")
        
        # Nota sobre dados indefinidos
        crises_indefinidas = len(df_crises[df_crises['sexo'] == 'I'])
        if crises_indefinidas > 0:
            st.info(f"**Nota:** {crises_indefinidas} crise(s) de pacientes com sexo indefinido não aparecem na análise por sexo devido à política de exclusão de dados pessoais.")
    
    else:
        st.warning("Não há dados de crises com sexo definido para análise comparativa.")
    
    # --- SEÇÃO 3: Tabela Detalhada ---
    st.markdown("---")
    st.subheader('Dados Detalhados das Crises')
    
    # Preparar dados para exibição
    df_exibicao = df_crises.copy()
    df_exibicao['Sexo'] = df_exibicao['sexo'].map({'M': 'Masculino', 'F': 'Feminino', 'I': 'Indefinido'})
    df_exibicao['Data Início'] = df_exibicao['data_inicio'].dt.strftime('%d/%m/%Y')
    df_exibicao['Data Fim'] = df_exibicao['data_fim'].dt.strftime('%d/%m/%Y')
    df_exibicao = df_exibicao[['paciente_id', 'Sexo', 'idade', 'duracao', 'Data Início', 'Data Fim', 'faixa_duracao']]
    df_exibicao = df_exibicao.rename(columns={
        'paciente_id': 'ID Paciente',
        'idade': 'Idade',
        'duracao': 'Duração (dias)',
        'faixa_duracao': 'Faixa de Duração'
    })
    
    st.dataframe(
        df_exibicao,
        use_container_width=True,
        column_config={
            "ID Paciente": st.column_config.TextColumn("ID Paciente", width="medium"),
            "Sexo": st.column_config.TextColumn("Sexo", width="small"),
            "Idade": st.column_config.NumberColumn("Idade", width="small"),
            "Duração (dias)": st.column_config.NumberColumn("Duração (dias)", width="small"),
            "Data Início": st.column_config.TextColumn("Data Início", width="medium"),
            "Data Fim": st.column_config.TextColumn("Data Fim", width="medium"),
            "Faixa de Duração": st.column_config.TextColumn("Faixa de Duração", width="medium")
        }
    )
    
    # Download dos dados completos
    csv_crises = df_exibicao.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Download Dados Completos (CSV)",
        data=csv_crises,
        file_name=f"crises_detalhadas_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.markdown('---') 