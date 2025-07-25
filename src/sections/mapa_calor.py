import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def mostrar_mapa_calor(df_recorte):
    st.subheader('🔥 Mapa de Calor: Correlação entre Uso de Funcionalidades')
    st.info('Para cada paciente, é verificado se ele utilizou (1) ou não (0) cada funcionalidade ao menos uma vez. A matriz de correlação mostra o quanto o uso de uma funcionalidade está associado ao uso das outras, variando de -1 (correlação negativa) a 1 (correlação positiva).')
    st.markdown('Visualização das correlações entre o uso das diferentes funcionalidades do sistema.')
    funcionalidades_cols = ['symptomDiaries', 'acqs', 'activityLogs', 'prescriptions', 'crisis']
    df_corr = pd.DataFrame()
    for col in funcionalidades_cols:
        df_corr[col] = df_recorte[col].apply(lambda x: 1 if isinstance(x, list) and len(x) > 0 else 0)
    df_corr.columns = ['Symptom Diaries', 'ACQs', 'Activity Logs', 'Prescriptions', 'Crisis']
    corr_matrix = df_corr.corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        colorbar=dict(title='Correlação')
    ))
    fig_heatmap.update_layout(
        title='Correlação entre Uso de Funcionalidades',
        xaxis_title='',
        yaxis_title='',
        autosize=True
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('---') 