import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS

def mostrar_funcionalidades_sexo(df_recorte):
    st.info('Comparative analysis of feature usage between male and female patients to identify adoption patterns by sex.')
    
    # Filtrar dados para excluir sexo indefinido ('I')
    df_sexo_definido = df_recorte[df_recorte['sex'].isin(['M', 'F'])].copy()
    
    if not df_sexo_definido.empty:
        # Mapear códigos para nomes completos
        df_sexo_definido['Sexo'] = df_sexo_definido['sex'].map({
            'M': 'Male',
            'F': 'Female'
        })
        
        # Calcular uso de funcionalidades por sexo
        funcionalidades_sexo = {}
        funcionalidades_nomes = {
            'symptomDiaries': 'Symptom Diaries',
            'acqs': 'ACQ (Asthma Control)',
            'activityLogs': 'Physical Activities',
            'prescriptions': 'Medications',
            'crisis': 'Crisis Records'
        }
        
        for func_key, func_nome in funcionalidades_nomes.items():
            # Contar usuários por sexo que usaram a funcionalidade
            masculino_count = df_sexo_definido[
                (df_sexo_definido['Sexo'] == 'Male') & 
                (df_sexo_definido[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            feminino_count = df_sexo_definido[
                (df_sexo_definido['Sexo'] == 'Female') & 
                (df_sexo_definido[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            # Total de usuários por sexo
            total_masculino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Male'].shape[0]
            total_feminino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Female'].shape[0]
            
            # Calcular percentuais
            perc_masculino = (masculino_count / total_masculino * 100) if total_masculino > 0 else 0
            perc_feminino = (feminino_count / total_feminino * 100) if total_feminino > 0 else 0
            
            funcionalidades_sexo[func_nome] = {
                'Male': {'count': masculino_count, 'total': total_masculino, 'perc': perc_masculino},
                'Female': {'count': feminino_count, 'total': total_feminino, 'perc': perc_feminino}
            }
        
        # Layout lado a lado: gráficos e tabelas
        col_graficos, col_tabelas = st.columns([3, 2])
        
        with col_graficos:
            # Preparar dados para gráficos
            dados_grafico = []
            for func_nome, dados in funcionalidades_sexo.items():
                dados_grafico.extend([
                    {'Feature': func_nome, 'Sex': 'Male', 'Percentage': dados['Male']['perc'], 'Users': dados['Male']['count']},
                    {'Feature': func_nome, 'Sex': 'Female', 'Percentage': dados['Female']['perc'], 'Users': dados['Female']['count']}
                ])
            
            df_grafico = pd.DataFrame(dados_grafico)
            
            # Gráfico de barras agrupadas - Percentual de adesão
            fig_perc = px.bar(
                df_grafico,
                x='Feature',
                y='Percentage',
                color='Sex',
                title='Feature Adoption Rate by Sex (%)',
                labels={'Percentage': 'Adoption Rate (%)', 'Feature': 'Feature'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_perc.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Features",
                yaxis_title="Adoption Rate (%)",
                legend_title="Sex",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_perc, use_container_width=True, height=400)
            
            # Gráfico de barras agrupadas - Número absoluto de usuários
            fig_abs = px.bar(
                df_grafico,
                x='Feature',
                y='Users',
                color='Sex',
                title='Number of Users by Feature and Sex',
                labels={'Users': 'Number of Users', 'Feature': 'Feature'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_abs.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Features",
                yaxis_title="Number of Users",
                legend_title="Sex",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_abs, use_container_width=True, height=400)
        
        with col_tabelas:
            # Tabela detalhada
            st.markdown("**Detailed Data by Sex:**")
            
            # Criar tabela para exibição
            tabela_dados = []
            for func_nome, dados in funcionalidades_sexo.items():
                tabela_dados.append({
                    'Feature': func_nome,
                    'Male Users': f"{dados['Male']['count']}/{dados['Male']['total']}",
                    'Male %': f"{dados['Male']['perc']:.1f}%",
                    'Female Users': f"{dados['Female']['count']}/{dados['Female']['total']}",
                    'Female %': f"{dados['Female']['perc']:.1f}%"
                })
            
            df_tabela = pd.DataFrame(tabela_dados)
            
            st.dataframe(
                df_tabela,
                use_container_width=True,
                column_config={
                    "Feature": st.column_config.TextColumn("Feature", width="large"),
                    "Male Users": st.column_config.TextColumn("Male Users", width="small"),
                    "Male %": st.column_config.TextColumn("Male %", width="small"),
                    "Female Users": st.column_config.TextColumn("Female Users", width="small"),
                    "Female %": st.column_config.TextColumn("Female %", width="small")
                }
            )
            
            # Resumo estatístico
            st.markdown("**Summary:**")
            total_masc = df_sexo_definido[df_sexo_definido['Sexo'] == 'Male'].shape[0]
            total_fem = df_sexo_definido[df_sexo_definido['Sexo'] == 'Female'].shape[0]
            
            st.markdown(f"• **Total Male:** {total_masc} patients")
            st.markdown(f"• **Total Female:** {total_fem} patients")
            
            # Identificar funcionalidade com maior diferença de adesão
            maior_diff = 0
            func_maior_diff = ""
            sexo_maior_adesao = ""
            
            for func_nome, dados in funcionalidades_sexo.items():
                diff = abs(dados['Male']['perc'] - dados['Female']['perc'])
                if diff > maior_diff:
                    maior_diff = diff
                    func_maior_diff = func_nome
                    if dados['Male']['perc'] > dados['Female']['perc']:
                        sexo_maior_adesao = "Male"
                    else:
                        sexo_maior_adesao = "Female"
            
            if maior_diff > 0:
                st.markdown(f"• **Largest difference:** {func_maior_diff}")
                st.markdown(f"• **Higher adoption:** {sexo_maior_adesao}")
                st.markdown(f"• **Difference:** {maior_diff:.1f}%")
            
            # Botão de download
            csv_sexo = df_tabela.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Data by Sex (CSV)",
                data=csv_sexo,
                file_name=f"funcionalidades_por_sexo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Nota sobre dados pessoais
        pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
        if pacientes_indefinidos > 0:
            st.info(f"**Note:** {pacientes_indefinidos} patient(s) with undefined sex do not appear in this analysis due to personal data exclusion policy.")
    
    else:
        st.warning("No data with defined sex available for comparative analysis.")
    
    st.markdown('---')
