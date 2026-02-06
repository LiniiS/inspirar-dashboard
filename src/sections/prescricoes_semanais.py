import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from dateutil import parser
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_prescricoes_semanais(pacientes_recorte):
    st.info(t('sections.prescricoes_semanais.description'))
    
    # Período fixo de extração dos dados
    data_inicio = pd.Timestamp('2025-03-01').tz_localize('UTC')
    data_fim = st.session_state.get('data_fim', pd.Timestamp.now(tz='UTC'))

    # pacientes_recorte já vem filtrado do dashboard.py (createdAt >= 2025-03-01)
    # Garante que todos os gráficos considerem apenas contas criadas a partir de março/2025
    pacientes_filtrados = pacientes_recorte
    
    # Converter números de semana para períodos de data legíveis
    def formatar_periodo_semana(semana_num):
        semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        mes_inicio = inicio_semana.strftime('%b')
        mes_fim = fim_semana.strftime('%b')
        if mes_inicio == mes_fim:
            return f"{mes_inicio} {inicio_semana.day}-{fim_semana.day}"
        else:
            return f"{mes_inicio} {inicio_semana.day} - {mes_fim} {fim_semana.day}"
    
    # Criar tabs para separar as duas análises
    tab1, tab2 = st.tabs([t('sections.prescricoes_semanais.tab_administrations'), t('sections.prescricoes_semanais.tab_prescriptions')])
    
    # ========== TAB 1: ADMINISTRATIONS BY WEEK ==========
    with tab1:
        st.subheader(t('sections.prescricoes_semanais.admin_title'))
        st.info(t('sections.prescricoes_semanais.admin_info'))
        
        # Calcular dados semanais de administrations
        semanas_administrations = {}
        usuarios_por_semana_admin = {}
        
        for semana in range(53):
            semana_data = data_inicio + pd.Timedelta(weeks=semana)
            if semana_data > data_fim:
                break
                
            inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
            fim_semana = inicio_semana + pd.Timedelta(days=6)
            
            if inicio_semana.tz is None:
                inicio_semana = inicio_semana.tz_localize('UTC')
            if fim_semana.tz is None:
                fim_semana = fim_semana.tz_localize('UTC')
            
            total_admin_semana = 0
            usuarios_ativos = 0
            
            for paciente in pacientes_filtrados:
                prescs = paciente.get('prescriptions', [])
                admin_na_semana = 0
                
                for presc in prescs:
                    for admin in presc.get('administrations', []):
                        data_admin = admin.get('date')
                        if data_admin:
                            if isinstance(data_admin, str):
                                data_admin = parser.parse(data_admin)
                            else:
                                continue
                                
                            if inicio_semana <= data_admin <= fim_semana:
                                admin_na_semana += 1
                
                if admin_na_semana > 0:
                    total_admin_semana += admin_na_semana
                    usuarios_ativos += 1
            
            semanas_administrations[semana] = total_admin_semana
            usuarios_por_semana_admin[semana] = usuarios_ativos
        
        # Criar DataFrame
        df_admin_semanas = pd.DataFrame({
            'Semana': list(semanas_administrations.keys()),
            'Total Administrations': list(semanas_administrations.values()),
            'Active Users': list(usuarios_por_semana_admin.values())
        })
        df_admin_semanas = df_admin_semanas[df_admin_semanas['Active Users'] > 0]
        df_admin_semanas['Period'] = df_admin_semanas['Semana'].apply(formatar_periodo_semana)
        
        # Layout gráficos e tabela
        col_graf_admin, col_tab_admin = st.columns([2, 1])
        
        with col_graf_admin:
            fig_admin = px.bar(
                df_admin_semanas,
                x='Period',
                y='Total Administrations',
                title='Total Administrations (Medication Intakes) by Period',
                color_discrete_sequence=[CHART_COLORS[2]],
                labels={'Total Administrations': 'Total Administrations', 'Period': 'Period'}
            )
            fig_admin.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Period",
                yaxis_title="Total Administrations"
            )
            st.plotly_chart(fig_admin, use_container_width=True, height=400)
            
            fig_usuarios_admin = px.line(
                df_admin_semanas,
                x='Period',
                y='Active Users',
                title='Active Users Evolution by Period',
                color_discrete_sequence=[CHART_COLORS[2]]
            )
            fig_usuarios_admin.update_layout(
                height=300,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Period",
                yaxis_title="Number of Active Users"
            )
            st.plotly_chart(fig_usuarios_admin, use_container_width=True, height=300)
        
        with col_tab_admin:
            st.markdown(f"**{t('sections.prescricoes_semanais.data_by_period')}**")
            df_exib_admin = df_admin_semanas[['Period', 'Total Administrations', 'Active Users']].copy()
            df_exib_admin['Total Administrations'] = df_exib_admin['Total Administrations'].astype(int)
            df_exib_admin['Active Users'] = df_exib_admin['Active Users'].astype(int)
            
            st.dataframe(
                df_exib_admin,
                use_container_width=True,
                column_config={
                    "Period": st.column_config.TextColumn(t('tables.period'), width="medium"),
                    "Total Administrations": st.column_config.NumberColumn("Total Administrations", width="medium"),
                    "Active Users": st.column_config.NumberColumn(t('tables.active_users'), width="small")
                }
            )
            
            st.markdown(f"**{t('sections.prescricoes_semanais.total_periods')}: {len(df_admin_semanas)}**")
            st.markdown(f"**{t('sections.prescricoes_semanais.total_administrations')}: {df_admin_semanas['Total Administrations'].sum()}**")
            st.markdown(f"**{t('sections.prescricoes_semanais.peak_admin_week')}: {df_admin_semanas['Total Administrations'].max()}**")
            st.markdown(f"**{t('sections.prescricoes_semanais.peak_active_users')}: {df_admin_semanas['Active Users'].max()}**")
            
            # Download CSV administrations
            csv_admin = df_exib_admin.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.prescricoes_semanais.download_admin'),
                data=csv_admin,
                file_name=f"administrations_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Tabela detalhada de administrations por semana
        st.markdown("---")
        st.markdown(f"### {t('sections.prescricoes_semanais.detailed_admin_title')}")
        st.info(t('sections.prescricoes_semanais.detailed_admin_info'))
        
        df_admin_detalhado = gerar_tabela_administrations_semana(pacientes_filtrados, data_inicio, data_fim)
        
        if not df_admin_detalhado.empty:
            st.markdown(f"**{t('sections.prescricoes_semanais.total_admin_records')}: {len(df_admin_detalhado)}**")
            st.dataframe(
                df_admin_detalhado.head(100),
                use_container_width=True,
                column_config={
                    "patient_id": st.column_config.TextColumn(t('tables.patient_id'), width="medium"),
                    "week_period": st.column_config.TextColumn("Week Period", width="medium"),
                    "week_number": st.column_config.NumberColumn("Week #", width="small"),
                    "total_administrations": st.column_config.NumberColumn("Total Administrations", width="medium")
                }
            )
            
            if len(df_admin_detalhado) > 100:
                st.info(t('sections.prescricoes_semanais.showing_first', count=100, total=len(df_admin_detalhado)))
            
            # Preparar para download
            df_admin_download = df_admin_detalhado.copy()
            csv_admin_detalhado = df_admin_download.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.prescricoes_semanais.download_detailed_admin'),
                data=csv_admin_detalhado,
                file_name=f"administrations_detalhado_semana_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Complete table with administrations grouped by patient and week"
            )
        else:
            st.warning(t('sections.prescricoes_semanais.no_admin_data'))
    
    # ========== TAB 2: PRESCRIPTIONS BY WEEK ==========
    with tab2:
        st.subheader(t('sections.prescricoes_semanais.presc_title'))
        st.info(t('sections.prescricoes_semanais.presc_info'))
        
        # Calcular dados semanais de prescriptions
        semanas_prescriptions = {}
        usuarios_por_semana_presc = {}
        
        for semana in range(53):
            semana_data = data_inicio + pd.Timedelta(weeks=semana)
            if semana_data > data_fim:
                break
                
            inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
            fim_semana = inicio_semana + pd.Timedelta(days=6)
            
            if inicio_semana.tz is None:
                inicio_semana = inicio_semana.tz_localize('UTC')
            if fim_semana.tz is None:
                fim_semana = fim_semana.tz_localize('UTC')
            
            total_presc_semana = 0
            usuarios_ativos = 0
            
            for paciente in pacientes_filtrados:
                prescs = paciente.get('prescriptions', [])
                presc_na_semana = 0
                
                for presc in prescs:
                    presc_created_at = presc.get('createdAt')
                    if presc_created_at:
                        if isinstance(presc_created_at, str):
                            presc_created_at = parser.parse(presc_created_at)
                        else:
                            continue
                            
                        if inicio_semana <= presc_created_at <= fim_semana:
                            presc_na_semana += 1
                
                if presc_na_semana > 0:
                    total_presc_semana += presc_na_semana
                    usuarios_ativos += 1
            
            semanas_prescriptions[semana] = total_presc_semana
            usuarios_por_semana_presc[semana] = usuarios_ativos
        
        # Criar DataFrame
        df_presc_semanas = pd.DataFrame({
            'Semana': list(semanas_prescriptions.keys()),
            'Total Prescriptions': list(semanas_prescriptions.values()),
            'Active Users': list(usuarios_por_semana_presc.values())
        })
        df_presc_semanas = df_presc_semanas[df_presc_semanas['Active Users'] > 0]
        df_presc_semanas['Period'] = df_presc_semanas['Semana'].apply(formatar_periodo_semana)
        
        # Layout gráficos e tabela
        col_graf_presc, col_tab_presc = st.columns([2, 1])
        
        with col_graf_presc:
            fig_presc = px.bar(
                df_presc_semanas,
                x='Period',
                y='Total Prescriptions',
                title='Total Prescriptions Created by Period',
                color_discrete_sequence=[CHART_COLORS[1]],
                labels={'Total Prescriptions': 'Total Prescriptions', 'Period': 'Period'}
            )
            fig_presc.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Period",
                yaxis_title="Total Prescriptions"
            )
            st.plotly_chart(fig_presc, use_container_width=True, height=400)
            
            fig_usuarios_presc = px.line(
                df_presc_semanas,
                x='Period',
                y='Active Users',
                title='Active Users Evolution by Period',
                color_discrete_sequence=[CHART_COLORS[1]]
            )
            fig_usuarios_presc.update_layout(
                height=300,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Period",
                yaxis_title="Number of Active Users"
            )
            st.plotly_chart(fig_usuarios_presc, use_container_width=True, height=300)
        
        with col_tab_presc:
            st.markdown(f"**{t('sections.prescricoes_semanais.data_by_period')}**")
            df_exib_presc = df_presc_semanas[['Period', 'Total Prescriptions', 'Active Users']].copy()
            df_exib_presc['Total Prescriptions'] = df_exib_presc['Total Prescriptions'].astype(int)
            df_exib_presc['Active Users'] = df_exib_presc['Active Users'].astype(int)
            
            st.dataframe(
                df_exib_presc,
                use_container_width=True,
                column_config={
                    "Period": st.column_config.TextColumn(t('tables.period'), width="medium"),
                    "Total Prescriptions": st.column_config.NumberColumn("Total Prescriptions", width="medium"),
                    "Active Users": st.column_config.NumberColumn(t('tables.active_users'), width="small")
                }
            )
            
            st.markdown(f"**{t('sections.prescricoes_semanais.total_periods')}: {len(df_presc_semanas)}**")
            st.markdown(f"**Total prescriptions: {df_presc_semanas['Total Prescriptions'].sum()}**")
            st.markdown(f"**Peak prescriptions/week: {df_presc_semanas['Total Prescriptions'].max()}**")
            st.markdown(f"**{t('sections.prescricoes_semanais.peak_active_users')}: {df_presc_semanas['Active Users'].max()}**")
            
            # Download CSV prescriptions
            csv_presc = df_exib_presc.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.prescricoes_semanais.download_presc'),
                data=csv_presc,
                file_name=f"prescriptions_periodos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Tabela detalhada de prescriptions por semana
        st.markdown("---")
        st.markdown(f"### {t('sections.prescricoes_semanais.detailed_presc_title')}")
        st.info(t('sections.prescricoes_semanais.detailed_presc_info'))
        
        df_presc_detalhado = gerar_tabela_prescriptions_semana(pacientes_filtrados, data_inicio, data_fim)
        
        if not df_presc_detalhado.empty:
            st.markdown(f"**{t('sections.prescricoes_semanais.total_presc_records')}: {len(df_presc_detalhado)}**")
            st.dataframe(
                df_presc_detalhado.head(100),
                use_container_width=True,
                column_config={
                    "patient_id": st.column_config.TextColumn(t('tables.patient_id'), width="medium"),
                    "week_period": st.column_config.TextColumn("Week Period", width="medium"),
                    "week_number": st.column_config.NumberColumn("Week #", width="small"),
                    "total_prescriptions": st.column_config.NumberColumn("Total Prescriptions", width="medium")
                }
            )
            
            if len(df_presc_detalhado) > 100:
                st.info(t('sections.prescricoes_semanais.showing_first', count=100, total=len(df_presc_detalhado)))
            
            # Preparar para download
            df_presc_download = df_presc_detalhado.copy()
            csv_presc_detalhado = df_presc_download.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.prescricoes_semanais.download_detailed_presc'),
                data=csv_presc_detalhado,
                file_name=f"prescriptions_detalhado_semana_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Complete table with prescriptions grouped by patient and week"
            )
        else:
            st.warning(t('sections.prescricoes_semanais.no_presc_data'))
    
    # Tabela de validação completa (mantida no final)
    st.markdown("---")
    st.markdown(f"### {t('sections.prescricoes_semanais.validation_title')}")
    st.info(t('sections.prescricoes_semanais.validation_info'))
    
    df_validacao = gerar_tabela_validacao_completa(pacientes_filtrados)
    
    if not df_validacao.empty:
        st.markdown(f"**{t('sections.prescricoes_semanais.total_presc_validation')}: {len(df_validacao)}**")
        
        st.dataframe(
            df_validacao.head(100),
            use_container_width=True,
            column_config={
                "patient_id": st.column_config.TextColumn(t('tables.patient_id'), width="medium"),
                "prescription_date": st.column_config.DatetimeColumn("Prescription Date", width="medium"),
                "prescription_id": st.column_config.TextColumn("Prescription ID", width="medium"),
                "taken": st.column_config.TextColumn("Taken", width="small")
            }
        )
        
        if len(df_validacao) > 100:
            st.info(t('sections.prescricoes_semanais.showing_first', count=100, total=len(df_validacao)))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t('sections.prescricoes_semanais.total_prescriptions'), len(df_validacao))
        with col2:
            presc_taken = len(df_validacao[df_validacao['taken'] == True])
            st.metric(t('sections.prescricoes_semanais.prescriptions_taken'), presc_taken)
        with col3:
            presc_not_taken = len(df_validacao[df_validacao['taken'] == False])
            st.metric(t('sections.prescricoes_semanais.prescriptions_not_taken'), presc_not_taken)
        
        df_download = df_validacao.copy()
        if 'prescription_date' in df_download.columns:
            df_download['prescription_date'] = df_download['prescription_date'].apply(
                lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(x) else ''
            )
        df_download['taken'] = df_download['taken'].map({True: 'true', False: 'false'})
        
        csv_validacao = df_download.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=t('sections.prescricoes_semanais.download_validation'),
            data=csv_validacao,
            file_name=f"prescriptions_validation_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download complete table with all prescriptions and their taken status"
        )
    else:
        st.warning(t('sections.prescricoes_semanais.no_presc_validation'))


