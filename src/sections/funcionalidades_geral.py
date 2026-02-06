import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.colors import CHART_COLORS
from utils.translations import t

def mostrar_funcionalidades_geral(df_recorte):
    st.markdown(t('sections.funcionalidades_geral.description'))
    
    # --- Distribuição do Número de Funcionalidades Utilizadas por Paciente ---
    st.subheader(t('sections.funcionalidades_geral.distribution_title'))
    st.info(t('sections.funcionalidades_geral.distribution_info'))
    
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
            labels={'x': t('sections.funcionalidades_geral.number_of_features'), 'y': t('sections.funcionalidades_geral.number_of_patients')},
            title=t('charts.titles.features_distribution'),
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig_func_count.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('sections.funcionalidades_geral.number_of_features'),
            yaxis_title=t('sections.funcionalidades_geral.number_of_patients')
        )
        st.plotly_chart(fig_func_count, use_container_width=True, height=400)
    
    with col_stats:
        st.markdown(f"**{t('sections.funcionalidades_geral.usage_statistics')}**")
        
        # Calcular estatísticas
        media_func = df_recorte['n_funcionalidades'].mean()
        mediana_func = df_recorte['n_funcionalidades'].median()
        moda_func = df_recorte['n_funcionalidades'].mode().iloc[0] if not df_recorte['n_funcionalidades'].mode().empty else 0
        
        st.metric(t('sections.funcionalidades_geral.average_features'), f"{media_func:.1f}")
        st.metric(t('sections.funcionalidades_geral.median'), f"{mediana_func:.0f}")
        st.metric(t('sections.funcionalidades_geral.mode_most_common'), f"{moda_func:.0f}")
        
        # Distribuição percentual
        st.markdown(f"**{t('sections.funcionalidades_geral.distribution')}**")
        for n_func, count in dist_funcionalidades.items():
            perc = (count / len(df_recorte)) * 100
            st.markdown(f"• **{n_func} {t('sections.funcionalidades_geral.features')}:** {count} {t('sections.funcionalidades_geral.patients')} ({perc:.1f}%)")
        
        # Pacientes ativos vs inativos
        pacientes_ativos = len(df_recorte[df_recorte['n_funcionalidades'] > 0])
        pacientes_inativos = len(df_recorte[df_recorte['n_funcionalidades'] == 0])
        
        st.markdown("---")
        st.markdown(f"**{t('sections.funcionalidades_geral.general_summary')}**")
        st.markdown(f"• **{t('sections.funcionalidades_geral.active')}:** {pacientes_ativos} {t('sections.funcionalidades_geral.patients')}")
        st.markdown(f"• **{t('sections.funcionalidades_geral.inactive')}:** {pacientes_inativos} {t('sections.funcionalidades_geral.patients')}")
        taxa_ativacao = (pacientes_ativos / len(df_recorte)) * 100 if len(df_recorte) > 0 else 0
        st.markdown(f"• **{t('sections.funcionalidades_geral.activation_rate')}:** {taxa_ativacao:.1f}%")
    
    st.markdown('---')

    # --- Funcionalidades Mais Utilizadas ---
    st.subheader(t('sections.funcionalidades_geral.most_used_title'))
    st.info(t('sections.funcionalidades_geral.most_used_info'))
    
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
            title=t('charts.titles.most_used_features'),
            labels={'x': t('sections.funcionalidades_geral.number_of_patients'), 'y': 'Feature'},
            color_discrete_sequence=[CHART_COLORS[1]]
        )
        fig_funcionalidades.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis_title=t('sections.funcionalidades_geral.number_of_patients'),
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
    
    # --- Distribuição por Gênero (Resumo) ---
    st.subheader('General Distribution by Gender')
    st.markdown('Summary view of patient distribution by gender.')
    
    if 'gender' in df_recorte.columns:
        # Calcular distribuição por gênero
        gender_counts = df_recorte['gender'].value_counts(dropna=False)
        gender_mapping = {'male': t('sections.ativos.male'), 'female': t('sections.ativos.female')}
        
        # Layout lado a lado: gráfico de pizza e métricas
        col_pizza, col_metricas = st.columns([2, 1])
        
        with col_pizza:
            # Preparar dados para o gráfico
            gender_labels = [gender_mapping.get(gender, str(gender)) for gender in gender_counts.index]
            
            fig_gender = px.pie(
                values=gender_counts.values,
                names=gender_labels,
                title="Patient Distribution by Gender",
                color_discrete_sequence=CHART_COLORS[2:5]
            )
            fig_gender.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig_gender, use_container_width=True, height=400)
        
        with col_metricas:
            st.markdown("**Detailed Distribution:**")
            
            total_pacientes = len(df_recorte)
            for gender_code, count in gender_counts.items():
                gender_name = gender_mapping.get(gender_code, str(gender_code))
                percentage = (count / total_pacientes) * 100 if total_pacientes > 0 else 0
                
                st.metric(
                    label=gender_name,
                    value=f"{count} patients",
                    delta=f"{percentage:.1f}%"
                )
            
            st.markdown("---")
            st.markdown("**Notes:**")
            
            # Mostrar proporção masculino/feminino
            masculino = gender_counts.get('male', 0)
            feminino = gender_counts.get('female', 0)
            total_pacientes = masculino + feminino
            
            if total_pacientes > 0:
                prop_masc = (masculino / total_pacientes) * 100
                prop_fem = (feminino / total_pacientes) * 100
                st.markdown(f"• **M/F Proportion:** {prop_masc:.1f}% / {prop_fem:.1f}%")
    else:
        st.warning('Field "gender" not found in data.')
    
    st.markdown('---')
