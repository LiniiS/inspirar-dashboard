import streamlit as st
from utils.translations import t

def mostrar_metricas(df_recorte):
    st.subheader(t('sections.metrics.title'))
    st.markdown(t('sections.metrics.description'))
    col1, col2, col3, col4 = st.columns(4)
    total_cadastrados_periodo = df_recorte.shape[0]
    total_com_medicamento = df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_com_medicamento = 100 * total_com_medicamento / len(df_recorte) if len(df_recorte) > 0 else 0
    total_atividade = df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    perc_atividade = 100 * total_atividade / len(df_recorte) if len(df_recorte) > 0 else 0
    media_idade = df_recorte['age'].replace(0, None).mean()
    # Obter período dinâmico do session_state
    periodo_texto = st.session_state.get('periodo_texto', 'março/2025-fevereiro/2026')
    col1.metric(f"{t('sections.metrics.total_registered')} ({periodo_texto})", total_cadastrados_periodo)
    col2.metric(t('sections.metrics.with_medication'), f"{perc_com_medicamento:.1f}%")
    col3.metric(t('sections.metrics.physical_activity'), f"{perc_atividade:.1f}%")
    col4.metric(t('sections.metrics.average_age'), f"{media_idade:.1f}")
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown('---') 