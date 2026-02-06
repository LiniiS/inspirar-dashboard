import streamlit as st
import plotly.express as px
import numpy as np
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_idade(df_recorte):
    st.markdown(t('sections.idade.description'))
    
    if not df_recorte.empty:
        # Layout lado a lado
        col_geral, col_sexo = st.columns(2)
        
        with col_geral:
            # Gráfico de distribuição geral de idade
            fig_idade_geral = px.histogram(
                df_recorte,
                x='age',
                nbins=15,
                title=t('sections.idade.general_distribution'),
                labels={'age': t('charts.labels.age'), 'count': 'Frequency'},
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_idade_geral.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title=f"{t('charts.labels.age')} ({t('sections.idade.years')})",
                yaxis_title=f"Number of {t('sections.idade.patients')}"
            )
            st.plotly_chart(fig_idade_geral, use_container_width=True, height=400)
        
        with col_sexo:
            # Copiar dados para análise por gênero
            df_gender = df_recorte.copy()
            
            if not df_gender.empty:
                # Mapear códigos para nomes completos
                df_gender['Sexo'] = df_gender['gender'].map({
                    'male': t('sections.ativos.male'),
                    'female': t('sections.ativos.female')
                })
                
                # Gráfico de distribuição de idade por sexo
                fig_idade_sexo = px.histogram(
                    df_gender,
                    x='age',
                    color='Sexo',
                    nbins=15,
                    title=t('sections.idade.distribution_by_sex'),
                    labels={'age': t('charts.labels.age'), 'count': 'Frequency'},
                    color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                    barmode='overlay',
                    opacity=0.7
                )
                fig_idade_sexo.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50),
                    xaxis_title=f"{t('charts.labels.age')} ({t('sections.idade.years')})",
                    yaxis_title=f"Number of {t('sections.idade.patients')}",
                    legend_title=t('tables.sex')
                )
                st.plotly_chart(fig_idade_sexo, use_container_width=True, height=400)
                
                # Estatísticas por sexo
                st.markdown(f"**{t('sections.idade.statistics_by_sex')}**")
                
                # Calcular estatísticas
                stats_masculino = df_gender[df_gender['Sexo'] == t('sections.ativos.male')]['age']
                stats_feminino = df_gender[df_gender['Sexo'] == t('sections.ativos.female')]['age']
                
                col_stats_m, col_stats_f = st.columns(2)
                
                with col_stats_m:
                    st.markdown(f"**{t('sections.ativos.male')}:**")
                    if not stats_masculino.empty:
                        st.markdown(f"• {t('sections.idade.total')}: {len(stats_masculino)} {t('sections.idade.patients')}")
                        st.markdown(f"• {t('sections.idade.mean')}: {stats_masculino.mean():.1f} {t('sections.idade.years')}")
                        st.markdown(f"• {t('sections.idade.median')}: {stats_masculino.median():.1f} {t('sections.idade.years')}")
                        st.markdown(f"• {t('sections.idade.min_max')}: {stats_masculino.min()}-{stats_masculino.max()} {t('sections.idade.years')}")
                    else:
                        st.markdown("• No data")
                
                with col_stats_f:
                    st.markdown(f"**{t('sections.ativos.female')}:**")
                    if not stats_feminino.empty:
                        st.markdown(f"• {t('sections.idade.total')}: {len(stats_feminino)} {t('sections.idade.patients')}")
                        st.markdown(f"• {t('sections.idade.mean')}: {stats_feminino.mean():.1f} {t('sections.idade.years')}")
                        st.markdown(f"• {t('sections.idade.median')}: {stats_feminino.median():.1f} {t('sections.idade.years')}")
                        st.markdown(f"• {t('sections.idade.min_max')}: {stats_feminino.min()}-{stats_feminino.max()} {t('sections.idade.years')}")
                    else:
                        st.markdown("• No data")
            else:
                st.warning(t('sections.idade.no_data_sex'))
        
        # Resumo geral
        st.markdown("---")
        col_resumo1, col_resumo2, col_resumo3, col_resumo4 = st.columns(4)
        
        with col_resumo1:
            st.metric(f"Total {t('sections.idade.patients')}", len(df_recorte))
        
        with col_resumo2:
            st.metric(f"{t('sections.idade.mean')} {t('charts.labels.age')}", f"{df_recorte['age'].mean():.1f} {t('sections.idade.years')}")
        
        with col_resumo3:
            st.metric(f"{t('sections.idade.median')} {t('charts.labels.age')}", f"{df_recorte['age'].median():.1f} {t('sections.idade.years')}")
        
        with col_resumo4:
            idade_min = df_recorte['age'].min()
            idade_max = df_recorte['age'].max()
            st.metric(f"{t('charts.labels.age')} {t('sections.idade.min_max')}", f"{idade_min}-{idade_max} {t('sections.idade.years')}")
        
    else:
        st.warning(t('sections.idade.no_data'))
    
    st.markdown('---') 