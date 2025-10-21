import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_prescricoes_semanais(pacientes_recorte):
    st.info("Esta seção mostra o comportamento semanal de tomada de medicamentos: análise considera apenas pacientes com contas criadas a partir de março de 2025.")
    
    # Calcular dados semanais com usuários ativos por semana
    semanas_medicamentos = {}
    usuarios_por_semana = {}
    
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
        
        total_registros_semana = 0
        usuarios_ativos = 0
        
        for paciente in pacientes_filtrados:
            # Calcular registros de medicamentos nesta semana específica para este paciente
            prescs = paciente.get('prescriptions', [])
            registros_na_semana = 0
            
            for presc in prescs:
                for admin in presc.get('administrations', []):
                    data_admin = admin.get('date')
                    if data_admin:
                        # Dados sempre vêm como string ISO com UTC
                        if isinstance(data_admin, str):
                            data_admin = parser.parse(data_admin)
                        else:
                            continue
                            
                        if inicio_semana <= data_admin <= fim_semana:
                            registros_na_semana += 1
            
            if registros_na_semana > 0:
                total_registros_semana += registros_na_semana
                usuarios_ativos += 1
        
        semanas_medicamentos[semana] = total_registros_semana
        usuarios_por_semana[semana] = usuarios_ativos
    
    # Criar DataFrame para análise
    df_semanas = pd.DataFrame({
        'Semana': list(semanas_medicamentos.keys()),
        'Total de Registros': list(semanas_medicamentos.values()),
        'Usuários Ativos': list(usuarios_por_semana.values())
    })
    
    # Filtrar apenas semanas com usuários ativos
    df_semanas = df_semanas[df_semanas['Usuários Ativos'] > 0]
    
    # Converter números de semana para períodos de data legíveis
    def formatar_periodo_semana(semana_num):
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
    df_semanas['Período'] = df_semanas['Semana'].apply(formatar_periodo_semana)
    
    # Layout lado a lado
    col_graf_alt, col_tab_alt = st.columns([2, 1])
    
    with col_graf_alt:
        # Gráfico de barras da versão alternativa
        fig_alt = px.bar(
            df_semanas,
            x='Período',
            y='Total de Registros',
            title='Total de Registros de Medicamentos por Período',
            color_discrete_sequence=[CHART_COLORS[2]],
            labels={'Total de Registros': 'Total de Registros', 'Período': 'Período'}
        )
        fig_alt.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Total de Registros de Medicamentos"
        )
        st.plotly_chart(fig_alt, use_container_width=True, height=400)
        
        # Gráfico adicional: Usuários ativos por período
        fig_usuarios = px.line(
            df_semanas,
            x='Período',
            y='Usuários Ativos',
            title='Evolução de Usuários Ativos por Período',
            color_discrete_sequence=[CHART_COLORS[2]]
        )
        fig_usuarios.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Número de Usuários Ativos"
        )
        st.plotly_chart(fig_usuarios, use_container_width=True, height=300)
    
    with col_tab_alt:
        # Tabela da versão alternativa
        st.markdown("**Dados por Período Detalhados**")
        
        # Formatar dados para exibição
        df_exibicao = df_semanas[['Período', 'Total de Registros', 'Usuários Ativos']].copy()
        df_exibicao['Total de Registros'] = df_exibicao['Total de Registros'].astype(int)
        df_exibicao['Usuários Ativos'] = df_exibicao['Usuários Ativos'].astype(int)
        
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            column_config={
                "Período": st.column_config.TextColumn("Período", width="medium"),
                "Total de Registros": st.column_config.NumberColumn("Total de Registros", width="medium"),
                "Usuários Ativos": st.column_config.NumberColumn("Usuários Ativos", width="small")
            }
        )
        
        # Resumo estatístico
        st.markdown(f"**Total de períodos analisados: {len(df_semanas)}**")
        st.markdown(f"**Total geral de registros: {df_semanas['Total de Registros'].sum()}**")
        st.markdown(f"**Pico de registros em uma semana: {df_semanas['Total de Registros'].max()}**")
        st.markdown(f"**Pico de usuários ativos: {df_semanas['Usuários Ativos'].max()}**")
        
        # Botão de download
        csv_alt = df_exibicao.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Dados por Período (CSV)",
            data=csv_alt,
            file_name=f"medicamentos_periodos_detalhado_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---')
