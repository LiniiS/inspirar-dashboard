import streamlit as st
import pandas as pd
from dateutil import parser

def mostrar_tabelas(df_recorte, pacientes_recorte):
    st.subheader('Tabelas Detalhadas com Filtro por Idade')
    st.markdown('Tabela detalhada dos pacientes, filtrável por faixa etária.')
    idade_min, idade_max = st.slider(
        "Faixa de Idade",
        min_value=int(df_recorte['age'].min()) if not df_recorte.empty else 0,
        max_value=int(df_recorte['age'].max()) if not df_recorte.empty else 100,
        value=(18, 80)
    )
    df_idade = df_recorte[df_recorte['age'].between(idade_min, idade_max)].copy()
    df_idade['total_symptom_diaries'] = df_idade['symptomDiaries'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df_idade['total_acqs'] = df_idade['acqs'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df_idade['total_activity_logs'] = df_idade['activityLogs'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df_idade['total_prescriptions'] = df_idade['prescriptions'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df_idade['total_crisis'] = df_idade['crisis'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    colunas_exibicao = [
        'id', 'age', 'height', 'weight', 
        'total_symptom_diaries', 'total_acqs', 'total_activity_logs', 
        'total_prescriptions', 'total_crisis'
    ]
    df_exibicao = df_idade[colunas_exibicao].copy()
    df_exibicao.columns = [
        'ID', 'Idade', 'Altura (m)', 'Peso (kg)',
        'Total Diários', 'Total ACQs', 'Total Atividades',
        'Total Prescrições', 'Total Crises'
    ]
    st.dataframe(df_exibicao, use_container_width=True)
    st.markdown('---') 