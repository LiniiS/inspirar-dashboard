import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from utils.colors import CHART_COLORS, METRIC_COLORS
from utils.translations import t

def mostrar_status_acq(pacientes_recorte):
    # Coletar apenas a primeira semana de ACQ de cada paciente
    acq_primeira_semana = []
    acq_status_primeira_semana = []
    acq_detalhes_pacientes = []  # Lista para armazenar detalhes de cada paciente
    
    # Contadores para taxa de preenchimento
    total_pacientes = len(pacientes_recorte)
    pacientes_com_acq = 0
    pacientes_sem_acq = 0
    
    for paciente in pacientes_recorte:
        acqs = paciente.get('acqs', [])
        if acqs and len(acqs) > 0:
            pacientes_com_acq += 1
            # Ordenar ACQs por data para garantir que pegamos o primeiro temporal
            acqs_ordenados = sorted(
                acqs,
                key=lambda a: a.get('createdAt') or a.get('answeredAt') or a.get('date') or '',
                reverse=False  # False para ordem cronológica (mais antigo primeiro)
            )
            primeiro_acq = acqs_ordenados[0]
            
            # Validar e converter o score para float
            media = primeiro_acq.get('average')
            if media is not None:
                try:
                    score_float = float(media)
                    # Validar se está na faixa esperada (0-6 para ACQ)
                    if 0 <= score_float <= 6:
                        acq_primeira_semana.append(score_float)
                        # Normalizar o status para consistência
                        status = str(primeiro_acq.get('controlStatus', 'N/A')).strip()
                        if status and status != 'N/A':
                            acq_status_primeira_semana.append(status)
                        else:
                            acq_status_primeira_semana.append('N/A')
                        
                        # Armazenar detalhes do paciente para a tabela
                        data_primeiro_acq = primeiro_acq.get('createdAt') or primeiro_acq.get('answeredAt') or primeiro_acq.get('date') or 'N/A'
                        # Mapear gender para exibição
                        gender_raw = paciente.get('gender', '')
                        gender_display = t('sections.ativos.male') if gender_raw == 'male' else t('sections.ativos.female') if gender_raw == 'female' else gender_raw
                        acq_detalhes_pacientes.append({
                            'Patient ID': paciente.get('id', 'N/A'),
                            'Age': paciente.get('age', 'N/A'),
                            'Gender': gender_display,
                            'First ACQ Date': data_primeiro_acq,
                            'ACQ Score': f"{score_float:.2f}",
                            'Status': status,
                            'Total ACQs': len(acqs)
                        })
                except (TypeError, ValueError):
                    # Se não conseguir converter para float, pular este ACQ
                    continue
        else:
            pacientes_sem_acq += 1
    
    # Calcular taxa de preenchimento
    taxa_preenchimento = (pacientes_com_acq / total_pacientes * 100) if total_pacientes > 0 else 0
    
    if acq_primeira_semana:
        st.subheader(t('sections.status_acq.title'))
        st.info(t('sections.status_acq.description'))
        
        # Métricas de engajamento
        st.markdown(f"### {t('sections.status_acq.engagement_metrics')}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(t('sections.status_acq.total_patients'), total_pacientes)
        col2.metric(t('sections.status_acq.with_acq'), pacientes_com_acq)
        col3.metric(t('sections.status_acq.without_acq'), pacientes_sem_acq)
        col4.metric(t('sections.status_acq.completion_rate'), f"{taxa_preenchimento:.1f}%")
        
        # Criar DataFrame para análise
        df_acq = pd.DataFrame({
            'score': acq_primeira_semana,
            'status': acq_status_primeira_semana
        })
        
        # Estatísticas descritivas
        st.markdown(t('sections.status_acq.statistics_description'))
        col1, col2, col3, col4 = st.columns(4)
        
        valores_validos = df_acq['score'].dropna()
        col1.metric(t('sections.status_acq.mean'), f'{valores_validos.mean():.2f}')
        col2.metric(t('sections.status_acq.std_deviation'), f'{valores_validos.std():.2f}')
        col3.metric(t('sections.status_acq.median'), f'{valores_validos.median():.2f}')
        col4.metric(t('sections.status_acq.iqr'), f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
        
        st.markdown(f"### {t('sections.status_acq.visualizations')}")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_box = px.box(
                df_acq, 
                y='score', 
                points='all', 
                title=t('charts.titles.acq_scores_distribution'),
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_box.update_layout(
                yaxis_title=t('charts.labels.acq_score'),
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_box, use_container_width=True, height=400)
        
        with col2:
            # Filtrar apenas status válidos para o gráfico de pizza
            df_status_valido = df_acq[df_acq['status'] != 'N/A']
            status_counts = df_status_valido['status'].value_counts()
            
            if len(status_counts) > 0:
                fig_pie = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title=t('charts.titles.control_status'),
                    color_discrete_sequence=CHART_COLORS[:len(status_counts)]
                )
                fig_pie.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig_pie, use_container_width=True, height=400)
        
        # Tabela detalhada dos pacientes
        st.markdown(f"### {t('sections.status_acq.patient_details')}")
        st.info(t('sections.status_acq.patient_details_info'))
        
        if acq_detalhes_pacientes:
            # Criar DataFrame para a tabela
            df_detalhes = pd.DataFrame(acq_detalhes_pacientes)
            
            # Ordenar por data do primeiro ACQ
            df_detalhes['First ACQ Date'] = pd.to_datetime(df_detalhes['First ACQ Date'], errors='coerce')
            df_detalhes = df_detalhes.sort_values('First ACQ Date', ascending=True)
            
            # Formatar a data para exibição
            df_detalhes['First ACQ Date'] = df_detalhes['First ACQ Date'].dt.strftime('%d/%m/%Y %H:%M')
            
            # Filtros para a tabela
            st.markdown(f"#### {t('sections.status_acq.table_filters')}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Filtro por status
                status_options = [t('sections.status_acq.all')] + list(df_detalhes['Status'].unique())
                status_filtro = st.selectbox(f"{t('sections.status_acq.status')}:", status_options)
            
            with col2:
                # Filtro por gênero
                gender_options = [t('sections.status_acq.all')] + list(df_detalhes['Gender'].unique())
                gender_filtro = st.selectbox(f"{t('sections.status_acq.sex')}:", gender_options)
            
            with col3:
                # Filtro por score mínimo
                score_min = st.number_input(f"{t('sections.status_acq.min_score')}:", min_value=0.0, max_value=6.0, value=0.0, step=0.1)
            
            with col4:
                # Filtro por score máximo
                score_max = st.number_input(f"{t('sections.status_acq.max_score')}:", min_value=0.0, max_value=6.0, value=6.0, step=0.1)
            
            # Aplicar filtros
            df_filtrado = df_detalhes.copy()
            
            if status_filtro != t('sections.status_acq.all'):
                df_filtrado = df_filtrado[df_filtrado['Status'] == status_filtro]
            
            if gender_filtro != t('sections.status_acq.all'):
                df_filtrado = df_filtrado[df_filtrado['Gender'] == gender_filtro]
            
            # Converter Score ACQ para float para filtro
            df_filtrado['ACQ Score'] = pd.to_numeric(df_filtrado['ACQ Score'], errors='coerce')
            df_filtrado = df_filtrado[
                (df_filtrado['ACQ Score'] >= score_min) & 
                (df_filtrado['ACQ Score'] <= score_max)
            ]
            
            st.markdown(f"**{t('sections.status_acq.filtered_patients', filtered=len(df_filtrado), total=len(df_detalhes))}**")
            
            # Exibir tabela
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                column_config={
                    "Patient ID": st.column_config.TextColumn(t('tables.patient_id'), width="medium"),
                    "Age": st.column_config.NumberColumn(t('tables.age'), width="small"),
                    "Gender": st.column_config.TextColumn(t('tables.sex'), width="small"),
                    "First ACQ Date": st.column_config.TextColumn(t('tables.first_acq_date'), width="medium"),
                    "ACQ Score": st.column_config.NumberColumn(t('tables.acq_score'), format="%.2f", width="small"),
                    "Status": st.column_config.TextColumn(t('tables.status'), width="small"),
                    "Total ACQs": st.column_config.NumberColumn(t('tables.total_acqs'), width="small")
                }
            )
            
            # Resumo da tabela
            st.markdown(f"**{t('sections.status_acq.total_with_valid_acq', total=len(df_filtrado))}**")
            
            # Botão de download da tabela (dados filtrados)
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.status_acq.download_table'),
                data=csv,
                file_name=f"acq_primeira_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help=t('sections.status_acq.download_help')
            )
    else:
        st.subheader(t('sections.status_acq.title_no_data'))
        st.warning(t('sections.status_acq.no_data'))
    
    st.markdown('---') 