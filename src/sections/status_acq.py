import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_status_acq(pacientes_recorte):
    acq_status = []
    for paciente in pacientes_recorte:
        for acq in paciente.get('acqs', []):
            if acq.get('controlStatus'):
                acq_status.append(acq['controlStatus'])
    if acq_status:
        st.subheader('🥧 Status de Controle da Asma (ACQ)')
        st.info('O ACQ (Asthma Control Questionnaire) é um score individual por paciente, baseado em respostas a um questionário. Nesta visualização, mostramos a distribuição dos status de controle (por exemplo: controlado, parcialmente controlado, não controlado) considerando todos os registros de todos os pacientes no período analisado.')
        st.markdown('Distribuição dos status de controle da asma conforme os registros de ACQ.')
        acq_status_series = pd.Series(acq_status)
        fig_pie = px.pie(
            values=acq_status_series.value_counts().values,
            names=acq_status_series.value_counts().index,
            title="Status de Controle da Asma",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('---') 