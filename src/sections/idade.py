import streamlit as st
import plotly.express as px
import numpy as np
from utils.colors import CHART_COLORS

def mostrar_idade(df_recorte):
    st.markdown('Análise da faixa etária dos pacientes cadastrados, incluindo distribuição geral e por sexo.')
    
    if not df_recorte.empty:
        # Layout lado a lado
        col_geral, col_sexo = st.columns(2)
        
        with col_geral:
            # Gráfico de distribuição geral de idade
            fig_idade_geral = px.histogram(
                df_recorte,
                x='age',
                nbins=15,
                title="Distribuição Geral de Idade",
                labels={'age': 'Idade', 'count': 'Frequência'},
                color_discrete_sequence=[CHART_COLORS[0]]
            )
            fig_idade_geral.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Idade (anos)",
                yaxis_title="Número de Pacientes"
            )
            st.plotly_chart(fig_idade_geral, use_container_width=True, height=400)
        
        with col_sexo:
            # Filtrar dados para excluir sexo indefinido ('I')
            df_sexo_definido = df_recorte[df_recorte['sex'].isin(['M', 'F'])].copy()
            
            if not df_sexo_definido.empty:
                # Mapear códigos para nomes completos
                df_sexo_definido['Sexo'] = df_sexo_definido['sex'].map({
                    'M': 'Masculino',
                    'F': 'Feminino'
                })
                
                # Gráfico de distribuição de idade por sexo
                fig_idade_sexo = px.histogram(
                    df_sexo_definido,
                    x='age',
                    color='Sexo',
                    nbins=15,
                    title="Distribuição de Idade por Sexo",
                    labels={'age': 'Idade', 'count': 'Frequência'},
                    color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                    barmode='overlay',
                    opacity=0.7
                )
                fig_idade_sexo.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50),
                    xaxis_title="Idade (anos)",
                    yaxis_title="Número de Pacientes",
                    legend_title="Sexo"
                )
                st.plotly_chart(fig_idade_sexo, use_container_width=True, height=400)
                
                # Estatísticas por sexo
                st.markdown("**Estatísticas por Sexo:**")
                
                # Calcular estatísticas
                stats_masculino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Masculino']['age']
                stats_feminino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Feminino']['age']
                
                col_stats_m, col_stats_f = st.columns(2)
                
                with col_stats_m:
                    st.markdown("**Masculino:**")
                    if not stats_masculino.empty:
                        st.markdown(f"• Total: {len(stats_masculino)} pacientes")
                        st.markdown(f"• Média: {stats_masculino.mean():.1f} anos")
                        st.markdown(f"• Mediana: {stats_masculino.median():.1f} anos")
                        st.markdown(f"• Min-Max: {stats_masculino.min()}-{stats_masculino.max()} anos")
                    else:
                        st.markdown("• Sem dados")
                
                with col_stats_f:
                    st.markdown("**Feminino:**")
                    if not stats_feminino.empty:
                        st.markdown(f"• Total: {len(stats_feminino)} pacientes")
                        st.markdown(f"• Média: {stats_feminino.mean():.1f} anos")
                        st.markdown(f"• Mediana: {stats_feminino.median():.1f} anos")
                        st.markdown(f"• Min-Max: {stats_feminino.min()}-{stats_feminino.max()} anos")
                    else:
                        st.markdown("• Sem dados")
            else:
                st.warning("Não há dados de idade com sexo definido para análise.")
        
        # Resumo geral
        st.markdown("---")
        col_resumo1, col_resumo2, col_resumo3, col_resumo4 = st.columns(4)
        
        with col_resumo1:
            st.metric("Total de Pacientes", len(df_recorte))
        
        with col_resumo2:
            st.metric("Idade Média", f"{df_recorte['age'].mean():.1f} anos")
        
        with col_resumo3:
            st.metric("Idade Mediana", f"{df_recorte['age'].median():.1f} anos")
        
        with col_resumo4:
            idade_min = df_recorte['age'].min()
            idade_max = df_recorte['age'].max()
            st.metric("Faixa Etária", f"{idade_min}-{idade_max} anos")
        
        # Nota sobre dados pessoais
        pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
        if pacientes_indefinidos > 0:
            st.info(f"**Nota:** {pacientes_indefinidos} paciente(s) com sexo indefinido não aparecem no gráfico por sexo devido à política de exclusão de dados pessoais.")
    
    else:
        st.warning("Não há dados de idade disponíveis para análise.")
    
    st.markdown('---') 