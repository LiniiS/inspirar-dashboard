import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_atividades_semanais(pacientes_recorte):
    st.subheader("Registro de Atividade Física por Semana")
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

        # Gráfico de Barras - Média de Passos por Semana
        if not df_semanas_atividades.empty:
            fig_barras_passos = px.bar(
                df_semanas_atividades,
                x='Período',
                y='Passos médios por usuário ativo',
                title='Média de Passos por Usuário Ativo por Período',
                color_discrete_sequence=[CHART_COLORS[2]],
                labels={
                    'Passos médios por usuário ativo': 'Média de Passos',
                    'Período': 'Período'
                }
            )
            fig_barras_passos.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Período",
                yaxis_title="Média de Passos por Usuário",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_barras_passos, use_container_width=True, height=400)
        else:
            st.info("Sem semanas com usuários ativos para exibir no gráfico.")
        
        # Novo gráfico: Passos diários de um paciente específico
        st.markdown("---")
        st.markdown("### Análise Individual de Passos Diários")
        
        # Obter lista de IDs dos pacientes
        ids_pacientes = [p.get('id', 'N/A') for p in pacientes_filtrados if p.get('id')]
        ids_pacientes = [id_p for id_p in ids_pacientes if id_p != 'N/A']
        
        if ids_pacientes:
            # Seletor de paciente
            paciente_selecionado = st.selectbox(
                "Selecione o paciente pelo ID:",
                ids_pacientes,
                index=0
            )
            
            # Seletor de mês
            meses_disponiveis = [
                "Março 2025", "Abril 2025", "Maio 2025", "Junho 2025",
                "Julho 2025", "Agosto 2025", "Setembro 2025", "Outubro 2025"
            ]
            
            mes_selecionado = st.selectbox(
                "Selecione o mês:",
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
                        title=f'Passos Diários - Paciente {paciente_selecionado} - {mes_selecionado}',
                        color_discrete_sequence=[CHART_COLORS[3]],
                        markers=True
                    )
                    fig_diario.update_layout(
                        height=400,
                        margin=dict(l=50, r=50, t=80, b=50),
                        xaxis_title="Dia do Mês",
                        yaxis_title="Total de Passos",
                        xaxis=dict(tickmode='linear', dtick=1)
                    )
                    st.plotly_chart(fig_diario, use_container_width=True, height=400)
                    
                    # Estatísticas do mês
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Passos no Mês", f"{passos_por_dia['passos'].sum():,}")
                    with col2:
                        st.metric("Média Diária", f"{passos_por_dia['passos'].mean():.0f}")
                    with col3:
                        st.metric("Dia com Mais Passos", f"{passos_por_dia['passos'].max():,}")
                    
                    # Tabela com dados diários
                    st.markdown("**Dados Diários Detalhados:**")
                    passos_por_dia['Dia'] = passos_por_dia['dia']
                    passos_por_dia['Passos'] = passos_por_dia['passos']
                    st.dataframe(
                        passos_por_dia[['Dia', 'Passos']],
                        use_container_width=True,
                        column_config={
                            "Dia": st.column_config.NumberColumn("Dia", width="small"),
                            "Passos": st.column_config.NumberColumn("Passos", format="%,d", width="medium")
                        }
                    )
                else:
                    st.warning(f"Nenhuma atividade registrada para o paciente {paciente_selecionado} em {mes_selecionado}.")
        else:
            st.warning("Nenhum paciente encontrado com ID válido.")

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
