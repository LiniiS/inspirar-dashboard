import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_diarios_semanais(pacientes_recorte):
    st.subheader(t('sections.diarios_semanais.title'))
    st.info(t('sections.diarios_semanais.description'))
    
    # Calcular dados semanais com usuários ativos por semana
    semanas_diarios = {}
    usuarios_por_semana_diarios = {}
    
    # Período fixo de extração dos dados
    data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
    data_fim = pd.Timestamp('2025-10-08').tz_localize('UTC')

    # pacientes_recorte já vem filtrado do dashboard.py (createdAt >= 2025-03-01)
    # Garante que todos os gráficos considerem apenas contas criadas a partir de março/2025
    pacientes_filtrados = pacientes_recorte


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
            # Calcular registros de diários nesta semana específica para este paciente
            diaries = paciente.get('symptomDiaries', [])
            registros_na_semana = 0
            
            for diary in diaries:
                data_diary = diary.get('createdAt')
                if data_diary:
                    # Dados sempre vêm como string ISO com UTC
                    if isinstance(data_diary, str):
                        data_diary = parser.parse(data_diary)
                    else:
                        continue
                        
                    if inicio_semana <= data_diary <= fim_semana:
                        registros_na_semana += 1
            
            if registros_na_semana > 0:
                registros_semana.append(registros_na_semana)
                usuarios_ativos += 1
        
        # Calcular média de registros para esta semana
        if registros_semana:
            media_registros = np.mean(registros_semana)
        else:
            media_registros = 0
            
        semanas_diarios[semana] = media_registros
        usuarios_por_semana_diarios[semana] = usuarios_ativos
    
    # Criar DataFrame para análise
    df_semanas_diarios = pd.DataFrame({
        'Week': list(semanas_diarios.keys()),
        'Average Records': list(semanas_diarios.values()),
        'Active Users': list(usuarios_por_semana_diarios.values())
    })
    
    # Filtrar apenas semanas com usuários ativos
    df_semanas_diarios = df_semanas_diarios[df_semanas_diarios['Active Users'] > 0]
    
    # Converter números de semana para períodos de data legíveis
    def formatar_periodo_semana_diarios(semana_num):
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
    df_semanas_diarios['Period'] = df_semanas_diarios['Week'].apply(formatar_periodo_semana_diarios)
    
    # Layout lado a lado
    col_graf_diarios, col_tab_diarios = st.columns([2, 1])
    
    with col_graf_diarios:
        # Gráfico de barras para diários de sintomas
        fig_diarios = px.bar(
            df_semanas_diarios,
            x='Period',
            y='Average Records',
            title=t('charts.titles.diaries_by_week'),
            color_discrete_sequence=[CHART_COLORS[2]],
            labels={'Average Records': t('charts.labels.average_records'), 'Period': t('charts.labels.period')}
        )
        fig_diarios.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('charts.labels.period'),
            yaxis_title=t('charts.labels.average_records')
        )
        st.plotly_chart(fig_diarios, use_container_width=True, height=400)
        
        # Gráfico adicional: Usuários ativos por período
        fig_usuarios_diarios = px.line(
            df_semanas_diarios,
            x='Period',
            y='Active Users',
            title=t('sections.diarios_semanais.active_users_evolution'),
            color_discrete_sequence=[CHART_COLORS[3]]
        )
        fig_usuarios_diarios.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('charts.labels.period'),
            yaxis_title=t('charts.labels.active_users')
        )
        st.plotly_chart(fig_usuarios_diarios, use_container_width=True, height=300)
    
    with col_tab_diarios:
        # Tabela da versão melhorada
        st.markdown(f"**{t('sections.diarios_semanais.data_by_period')}**")
        
        # Formatar dados para exibição
        df_exibicao_diarios = df_semanas_diarios[['Period', 'Average Records', 'Active Users']].copy()
        df_exibicao_diarios['Average Records'] = df_exibicao_diarios['Average Records'].round(2)
        df_exibicao_diarios['Active Users'] = df_exibicao_diarios['Active Users'].astype(int)
        
        st.dataframe(
            df_exibicao_diarios,
            use_container_width=True,
            column_config={
                "Period": st.column_config.TextColumn(t('tables.period'), width="medium"),
                "Average Records": st.column_config.NumberColumn(t('tables.average_records'), format="%.2f", width="medium"),
                "Active Users": st.column_config.NumberColumn(t('tables.active_users'), width="small")
            }
        )
        
        # Resumo estatístico
        st.markdown(f"**{t('sections.diarios_semanais.total_periods')}: {len(df_semanas_diarios)}**")
        st.markdown(f"**{t('sections.diarios_semanais.overall_average')}: {df_semanas_diarios['Average Records'].mean():.2f}**")
        st.markdown(f"**{t('sections.diarios_semanais.peak_active_users')}: {df_semanas_diarios['Active Users'].max()}**")
        
        # Botão de download
        csv_diarios = df_exibicao_diarios.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=t('sections.diarios_semanais.download_csv'),
            data=csv_diarios,
            file_name=f"diarios_sintomas_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---')
