import streamlit as st
import plotly.express as px

def mostrar_ativos(df_recorte):
    st.subheader('🥧 Distribuição de Pacientes Ativos vs Inativos')
    st.markdown('Mostra a proporção de pacientes que utilizaram pelo menos uma funcionalidade versus os inativos.')
    def paciente_ativo(row):
        return any([
            isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
            isinstance(row['acqs'], list) and len(row['acqs']) > 0,
            isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
            isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
            isinstance(row['crisis'], list) and len(row['crisis']) > 0
        ])
    df_recorte['is_ativo'] = df_recorte.apply(paciente_ativo, axis=1)
    n_ativos = df_recorte['is_ativo'].sum()
    n_inativos = len(df_recorte) - n_ativos
    
    fig_pizza_ativos = px.pie(
        names=['Ativos', 'Inativos'],
        values=[n_ativos, n_inativos],
        color_discrete_sequence=['#2ecc71', '#e74c3c'],
        title='Distribuição de Pacientes Ativos vs Inativos'
    )
    st.plotly_chart(fig_pizza_ativos, use_container_width=True)
    st.markdown('---') 