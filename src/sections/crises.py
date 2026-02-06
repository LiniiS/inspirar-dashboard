import streamlit as st
import pandas as pd
from dateutil import parser
from collections import Counter
import plotly.express as px
import numpy as np
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_crises(pacientes_recorte):
    st.info(t('sections.crises.description'))
    
    # Análise geral de crises
    total_crises = sum([len(p.get('crisis', [])) for p in pacientes_recorte])
    total_pacientes = len(pacientes_recorte)
    total_pacientes_com_crise = sum([1 for p in pacientes_recorte if len(p.get('crisis', [])) > 0])
    taxa_pacientes_crise = (total_pacientes_com_crise / total_pacientes * 100) if total_pacientes > 0 else 0
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t('sections.crises.total_crises'), total_crises)
    col2.metric(t('sections.crises.patients_with_crisis'), total_pacientes_com_crise)
    col3.metric(t('sections.crises.incidence_rate'), f"{taxa_pacientes_crise:.1f}%")
    
    if total_pacientes_com_crise > 0:
        media_crises_por_paciente = total_crises / total_pacientes_com_crise
        col4.metric(t('sections.crises.average_crises_patient'), f"{media_crises_por_paciente:.1f}")
    else:
        col4.metric(t('sections.crises.average_crises_patient'), "0")
    
    if total_crises == 0:
        st.warning(t('sections.crises.no_crisis_data'))
        st.markdown('---')
        return
    
    # Processamento detalhado das crises
    dados_crises = []
    medicamentos_crises = []
    
    for paciente in pacientes_recorte:
        gender_paciente = paciente.get('gender', '')
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
                    'gender': gender_paciente,
                    'idade': idade_paciente,
                    'duracao': duracao,
                    'data_inicio': ini,
                    'data_fim': fim
                })
                
                # Medicamentos utilizados durante a crise
                medicamentos = crise.get('medications', [])
                for med in medicamentos:
                    nome_med = med.get('name', 'Unspecified medication')
                    medicamentos_crises.append({
                        'paciente_id': paciente.get('id', 'N/A'),
                        'gender': gender_paciente,
                        'duracao_crise': duracao,
                        'medicamento': nome_med
                    })
            except Exception as e:
                continue
    
    if not dados_crises:
        st.warning(t('sections.crises.unable_to_process'))
        st.markdown('---')
        return
    
    df_crises = pd.DataFrame(dados_crises)
    df_medicamentos = pd.DataFrame(medicamentos_crises) if medicamentos_crises else pd.DataFrame()
    
    # --- SEÇÃO 1: Distribuição por Duração ---
    st.markdown("---")
    st.subheader(t('sections.crises.distribution_by_duration'))
    
    # Definir faixas de duração
    bins = [-1, 2, 5, 10, 15, 30, float('inf')]
    labels = [
        t('sections.crises.duration_ranges.1_2'),
        t('sections.crises.duration_ranges.3_5'),
        t('sections.crises.duration_ranges.6_10'),
        t('sections.crises.duration_ranges.11_15'),
        t('sections.crises.duration_ranges.16_30'),
        t('sections.crises.duration_ranges.more_30')
    ]
    df_crises['faixa_duracao'] = pd.cut(df_crises['duracao'], bins=bins, labels=labels)
    
    col_grafico1, col_stats1 = st.columns([2, 1])
    
    with col_grafico1:
        # Gráfico de distribuição por duração
        faixas_count = df_crises['faixa_duracao'].value_counts().reindex(labels, fill_value=0)
        
        fig_duracao = px.bar(
            x=faixas_count.values,
            y=faixas_count.index,
            orientation='h',
            title=t('charts.titles.crises_by_duration'),
            labels={'x': t('charts.labels.number_of_crises'), 'y': t('charts.labels.duration')},
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_duracao.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('charts.labels.number_of_crises'),
            yaxis_title=t('charts.labels.duration_range')
        )
        st.plotly_chart(fig_duracao, use_container_width=True, height=400)
    
    with col_stats1:
        st.markdown(f"**{t('sections.crises.duration_statistics')}**")
        
        duracao_media = df_crises['duracao'].mean()
        duracao_mediana = df_crises['duracao'].median()
        duracao_max = df_crises['duracao'].max()
        duracao_min = df_crises['duracao'].min()
        
        st.metric(t('sections.crises.average_duration'), f"{duracao_media:.1f} {t('sections.crises.days')}")
        st.metric(t('sections.crises.median'), f"{duracao_mediana:.0f} {t('sections.crises.days')}")
        st.metric(t('sections.crises.maximum_duration'), f"{duracao_max} {t('sections.crises.days')}")
        st.metric(t('sections.crises.minimum_duration'), f"{duracao_min} {t('sections.crises.days')}")
        
        st.markdown(f"**{t('sections.crises.distribution_by_range')}**")
        for faixa, count in faixas_count.items():
            perc = (count / len(df_crises)) * 100
            st.markdown(f"• **{faixa}:** {count} ({perc:.1f}%)")
    
    # --- SEÇÃO 2: Análise por Sexo ---
    st.markdown("---")
    st.subheader(t('sections.crises.analysis_by_sex'))
    
    # Copiar dados para análise por gênero
    df_crises_gender = df_crises.copy()
    
    if not df_crises_gender.empty:
        # Mapear códigos para nomes
        df_crises_gender['Sexo'] = df_crises_gender['gender'].map({
            'male': t('sections.ativos.male'),
            'female': t('sections.ativos.female')
        })
        
        col_sexo_grafico, col_sexo_stats = st.columns([2, 1])
        
        with col_sexo_grafico:
            # Gráfico de crises por sexo e faixa de duração
            crises_sexo_duracao = df_crises_gender.groupby(['Sexo', 'faixa_duracao'], observed=True).size().reset_index(name='count')
            
            fig_sexo_duracao = px.bar(
                crises_sexo_duracao,
                x='faixa_duracao',
                y='count',
                color='Sexo',
                title=t('charts.titles.crises_by_sex_duration'),
                labels={'count': t('charts.labels.number_of_crises'), 'faixa_duracao': t('charts.labels.duration_range')},
                color_discrete_sequence=[CHART_COLORS[2], CHART_COLORS[3]],
                barmode='group'
            )
            fig_sexo_duracao.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title=t('charts.labels.duration_range'),
                yaxis_title=t('charts.labels.number_of_crises'),
                legend_title=t('tables.sex'),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_sexo_duracao, use_container_width=True, height=400)
        
        with col_sexo_stats:
            st.markdown(f"**{t('sections.crises.statistics_by_sex')}**")
            
            # Análise por sexo
            for sexo_key in [t('sections.ativos.male'), t('sections.ativos.female')]:
                dados_sexo = df_crises_gender[df_crises_gender['Sexo'] == sexo_key]
                
                if not dados_sexo.empty:
                    num_crises = len(dados_sexo)
                    duracao_media_sexo = dados_sexo['duracao'].mean()
                    
                    st.markdown(f"**{sexo_key}:**")
                    st.markdown(f"• {t('sections.crises.crises')}: {num_crises}")
                    st.markdown(f"• {t('sections.crises.average_duration_sex')}: {duracao_media_sexo:.1f} {t('sections.crises.days')}")
                    
                    # Pacientes únicos por sexo
                    pacientes_unicos = dados_sexo['paciente_id'].nunique()
                    st.markdown(f"• {t('sections.crises.patients')}: {pacientes_unicos}")
                    st.markdown("---")
            
            # Comparação geral
            st.markdown(f"**{t('sections.crises.comparison')}**")
            crises_masc = len(df_crises_gender[df_crises_gender['Sexo'] == t('sections.ativos.male')])
            crises_fem = len(df_crises_gender[df_crises_gender['Sexo'] == t('sections.ativos.female')])
            total_crises_sexo = crises_masc + crises_fem
            
            if total_crises_sexo > 0:
                perc_masc = (crises_masc / total_crises_sexo) * 100
                perc_fem = (crises_fem / total_crises_sexo) * 100
                st.markdown(f"• **M/F:** {perc_masc:.1f}% / {perc_fem:.1f}%")
    
    else:
        st.warning(t('sections.crises.no_crisis_sex'))
    
    # --- SEÇÃO 3: Tabela Detalhada ---
    st.markdown("---")
    st.subheader(t('sections.crises.detailed_data'))
    
    # Preparar dados para exibição
    df_exibicao = df_crises.copy()
    df_exibicao['Sexo'] = df_exibicao['gender'].map({
        'male': t('sections.ativos.male'),
        'female': t('sections.ativos.female')
    })
    df_exibicao['Data Início'] = df_exibicao['data_inicio'].dt.strftime('%d/%m/%Y')
    df_exibicao['Data Fim'] = df_exibicao['data_fim'].dt.strftime('%d/%m/%Y')
    df_exibicao = df_exibicao[['paciente_id', 'Sexo', 'idade', 'duracao', 'Data Início', 'Data Fim', 'faixa_duracao']]
    df_exibicao = df_exibicao.rename(columns={
        'paciente_id': t('tables.patient_id'),
        'idade': t('tables.age'),
        'duracao': t('tables.duration_days'),
        'faixa_duracao': t('tables.duration_range'),
        'Data Início': t('tables.start_date'),
        'Data Fim': t('tables.end_date'),
        'Sexo': t('tables.sex')
    })
    
    st.dataframe(
        df_exibicao,
        use_container_width=True,
        column_config={
            t('tables.patient_id'): st.column_config.TextColumn(t('tables.patient_id'), width="medium"),
            t('tables.sex'): st.column_config.TextColumn(t('tables.sex'), width="small"),
            t('tables.age'): st.column_config.NumberColumn(t('tables.age'), width="small"),
            t('tables.duration_days'): st.column_config.NumberColumn(t('tables.duration_days'), width="small"),
            t('tables.start_date'): st.column_config.TextColumn(t('tables.start_date'), width="medium"),
            t('tables.end_date'): st.column_config.TextColumn(t('tables.end_date'), width="medium"),
            t('tables.duration_range'): st.column_config.TextColumn(t('tables.duration_range'), width="medium")
        }
    )
    
    # Download dos dados completos
    csv_crises = df_exibicao.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label=t('sections.crises.download_complete'),
        data=csv_crises,
        file_name=f"crises_detalhadas_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.markdown('---') 