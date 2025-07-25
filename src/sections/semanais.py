import streamlit as st
import pandas as pd
from dateutil import parser

def mostrar_semanais(df_recorte, pacientes_recorte):
    # Registro de tomada de medicamento por semana
    registros_presc = []
    for paciente in pacientes_recorte:
        prescs = paciente.get('prescriptions', [])
        datas = []
        for presc in prescs:
            for admin in presc.get('administrations', []):
                datas.append(admin.get('date'))
        datas = [parser.parse(d) for d in datas if d]
        if datas:
            semanas = pd.Series(datas).dt.isocalendar().week.value_counts()
            media_semana = semanas.mean()
        else:
            media_semana = 0
        registros_presc.append(media_semana)
    df_recorte['media_presc_semana'] = registros_presc
    hist_presc = df_recorte['media_presc_semana'].round().value_counts().sort_index()
    tabela_presc = pd.DataFrame({'Registros/semana': hist_presc.index.astype(int), 'Nº Usuários': hist_presc.values})
    st.subheader("💉 Registro de Tomada de Medicamento por Semana")
    st.info("O cálculo representa a média semanal de registros de administrações de medicamentos por paciente. Para cada paciente, é contado o número de registros de administração por semana, e a média é calculada considerando todas as semanas em que houve registro.")
    col_graf1, col_tab1 = st.columns([2,1])
    with col_graf1:
        st.bar_chart(hist_presc)
    with col_tab1:
        st.table(tabela_presc)

    # Registro de diário de sintomas por semana
    registros_diario = []
    for paciente in pacientes_recorte:
        diaries = paciente.get('symptomDiaries', [])
        datas = [parser.parse(d.get('createdAt')) for d in diaries if d.get('createdAt')]
        if datas:
            semanas = pd.Series(datas).dt.isocalendar().week.value_counts()
            media_semana = semanas.mean()
        else:
            media_semana = 0
        registros_diario.append(media_semana)
    df_recorte['media_diario_semana'] = registros_diario
    hist_diario = df_recorte['media_diario_semana'].round().value_counts().sort_index()
    tabela_diario = pd.DataFrame({'Registros/semana': hist_diario.index.astype(int), 'Nº Usuários': hist_diario.values})
    st.subheader("📓 Registro de Diário de Sintomas por Semana")
    st.info("O cálculo representa a média semanal de registros de diário de sintomas por paciente. Para cada paciente, é contado o número de registros de diário por semana, e a média é calculada considerando todas as semanas em que houve registro.")
    col_graf2, col_tab2 = st.columns([2,1])
    with col_graf2:
        st.bar_chart(hist_diario)
    with col_tab2:
        st.table(tabela_diario)

    # Registro de atividade física por semana
    registros_atividade = []
    for paciente in pacientes_recorte:
        acts = paciente.get('activityLogs', [])
        datas = [parser.parse(a.get('createdAt')) for a in acts if a.get('createdAt')]
        if datas:
            semanas = pd.Series(datas).dt.isocalendar().week.value_counts()
            media_semana = semanas.mean()
        else:
            media_semana = 0
        registros_atividade.append(media_semana)
    df_recorte['media_atividade_semana'] = registros_atividade
    hist_atividade = df_recorte['media_atividade_semana'].round().value_counts().sort_index()
    tabela_atividade = pd.DataFrame({'Registros/semana': hist_atividade.index.astype(int), 'Nº Usuários': hist_atividade.values})
    st.subheader("🏃 Registro de Atividade Física por Semana")
    st.info("O cálculo representa a média semanal de registros de atividade física por paciente. Para cada paciente, é contado o número de registros de atividade física por semana, e a média é calculada considerando todas as semanas em que houve registro.")
    col_graf, col_tab = st.columns([2,1])
    with col_graf:
        st.bar_chart(hist_atividade)
    with col_tab:
        st.table(tabela_atividade)
    st.markdown('---') 