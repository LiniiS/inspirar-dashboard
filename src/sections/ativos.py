import streamlit as st
import plotly.express as px
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_ativos(df_recorte):
    st.subheader(t('sections.ativos.title'))
    st.markdown(t('sections.ativos.description'))
    
    def paciente_ativo(row):
        return any([
            isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
            isinstance(row['acqs'], list) and len(row['acqs']) > 0,
            isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
            isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
            isinstance(row['crisis'], list) and len(row['crisis']) > 0
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