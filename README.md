# Inspirar Dashboard - Insights Avançados para Pacientes com Asma

Este projeto é um dashboard interativo desenvolvido em Python com Streamlit para análise avançada de dados de pacientes com asma. Ele permite o upload de arquivos JSON contendo informações dos pacientes e gera visualizações e métricas detalhadas para auxiliar em estudos e acompanhamento clínico.

## Funcionalidades
- Upload de arquivo JSON de pacientes
- Métricas principais (cadastros, medicamentos, atividades, idade média)
- Gráficos interativos (pizza, barras, histograma, heatmap)
- Tabelas detalhadas com filtros
- Destaques e recordes

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

## Estrutura do Projeto
- `src/dashboard.py`: Script principal do dashboard
- `requirements.txt`: Dependências do projeto
- `README.md`: Este arquivo
- `data/`: Pasta para arquivos de dados de exemplo
- `tests/`: Pasta para futuros testes automatizados

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, por favor abra uma issue primeiro para discutir o que você gostaria de modificar.

## Licença
[MIT](LICENSE) 