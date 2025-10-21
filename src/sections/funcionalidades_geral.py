import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS

def mostrar_funcionalidades_geral(df_recorte):
    st.markdown('Visão global do uso das funcionalidades do aplicativo pelos pacientes.')
    
    # --- Distribuição do Número de Funcionalidades Utilizadas por Paciente ---
    st.subheader('Distribuição do Número de Funcionalidades Utilizadas por Paciente')
    st.info('Para cada paciente, é contado quantas funcionalidades diferentes ele utilizou ao menos uma vez (diário de sintomas, ACQ, atividade física, prescrição, crise). O gráfico mostra a distribuição dessa contagem entre todos os pacientes.')
    
    def conta_funcionalidades(row):
        return sum([
            isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
            isinstance(row['acqs'], list) and len(row['acqs']) > 0,
            isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
            isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
            isinstance(row['crisis'], list) and len(row['crisis']) > 0
        ])
    
    df_recorte = df_recorte.copy()  # Evitar SettingWithCopyWarning
    df_recorte['n_funcionalidades'] = df_recorte.apply(conta_funcionalidades, axis=1)
    dist_funcionalidades = df_recorte['n_funcionalidades'].value_counts().sort_index()
    
    # Layout lado a lado: gráfico e estatísticas
    col_grafico, col_stats = st.columns([2, 1])
    
    with col_grafico:
        fig_func_count = px.bar(
            x=dist_funcionalidades.index,
            y=dist_funcionalidades.values,
            labels={'x': 'Número de Funcionalidades', 'y': 'Número de Pacientes'},
            title='Distribuição do Número de Funcionalidades Utilizadas',
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_func_count.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Número de Funcionalidades Utilizadas",
            yaxis_title="Número de Pacientes"
        )
        st.plotly_chart(fig_func_count, use_container_width=True, height=400)
    
    with col_stats:
        st.markdown("**Estatísticas de Uso:**")
        
        # Calcular estatísticas
        media_func = df_recorte['n_funcionalidades'].mean()
        mediana_func = df_recorte['n_funcionalidades'].median()
        moda_func = df_recorte['n_funcionalidades'].mode().iloc[0] if not df_recorte['n_funcionalidades'].mode().empty else 0
        
        st.metric("Média de Funcionalidades", f"{media_func:.1f}")
        st.metric("Mediana", f"{mediana_func:.0f}")
        st.metric("Moda (mais comum)", f"{moda_func:.0f}")
        
        # Distribuição percentual
        st.markdown("**Distribuição:**")
        for n_func, count in dist_funcionalidades.items():
            perc = (count / len(df_recorte)) * 100
            st.markdown(f"• **{n_func} func:** {count} pacientes ({perc:.1f}%)")
        
        # Pacientes ativos vs inativos
        pacientes_ativos = len(df_recorte[df_recorte['n_funcionalidades'] > 0])
        pacientes_inativos = len(df_recorte[df_recorte['n_funcionalidades'] == 0])
        
        st.markdown("---")
        st.markdown("**Resumo Geral:**")
        st.markdown(f"• **Ativos:** {pacientes_ativos} pacientes")
        st.markdown(f"• **Inativos:** {pacientes_inativos} pacientes")
        taxa_ativacao = (pacientes_ativos / len(df_recorte)) * 100 if len(df_recorte) > 0 else 0
        st.markdown(f"• **Taxa de Ativação:** {taxa_ativacao:.1f}%")
    
    st.markdown('---')

    # --- Funcionalidades Mais Utilizadas ---
    st.subheader('Ranking de Funcionalidades Mais Utilizadas')
    st.info('Para cada funcionalidade, é contado o número de pacientes que a utilizou ao menos uma vez no período analisado. O gráfico mostra o ranking das funcionalidades mais acessadas.')
    
    # Calcular uso de cada funcionalidade
    funcionalidades = {
        'Diários de Sintomas': df_recorte['symptomDiaries'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'ACQ (Controle Asma)': df_recorte['acqs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Atividades Físicas': df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Prescrições': df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Registro de Crises': df_recorte['crisis'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
    }
    
    # Layout lado a lado: gráfico e tabela
    col_ranking, col_tabela = st.columns([2, 1])
    
    with col_ranking:
        # Ordenar funcionalidades por uso
        func_ordenadas = dict(sorted(funcionalidades.items(), key=lambda x: x[1], reverse=True))
        
        fig_funcionalidades = px.bar(
            x=list(func_ordenadas.values()),
            y=list(func_ordenadas.keys()),
            orientation='h',
            title="Ranking de Funcionalidades por Número de Usuários",
            labels={'x': 'Número de Usuários', 'y': 'Funcionalidade'},
            color_discrete_sequence=[CHART_COLORS[1]]
        )
        fig_funcionalidades.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Número de Usuários",
            yaxis_title="Funcionalidades",
            showlegend=False
        )
        st.plotly_chart(fig_funcionalidades, use_container_width=True, height=400)
    
    with col_tabela:
        st.markdown("**Dados Detalhados:**")
        
        # Criar tabela com ranking
        tabela_ranking = []
        total_pacientes = len(df_recorte)
        
        for i, (func_nome, usuarios) in enumerate(func_ordenadas.items(), 1):
            taxa_uso = (usuarios / total_pacientes) * 100 if total_pacientes > 0 else 0
            tabela_ranking.append({
                'Posição': f"{i}º",
                'Funcionalidade': func_nome,
                'Usuários': usuarios,
                'Taxa de Uso': f"{taxa_uso:.1f}%"
            })
        
        df_ranking = pd.DataFrame(tabela_ranking)
        
        st.dataframe(
            df_ranking,
            use_container_width=True,
            column_config={
                "Posição": st.column_config.TextColumn("Pos.", width="small"),
                "Funcionalidade": st.column_config.TextColumn("Funcionalidade", width="large"),
                "Usuários": st.column_config.NumberColumn("Usuários", width="small"),
                "Taxa de Uso": st.column_config.TextColumn("Taxa", width="small")
            }
        )
        
        # Insights
        st.markdown("**Insights:**")
        if func_ordenadas:
            mais_usada = list(func_ordenadas.keys())[0]
            menos_usada = list(func_ordenadas.keys())[-1]
            
            taxa_mais_usada = (list(func_ordenadas.values())[0] / total_pacientes) * 100
            taxa_menos_usada = (list(func_ordenadas.values())[-1] / total_pacientes) * 100
            
            st.markdown(f"• **Mais usada:** {mais_usada}")
            st.markdown(f"• **Taxa:** {taxa_mais_usada:.1f}%")
            st.markdown(f"• **Menos usada:** {menos_usada}")
            st.markdown(f"• **Taxa:** {taxa_menos_usada:.1f}%")
            
            diferenca = taxa_mais_usada - taxa_menos_usada
            st.markdown(f"• **Diferença:** {diferenca:.1f}%")
        
        # Botão de download
        csv_ranking = df_ranking.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Ranking (CSV)",
            data=csv_ranking,
            file_name=f"ranking_funcionalidades_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('---')
    
    # --- Distribuição por Sexo (Resumo) ---
    st.subheader('Distribuição Geral por Sexo')
    st.markdown('Visão resumida da distribuição de pacientes por sexo.')
    
    if 'sex' in df_recorte.columns:
        # Calcular distribuição por sexo
        sex_counts = df_recorte['sex'].value_counts(dropna=False)
        sex_mapping = {'M': 'Masculino', 'F': 'Feminino', 'I': 'Indefinido'}
        
        # Layout lado a lado: gráfico de pizza e métricas
        col_pizza, col_metricas = st.columns([2, 1])
        
        with col_pizza:
            # Preparar dados para o gráfico
            sex_labels = [sex_mapping.get(sex, str(sex)) for sex in sex_counts.index]
            
            fig_sexo = px.pie(
                values=sex_counts.values,
                names=sex_labels,
                title="Distribuição de Pacientes por Sexo",
                color_discrete_sequence=CHART_COLORS[2:5]
            )
            fig_sexo.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_sexo, use_container_width=True, height=400)
        
        with col_metricas:
            st.markdown("**Distribuição Detalhada:**")
            
            total_pacientes = len(df_recorte)
            for sex_code, count in sex_counts.items():
                sex_name = sex_mapping.get(sex_code, str(sex_code))
                percentage = (count / total_pacientes) * 100 if total_pacientes > 0 else 0
                
                st.metric(
                    label=sex_name,
                    value=f"{count} pacientes",
                    delta=f"{percentage:.1f}%"
                )
            
            st.markdown("---")
            st.markdown("**Observações:**")
            
            # Verificar se há pacientes com sexo indefinido
            indefinidos = sex_counts.get('I', 0)
            if indefinidos > 0:
                st.markdown(f"• **{indefinidos} paciente(s)** com sexo indefinido devido à política de exclusão de dados pessoais")
            
            # Mostrar proporção masculino/feminino (excluindo indefinidos)
            masculino = sex_counts.get('M', 0)
            feminino = sex_counts.get('F', 0)
            total_definido = masculino + feminino
            
            if total_definido > 0:
                prop_masc = (masculino / total_definido) * 100
                prop_fem = (feminino / total_definido) * 100
                st.markdown(f"• **Proporção M/F:** {prop_masc:.1f}% / {prop_fem:.1f}%")
    else:
        st.warning('Campo "sex" não encontrado nos dados.')
    
    st.markdown('---')