def gerar_tabela_administrations_semana(pacientes_filtrados, data_inicio, data_fim):
    """
    Generates a detailed table with administrations grouped by patient and week.
    
    Args:
        pacientes_filtrados: Filtered patient list
        data_inicio: Start date of analysis period
        data_fim: End date of analysis period
    
    Returns:
        DataFrame with columns: patient_id, week_period, week_number, total_administrations
    """
    def formatar_periodo_semana(semana_num):
        semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        mes_inicio = inicio_semana.strftime('%b')
        mes_fim = fim_semana.strftime('%b')
        if mes_inicio == mes_fim:
            return f"{mes_inicio} {inicio_semana.day}-{fim_semana.day}"
        else:
            return f"{mes_inicio} {inicio_semana.day} - {mes_fim} {fim_semana.day}"
    
    registros_detalhados = []
    
    for semana in range(53):
        semana_data = data_inicio + pd.Timedelta(weeks=semana)
        if semana_data > data_fim:
            break
            
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        
        if inicio_semana.tz is None:
            inicio_semana = inicio_semana.tz_localize('UTC')
        if fim_semana.tz is None:
            fim_semana = fim_semana.tz_localize('UTC')
        
        for paciente in pacientes_filtrados:
            paciente_id = paciente.get('id', 'N/A')
            prescs = paciente.get('prescriptions', [])
            total_admin_paciente_semana = 0
            
            for presc in prescs:
                for admin in presc.get('administrations', []):
                    data_admin = admin.get('date')
                    if data_admin:
                        if isinstance(data_admin, str):
                            try:
                                data_admin = parser.parse(data_admin)
                            except Exception:
                                continue
                        else:
                            continue
                            
                        if inicio_semana <= data_admin <= fim_semana:
                            total_admin_paciente_semana += 1
            
            if total_admin_paciente_semana > 0:
                registros_detalhados.append({
                    'patient_id': paciente_id,
                    'week_period': formatar_periodo_semana(semana),
                    'week_number': semana,
                    'total_administrations': total_admin_paciente_semana
                })
    
    return pd.DataFrame(registros_detalhados)


