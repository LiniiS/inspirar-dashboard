import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def mostrar_boxplot_metricas(df_recorte, pacientes_recorte):
    st.subheader('📊 Análise Descritiva e Boxplot de Métricas Numéricas')
    metricas_numericas = {
        'Idade': 'age',
        'Peso (kg)': 'weight',
        'Altura (m)': 'height',
    }
    if 'imc' not in df_recorte.columns:
        df_recorte['imc'] = df_recorte.apply(lambda row: row['weight'] / (row['height'] ** 2) if row['height'] and row['weight'] else np.nan, axis=1)
    metricas_numericas['IMC'] = 'imc'
    acq_iniciais = []
    for paciente in pacientes_recorte:
        acqs = paciente.get('acqs', [])
        if acqs:
            acq_iniciais.append(acqs[0].get('average', np.nan))
        else:
            acq_iniciais.append(np.nan)
    df_recorte['score_acq_inicial'] = acq_iniciais
    metricas_numericas['Score ACQ inicial'] = 'score_acq_inicial'
    for col in ['media_presc_semana', 'media_diario_semana', 'media_atividade_semana', 'percentual_acq']:
        if col in df_recorte.columns:
            nome = {
                'media_presc_semana': 'Média de prescrições/semana',
                'media_diario_semana': 'Média de diários/semana',
                'media_atividade_semana': 'Média de atividades/semana',
                'percentual_acq': '% semanas com ACQ preenchido',
            }[col]
            metricas_numericas[nome] = col
    metrica_escolhida = st.selectbox(
        "Selecione a métrica para análise:",
        list(metricas_numericas.keys()),
        index=0
    )
    coluna = metricas_numericas[metrica_escolhida]
    valores_validos = df_recorte[coluna].replace(0, np.nan).dropna()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Média', f'{valores_validos.mean():.2f}')
    col2.metric('Desvio padrão', f'{valores_validos.std():.2f}')
    col3.metric('Mediana', f'{valores_validos.median():.2f}')
    col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
    st.markdown(f"### Boxplot de {metrica_escolhida}")
    fig_box = px.box(df_recorte, y=coluna, points='all', title=f'Boxplot de {metrica_escolhida}', color_discrete_sequence=['#2ecc71'])
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown('---') 