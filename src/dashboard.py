import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from dateutil import parser
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import carregar_json, processar_datas, filtrar_pacientes_marco_2025, DATA_LIMITE_MARCO_2025
from utils.translations import t
from sections.metricas import mostrar_metricas
from sections.ativos import mostrar_ativos
from sections.idade import mostrar_idade
from sections.crises import mostrar_crises
from sections.funcionalidades_geral import mostrar_funcionalidades_geral
from sections.funcionalidades_sexo import mostrar_funcionalidades_sexo
from sections.barplot_metricas import mostrar_barplot_metricas
from sections.prescricoes_semanais import mostrar_prescricoes_semanais
from sections.diarios_semanais import mostrar_diarios_semanais
from sections.atividades_semanais import mostrar_atividades_semanais
from sections.status_acq import mostrar_status_acq
from sections.recordes import mostrar_recordes
from sections.mapa_calor import mostrar_mapa_calor
from sections.tabelas import mostrar_tabelas

st.set_page_config(page_title="Dashboard Inspirar", page_icon="��", layout="wide")

# Inicializar idioma padrão se não existir
if 'language' not in st.session_state:
    st.session_state['language'] = 'pt'

# Sidebar com logo, instruções e sumário visual
st.sidebar.image("public/inspirar-logo.png", width=150)

# Seletor de idioma
st.sidebar.markdown("### 🌐 Idioma / Language")
language_options = ["🇧🇷 Português", "🇺🇸 English"]
current_lang_index = 0 if st.session_state.get('language', 'pt') == 'pt' else 1
selected_language = st.sidebar.radio(
    "Selecione o idioma / Select language:",
    language_options,
    index=current_lang_index,
    key='language_selector'
)

# Atualizar session_state com o idioma selecionado
st.session_state['language'] = 'pt' if selected_language == "🇧🇷 Português" else 'en'

st.sidebar.markdown("### Informações")
st.sidebar.info(t('dashboard.info'))


st.sidebar.markdown("---")

st.title(t('dashboard.title'))
st.markdown(f"<small>{t('dashboard.subtitle')}</small>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.sidebar.file_uploader(t('dashboard.upload_file'), type=["json"])

if uploaded_file:
    try:
        data = carregar_json(uploaded_file)
        if not isinstance(data, dict) or 'data' not in data or 'result' not in data['data']:
            error_msg = t('dashboard.error_processing').format(error="Invalid structure")
            raise ValueError(error_msg)
        pacientes = data['data']['result']
        df = processar_datas(pd.DataFrame(pacientes), 'createdAt')

        # CRÍTICO: Filtrar pacientes criados a partir de 01/03/2025
        # Este filtro é aplicado UMA VEZ aqui e TODAS as seções recebem dados já filtrados
        # Garante que todos os gráficos considerem apenas contas criadas a partir de março/2025
        pacientes_antes = len(pacientes)
        df_filtrado = filtrar_pacientes_marco_2025(df, 'createdAt')
        pacientes_recorte = filtrar_pacientes_marco_2025(pacientes, 'createdAt')
        pacientes_depois = len(pacientes_recorte)
        pacientes_removidos = pacientes_antes - pacientes_depois

        # Informação sobre o filtro aplicado
        st.info(f"📊 {t('dashboard.total_patients')}: {pacientes_depois} ({t('dashboard.accounts_from')})")
        
        # Período fixo de extração dos dados 
        periodo_texto = "março/2025-fevereiro/2026"
        data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
        data_fim = pd.Timestamp('2026-02-06').tz_localize('UTC')
        
        # Armazenar informações do período no session_state para uso nas seções
        st.session_state['periodo_texto'] = periodo_texto
        st.session_state['data_inicio'] = data_inicio
        st.session_state['data_fim'] = data_fim
        
        # Card informativo do período e filtro na sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### 📅 {t('dashboard.period_extraction')}")
        st.sidebar.success(f"📊 {t('dashboard.period')}: {periodo_texto}")
        st.sidebar.info(f"📅 {t('dashboard.data_extracted')}")
        
        # Log sobre o filtro aplicado (apenas se houver pacientes removidos)
        if pacientes_removidos > 0:
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔍 Filtro de Pacientes")
            st.sidebar.success(f"✅ **{pacientes_depois}** pacientes incluídos\n(contas criadas a partir de 01/03/2025)")
            st.sidebar.info(f"ℹ️ **{pacientes_removidos}** pacientes excluídos\n(criados antes de 01/03/2025)")

        # Criar estrutura de abas para organizar as seções
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            t('dashboard.tabs.overview'), 
            t('dashboard.tabs.demographics'), 
            t('dashboard.tabs.medications'), 
            t('dashboard.tabs.diaries'), 
            t('dashboard.tabs.advanced'),
            t('dashboard.tabs.details')
        ])
        
        with tab1:
            st.markdown(f"### {t('dashboard.tab_titles.overview')}")
            mostrar_metricas(df_filtrado)
            mostrar_ativos(df_filtrado)
            mostrar_idade(df_filtrado)
        
        with tab2:
            st.markdown(f"### {t('dashboard.tab_titles.demographics')}")
            mostrar_barplot_metricas(df_filtrado, pacientes_recorte)
            mostrar_crises(pacientes_recorte)
        
        with tab3:
            st.markdown(f"### {t('dashboard.tab_titles.medications')}")
            mostrar_prescricoes_semanais(pacientes_recorte)
            mostrar_status_acq(pacientes_recorte)
        
        with tab4:
            st.markdown(f"### {t('dashboard.tab_titles.diaries')}")
            mostrar_diarios_semanais(pacientes_recorte)
            mostrar_atividades_semanais(pacientes_recorte)
            mostrar_recordes(pacientes_recorte)
        
        with tab5:
            st.markdown(f"### {t('dashboard.tab_titles.advanced')}")
            mostrar_funcionalidades_geral(df_filtrado)
            mostrar_funcionalidades_sexo(df_filtrado)
            mostrar_mapa_calor(df_filtrado)
        
        with tab6:
            st.markdown(f"### {t('dashboard.tab_titles.details')}")
            mostrar_tabelas(df_filtrado, pacientes_recorte)
    except Exception as e:
        error_msg = t('dashboard.error_processing', error=str(e))
        st.error(error_msg)
else:
    st.info(t('dashboard.no_file'))

# Informações de contato na sidebar
st.sidebar.markdown("---")
st.sidebar.warning(t('dashboard.contact'))