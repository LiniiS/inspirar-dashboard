import json
import pandas as pd
from datetime import datetime

def carregar_json(uploaded_file):
    data = json.load(uploaded_file)
    return data

def processar_datas(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def obter_periodo_dados(df, col_data='createdAt'):
    """
    Obtém o período dos dados para exibição informativa.
    """
    if df.empty:
        return "período vazio", None, None
    
    # Encontrar a data mais antiga e mais recente nos dados
    data_min = df[col_data].min()
    data_max = df[col_data].max()
    
    # Formatar período para exibição
    mes_inicio = data_min.strftime('%b').lower()
    mes_fim = data_max.strftime('%b').lower()
    ano = data_min.year
    
    if mes_inicio == mes_fim:
        periodo_texto = f"{mes_inicio}/{ano}"
    else:
        periodo_texto = f"{mes_inicio}-{mes_fim}/{ano}"
    
    return periodo_texto, data_min, data_max 