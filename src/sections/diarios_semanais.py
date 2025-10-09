import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_diarios_semanais(pacientes_recorte):
    st.subheader("📓 Registro de Diário de Sintomas por Semana")
    st.info("Esta seção mostra o comportamento semanal de registros de diários de sintomas: análise considera apenas pacientes com contas criadas a partir de março de 2025.")
    
    # Calcular dados semanais com usuários ativos por semana
    semanas_diarios = {}
    usuarios_por_semana_diarios = {}
    
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
        'Semana': list(semanas_diarios.keys()),
        'Média de Registros': list(semanas_diarios.values()),
        'Usuários Ativos': list(usuarios_por_semana_diarios.values())
    })
    
    # Filtrar apenas semanas com usuários ativos
    df_semanas_diarios = df_semanas_diarios[df_semanas_diarios['Usuários Ativos'] > 0]
    
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
    df_semanas_diarios['Período'] = df_semanas_diarios['Semana'].apply(formatar_periodo_semana_diarios)
    
    # Layout lado a lado
    col_graf_diarios, col_tab_diarios = st.columns([2, 1])
    
    with col_graf_diarios:
        # Gráfico de barras para diários de sintomas
        fig_diarios = px.bar(
            df_semanas_diarios,
            x='Período',
            y='Média de Registros',
            title='Média de Registros de Diários de Sintomas por Período',
            color_discrete_sequence=[CHART_COLORS[2]],
            labels={'Média de Registros': 'Média de Registros', 'Período': 'Período'}
        )
        fig_diarios.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Média de Registros de Diários"
        )
        st.plotly_chart(fig_diarios, use_container_width=True, height=400)
        
        # Gráfico adicional: Usuários ativos por período
        fig_usuarios_diarios = px.line(
            df_semanas_diarios,
            x='Período',
            y='Usuários Ativos',
            title='Evolução de Usuários Ativos por Período - Diários',
            color_discrete_sequence=[CHART_COLORS[3]]
        )
        fig_usuarios_diarios.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Número de Usuários Ativos"
        )
        st.plotly_chart(fig_usuarios_diarios, use_container_width=True, height=300)
    
    with col_tab_diarios:
        # Tabela da versão melhorada
        st.markdown("**Dados por Período - Diários de Sintomas**")
        
        # Formatar dados para exibição
        df_exibicao_diarios = df_semanas_diarios[['Período', 'Média de Registros', 'Usuários Ativos']].copy()
        df_exibicao_diarios['Média de Registros'] = df_exibicao_diarios['Média de Registros'].round(2)
        df_exibicao_diarios['Usuários Ativos'] = df_exibicao_diarios['Usuários Ativos'].astype(int)
        
        st.dataframe(
            df_exibicao_diarios,
            use_container_width=True,
            column_config={
                "Período": st.column_config.TextColumn("Período", width="medium"),
                "Média de Registros": st.column_config.NumberColumn("Média de Registros", format="%.2f", width="medium"),
                "Usuários Ativos": st.column_config.NumberColumn("Usuários Ativos", width="small")
            }
        )
        
        # Resumo estatístico
        st.markdown(f"**Total de períodos analisados: {len(df_semanas_diarios)}**")
        st.markdown(f"**Média geral de registros: {df_semanas_diarios['Média de Registros'].mean():.2f}**")
        st.markdown(f"**Pico de usuários ativos: {df_semanas_diarios['Usuários Ativos'].max()}**")
        
        # Botão de download
        csv_diarios = df_exibicao_diarios.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Dados Diários (CSV)",
            data=csv_diarios,
            file_name=f"diarios_sintomas_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---')
