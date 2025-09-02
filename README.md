# Inspirar Dashboard - Insights Avançados para Pacientes com Asma

Este projeto é um dashboard interativo desenvolvido em Python com Streamlit para análise avançada de dados de pacientes com asma. Projetado especificamente para profissionais de saúde, oferece visualizações intuitivas e análises estatísticas robustas para auxiliar no acompanhamento clínico e tomada de decisões baseadas em dados.

## ✨ Principais Funcionalidades

### 📊 Análises Gerais
- **Métricas principais**: Cadastros, medicamentos, atividades, idade média
- **Pacientes ativos vs inativos**: Distribuição e análise por sexo
- **Boxplot de métricas**: Análise descritiva com tabelas detalhadas

### 📈 Análises Semanais Avançadas
- **Prescrições semanais**: Evolução temporal de medicamentos com usuários ativos
- **Diários semanais**: Análise de sintomas por período com formato de datas intuitivo
- **Atividades semanais**: Monitoramento de atividades físicas ao longo do tempo

### 🏥 Análises Clínicas Especializadas
- **Status ACQ**: Análise do primeiro questionário de controle da asma com estatísticas descritivas
- **Crises de asma**: Distribuição por duração, análise por sexo e dados detalhados
- **Distribuição de idade**: Análise geral e por sexo com estatísticas comparativas

### 👥 Análises por Sexo
- **Funcionalidades por sexo**: Comparação de adesão entre pacientes masculinos e femininos
- **Mapa de calor comparativo**: Correlações entre funcionalidades por grupo (geral, masculino, feminino)

### 🎨 Design e Usabilidade
- **Paleta de cores unificada**: Tons de roxo/lavanda consistentes em todo o dashboard
- **Períodos intuitivos**: Datas no formato "Mar 1-7", "Abr 15-21" para profissionais de saúde
- **Tabelas exportáveis**: Download CSV para análises externas
- **Política de dados**: Tratamento adequado de pacientes com dados pessoais removidos

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/inspirar-dashboard.git
cd inspirar-dashboard
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o dashboard:
```bash
streamlit run src/dashboard.py
```

2. Faça upload do arquivo JSON de pacientes na barra lateral.

## 🔧 Melhorias Técnicas Implementadas

### Modularização
- **15 seções independentes**: Cada análise em arquivo separado para manutenibilidade
- **Arquitetura limpa**: Separação clara entre lógica de negócio e apresentação
- **Reutilização de código**: Funções auxiliares compartilhadas

### Análises Avançadas
- **Análises temporais**: Consideração do crescimento da base de usuários ao longo do tempo
- **Primeira semana ACQ**: Análise específica do estado inicial de controle da asma
- **Correlações por grupo**: Mapas de calor segmentados por sexo

### Experiência do Usuário
- **Formato de datas intuitivo**: Períodos legíveis para profissionais não-técnicos
- **Tabelas interativas**: Filtros, ordenação e download CSV
- **Insights automáticos**: Identificação de padrões e diferenças significativas
- **Tratamento de dados sensíveis**: Política clara sobre dados pessoais removidos

### Qualidade de Código
- **Paleta de cores centralizada**: Sistema unificado em `utils/colors.py`
- **Tratamento robusto de erros**: Validação de tipos de dados e timezone
- **Documentação inline**: Explicações claras para profissionais de saúde

## 📁 Estrutura do Projeto

```
inspirar-dashboard/
├── src/
│   ├── dashboard.py              # Script principal do dashboard
│   ├── components/
│   │   └── cards.py              # Componentes reutilizáveis
│   ├── utils/
│   │   ├── colors.py             # Paleta de cores unificada
│   │   └── data_processing.py    # Funções de processamento de dados
│   └── sections/                 # Seções modulares do dashboard
│       ├── metricas.py           # Métricas principais
│       ├── ativos.py             # Análise de pacientes ativos
│       ├── boxplot_metricas.py   # Análise descritiva com boxplots
│       ├── prescricoes_semanais.py # Análise temporal de prescrições
│       ├── diarios_semanais.py   # Análise temporal de diários
│       ├── atividades_semanais.py # Análise temporal de atividades
│       ├── status_acq.py         # Análise do questionário ACQ
│       ├── recordes.py           # Recordes e destaques
│       ├── tabelas.py            # Tabelas detalhadas
│       ├── idade.py              # Distribuição de idade
│       ├── crises.py             # Análise de crises de asma
│       ├── funcionalidades_geral.py # Visão geral das funcionalidades
│       ├── funcionalidades_sexo.py  # Análise de funcionalidades por sexo
│       └── mapa_calor.py         # Correlações entre funcionalidades
├── data/                         # Arquivos de dados de exemplo
├── tests/                        # Testes automatizados
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação do projeto
```

## 🎨 Sistema de Cores

O dashboard utiliza uma paleta de cores unificada baseada em tons de roxo/lavanda:
- **Cores principais**: `#8B5CF6`, `#A78BFA`, `#C4B5FD`, `#7C3AED`
- **Cores secundárias**: `#9F7AEA`, `#B794F4`, `#DDD6FE`, `#6B46C1`
- **Cores neutras**: `#6B7280`, `#F3F4F6`, `#374151`

## 📊 Seções do Dashboard

### 1. **Métricas Gerais**
- Total de pacientes cadastrados
- Métricas de engajamento por funcionalidade
- Indicadores de atividade

### 2. **Pacientes Ativos**
- Distribuição ativo vs inativo
- Análise por sexo dos pacientes ativos
- Nota sobre política de dados pessoais

### 3. **Análise Descritiva**
- Boxplots de métricas numéricas (idade, peso, altura, IMC, ACQ)
- Tabelas detalhadas com ID do paciente
- Estatísticas descritivas (média, desvio padrão, mediana, IQR)

### 4. **Análises Semanais** (Modularizadas)
- **Prescrições**: Evolução temporal de medicamentos
- **Diários**: Análise de sintomas por período
- **Atividades**: Monitoramento de atividades físicas
- Formato de datas intuitivo para profissionais de saúde

### 5. **Status ACQ**
- Análise do primeiro questionário de cada paciente
- Estatísticas descritivas dos scores
- Boxplot e distribuição de status
- Tabela detalhada com filtros interativos

### 6. **Recordes e Destaques**
- Análise de tecnologias de atividades físicas (GHC, Manual, GPS)
- Métricas de engajamento
- Insights sobre uso de tecnologias

### 7. **Distribuição de Idade**
- Histograma geral de idades
- Distribuição por sexo
- Estatísticas comparativas entre sexos

### 8. **Análise de Crises**
- Distribuição por duração das crises
- Análise comparativa por sexo
- Taxa de incidência e estatísticas clínicas

### 9. **Funcionalidades** (Dividido em duas seções)
- **Visão Geral**: Ranking e distribuição de uso
- **Análise por Sexo**: Comparação de adesão entre sexos

### 10. **Mapa de Calor**
- Correlações entre funcionalidades (geral, masculino, feminino)
- Análise comparativa de padrões de uso
- Escala de cores personalizada

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, por favor abra uma issue primeiro para discutir o que você gostaria de modificar.

## Licença
[MIT](LICENSE) 