import json
import pandas as pd

def carregar_json(uploaded_file):
    data = json.load(uploaded_file)
    return data

def processar_datas(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    return df 