def gerar_tabela_prescriptions_semana(pacientes_filtrados, data_inicio, data_fim):
    """
    Generates a detailed table with prescriptions grouped by patient and week.
    
    Args:
        pacientes_filtrados: Filtered patient list
        data_inicio: Start date of analysis period
        data_fim: End date of analysis period
    
    Returns:
        DataFrame with columns: patient_id, week_period, week_number, total_prescriptions
    """
    def formatar_periodo_semana(semana_num):
        semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        mes_inicio = inicio_semana.strftime('%b')
        mes_fim = fim_semana.strftime('%b')
        if mes_inicio == mes_fim:
            return f"{mes_inicio} {inicio_semana.day}-{fim_semana.day}"
        else:
            return f"{mes_inicio} {inicio_semana.day} - {mes_fim} {fim_semana.day}"
    
    registros_detalhados = []
    
    for semana in range(53):
        semana_data = data_inicio + pd.Timedelta(weeks=semana)
        if semana_data > data_fim:
            break
            
        inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
        fim_semana = inicio_semana + pd.Timedelta(days=6)
        
        if inicio_semana.tz is None:
            inicio_semana = inicio_semana.tz_localize('UTC')
        if fim_semana.tz is None:
            fim_semana = fim_semana.tz_localize('UTC')
        
        for paciente in pacientes_filtrados:
            paciente_id = paciente.get('id', 'N/A')
            prescs = paciente.get('prescriptions', [])
            total_presc_paciente_semana = 0
            
            for presc in prescs:
                presc_created_at = presc.get('createdAt')
                if presc_created_at:
                    if isinstance(presc_created_at, str):
                        try:
                            presc_created_at = parser.parse(presc_created_at)
                        except Exception:
                            continue
                    else:
                        continue
                        
                    if inicio_semana <= presc_created_at <= fim_semana:
                        total_presc_paciente_semana += 1
            
            if total_presc_paciente_semana > 0:
                registros_detalhados.append({
                    'patient_id': paciente_id,
                    'week_period': formatar_periodo_semana(semana),
                    'week_number': semana,
                    'total_prescriptions': total_presc_paciente_semana
                })
    
    return pd.DataFrame(registros_detalhados)


