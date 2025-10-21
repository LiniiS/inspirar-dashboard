import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.colors import CHART_COLORS, SECONDARY_DARKER, PRIMARY_DARKER

def mostrar_barplot_metricas(df_recorte, pacientes_recorte):
    st.subheader('Análise Descritiva e Distribuição de Métricas Numéricas')
    
    metricas_numericas = {
        'Idade': 'age',
        'Peso (kg)': 'weight',
        'Altura (m)': 'height',
    }
    
    df_recorte = df_recorte.copy()  # Evitar SettingWithCopyWarning
    
    if 'imc' not in df_recorte.columns:
        df_recorte['imc'] = df_recorte.apply(lambda row: row['weight'] / (row['height'] ** 2) if row['height'] and row['weight'] else np.nan, axis=1)
    metricas_numericas['IMC'] = 'imc'
    
    # Removido ACQ inicial - não adequado para barplot
    
    for col in ['media_presc_semana', 'media_diario_semana', 'media_atividade_semana', 'percentual_acq']:
        if col in df_recorte.columns:
            nome = {
                'media_presc_semana': 'Média de prescrições/semana',
                'media_diario_semana': 'Média de diários/semana',
                'media_atividade_semana': 'Média de atividades/semana',
                'percentual_acq': '% semanas com ACQ preenchido',
            }[col]
            metricas_numericas[nome] = col
    
    metrica_escolhida = st.selectbox(
        "Selecione a métrica para análise:",
        list(metricas_numericas.keys()),
        index=0
    )
    
    coluna = metricas_numericas[metrica_escolhida]
    valores_validos = df_recorte[coluna].replace(0, np.nan).dropna()
    
    # Estatísticas descritivas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Média', f'{valores_validos.mean():.2f}')
    col2.metric('Desvio padrão', f'{valores_validos.std():.2f}')
    col3.metric('Mediana', f'{valores_validos.median():.2f}')
    col4.metric('IQR (25%-75%)', f'{valores_validos.quantile(0.25):.2f} - {valores_validos.quantile(0.75):.2f}')
    
    st.markdown(f"### Distribuição Percentual de {metrica_escolhida}")
    
    # Criar colunas para o gráfico de barras e tabela lado a lado
    col_grafico, col_tabela = st.columns([3, 2])
    
    with col_grafico:
        # Criar faixas/intervalos para a métrica
        def criar_faixas(valores, metrica_nome):
            """Cria faixas apropriadas para cada tipo de métrica"""
            valores_limpos = valores.dropna()
            if len(valores_limpos) == 0:
                return pd.DataFrame()
            
            if metrica_nome == 'Idade':
                # Faixas de idade: 0-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71+
                bins = [0, 20, 30, 40, 50, 60, 70, 100]
                labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
            elif metrica_nome == 'Peso (kg)':
                # Faixas de peso: 0-50, 51-60, 61-70, 71-80, 81-90, 91-100, 101+
                bins = [0, 50, 60, 70, 80, 90, 100, 200]
                labels = ['0-50kg', '51-60kg', '61-70kg', '71-80kg', '81-90kg', '91-100kg', '101+kg']
            elif metrica_nome == 'Altura (m)':
                # Faixas de altura: 1.40-1.50, 1.51-1.60, 1.61-1.70, 1.71-1.80, 1.81-1.90, 1.91+
                bins = [1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.20]
                labels = ['1.40-1.50m', '1.51-1.60m', '1.61-1.70m', '1.71-1.80m', '1.81-1.90m', '1.91+m']
            elif metrica_nome == 'IMC':
                # Faixas de IMC: <18.5, 18.5-24.9, 25-29.9, 30-34.9, 35-39.9, 40+
                bins = [0, 18.5, 25, 30, 35, 40, 100]
                labels = ['<18.5', '18.5-24.9', '25-29.9', '30-34.9', '35-39.9', '40+']
            # Removido ACQ - não adequado para barplot
            else:
                # Faixas genéricas baseadas em quartis
                q25, q50, q75 = valores_limpos.quantile([0.25, 0.5, 0.75])
                bins = [valores_limpos.min(), q25, q50, q75, valores_limpos.max()]
                labels = [f'Q1', f'Q2', f'Q3', f'Q4']
            
            # Criar faixas
            faixas = pd.cut(valores_limpos, bins=bins, labels=labels, include_lowest=True)
            contagem = faixas.value_counts().sort_index()
            percentual = (contagem / len(valores_limpos) * 100).round(1)
            
            return pd.DataFrame({
                'Faixa': contagem.index,
                'Contagem': contagem.values,
                'Percentual': percentual.values
            })
        
        # Criar dados para o gráfico de barras
        df_faixas = criar_faixas(valores_validos, metrica_escolhida)
        
        if not df_faixas.empty:
            # Gráfico de barras com paleta escura e contorno
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=df_faixas['Faixa'],
                    y=df_faixas['Percentual'],
                    marker=dict(
                        color=PRIMARY_DARKER,
                        line=dict(
                            color=PRIMARY_DARKER,
                            width=2
                        )
                    ),
                    hovertemplate='<b>%{x}</b><br>Pacientes: %{y:.1f}%<extra></extra>'
                )
            ])
            
            fig_bar.update_layout(
                title=f'Distribuição Percentual de {metrica_escolhida}',
                xaxis_title='Faixas',
                yaxis_title='Percentual de Pacientes (%)',
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#333333'),
                xaxis=dict(
                    tickangle=45,
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)'
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True, height=400)
        else:
            st.warning("Não há dados suficientes para criar o gráfico de distribuição.")
    
    with col_tabela:
        # Tabela com distribuição por faixas
        st.markdown(f"**Distribuição de {metrica_escolhida}**")
        
        if not df_faixas.empty:
            # Exibir tabela de distribuição
            st.dataframe(
                df_faixas,
                use_container_width=True,
                column_config={
                    "Faixa": st.column_config.TextColumn("Faixa", width="medium"),
                    "Contagem": st.column_config.NumberColumn("Pacientes", width="small"),
                    "Percentual": st.column_config.NumberColumn("Percentual (%)", format="%.1f", width="small")
                }
            )
            
            # Resumo estatístico
            st.markdown("**Resumo Estatístico:**")
            st.markdown(f"• Total de pacientes: {len(valores_validos)}")
            st.markdown(f"• Faixa mais comum: {df_faixas.loc[df_faixas['Percentual'].idxmax(), 'Faixa']} ({df_faixas['Percentual'].max():.1f}%)")
            st.markdown(f"• Faixa menos comum: {df_faixas.loc[df_faixas['Percentual'].idxmin(), 'Faixa']} ({df_faixas['Percentual'].min():.1f}%)")
            
            # Botão de download da distribuição
            csv_faixas = df_faixas.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download da Distribuição (CSV)",
                data=csv_faixas,
                file_name=f"distribuicao_{metrica_escolhida.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Não há dados suficientes para mostrar a distribuição.")
        
        # Separador
        st.markdown("---")
        
        # Tabela detalhada com dados individuais (colapsável)
        with st.expander("Ver dados individuais dos pacientes"):
            # Criar DataFrame para a tabela detalhada
            colunas_tabela = [coluna, 'sex', 'id']
            if coluna != 'age':
                colunas_tabela.append('age')
            
            df_tabela = df_recorte[colunas_tabela].copy()
            df_tabela = df_tabela.dropna(subset=[coluna])
            
            # Ordenar por valor ANTES da renomeação das colunas
            df_tabela = df_tabela.sort_values(coluna, ascending=False)
            
            # Renomear colunas para melhor legibilidade
            df_tabela = df_tabela.rename(columns={
                coluna: 'Valor',
                'sex': 'Sexo',
                'id': 'ID do Paciente'
            })
            
            # Adicionar coluna de idade se não for a métrica selecionada
            if coluna != 'age':
                df_tabela = df_tabela.rename(columns={'age': 'Idade'})
            else:
                # Se a métrica selecionada é 'age', renomear para 'Idade' também
                df_tabela = df_tabela.rename(columns={'Valor': 'Idade'})
            
            # Mapear códigos de sexo
            df_tabela['Sexo'] = df_tabela['Sexo'].map({
                'M': 'M',
                'F': 'F',
                'I': 'Indefinido'
            })
            
            # Formatar valores numéricos
            if 'Idade' in df_tabela.columns:
                df_tabela['Idade'] = df_tabela['Idade'].astype(int)
            
            # Exibir tabela
            st.dataframe(
                df_tabela,
                use_container_width=True,
                column_config={
                    "ID do Paciente": st.column_config.TextColumn("ID do Paciente", width="medium"),
                    "Valor": st.column_config.NumberColumn("Valor", format="%.2f", width="medium"),
                    "Idade": st.column_config.NumberColumn("Idade", width="small"),
                    "Sexo": st.column_config.TextColumn("Sexo", width="small")
                }
            )
            
            # Botão de download dos dados individuais
            csv = df_tabela.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download dos Dados Individuais (CSV)",
                data=csv,
                file_name=f"dados_individuais_{metrica_escolhida.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Pirâmide etária removida
    
    st.markdown('---') 