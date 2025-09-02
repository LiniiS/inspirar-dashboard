import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.colors import CHART_COLORS, PRIMARY_PURPLE, LIGHT_PURPLE, DARK_PURPLE

def mostrar_mapa_calor(df_recorte):
    st.subheader('🔥 Mapa de Calor: Correlação entre Uso de Funcionalidades')
    st.info('Para cada paciente, é verificado se ele utilizou (1) ou não (0) cada funcionalidade ao menos uma vez. A matriz de correlação mostra o quanto o uso de uma funcionalidade está associado ao uso das outras, variando de -1 (correlação negativa) a 1 (correlação positiva).')
    st.markdown('Análise comparativa das correlações entre funcionalidades: visão geral e por sexo.')
    
    funcionalidades_cols = ['symptomDiaries', 'acqs', 'activityLogs', 'prescriptions', 'crisis']
    funcionalidades_nomes = ['Diários', 'ACQ', 'Atividades', 'Prescrições', 'Crises']
    
    # Criar escala de cores personalizada baseada na nossa paleta
    custom_colorscale = [
        [0.0, "#F3F4F6"],      # Cinza claro para correlações baixas/negativas
        [0.2, "#DDD6FE"],      # Lavanda muito claro
        [0.4, "#C4B5FD"],      # Lavanda claro
        [0.6, "#A78BFA"],      # Lavanda médio
        [0.8, "#8B5CF6"],      # Roxo principal
        [1.0, "#7C3AED"]       # Roxo escuro para correlações altas
    ]
    
    def criar_matriz_correlacao(df_dados, titulo_sufixo=""):
        """Função auxiliar para criar matriz de correlação"""
        df_corr = pd.DataFrame()
        for col in funcionalidades_cols:
            df_corr[col] = df_dados[col].apply(lambda x: 1 if isinstance(x, list) and len(x) > 0 else 0)
        df_corr.columns = funcionalidades_nomes
        return df_corr.corr()
    
    # Layout em três colunas
    col_geral, col_masculino, col_feminino = st.columns(3)
    
    with col_geral:
        # Mapa de calor geral
        st.markdown("**Correlação Geral**")
        corr_matrix_geral = criar_matriz_correlacao(df_recorte)
        
        fig_heatmap_geral = go.Figure(data=go.Heatmap(
            z=corr_matrix_geral.values,
            x=corr_matrix_geral.columns,
            y=corr_matrix_geral.index,
            colorscale=custom_colorscale,
            zmin=-1, zmax=1,
            colorbar=dict(title='Correlação', x=1.02),
            text=corr_matrix_geral.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        fig_heatmap_geral.update_layout(
            title=f'Todos os Pacientes<br><small>({len(df_recorte)} pacientes)</small>',
            xaxis_title='',
            yaxis_title='',
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_heatmap_geral, use_container_width=True, height=400)
    
    with col_masculino:
        # Mapa de calor masculino
        st.markdown("**Correlação - Masculino**")
        df_masculino = df_recorte[df_recorte['sex'] == 'M']
        
        if len(df_masculino) > 1:  # Precisa de pelo menos 2 pacientes para correlação
            corr_matrix_masc = criar_matriz_correlacao(df_masculino)
            
            fig_heatmap_masc = go.Figure(data=go.Heatmap(
                z=corr_matrix_masc.values,
                x=corr_matrix_masc.columns,
                y=corr_matrix_masc.index,
                colorscale=custom_colorscale,
                zmin=-1, zmax=1,
                showscale=False,  # Não mostrar escala duplicada
                text=corr_matrix_masc.round(2).values,
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            fig_heatmap_masc.update_layout(
                title=f'Pacientes Masculinos<br><small>({len(df_masculino)} pacientes)</small>',
                xaxis_title='',
                yaxis_title='',
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_heatmap_masc, use_container_width=True, height=400)
        else:
            st.warning("Dados insuficientes para correlação (menos de 2 pacientes masculinos)")
    
    with col_feminino:
        # Mapa de calor feminino
        st.markdown("**Correlação - Feminino**")
        df_feminino = df_recorte[df_recorte['sex'] == 'F']
        
        if len(df_feminino) > 1:  # Precisa de pelo menos 2 pacientes para correlação
            corr_matrix_fem = criar_matriz_correlacao(df_feminino)
            
            fig_heatmap_fem = go.Figure(data=go.Heatmap(
                z=corr_matrix_fem.values,
                x=corr_matrix_fem.columns,
                y=corr_matrix_fem.index,
                colorscale=custom_colorscale,
                zmin=-1, zmax=1,
                showscale=False,  # Não mostrar escala duplicada
                text=corr_matrix_fem.round(2).values,
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            fig_heatmap_fem.update_layout(
                title=f'Pacientes Femininos<br><small>({len(df_feminino)} pacientes)</small>',
                xaxis_title='',
                yaxis_title='',
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_heatmap_fem, use_container_width=True, height=400)
        else:
            st.warning("Dados insuficientes para correlação (menos de 2 pacientes femininos)")
    
    # --- Análise Comparativa das Correlações ---
    st.markdown("---")
    st.subheader('📊 Análise Comparativa das Correlações')
    
    # Verificar se temos dados suficientes para análise comparativa
    if len(df_masculino) > 1 and len(df_feminino) > 1:
        col_analise, col_tabela = st.columns([2, 1])
        
        with col_analise:
            # Comparar correlações mais fortes
            st.markdown("**Correlações Mais Fortes por Grupo:**")
            
            # Função para encontrar correlações mais fortes (excluindo diagonal)
            def encontrar_correlacoes_fortes(matriz, nome_grupo):
                correlacoes = []
                for i in range(len(matriz.columns)):
                    for j in range(i+1, len(matriz.columns)):
                        func1 = matriz.columns[i]
                        func2 = matriz.columns[j]
                        corr_valor = matriz.iloc[i, j]
                        correlacoes.append({
                            'grupo': nome_grupo,
                            'funcionalidade_1': func1,
                            'funcionalidade_2': func2,
                            'correlacao': corr_valor
                        })
                return correlacoes
            
            # Obter correlações de todos os grupos
            corr_geral = encontrar_correlacoes_fortes(corr_matrix_geral, 'Geral')
            corr_masc = encontrar_correlacoes_fortes(corr_matrix_masc, 'Masculino')
            corr_fem = encontrar_correlacoes_fortes(corr_matrix_fem, 'Feminino')
            
            # Combinar e ordenar por valor absoluto
            todas_correlacoes = corr_geral + corr_masc + corr_fem
            df_correlacoes = pd.DataFrame(todas_correlacoes)
            df_correlacoes['correlacao_abs'] = df_correlacoes['correlacao'].abs()
            df_correlacoes = df_correlacoes.sort_values('correlacao_abs', ascending=False)
            
            # Mostrar top correlações por grupo
            for grupo in ['Geral', 'Masculino', 'Feminino']:
                top_grupo = df_correlacoes[df_correlacoes['grupo'] == grupo].head(3)
                st.markdown(f"**{grupo}:**")
                for _, row in top_grupo.iterrows():
                    st.markdown(f"• {row['funcionalidade_1']} ↔ {row['funcionalidade_2']}: {row['correlacao']:.3f}")
                st.markdown("")
        
        with col_tabela:
            st.markdown("**Resumo das Correlações:**")
            
            # Criar tabela resumo das correlações mais fortes
            resumo_correlacoes = []
            for grupo in ['Geral', 'Masculino', 'Feminino']:
                grupo_data = df_correlacoes[df_correlacoes['grupo'] == grupo]
                if not grupo_data.empty:
                    mais_forte = grupo_data.iloc[0]
                    resumo_correlacoes.append({
                        'Grupo': grupo,
                        'Correlação Mais Forte': f"{mais_forte['funcionalidade_1']} ↔ {mais_forte['funcionalidade_2']}",
                        'Valor': f"{mais_forte['correlacao']:.3f}"
                    })
            
            df_resumo = pd.DataFrame(resumo_correlacoes)
            
            st.dataframe(
                df_resumo,
                use_container_width=True,
                column_config={
                    "Grupo": st.column_config.TextColumn("Grupo", width="small"),
                    "Correlação Mais Forte": st.column_config.TextColumn("Correlação Mais Forte", width="large"),
                    "Valor": st.column_config.TextColumn("Valor", width="small")
                }
            )
            
            # Download das correlações
            csv_correlacoes = df_correlacoes.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Correlações (CSV)",
                data=csv_correlacoes,
                file_name=f"correlacoes_funcionalidades_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Insights
            st.markdown("**Insights:**")
            st.markdown("• Valores próximos a **1**: funcionalidades usadas juntas")
            st.markdown("• Valores próximos a **0**: uso independente")
            st.markdown("• Valores próximos a **-1**: uso mutuamente exclusivo")
    
    else:
        st.warning("Dados insuficientes para análise comparativa por sexo.")
    
    # Nota sobre dados pessoais
    pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
    if pacientes_indefinidos > 0:
        st.info(f"**Nota:** {pacientes_indefinidos} paciente(s) com sexo indefinido não aparecem na análise por sexo devido à política de exclusão de dados pessoais.")
    
    st.markdown('---')