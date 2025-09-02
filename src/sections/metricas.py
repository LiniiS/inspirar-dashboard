import streamlit as st

def mostrar_metricas(df_recorte):
    st.subheader('📈 Métricas Principais')
    st.markdown('Principais indicadores quantitativos da amostra de pacientes no período selecionado.')
    col1, col2, col3, col4 = st.columns(4)
    total_cadastrados_periodo = df_recorte.shape[0]
    total_com_medicamento = df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_com_medicamento = 100 * total_com_medicamento / len(df_recorte) if len(df_recorte) > 0 else 0
    total_atividade = df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_atividade = 100 * total_atividade / len(df_recorte) if len(df_recorte) > 0 else 0
    media_idade = df_recorte['age'].replace(0, None).mean()
    col1.metric("👥 Total cadastrados (mar-setembro/2025)", total_cadastrados_periodo)
    col2.metric("💊 Com medicamento (%)", f"{perc_com_medicamento:.1f}%")
    col3.metric("🏃 Atividade física (%)", f"{perc_atividade:.1f}%")
    col4.metric("🎂 Idade média", f"{media_idade:.1f}")
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown('---') 