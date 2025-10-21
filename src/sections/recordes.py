import streamlit as st
import pandas as pd
import numpy as np
from dateutil import parser

def mostrar_recordes(pacientes_recorte):
    st.subheader('Recordes e Destaques')
    st.markdown('Destaques individuais, como paciente mais ativo baseado na média diária de passos.')

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
            **Paciente Mais Ativo**
            - **ID:** {paciente_mais_ativo_detalhes['id']}
            - **Conta criada em:** {paciente_mais_ativo_detalhes['data_cadastro'].strftime('%d/%m/%Y')}
            - **Período analisado:** {paciente_mais_ativo_detalhes['periodo_dias']} dias
            - **Total de passos:** {paciente_mais_ativo_detalhes['total_passos']:,}
            - **Média diária:** {paciente_mais_ativo_detalhes['media_diaria']:,.0f} passos/dia
            """)
        else:
            st.warning("📊 Nenhum paciente com registros de atividade física encontrado")

    with col2:
        # Estatísticas gerais
        if todos_passos:
            st.info(f"""
            **📊 Estatísticas Gerais**
            - Pacientes ativos: {pacientes_ativos}
            - Média de passos: {np.mean(todos_passos):,.0f}
            - Total de passos: {sum(todos_passos):,}
            - Mediana: {np.median(todos_passos):,.0f}
            """)
        else:
            st.info("📊 Nenhum dado de atividade física encontrado")

    st.markdown('---') 