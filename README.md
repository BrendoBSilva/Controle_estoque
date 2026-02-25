📊 Sistema de Controle de Estoque com Pipeline de Dados 

Aplicação web desenvolvida em Python com foco em engenharia e análise de dados, simulando um pipeline completo de extração, transformação e visualização de dados (ETL).

O sistema permite controle de estoque multiusuário com geração de indicadores e dashboard analítico em tempo real. Armazenado em Streamlit Cloud.

🏗 Arquitetura de Dados

O projeto foi estruturado seguindo conceito de pipeline:

Extract  →  Transform  →  Load / Visualização
🔹 Extract (extract.py)

Responsável por extrair os dados brutos do JSON do usuário.

🔹 Transform (transform.py)

Aplicação de regras de negócio:

Cálculo de status do estoque

Identificação de produtos em alerta

Cálculo de quantidade faltante

Padronização de dados

🔹 Load / Analytics (app.py)

Responsável por:

Construção dos KPIs

Tabelas analíticas

Gráficos interativos com Altair

Visualização consolidada dos dados

📈 Indicadores Construídos

O dashboard apresenta:

📦 Total de produtos cadastrados

📊 Total de itens em estoque

⚠️ Quantidade de produtos em alerta

🔴 Produto mais crítico

📊 Estoque por categoria (gráfico de barras)

📜 Histórico de movimentações com data/hora automática

🧠 Regras Analíticas Aplicadas

Classificação automática de estoque:

OK

ALERTA

Cálculo de gap entre estoque atual e mínimo

Consolidação de estoque por categoria

Rastreamento temporal de movimentações

🛠 Tecnologias Utilizadas

Python

Pandas

Streamlit

Altair

JSON

📂 Estrutura do Projeto
controle-estoque-dados/
│
├── app.py              # Camada de visualização
├── services.py         # Camada de negócio e persistência
├── extract.py          # Extração de dados
├── transform.py        # Transformação e regras analíticas
├── usuarios.json       # Controle de autenticação
├── data/               # Base de dados por usuário
└── requirements.txt
🧩 Conceitos de Dados Demonstrados

✔ Estruturação de pipeline ETL
✔ Manipulação de DataFrames
✔ Modelagem de dados
✔ Cálculo de métricas analíticas
✔ Organização modular de código
✔ Tratamento de dados faltantes
✔ Construção de dashboard interativo

<img width="1920" height="904" alt="Streamlit e mais 3 páginas - Perfil 1 — Microsoft​ Edge 25_02_2026 20_47_46" src="https://github.com/user-attachments/assets/d1b577fc-f1ad-4087-bd10-f4e35ee7cca0" />



👨‍💻 Autor

Brendo Barbosa Silva
Estudante de Análise e Desenvolvimento de Sistemas e Ciência de dados
Foco em Engenharia de Dados e Analytics
