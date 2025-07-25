import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

def mostrar_funcionalidades(df_recorte):
    # --- Distribuição do Número de Funcionalidades Utilizadas por Paciente ---
    st.subheader('📊 Distribuição do Número de Funcionalidades Utilizadas por Paciente')
    st.info('Para cada paciente, é contado quantas funcionalidades diferentes ele utilizou ao menos uma vez (diário de sintomas, ACQ, atividade física, prescrição, crise). O gráfico mostra a distribuição dessa contagem entre todos os pacientes.')
    st.markdown('Visualiza quantas funcionalidades diferentes cada paciente utilizou no período.')
    def conta_funcionalidades(row):
        return sum([
            isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
            isinstance(row['acqs'], list) and len(row['acqs']) > 0,
            isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
            isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
            isinstance(row['crisis'], list) and len(row['crisis']) > 0
        ])
    df_recorte['n_funcionalidades'] = df_recorte.apply(conta_funcionalidades, axis=1)
    dist_funcionalidades = df_recorte['n_funcionalidades'].value_counts().sort_index()
    fig_func_count = px.bar(
        x=dist_funcionalidades.index,
        y=dist_funcionalidades.values,
        labels={'x': 'Número de Funcionalidades', 'y': 'Número de Pacientes'},
        title='Distribuição do Número de Funcionalidades Utilizadas por Paciente',
        color=dist_funcionalidades.values,
        color_continuous_scale='Oranges'
    )
    st.plotly_chart(fig_func_count, use_container_width=True)
    st.markdown('---')

    # --- Funcionalidades Mais Utilizadas ---
    funcionalidades = {
        'Symptom Diaries': df_recorte['symptomDiaries'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'ACQs': df_recorte['acqs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Activity Logs': df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Prescriptions': df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Crisis': df_recorte['crisis'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    }
    st.subheader('📊 Funcionalidades Mais Utilizadas')
    st.info('Para cada funcionalidade, é contado o número de pacientes que a utilizou ao menos uma vez no período analisado. O gráfico mostra o ranking das funcionalidades mais acessadas.')
    st.markdown('Ranking das funcionalidades mais acessadas pelos pacientes.')
    fig_funcionalidades = px.bar(
        x=list(funcionalidades.keys()),
        y=list(funcionalidades.values()),
        title="Funcionalidades Mais Utilizadas",
        labels={'x': 'Funcionalidade', 'y': 'Número de Pacientes'},
        color=list(funcionalidades.values()),
        color_continuous_scale='Blues'
    )
    fig_funcionalidades.update_layout(showlegend=False)
    st.plotly_chart(fig_funcionalidades, use_container_width=True)
    st.markdown('---') 