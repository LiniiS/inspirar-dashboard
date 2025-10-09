import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_atividades_semanais(pacientes_recorte):
    st.subheader("🏃 Registro de Atividade Física por Semana")
    st.info("Esta seção mostra o comportamento semanal de registros de atividades físicas: análise considera apenas pacientes com contas criadas a partir de março de 2025.")
    
    # Calcular dados semanais com usuários ativos por semana
    semanas_atividades = {}
    usuarios_por_semana_atividades = {}
    
    # Período fixo de extração dos dados
    data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
    data_fim = pd.Timestamp('2025-10-08').tz_localize('UTC')

    # Filtrar pacientes criados a partir de março de 2025
    pacientes_filtrados = []
    data_limite = pd.Timestamp('2025-03-01').tz_localize('UTC')
    for paciente in pacientes_recorte:
        data_cadastro = paciente.get('createdAt')
        if data_cadastro:
            if isinstance(data_cadastro, str):
                data_cadastro = parser.parse(data_cadastro)
            if data_cadastro >= data_limite:
                pacientes_filtrados.append(paciente)

    st.info(f"Pacientes incluídos na análise: {len(pacientes_filtrados)} (contas criadas a partir de março de 2025)")

    # Para cada semana no período
    for semana in range(53):  # Máximo de semanas no ano
        semana_data = data_inicio + pd.Timedelta(weeks=semana)
        if semana_data > data_fim:
            break
            
        # Calcular início e fim da semana
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        
        # Normalizar timezone para UTC
        if inicio_semana.tz is None:
            inicio_semana = inicio_semana.tz_localize('UTC')
        if fim_semana.tz is None:
            fim_semana = fim_semana.tz_localize('UTC')
        
        registros_semana = []
        usuarios_ativos = 0
        
        for paciente in pacientes_filtrados:
            # Calcular registros de atividades nesta semana específica para este paciente
            activities = paciente.get('activityLogs', [])
            registros_na_semana = 0
            
            for activity in activities:
                data_activity = activity.get('createdAt')
                if data_activity:
                    # Dados sempre vêm como string ISO com UTC
                    if isinstance(data_activity, str):
                        data_activity = parser.parse(data_activity)
                    else:
                        continue
                        
                    if inicio_semana <= data_activity <= fim_semana:
                        registros_na_semana += 1
            
            if registros_na_semana > 0:
                registros_semana.append(registros_na_semana)
                usuarios_ativos += 1
        
        # Calcular média de registros para esta semana
        if registros_semana:
            media_registros = np.mean(registros_semana)
        else:
            media_registros = 0
            
        semanas_atividades[semana] = media_registros
        usuarios_por_semana_atividades[semana] = usuarios_ativos
    
    # Criar DataFrame para análise
    df_semanas_atividades = pd.DataFrame({
        'Semana': list(semanas_atividades.keys()),
        'Média de Registros': list(semanas_atividades.values()),
        'Usuários Ativos': list(usuarios_por_semana_atividades.values())
    })
    
    # Filtrar apenas semanas com usuários ativos
    df_semanas_atividades = df_semanas_atividades[df_semanas_atividades['Usuários Ativos'] > 0]
    
    # Converter números de semana para períodos de data legíveis
    def formatar_periodo_semana_atividades(semana_num):
        # Calcular a data da semana
        semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
        # Calcular início e fim da semana
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        
        # Formatar para exibição
        mes_inicio = inicio_semana.strftime('%b')  # Abr, Mai, Jun, etc.
        mes_fim = fim_semana.strftime('%b')
        
        if mes_inicio == mes_fim:
            return f"{mes_inicio} {inicio_semana.day}-{fim_semana.day}"
        else:
            return f"{mes_inicio} {inicio_semana.day} - {mes_fim} {fim_semana.day}"
    
    # Aplicar formatação
    df_semanas_atividades['Período'] = df_semanas_atividades['Semana'].apply(formatar_periodo_semana_atividades)
    
    # Layout lado a lado
    col_graf_atividades, col_tab_atividades = st.columns([2, 1])
    
    with col_graf_atividades:
        # Gráfico de barras para atividades físicas
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
        
        # Gráfico adicional: Usuários ativos por período
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
    
    with col_tab_atividades:
        # Tabela da versão melhorada
        st.markdown("**Dados por Período - Atividades Físicas**")
        
        # Formatar dados para exibição
        df_exibicao_atividades = df_semanas_atividades[['Período', 'Média de Registros', 'Usuários Ativos']].copy()
        df_exibicao_atividades['Média de Registros'] = df_exibicao_atividades['Média de Registros'].round(2)
        df_exibicao_atividades['Usuários Ativos'] = df_exibicao_atividades['Usuários Ativos'].astype(int)
        
        st.dataframe(
            df_exibicao_atividades,
            use_container_width=True,
            column_config={
                "Período": st.column_config.TextColumn("Período", width="medium"),
                "Média de Registros": st.column_config.NumberColumn("Média de Registros", format="%.2f", width="medium"),
                "Usuários Ativos": st.column_config.NumberColumn("Usuários Ativos", width="small")
            }
        )
        
        # Resumo estatístico
        st.markdown(f"**Total de períodos analisados: {len(df_semanas_atividades)}**")
        st.markdown(f"**Média geral de registros: {df_semanas_atividades['Média de Registros'].mean():.2f}**")
        st.markdown(f"**Pico de usuários ativos: {df_semanas_atividades['Usuários Ativos'].max()}**")
        
        # Botão de download
        csv_atividades = df_exibicao_atividades.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Dados Atividades (CSV)",
            data=csv_atividades,
            file_name=f"atividades_fisicas_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---')
