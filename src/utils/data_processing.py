import json
import pandas as pd
from datetime import datetime
from dateutil import parser

# Constante para data limite: pacientes criados a partir de 01/03/2025
DATA_LIMITE_MARCO_2025 = pd.Timestamp('2025-03-01').tz_localize('UTC')

def carregar_json(uploaded_file):
    data = json.load(uploaded_file)
    return data

def processar_datas(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def filtrar_pacientes_marco_2025(pacientes, col_created_at='createdAt'):
    """
    Filtra pacientes criados a partir de março de 2025 (01/03/2025).
    
    CRÍTICO: Esta função garante que apenas pacientes com contas criadas a partir
    de 01/03/2025 sejam incluídos nas análises e gráficos do dashboard.
    
    Args:
        pacientes: Lista de dicionários de pacientes OU DataFrame pandas
        col_created_at: Nome da coluna com data de criação (padrão: 'createdAt')
    
    Returns:
        - Se entrada for DataFrame: DataFrame filtrado
        - Se entrada for lista: Lista filtrada de dicionários
        - Apenas pacientes com createdAt >= 2025-03-01 são retornados
    """
    if isinstance(pacientes, pd.DataFrame):
        # Se for DataFrame
        df = pacientes.copy()
        if col_created_at in df.columns:
            # Garantir que a coluna está como datetime
            if not pd.api.types.is_datetime64_any_dtype(df[col_created_at]):
                df[col_created_at] = pd.to_datetime(df[col_created_at], errors='coerce')
            # Filtrar pacientes criados a partir de março/2025
            df_filtrado = df[df[col_created_at] >= DATA_LIMITE_MARCO_2025]
            return df_filtrado
        return df
    else:
        # Se for lista de dicionários
        pacientes_filtrados = []
        for paciente in pacientes:
            data_cadastro = paciente.get(col_created_at)
            if data_cadastro:
                # Converter string para datetime se necessário
                if isinstance(data_cadastro, str):
                    try:
                        data_cadastro = parser.parse(data_cadastro)
                    except (ValueError, TypeError):
                        continue
                
                # Converter para Timestamp com timezone UTC se necessário
                if isinstance(data_cadastro, pd.Timestamp):
                    data_ts = data_cadastro
                elif hasattr(data_cadastro, 'tzinfo'):
                    # datetime com ou sem timezone
                    if data_cadastro.tzinfo is None:
                        data_ts = pd.Timestamp(data_cadastro).tz_localize('UTC')
                    else:
                        data_ts = pd.Timestamp(data_cadastro)
                else:
                    # Tentar converter para Timestamp
                    try:
                        data_ts = pd.Timestamp(data_cadastro)
                        if data_ts.tzinfo is None:
                            data_ts = data_ts.tz_localize('UTC')
                    except (ValueError, TypeError):
                        continue
                
                # Verificar se data é >= 01/03/2025
                if data_ts >= DATA_LIMITE_MARCO_2025:
                    pacientes_filtrados.append(paciente)
        
        return pacientes_filtrados

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