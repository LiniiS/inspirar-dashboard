import streamlit as st
import pandas as pd
from dateutil import parser
from collections import Counter
from components.cards import card_metric
import plotly.express as px

def mostrar_crises(pacientes_recorte):
    st.markdown('---')
    st.subheader('🚨 Crises - Total, Pacientes e Distribuição por Período')
    st.markdown('Resumo do total de crises reportadas, pacientes afetados e análise da duração das crises.')
    # Total de crises reportadas
    total_crises = sum([len(p.get('crisis', [])) for p in pacientes_recorte])
    # Total de pacientes que reportaram pelo menos uma crise
    total_pacientes_com_crise = sum([1 for p in pacientes_recorte if len(p.get('crisis', [])) > 0])
    # Tabela de crises por período
    crises_periodos = []
    for paciente in pacientes_recorte:
        for crise in paciente.get('crisis', []):
            try:
                ini = parser.parse(crise.get('initialUsageDate'))
                fim = parser.parse(crise.get('finalUsageDate'))
                dur = (fim - ini).days
                crises_periodos.append(dur)
            except:
                continue
    if crises_periodos:
        contagem = Counter(crises_periodos)
        tabela_crises = pd.DataFrame({'Período (dias)': list(contagem.keys()), 'Quantidade de crises': list(contagem.values())})
    else:
        tabela_crises = pd.DataFrame({'Período (dias)': [], 'Quantidade de crises': []})
    # Gráfico de barras por faixas de duração
    bins = [0, 5, 10, 15, 1000]
    labels = ['1-5 dias', '6-10 dias', '11-15 dias', 'Acima de 15 dias']
    tabela_crises['Faixa de duração'] = pd.cut(tabela_crises['Período (dias)'], bins=bins, labels=labels, right=False)
    grafico = tabela_crises.groupby('Faixa de duração', observed=False)['Quantidade de crises'].sum().reindex(labels, fill_value=0)
    st.bar_chart(grafico)
    st.dataframe(tabela_crises, use_container_width=True)
    st.markdown('---') 