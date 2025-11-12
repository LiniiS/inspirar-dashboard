import streamlit as st
import plotly.express as px
import numpy as np
from utils.colors import CHART_COLORS

def mostrar_idade(df_recorte):
    st.markdown('Analysis of registered patients age range, including general and sex-based distribution.')
    
    if not df_recorte.empty:
        # Layout lado a lado
        col_geral, col_sexo = st.columns(2)
        
        with col_geral:
            # Gráfico de distribuição geral de idade
            fig_idade_geral = px.histogram(
                df_recorte,
                x='age',
                nbins=15,
                title="General Age Distribution",
                labels={'age': 'Age', 'count': 'Frequency'},
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_idade_geral.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Age (years)",
                yaxis_title="Number of Patients"
            )
            st.plotly_chart(fig_idade_geral, use_container_width=True, height=400)
        
        with col_sexo:
            # Filtrar dados para excluir sexo indefinido ('I')
            df_sexo_definido = df_recorte[df_recorte['sex'].isin(['M', 'F'])].copy()
            
            if not df_sexo_definido.empty:
                # Mapear códigos para nomes completos
                df_sexo_definido['Sexo'] = df_sexo_definido['sex'].map({
                    'M': 'Male',
                    'F': 'Female'
                })
                
                # Gráfico de distribuição de idade por sexo
                fig_idade_sexo = px.histogram(
                    df_sexo_definido,
                    x='age',
                    color='Sexo',
                    nbins=15,
                    title="Age Distribution by Sex",
                    labels={'age': 'Age', 'count': 'Frequency'},
                    color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                    barmode='overlay',
                    opacity=0.7
                )
                fig_idade_sexo.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50),
                    xaxis_title="Age (years)",
                    yaxis_title="Number of Patients",
                    legend_title="Sex"
                )
                st.plotly_chart(fig_idade_sexo, use_container_width=True, height=400)
                
                # Estatísticas por sexo
                st.markdown("**Statistics by Sex:**")
                
                # Calcular estatísticas
                stats_masculino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Male']['age']
                stats_feminino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Female']['age']
                
                col_stats_m, col_stats_f = st.columns(2)
                
                with col_stats_m:
                    st.markdown("**Male:**")
                    if not stats_masculino.empty:
                        st.markdown(f"• Total: {len(stats_masculino)} patients")
                        st.markdown(f"• Mean: {stats_masculino.mean():.1f} years")
                        st.markdown(f"• Median: {stats_masculino.median():.1f} years")
                        st.markdown(f"• Min-Max: {stats_masculino.min()}-{stats_masculino.max()} years")
                    else:
                        st.markdown("• No data")
                
                with col_stats_f:
                    st.markdown("**Female:**")
                    if not stats_feminino.empty:
                        st.markdown(f"• Total: {len(stats_feminino)} patients")
                        st.markdown(f"• Mean: {stats_feminino.mean():.1f} years")
                        st.markdown(f"• Median: {stats_feminino.median():.1f} years")
                        st.markdown(f"• Min-Max: {stats_feminino.min()}-{stats_feminino.max()} years")
                    else:
                        st.markdown("• No data")
            else:
                st.warning("No age data with defined sex available for analysis.")
        
        # Resumo geral
        st.markdown("---")
        col_resumo1, col_resumo2, col_resumo3, col_resumo4 = st.columns(4)
        
        with col_resumo1:
            st.metric("Total Patients", len(df_recorte))
        
        with col_resumo2:
            st.metric("Average Age", f"{df_recorte['age'].mean():.1f} years")
        
        with col_resumo3:
            st.metric("Median Age", f"{df_recorte['age'].median():.1f} years")
        
        with col_resumo4:
            idade_min = df_recorte['age'].min()
            idade_max = df_recorte['age'].max()
            st.metric("Age Range", f"{idade_min}-{idade_max} years")
        
        # Nota sobre dados pessoais
        pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
        if pacientes_indefinidos > 0:
            st.info(f"**Note:** {pacientes_indefinidos} patient(s) with undefined sex do not appear in the sex chart due to personal data exclusion policy.")
    
    else:
        st.warning("No age data available for analysis.")
    
    st.markdown('---') 