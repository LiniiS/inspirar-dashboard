import streamlit as st
from datetime import timedelta
from dateutil import parser

def mostrar_recordes(pacientes_recorte):
    st.subheader('🏆 Recordes e Destaques')
    st.markdown('Destaques individuais, como paciente mais ativo e maior tempo de crise.')
    paciente_mais_ativo = None
    maior_distancia = 0
    for paciente in pacientes_recorte:
        total_passos = sum([a.get('steps', 0) for a in paciente.get('activityLogs', [])])
        if total_passos > maior_distancia:
            maior_distancia = total_passos
            paciente_mais_ativo = paciente['id']
    paciente_maior_crise = None
    maior_duracao_crise = timedelta(0)
    for paciente in pacientes_recorte:
        for crise in paciente.get('crisis', []):
            try:
                ini = parser.parse(crise.get('initialUsageDate'))
                fim = parser.parse(crise.get('finalUsageDate'))
                dur = fim - ini
                if dur > maior_duracao_crise:
                    maior_duracao_crise = dur
                    paciente_maior_crise = paciente['id']
            except:
                continue
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **🏃‍♂️ Paciente Mais Ativo**
        - ID: {paciente_mais_ativo if paciente_mais_ativo else 'N/A'}
        - Passos: {maior_distancia:,}
        """)
    with col2:
        if maior_duracao_crise > timedelta(0):
            st.warning(f"""
            **⚠️ Maior Tempo de Crise**
            - ID: {paciente_maior_crise if paciente_maior_crise else 'N/A'}
            - Duração: {maior_duracao_crise.days} dias
            """)
        else:
            st.success("✅ Nenhuma crise registrada no período")
    st.markdown('---') 