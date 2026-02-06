import streamlit as st
import pandas as pd
import numpy as np
from dateutil import parser
from utils.translations import t

def mostrar_recordes(pacientes_recorte):
    st.subheader(t('sections.recordes.title'))
    st.markdown(t('sections.recordes.description'))

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
            **{t('sections.recordes.most_active')}**
            - **{t('sections.recordes.id')}:** {paciente_mais_ativo_detalhes['id']}
            - **{t('sections.recordes.account_created')}:** {paciente_mais_ativo_detalhes['data_cadastro'].strftime('%d/%m/%Y')}
            - **{t('sections.recordes.analyzed_period')}:** {paciente_mais_ativo_detalhes['periodo_dias']} {t('sections.recordes.days')}
            - **{t('sections.recordes.total_steps')}:** {paciente_mais_ativo_detalhes['total_passos']:,}
            - **{t('sections.recordes.daily_average')}:** {paciente_mais_ativo_detalhes['media_diaria']:,.0f} {t('sections.recordes.steps_per_day')}
            """)
        else:
            st.warning(t('sections.recordes.no_patient'))

    with col2:
        # Estatísticas gerais
        if todos_passos:
            st.info(f"""
            **{t('sections.recordes.general_statistics')}**
            - {t('sections.recordes.active_patients')}: {pacientes_ativos}
            - {t('sections.recordes.average_steps')}: {np.mean(todos_passos):,.0f}
            - {t('sections.recordes.total_steps_all')}: {sum(todos_passos):,}
            - {t('sections.recordes.median')}: {np.median(todos_passos):,.0f}
            """)
        else:
            st.info(t('sections.recordes.no_data'))

    st.markdown('---') 