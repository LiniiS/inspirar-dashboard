import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS

def mostrar_funcionalidades_geral(df_recorte):
    st.markdown('Global overview of app feature usage by patients.')
    
    # --- Distribuição do Número de Funcionalidades Utilizadas por Paciente ---
    st.subheader('Distribution of Number of Features Used per Patient')
    st.info('For each patient, it counts how many different features they used at least once (symptom diary, ACQ, physical activity, prescription, crisis). The chart shows the distribution of this count among all patients.')
    
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
            labels={'x': 'Number of Features', 'y': 'Number of Patients'},
            title='Distribution of Number of Features Used',
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_func_count.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Number of Features Used",
            yaxis_title="Number of Patients"
        )
        st.plotly_chart(fig_func_count, use_container_width=True, height=400)
    
    with col_stats:
        st.markdown("**Usage Statistics:**")
        
        # Calcular estatísticas
        media_func = df_recorte['n_funcionalidades'].mean()
        mediana_func = df_recorte['n_funcionalidades'].median()
        moda_func = df_recorte['n_funcionalidades'].mode().iloc[0] if not df_recorte['n_funcionalidades'].mode().empty else 0
        
        st.metric("Average Features", f"{media_func:.1f}")
        st.metric("Median", f"{mediana_func:.0f}")
        st.metric("Mode (most common)", f"{moda_func:.0f}")
        
        # Distribuição percentual
        st.markdown("**Distribution:**")
        for n_func, count in dist_funcionalidades.items():
            perc = (count / len(df_recorte)) * 100
            st.markdown(f"• **{n_func} features:** {count} patients ({perc:.1f}%)")
        
        # Pacientes ativos vs inativos
        pacientes_ativos = len(df_recorte[df_recorte['n_funcionalidades'] > 0])
        pacientes_inativos = len(df_recorte[df_recorte['n_funcionalidades'] == 0])
        
        st.markdown("---")
        st.markdown("**General Summary:**")
        st.markdown(f"• **Active:** {pacientes_ativos} patients")
        st.markdown(f"• **Inactive:** {pacientes_inativos} patients")
        taxa_ativacao = (pacientes_ativos / len(df_recorte)) * 100 if len(df_recorte) > 0 else 0
        st.markdown(f"• **Activation Rate:** {taxa_ativacao:.1f}%")
    
    st.markdown('---')

    # --- Funcionalidades Mais Utilizadas ---
    st.subheader('Most Used Features Ranking')
    st.info('For each feature, it counts the number of patients who used it at least once in the analyzed period. The chart shows the ranking of the most accessed features.')
    
    # Calcular uso de cada funcionalidade
    funcionalidades = {
        'Symptom Diaries': df_recorte['symptomDiaries'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'ACQ (Asthma Control)': df_recorte['acqs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Physical Activities': df_recorte['activityLogs'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Medications': df_recorte['prescriptions'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum(),
        'Crisis Records': df_recorte['crisis'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).sum()
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
            title="Feature Ranking by Number of Users",
            labels={'x': 'Number of Users', 'y': 'Feature'},
            color_discrete_sequence=[CHART_COLORS[1]]
        )
        fig_funcionalidades.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title="Number of Users",
            yaxis_title="Features",
            showlegend=False
        )
        st.plotly_chart(fig_funcionalidades, use_container_width=True, height=400)
    
    with col_tabela:
        st.markdown("**Detailed Data:**")
        
        # Criar tabela com ranking
        tabela_ranking = []
        total_pacientes = len(df_recorte)
        
        for i, (func_nome, usuarios) in enumerate(func_ordenadas.items(), 1):
            taxa_uso = (usuarios / total_pacientes) * 100 if total_pacientes > 0 else 0
            tabela_ranking.append({
                'Position': f"{i}",
                'Feature': func_nome,
                'Users': usuarios,
                'Usage Rate': f"{taxa_uso:.1f}%"
            })
        
        df_ranking = pd.DataFrame(tabela_ranking)
        
        st.dataframe(
            df_ranking,
            use_container_width=True,
            column_config={
                "Position": st.column_config.TextColumn("Pos.", width="small"),
                "Feature": st.column_config.TextColumn("Feature", width="large"),
                "Users": st.column_config.NumberColumn("Users", width="small"),
                "Usage Rate": st.column_config.TextColumn("Rate", width="small")
            }
        )
        
        # Insights
        st.markdown("**Insights:**")
        if func_ordenadas:
            mais_usada = list(func_ordenadas.keys())[0]
            menos_usada = list(func_ordenadas.keys())[-1]
            
            taxa_mais_usada = (list(func_ordenadas.values())[0] / total_pacientes) * 100
            taxa_menos_usada = (list(func_ordenadas.values())[-1] / total_pacientes) * 100
            
            st.markdown(f"• **Most used:** {mais_usada}")
            st.markdown(f"• **Rate:** {taxa_mais_usada:.1f}%")
            st.markdown(f"• **Least used:** {menos_usada}")
            st.markdown(f"• **Rate:** {taxa_menos_usada:.1f}%")
            
            diferenca = taxa_mais_usada - taxa_menos_usada
            st.markdown(f"• **Difference:** {diferenca:.1f}%")
        
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
    st.subheader('General Distribution by Sex')
    st.markdown('Summary view of patient distribution by sex.')
    
    if 'sex' in df_recorte.columns:
        # Calcular distribuição por sexo
        sex_counts = df_recorte['sex'].value_counts(dropna=False)
        sex_mapping = {'M': 'Male', 'F': 'Female', 'I': 'Undefined'}
        
        # Layout lado a lado: gráfico de pizza e métricas
        col_pizza, col_metricas = st.columns([2, 1])
        
        with col_pizza:
            # Preparar dados para o gráfico
            sex_labels = [sex_mapping.get(sex, str(sex)) for sex in sex_counts.index]
            
            fig_sexo = px.pie(
                values=sex_counts.values,
                names=sex_labels,
                title="Patient Distribution by Sex",
                color_discrete_sequence=CHART_COLORS[2:5]
            )
            fig_sexo.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_sexo, use_container_width=True, height=400)
        
        with col_metricas:
            st.markdown("**Detailed Distribution:**")
            
            total_pacientes = len(df_recorte)
            for sex_code, count in sex_counts.items():
                sex_name = sex_mapping.get(sex_code, str(sex_code))
                percentage = (count / total_pacientes) * 100 if total_pacientes > 0 else 0
                
                st.metric(
                    label=sex_name,
                    value=f"{count} patients",
                    delta=f"{percentage:.1f}%"
                )
            
            st.markdown("---")
            st.markdown("**Notes:**")
            
            # Verificar se há pacientes com sexo indefinido
            indefinidos = sex_counts.get('I', 0)
            if indefinidos > 0:
                st.markdown(f"• **{indefinidos} patient(s)** with undefined sex due to personal data exclusion policy")
            
            # Mostrar proporção masculino/feminino (excluindo indefinidos)
            masculino = sex_counts.get('M', 0)
            feminino = sex_counts.get('F', 0)
            total_definido = masculino + feminino
            
            if total_definido > 0:
                prop_masc = (masculino / total_definido) * 100
                prop_fem = (feminino / total_definido) * 100
                st.markdown(f"• **M/F Proportion:** {prop_masc:.1f}% / {prop_fem:.1f}%")
    else:
        st.warning('Field "sex" not found in data.')
    
    st.markdown('---')
