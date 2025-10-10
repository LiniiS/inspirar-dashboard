# Paleta de tons escuros - do mais claro ao mais escuro (melhor contraste)
PRIMARY_DARK = "#8B9094"      # Tom mais claro da paleta
PRIMARY_MEDIUM = "#6B6F73"    # Tom médio-claro
PRIMARY_DARKER = "#4A4E52"    # Tom médio
PRIMARY_DARKEST = "#292D31"   # Tom escuro

SECONDARY_DARK = "#757A7E"    # Tom secundário claro
SECONDARY_MEDIUM = "#555A5E"  # Tom secundário médio
SECONDARY_DARKER = "#353A3E"  # Tom secundário escuro
SECONDARY_DARKEST = "#151A1E" # Tom secundário mais escuro

# Tons neutros
NEUTRAL_GRAY = "#65696D"      # Cinza neutro
LIGHT_GRAY = "#808489"        # Cinza claro
DARK_GRAY = "#070808"         # Tom mais escuro da paleta

CHART_COLORS = [
    PRIMARY_DARK,
    PRIMARY_MEDIUM,
    PRIMARY_DARKER,
    PRIMARY_DARKEST,
    SECONDARY_DARK,
    SECONDARY_MEDIUM,
    SECONDARY_DARKER,
    SECONDARY_DARKEST
]

# Paleta para métricas específicas
METRIC_COLORS = {
    'success': PRIMARY_MEDIUM,
    'warning': SECONDARY_DARKER,
    'error': PRIMARY_DARKEST,
    'info': PRIMARY_DARK,
    'primary': PRIMARY_DARK,
    'secondary': SECONDARY_DARK
}

# Paleta para tecnologias
TECH_COLORS = {
    'GHC': PRIMARY_DARK,
    'MANUAL': PRIMARY_DARKER,
    'GPS': SECONDARY_DARK,
    'DEFAULT': NEUTRAL_GRAY
}
