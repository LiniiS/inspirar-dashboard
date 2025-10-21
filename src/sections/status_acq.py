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
                            'ID do Paciente': paciente.get('id', 'N/A'),
                            'Idade': paciente.get('age', 'N/A'),
                            'Sexo': paciente.get('sex', 'N/A'),
                            'Data do Primeiro ACQ': data_primeiro_acq,
                            'Score ACQ': f"{score_float:.2f}",
                            'Status': status,
                            'Total de ACQs': len(acqs)
                        })
                except (TypeError, ValueError):
                    # Se não conseguir converter para float, pular este ACQ
                    continue
        else:
            pacientes_sem_acq += 1
    
    # Calcular taxa de preenchimento
    taxa_preenchimento = (pacientes_com_acq / total_pacientes * 100) if total_pacientes > 0 else 0
    
    if acq_primeira_semana:
        st.subheader('Status de Controle da Asma (ACQ) - Primeira Semana')
        st.info('Análise do ACQ (Asthma Control Questionnaire) considerando apenas o **primeiro preenchimento temporal** de cada paciente (ordenado por data de criação/resposta). Isso fornece uma visão mais precisa do controle inicial da asma, garantindo consistência para análise médica.')
        
        # Métricas de engajamento
        st.markdown('### Métricas de Engajamento com ACQ')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Pacientes", total_pacientes)
        col2.metric("Com ACQ", pacientes_com_acq)
        col3.metric("Sem ACQ", pacientes_sem_acq)
        col4.metric("Taxa de Preenchimento", f"{taxa_preenchimento:.1f}%")
        
        # Criar DataFrame para análise
        df_acq = pd.DataFrame({
            'score': acq_primeira_semana,
            'status': acq_status_primeira_semana
        })
        
        # Estatísticas descritivas
        st.markdown('Estas estatísticas resumem a condição asmática registrada no **primeiro questionário ACQ** preenchido por cada paciente, na **primeira semana após a criação da conta**. Elas refletem o estado inicial do controle da asma, antes de quaisquer efeitos de acompanhamento.')
        col1, col2, col3, col4 = st.columns(4)
        
        valores_validos = df_acq['score'].dropna()
        col1.metric('Média', f'{valores_validos.mean():.2f}')
        col2.metric('Desvio Padrão', f'{valores_validos.std():.2f}')
        col3.metric('Mediana', f'{valores_validos.median():.2f}')
        col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
        
        st.markdown('### Visualizações - Primeira Semana')
        col1, col2 = st.columns(2)
        
        with col1:
            fig_box = px.box(
                df_acq, 
                y='score', 
                points='all', 
                title="Distribuição dos Scores ACQ",
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_box.update_layout(
                yaxis_title="Score ACQ",
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
                    title="Status de Controle da Asma",
                    color_discrete_sequence=CHART_COLORS[:len(status_counts)]
                )
                fig_pie.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig_pie, use_container_width=True, height=400)
        
        # Tabela detalhada dos pacientes
        st.markdown('### Detalhamento por Paciente - Primeiro ACQ')
        st.info('Tabela com detalhes do primeiro preenchimento de ACQ de cada paciente, incluindo idade, sexo, data, score e status de controle.')
        
        if acq_detalhes_pacientes:
            # Criar DataFrame para a tabela
            df_detalhes = pd.DataFrame(acq_detalhes_pacientes)
            
            # Ordenar por data do primeiro ACQ
            df_detalhes['Data do Primeiro ACQ'] = pd.to_datetime(df_detalhes['Data do Primeiro ACQ'], errors='coerce')
            df_detalhes = df_detalhes.sort_values('Data do Primeiro ACQ', ascending=True)
            
            # Formatar a data para exibição
            df_detalhes['Data do Primeiro ACQ'] = df_detalhes['Data do Primeiro ACQ'].dt.strftime('%d/%m/%Y %H:%M')
            
            # Filtros para a tabela
            st.markdown('#### Filtros da Tabela')
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Filtro por status
                status_options = ['Todos'] + list(df_detalhes['Status'].unique())
                status_filtro = st.selectbox('Status:', status_options)
            
            with col2:
                # Filtro por sexo
                sexo_options = ['Todos'] + list(df_detalhes['Sexo'].unique())
                sexo_filtro = st.selectbox('Sexo:', sexo_options)
            
            with col3:
                # Filtro por score mínimo
                score_min = st.number_input('Score mínimo:', min_value=0.0, max_value=6.0, value=0.0, step=0.1)
            
            with col4:
                # Filtro por score máximo
                score_max = st.number_input('Score máximo:', min_value=0.0, max_value=6.0, value=6.0, step=0.1)
            
            # Aplicar filtros
            df_filtrado = df_detalhes.copy()
            
            if status_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['Status'] == status_filtro]
            
            if sexo_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['Sexo'] == sexo_filtro]
            
            # Converter Score ACQ para float para filtro
            df_filtrado['Score ACQ'] = pd.to_numeric(df_filtrado['Score ACQ'], errors='coerce')
            df_filtrado = df_filtrado[
                (df_filtrado['Score ACQ'] >= score_min) & 
                (df_filtrado['Score ACQ'] <= score_max)
            ]
            
            st.markdown(f"**Pacientes filtrados: {len(df_filtrado)} de {len(df_detalhes)}**")
            
            # Exibir tabela
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                column_config={
                    "ID do Paciente": st.column_config.TextColumn("ID do Paciente", width="medium"),
                    "Idade": st.column_config.NumberColumn("Idade", width="small"),
                    "Sexo": st.column_config.TextColumn("Sexo", width="small"),
                    "Data do Primeiro ACQ": st.column_config.TextColumn("Data do Primeiro ACQ", width="medium"),
                    "Score ACQ": st.column_config.NumberColumn("Score ACQ", format="%.2f", width="small"),
                    "Status": st.column_config.TextColumn("Status", width="small"),
                    "Total de ACQs": st.column_config.NumberColumn("Total de ACQs", width="small")
                }
            )
            
            # Resumo da tabela
            st.markdown(f"**Total de pacientes com ACQ válido na tabela: {len(df_filtrado)}**")
            
            # Botão de download da tabela (dados filtrados)
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download da Tabela (CSV)",
                data=csv,
                file_name=f"acq_primeira_semana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Baixar tabela com detalhes do primeiro ACQ de cada paciente"
            )
    else:
        st.subheader('Status de Controle da Asma (ACQ)')
        st.warning('Nenhum registro de ACQ encontrado para a primeira semana dos pacientes no período selecionado.')
    
    st.markdown('---') 