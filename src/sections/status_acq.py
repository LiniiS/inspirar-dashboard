import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from utils.colors import CHART_COLORS, METRIC_COLORS

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
                        acq_detalhes_pacientes.append({
                            'Patient ID': paciente.get('id', 'N/A'),
                            'Age': paciente.get('age', 'N/A'),
                            'Sex': paciente.get('sex', 'N/A'),
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
        st.subheader('Asthma Control Status (ACQ) - First Week')
        st.info('Analysis of ACQ (Asthma Control Questionnaire) considering only the **first temporal completion** of each patient (ordered by creation/answer date). This provides a more accurate view of initial asthma control, ensuring consistency for medical analysis.')
        
        # Métricas de engajamento
        st.markdown('### ACQ Engagement Metrics')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Patients", total_pacientes)
        col2.metric("With ACQ", pacientes_com_acq)
        col3.metric("Without ACQ", pacientes_sem_acq)
        col4.metric("Completion Rate", f"{taxa_preenchimento:.1f}%")
        
        # Criar DataFrame para análise
        df_acq = pd.DataFrame({
            'score': acq_primeira_semana,
            'status': acq_status_primeira_semana
        })
        
        # Estatísticas descritivas
        st.markdown('These statistics summarize the asthmatic condition recorded in the **first ACQ questionnaire** completed by each patient, in the **first week after account creation**. They reflect the initial state of asthma control, before any follow-up effects.')
        col1, col2, col3, col4 = st.columns(4)
        
        valores_validos = df_acq['score'].dropna()
        col1.metric('Mean', f'{valores_validos.mean():.2f}')
        col2.metric('Std Deviation', f'{valores_validos.std():.2f}')
        col3.metric('Median', f'{valores_validos.median():.2f}')
        col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
        
        st.markdown('### Visualizations - First Week')
        col1, col2 = st.columns(2)
        
        with col1:
            fig_box = px.box(
                df_acq, 
                y='score', 
                points='all', 
                title="ACQ Scores Distribution",
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_box.update_layout(
                yaxis_title="ACQ Score",
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
                    title="Asthma Control Status",
                    color_discrete_sequence=CHART_COLORS[:len(status_counts)]
                )
                fig_pie.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig_pie, use_container_width=True, height=400)
        
        # Tabela detalhada dos pacientes
        st.markdown('### Patient Details - First ACQ')
        st.info('Table with details of the first ACQ completion of each patient, including age, sex, date, score and control status.')
        
        if acq_detalhes_pacientes:
            # Criar DataFrame para a tabela
            df_detalhes = pd.DataFrame(acq_detalhes_pacientes)
            
            # Ordenar por data do primeiro ACQ
            df_detalhes['First ACQ Date'] = pd.to_datetime(df_detalhes['First ACQ Date'], errors='coerce')
            df_detalhes = df_detalhes.sort_values('First ACQ Date', ascending=True)
            
            # Formatar a data para exibição
            df_detalhes['First ACQ Date'] = df_detalhes['First ACQ Date'].dt.strftime('%d/%m/%Y %H:%M')
            
            # Filtros para a tabela
            st.markdown('#### Table Filters')
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Filtro por status
                status_options = ['All'] + list(df_detalhes['Status'].unique())
                status_filtro = st.selectbox('Status:', status_options)
            
            with col2:
                # Filtro por sexo
                sexo_options = ['All'] + list(df_detalhes['Sex'].unique())
                sexo_filtro = st.selectbox('Sex:', sexo_options)
            
            with col3:
                # Filtro por score mínimo
                score_min = st.number_input('Min Score:', min_value=0.0, max_value=6.0, value=0.0, step=0.1)
            
            with col4:
                # Filtro por score máximo
                score_max = st.number_input('Max Score:', min_value=0.0, max_value=6.0, value=6.0, step=0.1)
            
            # Aplicar filtros
            df_filtrado = df_detalhes.copy()
            
            if status_filtro != 'All':
                df_filtrado = df_filtrado[df_filtrado['Status'] == status_filtro]
            
            if sexo_filtro != 'All':
                df_filtrado = df_filtrado[df_filtrado['Sex'] == sexo_filtro]
            
            # Converter Score ACQ para float para filtro
            df_filtrado['ACQ Score'] = pd.to_numeric(df_filtrado['ACQ Score'], errors='coerce')
            df_filtrado = df_filtrado[
                (df_filtrado['ACQ Score'] >= score_min) & 
                (df_filtrado['ACQ Score'] <= score_max)
            ]
            
            st.markdown(f"**Filtered patients: {len(df_filtrado)} of {len(df_detalhes)}**")
            
            # Exibir tabela
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                column_config={
                    "Patient ID": st.column_config.TextColumn("Patient ID", width="medium"),
                    "Age": st.column_config.NumberColumn("Age", width="small"),
                    "Sex": st.column_config.TextColumn("Sex", width="small"),
                    "First ACQ Date": st.column_config.TextColumn("First ACQ Date", width="medium"),
                    "ACQ Score": st.column_config.NumberColumn("ACQ Score", format="%.2f", width="small"),
                    "Status": st.column_config.TextColumn("Status", width="small"),
                    "Total ACQs": st.column_config.NumberColumn("Total ACQs", width="small")
                }
            )
            
            # Resumo da tabela
            st.markdown(f"**Total patients with valid ACQ in table: {len(df_filtrado)}**")
            
            # Botão de download da tabela (dados filtrados)
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Table (CSV)",
                data=csv,
                file_name=f"acq_primeira_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download table with details of the first ACQ of each patient"
            )
    else:
        st.subheader('Asthma Control Status (ACQ)')
        st.warning('No ACQ records found for the first week of patients in the selected period.')
    
    st.markdown('---') 