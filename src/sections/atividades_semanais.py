import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_atividades_semanais(pacientes_recorte):
    st.subheader("🏃 Registro de Atividade Física por Semana")
    st.info("Esta seção mostra o comportamento semanal de registros de atividades físicas: análise considera apenas pacientes com contas criadas a partir de março de 2025.")
    
    # --- Helpers ---------------------------------------------------------
    def safe_parse_dt(dt):
        if not dt:
            return None
        if isinstance(dt, str):
            try:
                return parser.parse(dt)
            except Exception:
                return None
        return dt

    def extrair_passos(activity: dict) -> int:
        """
        Tenta capturar o total de passos do registro de atividade.
        Lida com chaves comuns: 'steps', 'stepCount', 'totalSteps', 'passos', etc.
        Se não houver, retorna 0.
        """
        candidatas = ['steps', 'stepCount', 'totalSteps', 'passos', 'total_passos', 'quantity', 'count']
        for k in candidatas:
            v = activity.get(k)
            if isinstance(v, (int, float)):
                return int(v)
        # Alguns modelos guardam em 'data' / 'attributes'
        for cont_key in ['data', 'attributes', 'payload']:
            cont = activity.get(cont_key)
            if isinstance(cont, dict):
                for k in candidatas:
                    v = cont.get(k)
                    if isinstance(v, (int, float)):
                        return int(v)
        return 0
    # --------------------------------------------------------------------

    # Estruturas de acumulação
    semanas_atividades = {}
    usuarios_por_semana_atividades = {}
    passos_por_semana = {}

    # Janela fixa de análise
    data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
    data_fim = pd.Timestamp('2025-10-08').tz_localize('UTC')

    # Filtrar pacientes criados a partir de março de 2025
    pacientes_filtrados = []
    data_limite = pd.Timestamp('2025-03-01').tz_localize('UTC')
    for paciente in pacientes_recorte:
        data_cadastro = safe_parse_dt(paciente.get('createdAt'))
        if data_cadastro and data_cadastro >= data_limite:
            pacientes_filtrados.append(paciente)

    st.info(f"Pacientes incluídos na análise: {len(pacientes_filtrados)} (contas criadas a partir de março de 2025)")

    # Loop semanal
    for semana in range(53):
        semana_data = data_inicio + pd.Timedelta(weeks=semana)
        if semana_data > data_fim:
            break

        # início/fim da semana (seg–dom)
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        if inicio_semana.tz is None:
            inicio_semana = inicio_semana.tz_localize('UTC')
        if fim_semana.tz is None:
            fim_semana = fim_semana.tz_localize('UTC')

        registros_semana = []
        usuarios_ativos = 0
        total_passos_semana = 0

        for paciente in pacientes_filtrados:
            activities = paciente.get('activityLogs', []) or []
            registros_na_semana = 0
            passos_paciente_semana = 0

            for activity in activities:
                data_activity = safe_parse_dt(activity.get('createdAt'))
                if data_activity and (inicio_semana <= data_activity <= fim_semana):
                    registros_na_semana += 1
                    passos_paciente_semana += extrair_passos(activity)

            if registros_na_semana > 0:
                registros_semana.append(registros_na_semana)
                usuarios_ativos += 1
                total_passos_semana += passos_paciente_semana

        media_registros = np.mean(registros_semana) if registros_semana else 0
        semanas_atividades[semana] = media_registros
        usuarios_por_semana_atividades[semana] = usuarios_ativos
        passos_por_semana[semana] = int(total_passos_semana)

    # DataFrame base
    df_semanas_atividades = pd.DataFrame({
        'Semana': list(semanas_atividades.keys()),
        'Média de Registros': list(semanas_atividades.values()),
        'Usuários Ativos': list(usuarios_por_semana_atividades.values()),
        'Total de Passos': list(passos_por_semana.values())
    })

    # Filtrar semanas com atividade
    df_semanas_atividades = df_semanas_atividades[df_semanas_atividades['Usuários Ativos'] > 0]

    # Período legível
    def formatar_periodo_semana_atividades(semana_num):
        semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        mes_inicio = inicio_semana.strftime('%b')
        mes_fim = fim_semana.strftime('%b')
        if mes_inicio == mes_fim:
            return f"{mes_inicio} {inicio_semana.day}-{fim_semana.day}"
        else:
            return f"{mes_inicio} {inicio_semana.day} - {mes_fim} {fim_semana.day}"

    df_semanas_atividades['Período'] = df_semanas_atividades['Semana'].apply(formatar_periodo_semana_atividades)
    df_semanas_atividades['Passos médios por usuário ativo'] = (
        df_semanas_atividades['Total de Passos'] / df_semanas_atividades['Usuários Ativos']
    ).fillna(0).round(0).astype(int)

    # Layout
    col_graf_atividades, col_tab_atividades = st.columns([2, 1])

    with col_graf_atividades:
        # Barras: média de registros
        fig_atividades = px.bar(
            df_semanas_atividades,
            x='Período',
            y='Média de Registros',
            title='Média de Registros de Atividades Físicas por Período',
            color_discrete_sequence=[CHART_COLORS[2]],
            labels={'Média de Registros': 'Média de Registros', 'Período': 'Período'}
        )
        fig_atividades.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Média de Registros de Atividades"
        )
        st.plotly_chart(fig_atividades, use_container_width=True, height=400)

        # Linha: usuários ativos
        fig_usuarios_atividades = px.line(
            df_semanas_atividades,
            x='Período',
            y='Usuários Ativos',
            title='Evolução de Usuários Ativos por Período - Atividades',
            color_discrete_sequence=[CHART_COLORS[2]]
        )
        fig_usuarios_atividades.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Número de Usuários Ativos"
        )
        st.plotly_chart(fig_usuarios_atividades, use_container_width=True, height=300)

        # Gráfico de Bolhas — x: número da Semana, y: Usuários Ativos, raio: Total de Passos
        if not df_semanas_atividades.empty:
            max_area_px = 60  # diâmetro máximo (px)
            max_passos = max(1, df_semanas_atividades['Total de Passos'].max())
            sizeref = 2.0 * max_passos / (max_area_px ** 2)

            fig_bolhas = px.scatter(
                df_semanas_atividades,
                x='Semana',
                y='Usuários Ativos',
                size='Total de Passos',            
                size_max=max_area_px,
                title='Bolhas Semanais: Usuários Ativos × Total de Passos',
                color_discrete_sequence=[CHART_COLORS[5]], 
                labels={'Semana': 'Semana (nº)', 'Usuários Ativos': 'Pessoas'},
                hover_data={
                    'Período': True,
                    'Média de Registros': ':.2f',
                    'Total de Passos': ':,',
                    'Passos médios por usuário ativo': ':,',
                    'Semana': False  
                }
            )
            # Força a referência de área para manter a leitura do raio
            fig_bolhas.update_traces(marker=dict(sizeref=sizeref, sizemode='area', opacity=0.75, line_width=0.5))
            fig_bolhas.update_layout(
                height=420,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Semana (número desde 01/03/2025)",
                yaxis_title="Usuários Ativos",
            )
            st.plotly_chart(fig_bolhas, use_container_width=True, height=420)
        else:
            st.info("Sem semanas com usuários ativos para exibir no gráfico de bolhas.")

    with col_tab_atividades:
        st.markdown("**Dados por Período - Atividades Físicas**")
        df_exibicao_atividades = df_semanas_atividades[
            ['Período', 'Semana', 'Média de Registros', 'Usuários Ativos', 'Total de Passos', 'Passos médios por usuário ativo']
        ].copy()
        df_exibicao_atividades['Média de Registros'] = df_exibicao_atividades['Média de Registros'].round(2)
        df_exibicao_atividades['Usuários Ativos'] = df_exibicao_atividades['Usuários Ativos'].astype(int)

        st.dataframe(
            df_exibicao_atividades,
            use_container_width=True,
            column_config={
                "Período": st.column_config.TextColumn("Período", width="medium"),
                "Semana": st.column_config.NumberColumn("Semana", width="small"),
                "Média de Registros": st.column_config.NumberColumn("Média de Registros", format="%.2f", width="medium"),
                "Usuários Ativos": st.column_config.NumberColumn("Usuários Ativos", width="small"),
                "Total de Passos": st.column_config.NumberColumn("Total de Passos", format="%,d", width="medium"),
                "Passos médios por usuário ativo": st.column_config.NumberColumn("Passos médios/usuário", format="%,d", width="medium"),
            }
        )

        st.markdown(f"**Total de períodos analisados:** {len(df_semanas_atividades)}")
        st.markdown(f"**Média geral de registros:** {df_semanas_atividades['Média de Registros'].mean():.2f}")
        st.markdown(f"**Pico de usuários ativos:** {df_semanas_atividades['Usuários Ativos'].max()}")
        st.markdown(f"**Maior total de passos em uma semana:** {df_semanas_atividades['Total de Passos'].max():,}")

        csv_atividades = df_exibicao_atividades.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Dados Atividades (CSV)",
            data=csv_atividades,
            file_name=f"atividades_fisicas_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    st.markdown('---')
