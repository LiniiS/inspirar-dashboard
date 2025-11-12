import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.colors import CHART_COLORS, PRIMARY_DARK, PRIMARY_MEDIUM, PRIMARY_DARKER, PRIMARY_DARKEST

def mostrar_mapa_calor(df_recorte):
    st.subheader('Heatmap: Correlation between Feature Usage')
    st.info('For each patient, it checks if they used (1) or not (0) each feature at least once. '
            'The correlation matrix shows how much the use of one feature is associated with the use of others.')

    st.markdown('Comparative analysis of correlations between features: general view and by sex.')

    funcionalidades_cols = ['symptomDiaries', 'acqs', 'activityLogs', 'prescriptions', 'crisis']
    funcionalidades_nomes = ['Diaries', 'ACQ', 'Activities', 'Medications', 'Crises']

    # --------- Helpers ---------

    def criar_matriz_correlacao(df_dados: pd.DataFrame) -> pd.DataFrame:
        """Binariza o uso das funcionalidades e retorna a matriz de correlação."""
        df_bin = pd.DataFrame()
        for col in funcionalidades_cols:
            df_bin[col] = df_dados[col].apply(lambda x: 1 if isinstance(x, list) and len(x) > 0 else 0)
        df_bin.columns = funcionalidades_nomes
        return df_bin.corr()

    def escolher_paleta(cmin: float, cmax: float):
        """
        Decide paleta e limites:
        - Divergente centrada em 0 (RdBu_r) se houver valores negativos.
        - Sequencial uniforme (cividis) se todos >= 0.
        Retorna: (colorscale, zmin, zmax, zmid, colorbar_dict)
        """
        if cmin < 0:
            return 'RdBu_r', -1, 1, 0, dict(title='Correlation', tickvals=[-1, -0.5, 0, 0.5, 1])
        else:
            return 'cividis', 0, 1, None, dict(title='Correlation', tickvals=[0, 0.25, 0.5, 0.75, 1])

    def heatmap_plot(matriz_corr: pd.DataFrame, titulo: str, mostrar_escala: bool = True, altura: int = 420) -> go.Figure:
        """
        Cria o heatmap mostrando a matriz completa.
        Anotações com contraste adaptativo.
        """
        # Usar matriz completa sem mascarar
        m = matriz_corr.copy()

        # Limites para escolher paleta
        cmin = np.nanmin(m.values)
        cmax = np.nanmax(m.values)
        if np.isnan(cmin) or np.isnan(cmax):
            cmin, cmax = 0.0, 1.0  # fallback seguro

        colorscale, zmin, zmax, zmid, cbar = escolher_paleta(cmin, cmax)

        fig = go.Figure()

        fig.add_trace(go.Heatmap(
            z=m.values,
            x=m.columns,
            y=m.index,
            colorscale=colorscale,
            zmin=zmin, zmax=zmax,
            zmid=zmid,                 # usado quando divergente
            showscale=mostrar_escala,
            colorbar=cbar if mostrar_escala else None,
            hovertemplate=" %{y} ↔ %{x}<br>corr=%{z:.2f}<extra></extra>",
        ))

        # Anotações (preto em células claras, branco em escuras)
        for i, yi in enumerate(m.index):
            for j, xj in enumerate(m.columns):
                val = m.iat[i, j]
                if np.isnan(val):
                    continue
                # normaliza para 0..1 com base em zmin/zmax
                norm = (val - zmin) / (zmax - zmin + 1e-9)
                text_color = "black" if norm > 0.55 else "white"
                fig.add_annotation(
                    x=xj, y=yi, text=f"{val:.1f}",
                    showarrow=False,
                    font=dict(color=text_color, size=11)
                )

        fig.update_layout(
            title=titulo,
            xaxis=dict(title='', tickangle=0, side='bottom', constrain='domain'),
            yaxis=dict(title='', autorange='reversed'),  # mesma ordem em X e Y
            margin=dict(l=50, r=20, t=60, b=40),
            height=altura
        )
        return fig

    # --------- 3 colunas: Geral, Masculino, Feminino ---------

    col_geral, col_masculino, col_feminino = st.columns(3)

    # --- Geral
    with col_geral:
        st.markdown("**General Correlation**")
        corr_matrix_geral = criar_matriz_correlacao(df_recorte)
        fig_heatmap_geral = heatmap_plot(
            corr_matrix_geral,
            titulo=f'All Patients ({len(df_recorte)} patients)',
            mostrar_escala=True
        )
        st.plotly_chart(fig_heatmap_geral, use_container_width=True)

    # --- Masculino
    with col_masculino:
        st.markdown("**Correlation - Male**")
        df_masculino = df_recorte[df_recorte['sex'] == 'M']
        if len(df_masculino) > 1:
            corr_matrix_masc = criar_matriz_correlacao(df_masculino)
            fig_heatmap_masc = heatmap_plot(
                corr_matrix_masc,
                titulo=f'Male Patients ({len(df_masculino)} patients)',
                mostrar_escala=True
            )
            st.plotly_chart(fig_heatmap_masc, use_container_width=True)
        else:
            corr_matrix_masc = None
            st.warning("Insufficient data for correlation (less than 2 male patients)")

    # --- Feminino
    with col_feminino:
        st.markdown("**Correlation - Female**")
        df_feminino = df_recorte[df_recorte['sex'] == 'F']
        if len(df_feminino) > 1:
            corr_matrix_fem = criar_matriz_correlacao(df_feminino)
            fig_heatmap_fem = heatmap_plot(
                corr_matrix_fem,
                titulo=f'Female Patients ({len(df_feminino)} patients)',
                mostrar_escala=True
            )
            st.plotly_chart(fig_heatmap_fem, use_container_width=True)
        else:
            corr_matrix_fem = None
            st.warning("Insufficient data for correlation (less than 2 female patients)")

    # --------- Análise comparativa (se houver dados) ---------
    st.markdown("---")
    st.subheader('Comparative Correlation Analysis')

    if (len(df_masculino) > 1 and len(df_feminino) > 1) and (corr_matrix_masc is not None and corr_matrix_fem is not None):
        col_analise, col_tabela = st.columns([2, 1])

        with col_analise:
            st.markdown("**Strongest Correlations by Group:**")

            def encontrar_correlacoes_fortes(matriz, nome_grupo):
                correlacoes = []
                for i in range(len(matriz.columns)):
                    for j in range(i + 1, len(matriz.columns)):
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

            corr_geral = encontrar_correlacoes_fortes(corr_matrix_geral, 'General')
            corr_masc = encontrar_correlacoes_fortes(corr_matrix_masc, 'Male')
            corr_fem = encontrar_correlacoes_fortes(corr_matrix_fem, 'Female')

            todas_correlacoes = corr_geral + corr_masc + corr_fem
            df_correlacoes = pd.DataFrame(todas_correlacoes)
            df_correlacoes['correlacao_abs'] = df_correlacoes['correlacao'].abs()
            df_correlacoes = df_correlacoes.sort_values('correlacao_abs', ascending=False)

            for grupo in ['General', 'Male', 'Female']:
                top_grupo = df_correlacoes[df_correlacoes['grupo'] == grupo].head(3)
                st.markdown(f"**{grupo}:**")
                for _, row in top_grupo.iterrows():
                    st.markdown(f"• {row['funcionalidade_1']} ↔ {row['funcionalidade_2']}: {row['correlacao']:.3f}")
                st.markdown("")

        with col_tabela:
            st.markdown("**Correlation Summary:**")
            resumo_correlacoes = []
            for grupo in ['General', 'Male', 'Female']:
                grupo_data = df_correlacoes[df_correlacoes['grupo'] == grupo]
                if not grupo_data.empty:
                    mais_forte = grupo_data.iloc[0]
                    resumo_correlacoes.append({
                        'Group': grupo,
                        'Strongest Correlation': f"{mais_forte['funcionalidade_1']} ↔ {mais_forte['funcionalidade_2']}",
                        'Value': f"{mais_forte['correlacao']:.3f}"
                    })

            df_resumo = pd.DataFrame(resumo_correlacoes)
            st.dataframe(
                df_resumo,
                use_container_width=True,
                column_config={
                    "Group": st.column_config.TextColumn("Group", width="small"),
                    "Strongest Correlation": st.column_config.TextColumn("Strongest Correlation", width="large"),
                    "Value": st.column_config.TextColumn("Value", width="small")
                }
            )

            csv_correlacoes = df_correlacoes.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Correlations (CSV)",
                data=csv_correlacoes,
                file_name=f"correlacoes_funcionalidades_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

            st.markdown("**Insights:**")
            st.markdown("• Values close to **1**: features used together")
            st.markdown("• Values close to **0**: independent use")
            st.markdown("• Values close to **-1**: mutually exclusive use")
    else:
        st.warning("Insufficient data for comparative analysis by sex.")

    # Nota sobre dados pessoais
    pacientes_indefinidos = len(df_recorte[df_recorte['sex'] == 'I'])
    if pacientes_indefinidos > 0:
        st.info(f"**Note:** {pacientes_indefinidos} patient(s) with undefined sex do not appear in the sex analysis "
                f"due to personal data exclusion policy.")
    st.markdown('---')
