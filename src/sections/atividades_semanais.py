import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_atividades_semanais(pacientes_recorte):
    st.subheader(t('sections.atividades_semanais.title'))
    st.info(t('sections.atividades_semanais.description'))
    
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
    data_fim = st.session_state.get('data_fim', pd.Timestamp.now(tz='UTC'))

    # pacientes_recorte já vem filtrado do dashboard.py (createdAt >= 2025-03-01)
    # Garante que todos os gráficos considerem apenas contas criadas a partir de março/2025
    pacientes_filtrados = pacientes_recorte


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
        'Week': list(semanas_atividades.keys()),
        'Average Records': list(semanas_atividades.values()),
        'Active Users': list(usuarios_por_semana_atividades.values()),
        'Total Steps': list(passos_por_semana.values())
    })

    # Filtrar semanas com atividade
    df_semanas_atividades = df_semanas_atividades[df_semanas_atividades['Active Users'] > 0]

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

    df_semanas_atividades['Period'] = df_semanas_atividades['Week'].apply(formatar_periodo_semana_atividades)
    df_semanas_atividades['Average Steps per Active User'] = (
        df_semanas_atividades['Total Steps'] / df_semanas_atividades['Active Users']
    ).fillna(0).round(0).astype(int)

    # Layout
    col_graf_atividades, col_tab_atividades = st.columns([2, 1])

    with col_graf_atividades:
        # Barras: média de registros
        fig_atividades = px.bar(
            df_semanas_atividades,
            x='Period',
            y='Average Records',
            title=t('charts.titles.activities_by_week'),
            color_discrete_sequence=[CHART_COLORS[2]],
            labels={'Average Records': t('charts.labels.average_records'), 'Period': t('charts.labels.period')}
        )
        fig_atividades.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('charts.labels.period'),
            yaxis_title=t('charts.labels.average_records')
        )
        st.plotly_chart(fig_atividades, use_container_width=True, height=400)

        # Linha: usuários ativos
        fig_usuarios_atividades = px.line(
            df_semanas_atividades,
            x='Period',
            y='Active Users',
            title=t('sections.atividades_semanais.active_users_evolution'),
            color_discrete_sequence=[CHART_COLORS[2]]
        )
        fig_usuarios_atividades.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('charts.labels.period'),
            yaxis_title=t('charts.labels.active_users')
        )
        st.plotly_chart(fig_usuarios_atividades, use_container_width=True, height=300)

        # Gráfico de Barras - Média de Passos por Semana
        if not df_semanas_atividades.empty:
            fig_barras_passos = px.bar(
                df_semanas_atividades,
                x='Period',
                y='Average Steps per Active User',
                title=t('charts.titles.steps_by_week'),
                color_discrete_sequence=[CHART_COLORS[2]],
                labels={
                    'Average Steps per Active User': t('charts.labels.total_steps'),
                    'Period': t('charts.labels.period')
                }
            )
            fig_barras_passos.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title=t('charts.labels.period'),
                yaxis_title=t('charts.labels.total_steps'),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_barras_passos, use_container_width=True, height=400)
        else:
            st.info(t('sections.atividades_semanais.no_weeks'))
        
        # Novo gráfico: Passos diários de um paciente específico
        st.markdown("---")
        st.markdown(f"### {t('sections.atividades_semanais.individual_analysis')}")
        
        # Obter lista de IDs dos pacientes
        ids_pacientes = [p.get('id', 'N/A') for p in pacientes_filtrados if p.get('id')]
        ids_pacientes = [id_p for id_p in ids_pacientes if id_p != 'N/A']
        
        if ids_pacientes:
            # Seletor de paciente
            paciente_selecionado = st.selectbox(
                t('sections.atividades_semanais.select_patient'),
                ids_pacientes,
                index=0
            )
            
            # Seletor de mês
            meses_disponiveis = [
                "March 2025", "April 2025", "May 2025", "June 2025",
                "July 2025", "August 2025", "September 2025", "October 2025"
            ]
            
            mes_selecionado = st.selectbox(
                t('sections.atividades_semanais.select_month'),
                meses_disponiveis,
                index=0
            )
            
            # Converter mês para período
            mes_num = meses_disponiveis.index(mes_selecionado) + 3  # Março = 3
            ano = 2025
            
            # Calcular início e fim do mês
            inicio_mes = pd.Timestamp(f'{ano}-{mes_num:02d}-01').tz_localize('UTC')
            if mes_num == 12:
                fim_mes = pd.Timestamp(f'{ano+1}-01-01').tz_localize('UTC') - pd.Timedelta(days=1)
            else:
                fim_mes = pd.Timestamp(f'{ano}-{mes_num+1:02d}-01').tz_localize('UTC') - pd.Timedelta(days=1)
            
            # Encontrar o paciente selecionado
            paciente_dados = None
            for p in pacientes_filtrados:
                if p.get('id') == paciente_selecionado:
                    paciente_dados = p
                    break
            
            if paciente_dados:
                # Extrair atividades do paciente no mês selecionado
                atividades_mes = []
                activities = paciente_dados.get('activityLogs', []) or []
                
                for activity in activities:
                    data_activity = safe_parse_dt(activity.get('createdAt'))
                    if data_activity and inicio_mes <= data_activity <= fim_mes:
                        passos = extrair_passos(activity)
                        atividades_mes.append({
                            'data': data_activity,
                            'passos': passos
                        })
                
                if atividades_mes:
                    # Criar DataFrame com dados diários
                    df_diario = pd.DataFrame(atividades_mes)
                    df_diario['data'] = pd.to_datetime(df_diario['data'])
                    df_diario['dia'] = df_diario['data'].dt.day
                    
                    # Agrupar por dia e somar passos
                    passos_por_dia = df_diario.groupby('dia')['passos'].sum().reset_index()
                    
                    # Criar gráfico de linha para passos diários
                    fig_diario = px.line(
                        passos_por_dia,
                        x='dia',
                        y='passos',
                        title=f'Daily Steps - Patient {paciente_selecionado} - {mes_selecionado}',
                        color_discrete_sequence=[CHART_COLORS[3]],
                        markers=True
                    )
                    fig_diario.update_layout(
                        height=400,
                        margin=dict(l=50, r=50, t=80, b=50),
                        xaxis_title="Day of Month",
                        yaxis_title="Total Steps",
                        xaxis=dict(tickmode='linear', dtick=1)
                    )
                    st.plotly_chart(fig_diario, use_container_width=True, height=400)
                    
                    # Estatísticas do mês
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Steps in Month", f"{passos_por_dia['passos'].sum():,}")
                    with col2:
                        st.metric("Daily Average", f"{passos_por_dia['passos'].mean():.0f}")
                    with col3:
                        st.metric("Day with Most Steps", f"{passos_por_dia['passos'].max():,}")
                    
                    # Tabela com dados diários
                    st.markdown(f"**{t('sections.atividades_semanais.detailed_daily_data')}**")
                    passos_por_dia['Day'] = passos_por_dia['dia']
                    passos_por_dia['Steps'] = passos_por_dia['passos']
                    st.dataframe(
                        passos_por_dia[['Day', 'Steps']],
                        use_container_width=True,
                        column_config={
                            "Day": st.column_config.NumberColumn("Day", width="small"),
                            "Steps": st.column_config.NumberColumn("Steps", format="%,d", width="medium")
                        }
                    )
                else:
                    st.warning(t('sections.atividades_semanais.no_activity_patient', patient=paciente_selecionado, month=mes_selecionado))
        else:
            st.warning(t('sections.atividades_semanais.no_patient_found'))

    with col_tab_atividades:
        st.markdown(f"**{t('sections.atividades_semanais.data_by_period')}**")
        df_exibicao_atividades = df_semanas_atividades[
            ['Period', 'Week', 'Average Records', 'Active Users', 'Total Steps', 'Average Steps per Active User']
        ].copy()
        df_exibicao_atividades['Average Records'] = df_exibicao_atividades['Average Records'].round(2)
        df_exibicao_atividades['Active Users'] = df_exibicao_atividades['Active Users'].astype(int)

        st.dataframe(
            df_exibicao_atividades,
            use_container_width=True,
            column_config={
                "Period": st.column_config.TextColumn(t('tables.period'), width="medium"),
                "Week": st.column_config.NumberColumn(t('charts.labels.week'), width="small"),
                "Average Records": st.column_config.NumberColumn(t('tables.average_records'), format="%.2f", width="medium"),
                "Active Users": st.column_config.NumberColumn(t('tables.active_users'), width="small"),
                "Total Steps": st.column_config.NumberColumn(t('tables.total_steps'), format="%,d", width="medium"),
                "Average Steps per Active User": st.column_config.NumberColumn("Avg Steps/User", format="%,d", width="medium"),
            }
        )

        st.markdown(f"**{t('sections.atividades_semanais.total_periods')}: {len(df_semanas_atividades)}**")
        st.markdown(f"**{t('sections.atividades_semanais.overall_average')}: {df_semanas_atividades['Average Records'].mean():.2f}**")
        st.markdown(f"**{t('sections.atividades_semanais.peak_active_users')}: {df_semanas_atividades['Active Users'].max()}**")
        st.markdown(f"**{t('sections.atividades_semanais.highest_steps')}: {df_semanas_atividades['Total Steps'].max():,}**")

        csv_atividades = df_exibicao_atividades.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=t('sections.atividades_semanais.download_csv'),
            data=csv_atividades,
            file_name=f"atividades_fisicas_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    st.markdown('---')
