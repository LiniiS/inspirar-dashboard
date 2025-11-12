import streamlit as st
import pandas as pd
import numpy as np
from dateutil import parser

def mostrar_recordes(pacientes_recorte):
    st.subheader('Records and Highlights')
    st.markdown('Individual highlights, such as most active patient based on daily average steps.')

    # Encontrar paciente mais ativo baseado na média diária de passos
    paciente_mais_ativo = None
    melhor_media_diaria = 0
    paciente_mais_ativo_detalhes = None

    # Data final de coleta
    data_coleta = pd.Timestamp('2025-10-08').tz_localize('UTC')

    for paciente in pacientes_recorte:
        # Data de criação da conta
        data_cadastro = paciente.get('createdAt')
        if not data_cadastro:
            continue

        if isinstance(data_cadastro, str):
            data_cadastro = parser.parse(data_cadastro)

        # Calcular período em dias
        periodo_dias = (data_coleta - data_cadastro).days
        if periodo_dias <= 0:
            continue

        # Calcular total de passos
        total_passos = sum([a.get('steps', 0) for a in paciente.get('activityLogs', [])])

        if total_passos > 0:
            # Calcular média diária
            media_diaria = total_passos / periodo_dias

            if media_diaria > melhor_media_diaria:
                melhor_media_diaria = media_diaria
                paciente_mais_ativo = paciente['id']
                paciente_mais_ativo_detalhes = {
                    'id': paciente['id'],
                    'data_cadastro': data_cadastro,
                    'total_passos': total_passos,
                    'periodo_dias': periodo_dias,
                    'media_diaria': media_diaria
                }

    # Estatísticas gerais de atividade física
    todos_passos = []
    pacientes_ativos = 0

    for paciente in pacientes_recorte:
        passos = sum([a.get('steps', 0) for a in paciente.get('activityLogs', [])])
        if passos > 0:
            todos_passos.append(passos)
            pacientes_ativos += 1

    # Layout principal
    col1, col2 = st.columns([2, 1])

    with col1:
        if paciente_mais_ativo_detalhes:
            st.success(f"""
            **Most Active Patient**
            - **ID:** {paciente_mais_ativo_detalhes['id']}
            - **Account created on:** {paciente_mais_ativo_detalhes['data_cadastro'].strftime('%d/%m/%Y')}
            - **Analyzed period:** {paciente_mais_ativo_detalhes['periodo_dias']} days
            - **Total steps:** {paciente_mais_ativo_detalhes['total_passos']:,}
            - **Daily average:** {paciente_mais_ativo_detalhes['media_diaria']:,.0f} steps/day
            """)
        else:
            st.warning("📊 No patient with physical activity records found")

    with col2:
        # Estatísticas gerais
        if todos_passos:
            st.info(f"""
            **📊 General Statistics**
            - Active patients: {pacientes_ativos}
            - Average steps: {np.mean(todos_passos):,.0f}
            - Total steps: {sum(todos_passos):,}
            - Median: {np.median(todos_passos):,.0f}
            """)
        else:
            st.info("📊 No physical activity data found")

    st.markdown('---') 