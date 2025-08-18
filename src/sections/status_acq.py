import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.colors import CHART_COLORS, METRIC_COLORS

def mostrar_status_acq(pacientes_recorte):
    # Coletar apenas a primeira semana de ACQ de cada paciente
    acq_primeira_semana = []
    acq_status_primeira_semana = []
    
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
                except (TypeError, ValueError):
                    # Se não conseguir converter para float, pular este ACQ
                    continue
        else:
            pacientes_sem_acq += 1
    
    # Calcular taxa de preenchimento
    taxa_preenchimento = (pacientes_com_acq / total_pacientes * 100) if total_pacientes > 0 else 0
    
    # Validação de consistência dos dados
    acqs_com_score_valido = len(acq_primeira_semana)
    acqs_com_status_valido = len([s for s in acq_status_primeira_semana if s != 'N/A'])
    
    if acq_primeira_semana:
        st.subheader('🥧 Status de Controle da Asma (ACQ) - Primeira Semana')
        st.info('Análise do ACQ (Asthma Control Questionnaire) considerando apenas o **primeiro preenchimento temporal** de cada paciente (ordenado por data de criação/resposta). Isso fornece uma visão mais precisa do controle inicial da asma, garantindo consistência para análise médica.')
        
        # Métricas de engajamento
        st.markdown('### 📊 Métricas de Engajamento com ACQ')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total de Pacientes", total_pacientes)
        col2.metric("✅ Com ACQ", pacientes_com_acq)
        col3.metric("❌ Sem ACQ", pacientes_sem_acq)
        col4.metric("📈 Taxa de Preenchimento", f"{taxa_preenchimento:.1f}%")
        
        # Validação de consistência
        st.markdown('### 🔍 Validação de Consistência dos Dados')
        col1, col2 = st.columns(2)
        col1.metric("📊 ACQs com Score Válido", acqs_com_score_valido)
        col2.metric("📋 ACQs com Status Válido", acqs_com_status_valido)
        
        if acqs_com_score_valido != acqs_com_status_valido:
            st.warning(f"⚠️ **Atenção**: {acqs_com_score_valido - acqs_com_status_valido} ACQs têm score válido mas status 'N/A'. Isso pode indicar inconsistência nos dados.")
        
        # Criar DataFrame para análise
        df_acq = pd.DataFrame({
            'score': acq_primeira_semana,
            'status': acq_status_primeira_semana
        })
        
        # Estatísticas descritivas
        st.markdown('### 📊 Estatísticas Descritivas - Score ACQ Primeira Semana')
        col1, col2, col3, col4 = st.columns(4)
        
        valores_validos = df_acq['score'].dropna()
        col1.metric('Média', f'{valores_validos.mean():.2f}')
        col2.metric('Desvio Padrão', f'{valores_validos.std():.2f}')
        col3.metric('Mediana', f'{valores_validos.median():.2f}')
        col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
        
        st.markdown('### 📊 Visualizações - Primeira Semana')
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
        
    else:
        st.subheader('🥧 Status de Controle da Asma (ACQ)')
        st.warning('Nenhum registro de ACQ encontrado para a primeira semana dos pacientes no período selecionado.')
    
    st.markdown('---') 