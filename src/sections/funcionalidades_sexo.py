import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS

def mostrar_funcionalidades_sexo(df_recorte):
    st.subheader('👥 Análise de Adesão às Funcionalidades por Sexo')
    st.info('Análise comparativa do uso de funcionalidades entre pacientes masculinos e femininos para identificar padrões de adesão por sexo.')
    
    # Filtrar dados para excluir sexo indefinido ('I')
    df_sexo_definido = df_recorte[df_recorte['sex'].isin(['M', 'F'])].copy()
    
    if not df_sexo_definido.empty:
        # Mapear códigos para nomes completos
        df_sexo_definido['Sexo'] = df_sexo_definido['sex'].map({
            'M': 'Masculino',
            'F': 'Feminino'
        })
        
        # Calcular uso de funcionalidades por sexo
        funcionalidades_sexo = {}
        funcionalidades_nomes = {
            'symptomDiaries': 'Diários de Sintomas',
            'acqs': 'ACQ (Controle Asma)',
            'activityLogs': 'Atividades Físicas',
            'prescriptions': 'Prescrições',
            'crisis': 'Registro de Crises'
        }
        
        for func_key, func_nome in funcionalidades_nomes.items():
            # Contar usuários por sexo que usaram a funcionalidade
            masculino_count = df_sexo_definido[
                (df_sexo_definido['Sexo'] == 'Masculino') & 
                (df_sexo_definido[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            feminino_count = df_sexo_definido[
                (df_sexo_definido['Sexo'] == 'Feminino') & 
                (df_sexo_definido[func_key].apply(lambda x: len(x) > 0 if isinstance(x, list) else False))
            ].shape[0]
            
            # Total de usuários por sexo
            total_masculino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Masculino'].shape[0]
            total_feminino = df_sexo_definido[df_sexo_definido['Sexo'] == 'Feminino'].shape[0]
            
            # Calcular percentuais
            perc_masculino = (masculino_count / total_masculino * 100) if total_masculino > 0 else 0
            perc_feminino = (feminino_count / total_feminino * 100) if total_feminino > 0 else 0
            
            funcionalidades_sexo[func_nome] = {
                'Masculino': {'count': masculino_count, 'total': total_masculino, 'perc': perc_masculino},
                'Feminino': {'count': feminino_count, 'total': total_feminino, 'perc': perc_feminino}
            }
        
        # Layout lado a lado: gráficos e tabelas
        col_graficos, col_tabelas = st.columns([3, 2])
        
        with col_graficos:
            # Preparar dados para gráficos
            dados_grafico = []
            for func_nome, dados in funcionalidades_sexo.items():
                dados_grafico.extend([
                    {'Funcionalidade': func_nome, 'Sexo': 'Masculino', 'Percentual': dados['Masculino']['perc'], 'Usuários': dados['Masculino']['count']},
                    {'Funcionalidade': func_nome, 'Sexo': 'Feminino', 'Percentual': dados['Feminino']['perc'], 'Usuários': dados['Feminino']['count']}
                ])
            
            df_grafico = pd.DataFrame(dados_grafico)
            
            # Gráfico de barras agrupadas - Percentual de adesão
            fig_perc = px.bar(
                df_grafico,
                x='Funcionalidade',
                y='Percentual',
                color='Sexo',
                title='Taxa de Adesão às Funcionalidades por Sexo (%)',
                labels={'Percentual': 'Taxa de Adesão (%)', 'Funcionalidade': 'Funcionalidade'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_perc.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Funcionalidades",
                yaxis_title="Taxa de Adesão (%)",
                legend_title="Sexo",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_perc, use_container_width=True, height=400)
            
            # Gráfico de barras agrupadas - Número absoluto de usuários
            fig_abs = px.bar(
                df_grafico,
                x='Funcionalidade',
                y='Usuários',
                color='Sexo',
                title='Número de Usuários por Funcionalidade e Sexo',
                labels={'Usuários': 'Número de Usuários', 'Funcionalidade': 'Funcionalidade'},
                color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[2]],
                barmode='group'
            )
            fig_abs.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis_title="Funcionalidades",
                yaxis_title="Número de Usuários",
                legend_title="Sexo",
                xaxis=dict(tickangle=45)
            )
            st.plotly_chart(fig_abs, use_container_width=True, height=400)
        
        with col_tabelas:
            # Tabela detalhada
            st.markdown("**Dados Detalhados por Sexo:**")
            
            # Criar tabela para exibição
            tabela_dados = []
            for func_nome, dados in funcionalidades_sexo.items():
                tabela_dados.append({
                    'Funcionalidade': func_nome,
                    'Masc. Usuários': f"{dados['Masculino']['count']}/{dados['Masculino']['total']}",
                    'Masc. %': f"{dados['Masculino']['perc']:.1f}%",
                    'Fem. Usuários': f"{dados['Feminino']['count']}/{dados['Feminino']['total']}",
                    'Fem. %': f"{dados['Feminino']['perc']:.1f}%"
                })
            
            df_tabela = pd.DataFrame(tabela_dados)
            
            st.dataframe(
                df_tabela,
                use_container_width=True,
                column_config={
                    "Funcionalidade": st.column_config.TextColumn("Funcionalidade", width="large"),
                    "Masc. Usuários": st.column_config.TextColumn("Masc. Usuários", width="small"),
                    "Masc. %": st.column_config.TextColumn("Masc. %", width="small"),
                    "Fem. Usuários": st.column_config.TextColumn("Fem. Usuários", width="small"),
                    "Fem. %": st.column_config.TextColumn("Fem. %", width="small")
                }
            )
            
            # Resumo estatístico
            st.markdown("**Resumo:**")
            total_masc = df_sexo_definido[df_sexo_definido['Sexo'] == 'Masculino'].shape[0]
            total_fem = df_sexo_definido[df_sexo_definido['Sexo'] == 'Feminino'].shape[0]
            
            st.markdown(f"• **Total Masculino:** {total_masc} pacientes")
            st.markdown(f"• **Total Feminino:** {total_fem} pacientes")
            
            # Identificar funcionalidade com maior diferença de adesão
            maior_diff = 0
            func_maior_diff = ""
            sexo_maior_adesao = ""
            
            for func_nome, dados in funcionalidades_sexo.items():
                diff = abs(dados['Masculino']['perc'] - dados['Feminino']['perc'])
                if diff > maior_diff:
                    maior_diff = diff
                    func_maior_diff = func_nome
                    if dados['Masculino']['perc'] > dados['Feminino']['perc']:
                        sexo_maior_adesao = "Masculino"
                    else:
                        sexo_maior_adesao = "Feminino"
            
            if maior_diff > 0:
                st.markdown(f"• **Maior diferença:** {func_maior_diff}")
                st.markdown(f"• **Maior adesão:** {sexo_maior_adesao}")
                st.markdown(f"• **Diferença:** {maior_diff:.1f}%")
            
            # Botão de download
            csv_sexo = df_tabela.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Dados por Sexo (CSV)",
                data=csv_sexo,
                file_name=f"funcionalidades_por_sexo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Nota sobre dados pessoais
        pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
        if pacientes_indefinidos > 0:
            st.info(f"**Nota:** {pacientes_indefinidos} paciente(s) com sexo indefinido não aparecem nesta análise devido à política de exclusão de dados pessoais.")
    
    else:
        st.warning("Não há dados com sexo definido para análise comparativa.")
    
    st.markdown('---')
