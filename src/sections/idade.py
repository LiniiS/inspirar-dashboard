import streamlit as st
import plotly.express as px
import numpy as np

def mostrar_idade(df_recorte):
    st.subheader('📊 Distribuição de Idade dos Pacientes')
    st.markdown('Histograma mostrando a faixa etária dos pacientes cadastrados.')
    if not df_recorte.empty:
        fig_idade = px.histogram(
            df_recorte,
            x='age',
            nbins=15,
            title="Distribuição de Idade dos Pacientes",
            labels={'age': 'Idade', 'count': 'Frequência'},
            color_discrete_sequence=['#2ecc71']
        )
        st.plotly_chart(fig_idade, use_container_width=True)
    st.markdown('---') 