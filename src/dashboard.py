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
from sections.boxplot_metricas import mostrar_boxplot_metricas
from sections.prescricoes_semanais import mostrar_prescricoes_semanais
from sections.diarios_semanais import mostrar_diarios_semanais
from sections.atividades_semanais import mostrar_atividades_semanais
from sections.status_acq import mostrar_status_acq
from sections.recordes import mostrar_recordes
from sections.tabelas import mostrar_tabelas
from sections.mapa_calor import mostrar_mapa_calor

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

        mostrar_metricas(df_filtrado)
        mostrar_ativos(df_filtrado)
        mostrar_boxplot_metricas(df_filtrado, pacientes_recorte)
        mostrar_prescricoes_semanais(pacientes_recorte)
        mostrar_diarios_semanais(pacientes_recorte)
        mostrar_atividades_semanais(pacientes_recorte)
        mostrar_status_acq(pacientes_recorte)
        mostrar_recordes(pacientes_recorte)
        mostrar_tabelas(df_filtrado, pacientes_recorte)
        mostrar_idade(df_filtrado)
        mostrar_crises(pacientes_recorte)
        mostrar_funcionalidades_geral(df_filtrado)
        mostrar_funcionalidades_sexo(df_filtrado)
        mostrar_mapa_calor(df_filtrado)
        # As demais seções podem ser integradas de forma similar
    except Exception as e:
        st.error(f"Erro ao processar o arquivo JSON: {e}\n\nVerifique se o arquivo segue o formato correto. Consulte o exemplo em data/README.md.")
else:
    st.info("Faça upload do arquivo JSON para visualizar os insights.")

# Informações de contato na sidebar
st.sidebar.markdown("---")
st.sidebar.warning("Dúvidas, sugestões, críticas, elogios: aline.dev@proton.me")