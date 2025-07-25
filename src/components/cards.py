import streamlit as st

def card_metric(title, value, emoji=None, color='#f5f5f5'):
    st.markdown(f"""
    <div style='background-color:{color};padding:20px 10px 20px 10px;margin-bottom:20px;border-radius:10px;text-align:center;'>
    <span style='font-size:2em;'>{emoji if emoji else ''}</span><br>
    <b>{title}</b><br>
    <span style='font-size:2.5em;font-weight:bold'>{value}</span>
    </div>
    """, unsafe_allow_html=True) 