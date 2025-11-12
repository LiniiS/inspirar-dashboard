import streamlit as st

def mostrar_metricas(df_recorte):
    st.subheader('Main Metrics')
    st.markdown('Main quantitative indicators of the patient sample in the selected period.')
    col1, col2, col3, col4 = st.columns(4)
    total_cadastrados_periodo = df_recorte.shape[0]
    total_com_medicamento = df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_com_medicamento = 100 * total_com_medicamento / len(df_recorte) if len(df_recorte) > 0 else 0
    total_atividade = df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_atividade = 100 * total_atividade / len(df_recorte) if len(df_recorte) > 0 else 0
    media_idade = df_recorte['age'].replace(0, None).mean()
    # Obter período dinâmico do session_state
    periodo_texto = st.session_state.get('periodo_texto', 'mar-out/2025')
    col1.metric(f"Total registered ({periodo_texto})", total_cadastrados_periodo)
    col2.metric("With medication (%)", f"{perc_com_medicamento:.1f}%")
    col3.metric("Physical activity (%)", f"{perc_atividade:.1f}%")
    col4.metric("Average age", f"{media_idade:.1f}")
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown('---') 