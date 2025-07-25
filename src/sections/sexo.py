import streamlit as st
import pandas as pd

def mostrar_sexo(df_recorte):
    st.subheader('👤 Distribuição e Funcionalidades por Sexo')
    st.markdown('Distribuição percentual dos pacientes por sexo e uso de funcionalidades por sexo.')
    if 'sex' in df_recorte.columns:
        sex_counts = df_recorte['sex'].value_counts(dropna=False)
        sex_perc = 100 * sex_counts / len(df_recorte) if len(df_recorte) > 0 else 0
        dist_sex_df = pd.DataFrame({'Quantidade': sex_counts, 'Percentual (%)': sex_perc.round(1)})
        funcionalidades_sex = {}
        for func in ['symptomDiaries', 'acqs', 'activityLogs', 'prescriptions', 'crisis']:
            funcionalidades_sex[func] = df_recorte.groupby('sex', observed=False)[func].apply(lambda x: x.apply(lambda y: len(y) > 0 if isinstance(y, list) else False).sum())
        func_sex_df = pd.DataFrame(funcionalidades_sex)
        col1, col2 = st.columns(2)
        with col1:
            st.write('**Distribuição percentual por sexo:**')
            st.dataframe(dist_sex_df)
        with col2:
            st.write('**Número de usuários por sexo que utilizaram cada funcionalidade:**')
            st.dataframe(func_sex_df)
    else:
        st.info('Campo "sex" não encontrado nos dados.')
    st.markdown('---') 