def gerar_tabela_validacao_completa(pacientes_filtrados):
    """
    Generates a complete validation table with all prescriptions and their taken status.
    
    Args:
        pacientes_filtrados: Filtered patient list
    
    Returns:
        DataFrame with columns: patient_id, prescription_date, prescription_id, taken
    """
    registros_validacao = []
    
    for paciente in pacientes_filtrados:
        paciente_id = paciente.get('id', 'N/A')
        prescs = paciente.get('prescriptions', [])
        
        for presc in prescs:
            presc_id = presc.get('id', 'N/A')
            presc_created_at = presc.get('createdAt')
            administrations = presc.get('administrations', [])
            
            # Verificar se a prescrição foi tomada (tem pelo menos uma administration)
            taken = len(administrations) > 0
            
            # Processar data de criação da prescrição
            if presc_created_at:
                if isinstance(presc_created_at, str):
                    try:
                        presc_created_at = parser.parse(presc_created_at)
                    except Exception:
                        presc_created_at = None
                
                if presc_created_at:
                    registros_validacao.append({
                        'patient_id': paciente_id,
                        'prescription_date': presc_created_at,
                        'prescription_id': presc_id,
                        'taken': taken
                    })
            else:
                # Se não tem data, ainda assim incluir na tabela
                registros_validacao.append({
                    'patient_id': paciente_id,
                    'prescription_date': None,
                    'prescription_id': presc_id,
                    'taken': taken
                })
    
    df_validacao = pd.DataFrame(registros_validacao)
    
    # Ordenar por data de prescrição (mais antigas primeiro)
    if not df_validacao.empty and 'prescription_date' in df_validacao.columns:
        df_validacao = df_validacao.sort_values('prescription_date', na_position='last')
        # Formatar data para exibição
        df_validacao['prescription_date'] = pd.to_datetime(df_validacao['prescription_date'], errors='coerce')
    
    # Garantir que 'taken' seja boolean
    if not df_validacao.empty:
        df_validacao['taken'] = df_validacao['taken'].astype(bool)
    
    return df_validacao


