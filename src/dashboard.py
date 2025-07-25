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
from sections.sexo import mostrar_sexo
from sections.crises import mostrar_crises
from sections.funcionalidades import mostrar_funcionalidades
from sections.boxplot_metricas import mostrar_boxplot_metricas
from sections.semanais import mostrar_semanais
from sections.status_acq import mostrar_status_acq
from sections.recordes import mostrar_recordes
from sections.tabelas import mostrar_tabelas
from sections.mapa_calor import mostrar_mapa_calor

st.set_page_config(page_title="Dashboard Inspirar", page_icon="��", layout="wide")

# Sidebar com logo, instruções e sumário visual
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=150)
st.sidebar.markdown("### Informações")
st.sidebar.info("Dashboard para análise de dados de pacientes usuários do app Inspirar")

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
        df = processar_datas(st.session_state.get('df', pd.DataFrame(pacientes)), 'createdAt')
        mask_periodo = (df['createdAt'] >= '2025-03-01') & (df['createdAt'] <= '2025-07-31')
        df_recorte = df[mask_periodo].copy()
        pacientes_recorte = df_recorte.to_dict(orient='records')

        mostrar_metricas(df_recorte)
        mostrar_ativos(df_recorte) 
        mostrar_boxplot_metricas(df_recorte, pacientes_recorte)
        mostrar_semanais(df_recorte, pacientes_recorte)  
        mostrar_status_acq(pacientes_recorte)
        mostrar_recordes(pacientes_recorte)
        mostrar_tabelas(df_recorte, pacientes_recorte)  
        mostrar_idade(df_recorte)
        mostrar_sexo(df_recorte)
        mostrar_crises(pacientes_recorte)
        mostrar_funcionalidades(df_recorte)
        mostrar_mapa_calor(df_recorte)
        # As demais seções podem ser integradas de forma similar
    except Exception as e:
        st.error(f"Erro ao processar o arquivo JSON: {e}\n\nVerifique se o arquivo segue o formato correto. Consulte o exemplo em data/README.md.")
else:
    st.info("Faça upload do arquivo JSON para visualizar os insights.")