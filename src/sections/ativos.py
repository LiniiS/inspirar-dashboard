import streamlit as st
import plotly.express as px
from utils.colors import CHART_COLORS

def mostrar_ativos(df_recorte):
    st.subheader('Distribuição de Pacientes Ativos vs Inativos')
    st.markdown('Mostra a proporção de pacientes que utilizaram pelo menos uma funcionalidade versus os inativos.')
    
    st.info('**Nota sobre dados pessoais:** Pacientes que solicitaram exclusão de conta e dados pessoais têm seus dados de saúde mantidos para fins médicos, mas todos os dados pessoais (incluindo sexo) são removidos. Nestes casos, o sexo é registrado como "INDEFINIDO (I)" e esses pacientes não são representados no gráfico de distribuição por sexo dos usuários ativos.')
    
    def paciente_ativo(row):
        return any([
            isinstance(row['symptomDiaries'], list) and len(row['symptomDiaries']) > 0,
            isinstance(row['acqs'], list) and len(row['acqs']) > 0,
            isinstance(row['activityLogs'], list) and len(row['activityLogs']) > 0,
            isinstance(row['prescriptions'], list) and len(row['prescriptions']) > 0,
            isinstance(row['crisis'], list) and len(row['crisis']) > 0
        ])
    
    df_recorte = df_recorte.copy()  # Evitar SettingWithCopyWarning
    df_recorte['is_ativo'] = df_recorte.apply(paciente_ativo, axis=1)
    n_ativos = df_recorte['is_ativo'].sum()
    n_inativos = len(df_recorte) - n_ativos
    
    # Criar colunas para os gráficos lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Ativos vs Inativos
        fig_pizza_ativos = px.pie(
            names=['Ativos', 'Inativos'],
            values=[n_ativos, n_inativos],
            color_discrete_sequence=[CHART_COLORS[2], CHART_COLORS[4]],
            title='Distribuição de Pacientes Ativos vs Inativos'
        )
        fig_pizza_ativos.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_pizza_ativos, use_container_width=True, height=400)
    
    with col2:
        # Gráfico de distribuição por sexo - Apenas pacientes ativos
        df_ativos = df_recorte[df_recorte['is_ativo'] == True]
        
        if len(df_ativos) > 0:
            # Filtrar apenas sexos válidos (excluir 'I' - indefinido)
            df_ativos_sexo = df_ativos[df_ativos['sex'].isin(['M', 'F'])]
            
            if len(df_ativos_sexo) > 0:
                # Contar pacientes ativos por sexo
                sexo_counts = df_ativos_sexo['sex'].value_counts()
                
                # Mapear códigos para nomes completos
                sexo_labels = {'M': 'Masculino', 'F': 'Feminino'}
                sexo_counts_labeled = sexo_counts.rename(index=sexo_labels)
                
                fig_sexo_ativos = px.pie(
                    values=sexo_counts_labeled.values,
                    names=sexo_counts_labeled.index,
                    color_discrete_sequence=CHART_COLORS[2:4],
                    title='Distribuição por Sexo - Pacientes Ativos'
                )
                fig_sexo_ativos.update_layout(
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig_sexo_ativos, use_container_width=True, height=400)
                
                # Métricas resumidas
                st.markdown(f"**Total de pacientes ativos: {len(df_ativos)}**")
                st.markdown(f"**Ativos por sexo:** Masculino: {sexo_counts.get('M', 0)}, Feminino: {sexo_counts.get('F', 0)}")
            else:
                st.warning("Não há pacientes ativos com sexo definido para análise.")
        else:
            st.warning("Não há pacientes ativos para análise de distribuição por sexo.")
    
    st.markdown('---') 