import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from dateutil import parser
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import carregar_json, processar_datas
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
from sections.tabelas import mostrar_tabelas
from sections.mapa_calor import mostrar_mapa_calor
#from sections.tomadas_mapa_calor import mostrar_tomadas_mapa_calor
#from sections.ecdf_onboarding import mostrar_ecdf_onboarding
#from sections.transicoes_mensais_acq import mostrar_transicoes_mensais_acq
#from sections.radar_spider import mostrar_radar_spider

st.set_page_config(page_title="Dashboard Inspirar", page_icon="��", layout="wide")

# Sidebar com logo, instruções e sumário visual
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=150)
st.sidebar.markdown("### Informações")
st.sidebar.info("Dashboard personalizado para análise de dados de pacientes usuários do app Inspirar")


st.sidebar.markdown("---")

st.title("🏥 Dashboard Insights Avançados - Usuários do app Inspirar")
st.markdown("<small>Visualize, explore e compare dados de pacientes de forma interativa.</small>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.sidebar.file_uploader("Carregue o arquivo JSON de pacientes", type=["json"])

if uploaded_file:
    try:
        data = carregar_json(uploaded_file)
        if not isinstance(data, dict) or 'data' not in data or 'result' not in data['data']:
            raise ValueError("O arquivo JSON não possui a estrutura esperada. Consulte o exemplo em data/README.md.")
        pacientes = data['data']['result']
        df = processar_datas(pd.DataFrame(pacientes), 'createdAt')

        # Filtrar pacientes criados a partir de março de 2025
        data_limite = pd.Timestamp('2025-03-01').tz_localize('UTC')
        df_filtrado = df[df['createdAt'] >= data_limite]
        pacientes_recorte = df_filtrado.to_dict(orient='records')

        st.info(f"📊 Total de pacientes analisados: {len(pacientes_recorte)} (contas criadas a partir de março de 2025)")
        
        # Período fixo de extração dos dados 
        periodo_texto = "mar-out/2025"
        data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
        data_fim = pd.Timestamp('2025-10-08').tz_localize('UTC')
        
        # Armazenar informações do período no session_state para uso nas seções
        st.session_state['periodo_texto'] = periodo_texto
        st.session_state['data_inicio'] = data_inicio
        st.session_state['data_fim'] = data_fim
        
        # Card informativo do período na sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📅 Período de Extração dos Dados")
        st.sidebar.success(f"📊 Período: {periodo_texto}")
        st.sidebar.info(f"📅 Dados extraídos de 01/03/2025 a 08/10/2025")

        # Criar estrutura de abas para organizar as seções
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Visão Geral", 
            "👥 Demografia", 
            "💊 Medicamentos", 
            "📝 Diários & Atividades", 
            "📈 Análises Avançadas",
            "📋 Dados Detalhados"
        ])
        
        with tab1:
            st.markdown("### 📊 Visão Geral dos Pacientes")
            mostrar_metricas(df_filtrado)
            mostrar_ativos(df_filtrado)
            mostrar_idade(df_filtrado)
        
        with tab2:
            st.markdown("### 👥 Análise Demográfica")
            mostrar_barplot_metricas(df_filtrado, pacientes_recorte)
            mostrar_crises(pacientes_recorte)
        
        with tab3:
            st.markdown("### 💊 Medicamentos e Prescrições")
            mostrar_prescricoes_semanais(pacientes_recorte)
            mostrar_status_acq(pacientes_recorte)
        
        with tab4:
            st.markdown("### 📝 Diários e Atividades Físicas")
            mostrar_diarios_semanais(pacientes_recorte)
            mostrar_atividades_semanais(pacientes_recorte)
            mostrar_recordes(pacientes_recorte)
        
        with tab5:
            st.markdown("### 📈 Análises Avançadas")
            mostrar_funcionalidades_geral(df_filtrado)
            mostrar_funcionalidades_sexo(df_filtrado)
            mostrar_mapa_calor(df_filtrado)
            # Seções comentadas para futuras implementações
            #mostrar_tomadas_mapa_calor(pacientes_recorte)
            #mostrar_ecdf_onboarding(pacientes_recorte)
            #mostrar_transicoes_mensais_acq(pacientes_recorte)
            #mostrar_radar_spider(pacientes_recorte)
        
        with tab6:
            st.markdown("### 📋 Dados Detalhados")
            mostrar_tabelas(df_filtrado, pacientes_recorte)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo JSON: {e}\n\nVerifique se o arquivo segue o formato correto. Consulte o exemplo em data/README.md.")
else:
    st.info("Faça upload do arquivo JSON para visualizar os insights.")

# Informações de contato na sidebar
st.sidebar.markdown("---")
st.sidebar.warning("Dúvidas, sugestões, críticas, elogios: aline.dev@proton.me")