def gerar_tabela_detalhada_semana(pacientes_filtrados, semana_num, data_inicio):
    """
    Generates a detailed table with medication records for a specific week.
    
    Args:
        pacientes_filtrados: Filtered patient list
        semana_num: Week number to analyze
        data_inicio: Start date of analysis period
    
    Returns:
        DataFrame with columns: Patient_ID, Prescription_ID, Record_Date, Formatted_Date
    """
    # Calcular início e fim da semana
    semana_data = data_inicio + pd.Timedelta(weeks=semana_num)
    inicio_semana = semana_data - pd.Timedelta(days=semana_data.weekday())
    fim_semana = inicio_semana + pd.Timedelta(days=6)
    
    # Normalizar timezone para UTC
    if inicio_semana.tz is None:
        inicio_semana = inicio_semana.tz_localize('UTC')
    if fim_semana.tz is None:
        fim_semana = fim_semana.tz_localize('UTC')
    
    registros_detalhados = []
    
    for paciente in pacientes_filtrados:
        paciente_id = paciente.get('id', 'N/A')
        prescs = paciente.get('prescriptions', [])
        
        for presc in prescs:
            presc_id = presc.get('id', 'N/A')
            presc_created_at = presc.get('createdAt')
            
            # Processar data de criação da prescrição
            if presc_created_at:
                if isinstance(presc_created_at, str):
                    presc_created_at = parser.parse(presc_created_at)
                
                # Verificar se a prescrição foi criada na semana analisada
                if inicio_semana <= presc_created_at <= fim_semana:
                    registros_detalhados.append({
                        'Patient_ID': paciente_id,
                        'Prescription_ID': presc_id,
                        'Record_Date': presc_created_at,
                        'Formatted_Date': presc_created_at.strftime('%d/%m/%Y %H:%M:%S')
                    })
    
    return pd.DataFrame(registros_detalhados)