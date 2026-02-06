import streamlit as st
import pandas as pd
from dateutil import parser
from utils.translations import t

def mostrar_tabelas(df_recorte, pacientes_recorte):
    st.subheader(t('sections.tabelas.title'))
    st.markdown(t('sections.tabelas.description'))
    idade_min, idade_max = st.slider(
        t('sections.tabelas.age_range'),
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
        'id', 'age', 'gender', 'height', 'weight', 
        'total_symptom_diaries', 'total_acqs', 'total_activity_logs', 
        'total_prescriptions', 'total_crisis'
    ]
    colunas_disponiveis = [c for c in colunas_exibicao if c in df_idade.columns]
    df_exibicao = df_idade[colunas_disponiveis].copy()
    if 'gender' in df_exibicao.columns:
        df_exibicao['gender'] = df_exibicao['gender'].map({
            'male': t('sections.ativos.male'),
            'female': t('sections.ativos.female')
        })
    mapeamento_colunas = {
        'id': 'ID',
        'age': t('tables.age'),
        'gender': t('tables.sex'),
        'height': t('tables.height'),
        'weight': t('tables.weight'),
        'total_symptom_diaries': t('tables.total_diaries'),
        'total_acqs': t('tables.total_acqs_table'),
        'total_activity_logs': t('tables.total_activities'),
        'total_prescriptions': t('tables.total_medications'),
        'total_crisis': t('tables.total_crises')
    }
    df_exibicao = df_exibicao.rename(columns={c: mapeamento_colunas[c] for c in df_exibicao.columns if c in mapeamento_colunas})
    st.dataframe(df_exibicao, use_container_width=True)
    st.markdown('---')
