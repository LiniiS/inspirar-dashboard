import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils.colors import CHART_COLORS

def mostrar_boxplot_metricas(df_recorte, pacientes_recorte):
    st.subheader('📊 Análise Descritiva e Boxplot de Métricas Numéricas')
    
    metricas_numericas = {
        'Idade': 'age',
        'Peso (kg)': 'weight',
        'Altura (m)': 'height',
    }
    
    df_recorte = df_recorte.copy()  # Evitar SettingWithCopyWarning
    
    if 'imc' not in df_recorte.columns:
        df_recorte['imc'] = df_recorte.apply(lambda row: row['weight'] / (row['height'] ** 2) if row['height'] and row['weight'] else np.nan, axis=1)
    metricas_numericas['IMC'] = 'imc'
    
    acq_iniciais = []
    for paciente in pacientes_recorte:
        acqs = paciente.get('acqs', [])
        if acqs:
            acq_iniciais.append(acqs[0].get('average', np.nan))
        else:
            acq_iniciais.append(np.nan)
    df_recorte['score_acq_inicial'] = acq_iniciais
    metricas_numericas['Score ACQ inicial'] = 'score_acq_inicial'
    
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
    
    st.markdown(f"### Boxplot e Dados de {metrica_escolhida}")
    
    # Criar colunas para o boxplot e tabela lado a lado
    col_grafico, col_tabela = st.columns([3, 2])
    
    with col_grafico:
        # Boxplot
        fig_box = px.box(
            df_recorte, 
            y=coluna, 
            points='all', 
            title=f'Boxplot de {metrica_escolhida}',
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_box.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_box, use_container_width=True, height=400)
    
    with col_tabela:
        # Tabela com os dados
        st.markdown(f"**Dados de {metrica_escolhida}**")
        
        # Criar DataFrame para a tabela
        # Verificar se a coluna selecionada já é 'age' para evitar duplicação
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
        
        # Resumo da tabela
        st.markdown(f"**Total de registros válidos: {len(df_tabela)}**")
        
        # Botão de download
        csv = df_tabela.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download dos Dados (CSV)",
            data=csv,
            file_name=f"{metrica_escolhida.replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---') 