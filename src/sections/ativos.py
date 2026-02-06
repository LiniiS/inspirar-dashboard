import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil import parser as dateutil_parser
from utils.colors import CHART_COLORS
from utils.translations import t

DIAS_ATIVIDADE_RECENTE = 45

def _tem_registro_recente(registros, campos_data, data_limite):
    """Verifica se algum registro tem data >= data_limite."""
    if not isinstance(registros, list) or not registros:
        return False
    for item in registros:
        if not isinstance(item, dict):
            continue
        for campo in campos_data:
            data_str = item.get(campo)
            if not data_str:
                continue
            try:
                data_ts = pd.Timestamp(dateutil_parser.parse(data_str))
                if data_ts.tzinfo is None:
                    data_ts = data_ts.tz_localize('UTC', ambiguous='infer')
                if data_ts >= data_limite:
                    return True
            except (TypeError, ValueError):
                continue
    return False

def _prescription_tem_uso_recente(prescriptions, data_limite):
    """Verifica prescrições: createdAt ou data de administrations."""
    if not isinstance(prescriptions, list) or not prescriptions:
        return False
    for presc in prescriptions:
        if not isinstance(presc, dict):
            continue
        # Prescrição criada recentemente
        if _tem_registro_recente([presc], ['createdAt'], data_limite):
            return True
        # Administrações (tomadas) recentes
        admins = presc.get('administrations', [])
        if _tem_registro_recente(admins, ['date'], data_limite):
            return True
    return False

def mostrar_ativos(df_recorte):
    st.subheader(t('sections.ativos.title'))
    st.markdown(t('sections.ativos.description'))
    st.info(t('sections.ativos.note_active_45_days'))
    
    data_fim = st.session_state.get('data_fim', pd.Timestamp.now(tz='UTC'))
    data_limite = data_fim - pd.Timedelta(days=DIAS_ATIVIDADE_RECENTE)
    
    def paciente_ativo(row):
        return any([
            _tem_registro_recente(row.get('symptomDiaries', []), ['createdAt'], data_limite),
            _tem_registro_recente(row.get('acqs', []), ['createdAt', 'answeredAt'], data_limite),
            _tem_registro_recente(row.get('activityLogs', []), ['createdAt', 'date'], data_limite),
            _prescription_tem_uso_recente(row.get('prescriptions', []), data_limite),
            _tem_registro_recente(row.get('crisis', []), ['initialUsageDate', 'finalUsageDate', 'updatedAt'], data_limite),
        ])
    
    df_recorte = df_recorte.copy()  # Evitar SettingWithCopyWarning
    df_recorte['is_ativo'] = df_recorte.apply(paciente_ativo, axis=1)
    n_ativos = df_recorte['is_ativo'].sum()
    n_inativos = len(df_recorte) - n_ativos
    
    # Criar colunas para os gráficos lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Ativos vs Inativos
        fig_pizza_ativos = px.pie(
            names=[t('sections.ativos.active'), t('sections.ativos.inactive')],
            values=[n_ativos, n_inativos],
            color_discrete_sequence=[CHART_COLORS[2], CHART_COLORS[4]],
            title=t('sections.ativos.distribution_title')
        )
        fig_pizza_ativos.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_pizza_ativos, use_container_width=True, height=400)
    
    with col2:
        # Gráfico de distribuição por sexo - Apenas pacientes ativos
        df_ativos = df_recorte[df_recorte['is_ativo'] == True]
        
        if len(df_ativos) > 0:
            # Contar pacientes ativos por gênero
            gender_counts = df_ativos['gender'].value_counts()
            
            if len(gender_counts) > 0:
                # Mapear códigos para nomes completos
                gender_labels = {'male': t('sections.ativos.male'), 'female': t('sections.ativos.female')}
                gender_counts_labeled = gender_counts.rename(index=gender_labels)
                
                fig_gender_ativos = px.pie(
                    values=gender_counts_labeled.values,
                    names=gender_counts_labeled.index,
                    color_discrete_sequence=CHART_COLORS[2:4],
                    title=t('sections.ativos.distribution_by_sex')
                )
                fig_gender_ativos.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig_gender_ativos, use_container_width=True, height=400)
                
                # Métricas resumidas
                st.markdown(f"**{t('sections.ativos.total_active')}: {len(df_ativos)}**")
                st.markdown(f"**{t('sections.ativos.active_by_sex')}:** {t('sections.ativos.male')}: {gender_counts.get('male', 0)}, {t('sections.ativos.female')}: {gender_counts.get('female', 0)}")
            else:
                st.warning(t('sections.ativos.no_active_sex'))
        else:
            st.warning(t('sections.ativos.no_active'))
    
    st.markdown('---') 