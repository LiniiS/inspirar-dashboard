import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS

def mostrar_prescricoes_semanais(pacientes_recorte):
    st.subheader("💉 Registro de Tomada de Medicamento por Semana")
    st.info("Esta seção mostra o comportamento semanal de tomada de medicamentos: para cada período, calcula a média de registros de medicamentos considerando apenas os usuários que já estavam cadastrados naquele período.")
    
    # Calcular dados semanais com usuários ativos por semana
    semanas_medicamentos = {}
    usuarios_por_semana = {}
    
    # Definir período de análise (março a setembro 2025)
    data_inicio = pd.Timestamp('2025-03-01')
    data_fim = pd.Timestamp('2025-09-30')
    
    # Para cada semana no período
    for semana in range(53):  # Máximo de semanas no ano
        semana_data = data_inicio + pd.Timedelta(weeks=semana)
        if semana_data > data_fim:
            break
            
        # Calcular início e fim da semana
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        
        # Normalizar timezone para UTC
        inicio_semana = inicio_semana.tz_localize('UTC')
        fim_semana = fim_semana.tz_localize('UTC')
        
        registros_semana = []
        usuarios_ativos = 0
        
        for paciente in pacientes_recorte:
            # Verificar se o paciente já estava cadastrado nesta semana
            data_cadastro = paciente.get('createdAt')
            if data_cadastro:
                # Verificar se já é um Timestamp ou se precisa fazer parsing
                if isinstance(data_cadastro, str):
                    data_cadastro = parser.parse(data_cadastro)
                elif not isinstance(data_cadastro, pd.Timestamp):
                    continue
                
                # Converter para pandas Timestamp se for datetime.datetime
                if not isinstance(data_cadastro, pd.Timestamp):
                    data_cadastro = pd.Timestamp(data_cadastro)
                
                # Normalizar timezone para UTC
                if data_cadastro.tz is None:
                    data_cadastro = data_cadastro.tz_localize('UTC')
                else:
                    data_cadastro = data_cadastro.tz_convert('UTC')
                    
                if data_cadastro <= fim_semana:
                    usuarios_ativos += 1
                    
                    # Calcular registros de medicamentos nesta semana específica
                    prescs = paciente.get('prescriptions', [])
                    registros_na_semana = 0
                    
                    for presc in prescs:
                        for admin in presc.get('administrations', []):
                            data_admin = admin.get('date')
                            if data_admin:
                                # Verificar se já é um Timestamp ou se precisa fazer parsing
                                if isinstance(data_admin, str):
                                    data_admin = parser.parse(data_admin)
                                elif not isinstance(data_admin, pd.Timestamp):
                                    continue
                                
                                # Converter para pandas Timestamp se for datetime.datetime
                                if not isinstance(data_admin, pd.Timestamp):
                                    data_admin = pd.Timestamp(data_admin)
                                
                                # Normalizar timezone para UTC
                                if data_admin.tz is None:
                                    data_admin = data_admin.tz_localize('UTC')
                                else:
                                    data_admin = data_admin.tz_convert('UTC')
                                    
                                if inicio_semana <= data_admin <= fim_semana:
                                    registros_na_semana += 1
                    
                    if registros_na_semana > 0:
                        registros_semana.append(registros_na_semana)
        
        # Calcular média de registros para esta semana
        if registros_semana:
            media_registros = np.mean(registros_semana)
        else:
            media_registros = 0
            
        semanas_medicamentos[semana] = media_registros
        usuarios_por_semana[semana] = usuarios_ativos
    
    # Criar DataFrame para análise
    df_semanas = pd.DataFrame({
        'Semana': list(semanas_medicamentos.keys()),
        'Média de Registros': list(semanas_medicamentos.values()),
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
            y='Média de Registros',
            title='Média de Registros de Medicamentos por Período',
            color_discrete_sequence=[CHART_COLORS[0]],
            labels={'Média de Registros': 'Média de Registros', 'Período': 'Período'}
        )
        fig_alt.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Período",
            yaxis_title="Média de Registros de Medicamentos"
        )
        st.plotly_chart(fig_alt, use_container_width=True, height=400)
        
        # Gráfico adicional: Usuários ativos por período
        fig_usuarios = px.line(
            df_semanas,
            x='Período',
            y='Usuários Ativos',
            title='Evolução de Usuários Ativos por Período',
            color_discrete_sequence=[CHART_COLORS[1]]
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
        df_exibicao = df_semanas[['Período', 'Média de Registros', 'Usuários Ativos']].copy()
        df_exibicao['Média de Registros'] = df_exibicao['Média de Registros'].round(2)
        df_exibicao['Usuários Ativos'] = df_exibicao['Usuários Ativos'].astype(int)
        
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            column_config={
                "Período": st.column_config.TextColumn("Período", width="medium"),
                "Média de Registros": st.column_config.NumberColumn("Média de Registros", format="%.2f", width="medium"),
                "Usuários Ativos": st.column_config.NumberColumn("Usuários Ativos", width="small")
            }
        )
        
        # Resumo estatístico
        st.markdown(f"**Total de períodos analisados: {len(df_semanas)}**")
        st.markdown(f"**Média geral de registros: {df_semanas['Média de Registros'].mean():.2f}**")
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
