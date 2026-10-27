# ⭐️ Trabalhômetro

Painel independente e 100% estático que reúne **dados públicos oficiais** sobre os atos, entregas, gastos e viagens da Presidência da República (3º Mandato).

🌐 **Site no ar:** [https://caminhandoaocentro.github.io/trabalhometro/](https://caminhandoaocentro.github.io/trabalhometro/)

Cada indicador e dado exibido possui link direto para sua respectiva fonte oficial, sem qualquer juízo editorial — apenas transparência e números.

---

## 📌 Funcionalidades

- **Cartão Corporativo (CPGF):** Gastos mensais consolidados diretamente dos Dados Abertos da Controladoria-Geral da União (CGU / Portal da Transparência), com contagem de transações, média mensal, destaque do último mês apurado e gráfico temporal com filtros por ano.
- **Viagens Oficiais:** Mapa mundial interativo (Leaflet) com destinos nacionais e internacionais da Presidência da República, datas, motivos e coordenadas alimentados via API oficial da CGU.
- **Painel Novo PAC (Casa Civil):** Indicadores oficiais de investimentos (R$ 1,9 tri previsto, R$ 1,3 tri no mandato), 41,1 mil empreendimentos, percentuais por fonte de financiamento e links para fiscalização no Transferegov.br e mapas estaduais.
- **Entregas e Programas (2023 - 2026):** Catálogo interativo com busca rápida e filtros por ano (2023 a 2026) das principais leis, reformas e políticas sancionadas.
- **Data Lake Local (`data/raw/`):** Download em lote de dados brutos (CSVs e JSONs) para consultas e auditorias locais sem depender de conexão com a internet.

---

## 🎨 Design System

Interface inspirada na identidade visual e estética do **Partido dos Trabalhadores (PT)**:
- Paleta oficial em tons de vermelho (`#D71920`, `#FF3843`) e branco puro sobre fundo dark moderno.
- Elementos com a estrela clássica (★) no logotipo e cabeçalhos.
- Visual refinado com *glassmorphism*, responsividade total e alta legibilidade.

---

## 📂 Estrutura do Projeto

```text
trabalhometro/
├── index.html            # Página estática única (roda direto no navegador)
├── assets/
│   ├── style.css         # Design system PT, modo escuro, gráficos, PAC e mapa
│   └── app.js            # Lógica dos componentes, busca e interatividade
├── data/
│   ├── meta.js           # Metadados de atualização e contadores
│   ├── gastos.js         # Gastos reais do Cartão Corporativo (CGU)
│   ├── compras_diretas.js # Compras diretas, mobília e dispensas (DOU / TCU)
│   ├── viagens.js        # Deslocamentos oficiais e coordenadas
│   ├── novopac.js        # Indicadores oficiais de transparência do Novo PAC
│   ├── entregas.js       # Entregas, leis e programas governamentais
│   ├── avaliacao.js      # Matriz desenvolvimentista e projetos estruturantes
│   ├── export/           # 📦 Datasets prontos para uso (CSV e JSON limpos)
│   │   ├── gastos.csv / .json       # Série histórica mensal do CPGF
│   │   ├── compras_diretas.csv / .json # Dispensas de licitação e mobília
│   │   ├── viagens.csv / .json      # Destinos, coordenadas e motivos
│   │   ├── entregas.csv / .json     # 32 leis e atos com links oficiais
│   │   ├── novopac.json / fontes.csv # Financiamento e metas do Novo PAC
│   │   └── avaliacao.json           # Pilares e projetos de referência
│   └── raw/              # 🗄️ Data Lake Bruto da CGU (linha por linha)
│       ├── cpgf/         # 44 CSVs mensais originais do cartão corporativo
│       ├── viagens/      # 46 JSONs mensais brutos da API da CGU
│       └── despesas/     # Fornecedores e favorecidos da Presidência
├── scripts/
│   ├── config.py         # Configurações gerais, rotas e coordenadas
│   ├── fetch_cartao.py   # Coleta e consolidação de gastos no Portal da Transparência
│   ├── fetch_compras_diretas.py # Compras diretas de bens e dispensas de licitação
│   ├── fetch_viagens_api.py # Consulta direta à API oficial da CGU (viagens)
│   ├── fetch_viagens_oficiais.py # Consolidação de viagens internacionais e de Estado
│   ├── fetch_novopac.py  # Captura de dados de transparência do Novo PAC (Casa Civil)
│   ├── fetch_entregas.py # Catálogo de entregas e atos sancionados (2023 - 2026)
│   ├── export_datasets.py # Exportador de datasets para CSV e JSON limpos
│   ├── update_all.py     # Orquestrador único que atualiza todo o site
│   └── download_raw_data.py # Download massivo de dados brutos para o Data Lake local
├── requirements.txt      # Dependências Python (requests, beautifulsoup4, etc.)
└── README.md
```

---

## 📊 Como consumir os dados (Open Data)

Você pode usar os dados diretamente em Python (Pandas), R, Excel ou na sua aplicação:

### Em Python / Pandas:
```python
import pandas as pd

# Carregar série histórica de gastos do cartão corporativo
url_gastos = "https://raw.githubusercontent.com/caminhandoaocentro/trabalhometro/main/data/export/gastos.csv"
df_gastos = pd.read_csv(url_gastos)
print(df_gastos.head())

# Carregar viagens oficiais com coordenadas
url_viagens = "https://raw.githubusercontent.com/caminhandoaocentro/trabalhometro/main/data/export/viagens.csv"
df_viagens = pd.read_csv(url_viagens)
print(df_viagens.describe())
```

### Arquivos disponíveis para download direto:
* 💳 **Gastos do CPGF:** [`data/export/gastos.csv`](data/export/gastos.csv) · [`gastos.json`](data/export/gastos.json)
* 🪑 **Compras Diretas & Mobília:** [`data/export/compras_diretas.csv`](data/export/compras_diretas.csv) · [`compras_diretas.json`](data/export/compras_diretas.json)
* ✈️ **Viagens Oficiais:** [`data/export/viagens.csv`](data/export/viagens.csv) · [`viagens.json`](data/export/viagens.json)
* 🏛️ **Entregas e Reformas:** [`data/export/entregas.csv`](data/export/entregas.csv) · [`entregas.json`](data/export/entregas.json)
* 🏗️ **Novo PAC:** [`data/export/novopac.json`](data/export/novopac.json) · [`novopac_fontes.csv`](data/export/novopac_fontes.csv)
* 🎯 **Matriz Desenvolvimentista:** [`data/export/avaliacao.json`](data/export/avaliacao.json)
* 🗄️ **Data Lake Bruto Oficial:** [`data/raw/`](data/raw/) com os 44 CSVs mensais do CPGF e 46 JSONs de viagens da CGU.

---

## 🔄 Como usar os scripts (Python)

```bash
# 1. Ativar o ambiente virtual e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Atualizar todos os dados do site (gera data/*.js)
python3 scripts/update_all.py

# 3. Baixar todos os dados brutos oficiais para o Data Lake local (data/raw/)
python3 scripts/download_raw_data.py
```

---

## 📄 Fontes de Dados Públicas

- [Portal da Transparência — Cartões de Pagamento (CPGF)](https://portaldatransparencia.gov.br/cartoes)
- [Portal da Transparência — Download de Dados Abertos](https://portaldatransparencia.gov.br/download-de-dados)
- [Portal da Transparência — API Oficial de Dados da CGU](https://api.portaldatransparencia.gov.br)
- [Casa Civil — Transparência do Novo PAC](https://www.gov.br/casacivil/pt-br/novopac/transparencia)
- [Presidência da República — Agenda Oficial](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica)
- [Presidência da República — Legislação](https://www.planalto.gov.br/legislacao)

---

## ⚖️ Licença

Projeto independente de código aberto sob licença MIT.
