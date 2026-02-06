import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_funcionalidades_sexo(df_recorte):
    st.info(t('sections.funcionalidades_sexo.description'))
    
    # Copiar dados para análise por gênero
    df_gender = df_recorte.copy()
    
    if not df_gender.empty:
        # Mapear códigos para nomes completos
        df_gender['Sexo'] = df_gender['gender'].map({
            'male': t('sections.ativos.male'),
            'female': t('sections.ativos.female')
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
        
        male_label = t('sections.ativos.male')
        female_label = t('sections.ativos.female')
        
        for func_key, func_nome in funcionalidades_nomes.items():
            # Contar usuários por sexo que usaram a funcionalidade
            masculino_count = df_gender[
                (df_gender['Sexo'] == male_label) & 
                (df_gender[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            feminino_count = df_gender[
                (df_gender['Sexo'] == female_label) & 
                (df_gender[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            # Total de usuários por sexo
            total_masculino = df_gender[df_gender['Sexo'] == male_label].shape[0]
            total_feminino = df_gender[df_gender['Sexo'] == female_label].shape[0]
            
            # Calcular percentuais
            perc_masculino = (masculino_count / total_masculino * 100) if total_masculino > 0 else 0
            perc_feminino = (feminino_count / total_feminino * 100) if total_feminino > 0 else 0
            
            funcionalidades_sexo[func_nome] = {
                male_label: {'count': masculino_count, 'total': total_masculino, 'perc': perc_masculino},
                female_label: {'count': feminino_count, 'total': total_feminino, 'perc': perc_feminino}
            }
        
        # Layout lado a lado: gráficos e tabelas
        col_graficos, col_tabelas = st.columns([3, 2])
        
        with col_graficos:
            # Preparar dados para gráficos
            dados_grafico = []
            for func_nome, dados in funcionalidades_sexo.items():
                dados_grafico.extend([
                    {'Feature': func_nome, 'Sex': male_label, 'Percentage': dados[male_label]['perc'], 'Users': dados[male_label]['count']},
                    {'Feature': func_nome, 'Sex': female_label, 'Percentage': dados[female_label]['perc'], 'Users': dados[female_label]['count']}
                ])
            
            df_grafico = pd.DataFrame(dados_grafico)
            
            # Gráfico de barras agrupadas - Percentual de adesão
            fig_perc = px.bar(
                df_grafico,
                x='Feature',
                y='Percentage',
                color='Sex',
                title=t('charts.titles.adoption_rate_by_sex'),
                labels={'Percentage': t('sections.funcionalidades_sexo.adoption_rate'), 'Feature': 'Feature'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_perc.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Features",
                yaxis_title=t('sections.funcionalidades_sexo.adoption_rate'),
                legend_title=t('tables.sex'),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_perc, use_container_width=True, height=400)
            
            # Gráfico de barras agrupadas - Número absoluto de usuários
            fig_abs = px.bar(
                df_grafico,
                x='Feature',
                y='Users',
                color='Sex',
                title=t('charts.titles.users_by_feature_sex'),
                labels={'Users': t('sections.funcionalidades_sexo.number_of_users'), 'Feature': 'Feature'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_abs.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Features",
                yaxis_title=t('sections.funcionalidades_sexo.number_of_users'),
                legend_title=t('tables.sex'),
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_abs, use_container_width=True, height=400)
        
        with col_tabelas:
            # Tabela detalhada
            st.markdown(f"**{t('sections.funcionalidades_sexo.detailed_data')}**")
            
            # Criar tabela para exibição
            tabela_dados = []
            for func_nome, dados in funcionalidades_sexo.items():
                tabela_dados.append({
                    'Feature': func_nome,
                    'Male Users': f"{dados[male_label]['count']}/{dados[male_label]['total']}",
                    'Male %': f"{dados[male_label]['perc']:.1f}%",
                    'Female Users': f"{dados[female_label]['count']}/{dados[female_label]['total']}",
                    'Female %': f"{dados[female_label]['perc']:.1f}%"
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
            st.markdown(f"**{t('sections.funcionalidades_sexo.summary')}**")
            total_masc = df_gender[df_gender['Sexo'] == t('sections.ativos.male')].shape[0]
            total_fem = df_gender[df_gender['Sexo'] == t('sections.ativos.female')].shape[0]
            
            st.markdown(f"• **{t('sections.funcionalidades_sexo.total_male')}:** {total_masc} {t('sections.funcionalidades_geral.patients')}")
            st.markdown(f"• **{t('sections.funcionalidades_sexo.total_female')}:** {total_fem} {t('sections.funcionalidades_geral.patients')}")
            
            # Identificar funcionalidade com maior diferença de adesão
            maior_diff = 0
            func_maior_diff = ""
            sexo_maior_adesao = ""
            
            for func_nome, dados in funcionalidades_sexo.items():
                diff = abs(dados[male_label]['perc'] - dados[female_label]['perc'])
                if diff > maior_diff:
                    maior_diff = diff
                    func_maior_diff = func_nome
                    if dados[male_label]['perc'] > dados[female_label]['perc']:
                        sexo_maior_adesao = male_label
                    else:
                        sexo_maior_adesao = female_label
            
            if maior_diff > 0:
                st.markdown(f"• **{t('sections.funcionalidades_sexo.largest_difference')}:** {func_maior_diff}")
                st.markdown(f"• **{t('sections.funcionalidades_sexo.higher_adoption')}:** {sexo_maior_adesao}")
                st.markdown(f"• **{t('sections.funcionalidades_sexo.difference')}:** {maior_diff:.1f}%")
            
            # Botão de download
            csv_sexo = df_tabela.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label=t('sections.funcionalidades_sexo.download_csv'),
                data=csv_sexo,
                file_name=f"funcionalidades_por_sexo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
    else:
        st.warning(t('sections.funcionalidades_sexo.no_data_sex'))
    
    st.markdown('---')
