import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from dateutil import parser
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Inspirar", page_icon="🏥", layout="wide")

st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=150)
st.sidebar.markdown("### Filtros e opções")
st.sidebar.info("Faça upload do arquivo JSON de pacientes para visualizar os insights.")
st.sidebar.markdown("---")
st.sidebar.markdown("#### Sumário do Dashboard")
st.sidebar.markdown("""
- 📈 Métricas Principais
- 🥧 Distribuição Ativos/Inativos
- 📊 Funcionalidades Utilizadas
- 📊 Idade dos Pacientes
- 🥧 Status ACQ
- 🏆 Recordes e Destaques
- 📋 Tabelas Detalhadas
- 👤 Sexo
- 🚨 Crises
- 🔥 Mapa de Calor
""")

st.title("🏥 Dashboard Insights Avançados - Pacientes com Asma")
st.markdown("<small>Visualize, explore e compare dados de pacientes de forma interativa.</small>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.sidebar.file_uploader("Carregue o arquivo JSON de pacientes", type=["json"])

def carregar_json(uploaded_file):
    data = json.load(uploaded_file)
    return data

def processar_datas(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

if uploaded_file:
    try:
        data = carregar_json(uploaded_file)
        if not isinstance(data, dict) or 'data' not in data or 'result' not in data['data']:
            raise ValueError("O arquivo JSON não possui a estrutura esperada. Consulte o exemplo em data/README.md.")
        pacientes = data['data']['result']
        df = pd.DataFrame(pacientes)
        df = processar_datas(df, 'createdAt')
        mask_periodo = (df['createdAt'] >= '2025-03-01') & (df['createdAt'] <= '2025-07-31')
        df_recorte = df[mask_periodo].copy()
        pacientes_recorte = df_recorte.to_dict(orient='records')

        # --- Métricas Principais ---
        st.subheader('📈 Métricas Principais')
        st.markdown('Principais indicadores quantitativos da amostra de pacientes no período selecionado.')
        col1, col2, col3, col4 = st.columns(4)
        total_cadastrados_periodo = df_recorte.shape[0]
        total_com_medicamento = df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
        perc_com_medicamento = 100 * total_com_medicamento / len(df_recorte) if len(df_recorte) > 0 else 0
        total_atividade = df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
        perc_atividade = 100 * total_atividade / len(df_recorte) if len(df_recorte) > 0 else 0
        media_idade = df_recorte['age'].replace(0, np.nan).mean()
        col1.metric("👥 Total cadastrados (mar-jul/2025)", total_cadastrados_periodo)
        col2.metric("💊 Com medicamento (%)", f"{perc_com_medicamento:.1f}%")
        col3.metric("🏃 Atividade física (%)", f"{perc_atividade:.1f}%")
        col4.metric("🎂 Idade média", f"{media_idade:.1f}")
        st.markdown("&nbsp;", unsafe_allow_html=True)
        st.markdown('---')

        # --- Distribuição de Pacientes Ativos vs Inativos ---
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

        # --- Distribuição do Número de Funcionalidades Utilizadas por Paciente ---
        st.subheader('📊 Distribuição do Número de Funcionalidades Utilizadas por Paciente')
        st.markdown('Visualiza quantas funcionalidades diferentes cada paciente utilizou no período.')
        def conta_funcionalidades(row):
            return sum([
                isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
                isinstance(row['acqs'], list) and len(row['acqs']) > 0,
                isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
                isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
                isinstance(row['crisis'], list) and len(row['crisis']) > 0
            ])
        df_recorte['n_funcionalidades'] = df_recorte.apply(conta_funcionalidades, axis=1)
        dist_funcionalidades = df_recorte['n_funcionalidades'].value_counts().sort_index()
        fig_func_count = px.bar(
            x=dist_funcionalidades.index,
            y=dist_funcionalidades.values,
            labels={'x': 'Número de Funcionalidades', 'y': 'Número de Pacientes'},
            title='Distribuição do Número de Funcionalidades Utilizadas por Paciente',
            color=dist_funcionalidades.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_func_count, use_container_width=True)
        st.markdown('---')

        # --- Funcionalidades Mais Utilizadas ---
        funcionalidades = {
            'Symptom Diaries': df_recorte['symptomDiaries'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
            'ACQs': df_recorte['acqs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
            'Activity Logs': df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
            'Prescriptions': df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
            'Crisis': df_recorte['crisis'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
        }
        st.subheader('📊 Funcionalidades Mais Utilizadas')
        st.markdown('Ranking das funcionalidades mais acessadas pelos pacientes.')
        fig_funcionalidades = px.bar(
            x=list(funcionalidades.keys()),
            y=list(funcionalidades.values()),
            title="Funcionalidades Mais Utilizadas",
            labels={'x': 'Funcionalidade', 'y': 'Número de Pacientes'},
            color=list(funcionalidades.values()),
            color_continuous_scale='Blues'
        )
        fig_funcionalidades.update_layout(showlegend=False)
        st.plotly_chart(fig_funcionalidades, use_container_width=True)
        st.markdown('---')

        # --- Distribuição de Idade dos Pacientes ---
        st.subheader('📊 Distribuição de Idade dos Pacientes')
        st.markdown('Histograma mostrando a faixa etária dos pacientes cadastrados.')
        if not df_recorte.empty:
            fig_idade = px.histogram(
                df_recorte,
                x='age',
                nbins=15,
                title="Distribuição de Idade dos Pacientes",
                labels={'age': 'Idade', 'count': 'Frequência'},
                color_discrete_sequence=['#2ecc71']
            )
            st.plotly_chart(fig_idade, use_container_width=True)
        st.markdown('---')

        # --- Boxplot e Análise Descritiva Dinâmica ---
        st.subheader('📊 Análise Descritiva e Boxplot de Métricas Numéricas')
        metricas_numericas = {
            'Idade': 'age',
            'Peso (kg)': 'weight',
            'Altura (m)': 'height',
        }
        if 'imc' not in df_recorte.columns:
            df_recorte['imc'] = df_recorte.apply(lambda row: row['weight'] / (row['height'] ** 2) if row['height'] and row['weight'] else np.nan, axis=1)
        metricas_numericas['IMC'] = 'imc'
        acq_iniciais = []
        for paciente in pacientes_recorte:
            acqs = paciente.get('acqs', [])
            if acqs:
                acq_iniciais.append(acqs[0].get('average', np.nan))
            else:
                acq_iniciais.append(np.nan)
        df_recorte['score_acq_inicial'] = acq_iniciais
        metricas_numericas['Score ACQ inicial'] = 'score_acq_inicial'
        for col in ['media_presc_semana', 'media_diario_semana', 'media_atividade_semana', 'percentual_acq']:
            if col in df_recorte.columns:
                nome = {
                    'media_presc_semana': 'Média de prescrições/semana',
                    'media_diario_semana': 'Média de diários/semana',
                    'media_atividade_semana': 'Média de atividades/semana',
                    'percentual_acq': '% semanas com ACQ preenchido',
                }[col]
                metricas_numericas[nome] = col
        metrica_escolhida = st.selectbox(
            "Selecione a métrica para análise:",
            list(metricas_numericas.keys()),
            index=0
        )
        coluna = metricas_numericas[metrica_escolhida]
        valores_validos = df_recorte[coluna].replace(0, np.nan).dropna()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Média', f'{valores_validos.mean():.2f}')
        col2.metric('Desvio padrão', f'{valores_validos.std():.2f}')
        col3.metric('Mediana', f'{valores_validos.median():.2f}')
        col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
        st.markdown(f"### Boxplot de {metrica_escolhida}")
        fig_box = px.box(df_recorte, y=coluna, points='all', title=f'Boxplot de {metrica_escolhida}', color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('---')

        # --- Status de Controle da Asma (ACQ) ---
        acq_status = []
        for paciente in pacientes_recorte:
            for acq in paciente.get('acqs', []):
                if acq.get('controlStatus'):
                    acq_status.append(acq['controlStatus'])
        if acq_status:
            st.subheader('🥧 Status de Controle da Asma (ACQ)')
            st.markdown('Distribuição dos status de controle da asma conforme os registros de ACQ.')
            acq_status_series = pd.Series(acq_status)
            fig_pie = px.pie(
                values=acq_status_series.value_counts().values,
                names=acq_status_series.value_counts().index,
                title="Status de Controle da Asma",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('---')

        # --- Recordes e Destaques ---
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

        # --- Tabelas Detalhadas com Filtro por Idade ---
        st.subheader('📋 Tabelas Detalhadas com Filtro por Idade')
        st.markdown('Tabela detalhada dos pacientes, filtrável por faixa etária.')
        idade_min, idade_max = st.slider(
            "Faixa de Idade",
            min_value=int(df_recorte['age'].min()) if not df_recorte.empty else 0,
            max_value=int(df_recorte['age'].max()) if not df_recorte.empty else 100,
            value=(18, 80)
        )
        df_idade = df_recorte[df_recorte['age'].between(idade_min, idade_max)].copy()
        df_idade['total_symptom_diaries'] = df_idade['symptomDiaries'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df_idade['total_acqs'] = df_idade['acqs'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df_idade['total_activity_logs'] = df_idade['activityLogs'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df_idade['total_prescriptions'] = df_idade['prescriptions'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df_idade['total_crisis'] = df_idade['crisis'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        colunas_exibicao = [
            'id', 'age', 'height', 'weight', 
            'total_symptom_diaries', 'total_acqs', 'total_activity_logs', 
            'total_prescriptions', 'total_crisis'
        ]
        df_exibicao = df_idade[colunas_exibicao].copy()
        df_exibicao.columns = [
            'ID', 'Idade', 'Altura (m)', 'Peso (kg)',
            'Total Diários', 'Total ACQs', 'Total Atividades',
            'Total Prescrições', 'Total Crises'
        ]
        st.dataframe(df_exibicao, use_container_width=True)
        st.markdown('---')

        # --- Gráficos e Tabelas Semanais ---
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
        tabela_presc = pd.DataFrame({'Registros/semana': hist_presc.index, 'Nº Usuários': hist_presc.values})
        st.subheader("💉 Registro de Tomada de Medicamento por Semana")
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
        tabela_diario = pd.DataFrame({'Registros/semana': hist_diario.index, 'Nº Usuários': hist_diario.values})
        st.subheader("📓 Registro de Diário de Sintomas por Semana")
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
        tabela_atividade = pd.DataFrame({'Registros/semana': hist_atividade.index, 'Nº Usuários': hist_atividade.values})
        st.subheader("🏃 Registro de Atividade Física por Semana")
        col_graf, col_tab = st.columns([2,1])
        with col_graf:
            st.bar_chart(hist_atividade)
        with col_tab:
            st.table(tabela_atividade)
        st.markdown('---')

        # --- Percentual de Semanas com ACQ Preenchido ---
        acq_percentuais = []
        acq_detalhes = []
        for paciente in pacientes_recorte:
            acqs = paciente.get('acqs', [])
            datas = [parser.parse(a.get('createdAt')) for a in acqs if a.get('createdAt')]
            if datas:
                semanas_preenchidas = pd.Series(datas).dt.isocalendar().week.nunique()
                data_cadastro = paciente.get('createdAt')
                if data_cadastro:
                    if isinstance(data_cadastro, str):
                        data_cadastro = parser.parse(data_cadastro)
                    data_mais_recente = max(datas)
                    if hasattr(data_cadastro, 'tzinfo') and data_cadastro.tzinfo is not None:
                        data_cadastro = data_cadastro.replace(tzinfo=None)
                    if hasattr(data_mais_recente, 'tzinfo') and data_mais_recente.tzinfo is not None:
                        data_mais_recente = data_mais_recente.replace(tzinfo=None)
                    total_semanas = (data_mais_recente - data_cadastro).days // 7 + 1
                    percentual = min(100, 100 * semanas_preenchidas / total_semanas) if total_semanas > 0 else 0
                    acq_detalhes.append({
                        'paciente_id': paciente['id'],
                        'semanas_preenchidas': semanas_preenchidas,
                        'total_semanas': total_semanas,
                        'percentual': percentual
                    })
                else:
                    percentual = 0
            else:
                percentual = 0
            acq_percentuais.append(percentual)
        df_recorte['percentual_acq'] = acq_percentuais
        pacientes_com_acq = [p for p in acq_percentuais if p > 0]
        media_percentual_acq = np.mean(pacientes_com_acq) if pacientes_com_acq else 0
        total_pacientes_acq = len(pacientes_com_acq)
        total_pacientes_periodo = len(df_recorte)
        st.subheader("📝 Percentual de Semanas com ACQ Preenchido")
        col1, col2, col3 = st.columns(3)
        col1.metric("Média % semanas preenchidas", f"{media_percentual_acq:.1f}%")
        col2.metric("Pacientes com ACQ", f"{total_pacientes_acq}/{total_pacientes_periodo}")
        col3.metric("Pacientes sem ACQ", f"{total_pacientes_periodo - total_pacientes_acq}")
        if acq_detalhes:
            df_acq_detalhes = pd.DataFrame(acq_detalhes)
            st.subheader("📊 Detalhamento dos Percentuais de ACQ")
            st.dataframe(df_acq_detalhes, use_container_width=True)
        st.markdown('---')

        # --- Mapa de Calor de Correlação entre Funcionalidades ---
        st.subheader('🔥 Mapa de Calor: Correlação entre Uso de Funcionalidades')
        st.markdown('Visualização das correlações entre o uso das diferentes funcionalidades do sistema.')
        funcionalidades_cols = ['symptomDiaries', 'acqs', 'activityLogs', 'prescriptions', 'crisis']
        df_corr = pd.DataFrame()
        for col in funcionalidades_cols:
            df_corr[col] = df_recorte[col].apply(lambda x: 1 if isinstance(x, list) and len(x) > 0 else 0)
        df_corr.columns = ['Symptom Diaries', 'ACQs', 'Activity Logs', 'Prescriptions', 'Crisis']
        corr_matrix = df_corr.corr()
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            colorbar=dict(title='Correlação')
        ))
        fig_heatmap.update_layout(
            title='Correlação entre Uso de Funcionalidades',
            xaxis_title='',
            yaxis_title='',
            autosize=True
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo JSON: {e}\n\nVerifique se o arquivo segue o formato correto. Consulte o exemplo em data/README.md.")
else:
    st.info("Faça upload do arquivo JSON para visualizar os insights.") 