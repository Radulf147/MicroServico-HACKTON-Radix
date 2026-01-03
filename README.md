⚡ Mapa Inteligente de Perfis de Carga e Geração Distribuída

Hackathon Radix + AXIA + Cepel

Bem-vindo ao repositório oficial da nossa solução. Este projeto visa resolver a "cegueira" do Operador Nacional do Sistema (ONS) sobre a ponta da rede de distribuição, entregando dados enriquecidos sobre perfis de consumo e Geração Distribuída (MMGD) através de uma API escalável e Inteligência Artificial.

🎯 O Que Fazemos?

Desenvolvemos uma Camada de Inteligência de Dados que:

1. Ingestão: Recebe uma coordenada geográfica (Latitude/Longitude) de uma subestação.

2. Cruzamento: Integra dados demográficos (Censo IBGE) e regulatórios (ANEEL).

3. Visão Computacional: Aplica modelos de IA (YOLOv8) em imagens de satélite para detectar painéis solares e estimar a densidade de Geração Distribuída.

4. Entrega: Retorna um perfil estruturado (JSON) pronto para integração com o software ANATEM.

📂 Estrutura do Projeto

Organizamos o repositório para separar claramente a exploração de dados (Ciência) do código de produção (Engenharia).

nome-do-projeto/
│
├── .gitignore               # Impede o envio de arquivos pesados ou sensíveis
├── README.md                # Documentação geral (Este arquivo)
├── requirements.txt         # Lista de bibliotecas (pip install -r requirements.txt)
├── Dockerfile               # Configuração para rodar a aplicação em container
│
├── docs/                    # 📄 Documentação
│   ├── planejamento/        # Cronogramas e roteiros
│   └── arquitetura.md       # Desenhos da solução técnica
│
├── data/                    # 💾 Dados (Atenção às regras de Git)
│   ├── dados_originais/     # Arquivos brutos (CSV, ZIP) do IBGE/ANEEL. (Somente Leitura)
│   ├── dados_limpos/        # Dados tratados e convertidos para Parquet/GeoPackage.
│   └── amostra_de_dados/    # Pequenos recortes (ex: 1 bairro) para testes. (SOBE P/ GITHUB)
│
├── notebooks/               # 📓 Laboratório (Jupyter Notebooks)
│   ├── 01_etl_censo.ipynb        # Limpeza e preparação dos dados censitários
│   ├── 02_analise_gd.ipynb       # Análise da base da ANEEL
│   └── 03_yolo_training.ipynb    # Treinamento do modelo de Visão Computacional
│
├── models/                  # 🧠 Inteligência Artificial
│   └── yolo_solar_best.pt   # Arquivo de pesos do modelo treinado (se <100MB)
│
├── src/                     # 🚀 Código Fonte da API
│   ├── main.py              # Ponto de entrada (FastAPI)
│   ├── api/                 # Definição das rotas (Endpoints)
│   └── core/                # Lógica de negócio (Processamento de imagem e dados)
│
└── tests/                   # 🧪 Testes Automatizados
⚠️ Regras para a Pasta data/

Para não sobrecarregar o repositório e evitar erros de limite de arquivo (100MB)
:

1. dados_originais/ e dados_limpos/: Estão listadas no .gitignore. Elas existem na sua máquina local para processar os dados pesados, mas não sobem para o GitHub.

2. amostra_de_dados/: É a única pasta de dados que sobe. Coloque aqui apenas arquivos pequenos (csv com 50 linhas, 1 imagem de satélite exemplo) para que outros desenvolvedores consigam rodar os testes.

🚀 Como Rodar o Projeto

Pré-requisitos

. Docker instalado OU Python 3.9+

. Chave de API do Google Maps (para o módulo de visão) configurada no arquivo .env.

Opção 1: Via Docker (Recomendado para Avaliadores)

Garante que o ambiente seja idêntico ao de desenvolvimento.

# 1. Construir a imagem
docker build -t hackathon-energy-api .

# 2. Rodar o container
docker run -p 8000:8000 hackathon-energy-api

Opção 2: Desenvolvimento Local (Python)

# 1. Criar ambiente virtual

python -m venv venv
# Ativar: source venv/bin/activate (Linux/Mac) ou venv\Scripts\activate (Windows)

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar a API com hot-reload
uvicorn src.main:app --reload


🛠️ Tech Stack

. Linguagem: PythonAPI 
. Framework: FastAPI
. Processamento de Dados: Pandas, GeoPandas
. Visão Computacional: YOLOv8 (Ultralytics) + OpenCV
. Infra: Docker

👥 Equipe do Hackathon

Raul Montes Rosales do Nascimento
..
..
..
..
..