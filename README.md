# ⭐️ Trabalhômetro

Painel independente e 100% estático que reúne **dados públicos oficiais** sobre os atos, entregas, gastos e viagens da Presidência da República (3º Mandato).

🌐 **Site no ar:** [https://jeferson-guedes.github.io/trabalhometro/](https://jeferson-guedes.github.io/trabalhometro/)

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
│   ├── viagens.js        # Deslocamentos oficiais e coordenadas
│   ├── novopac.js        # Indicadores oficiais de transparência do Novo PAC
│   ├── entregas.js       # Entregas, leis e programas governamentais
│   └── raw/              # Data Lake Local (CSV e JSON brutos)
│       ├── cpgf/         # Transações linha por linha do cartão corporativo
│       ├── viagens/      # Processos brutos de viagens da API da CGU
│       └── despesas/     # Fornecedores e favorecidos da Presidência
├── scripts/
│   ├── config.py         # Configurações gerais, rotas e coordenadas
│   ├── fetch_cartao.py   # Coleta e consolidação de gastos no Portal da Transparência
│   ├── fetch_viagens_api.py # Consulta direta à API oficial da CGU (viagens)
│   ├── fetch_viagens_oficiais.py # Consolidação de viagens internacionais e de Estado
│   ├── fetch_novopac.py  # Captura de dados de transparência do Novo PAC (Casa Civil)
│   ├── fetch_entregas.py # Catálogo de entregas e atos sancionados (2023 - 2026)
│   ├── update_all.py     # Orquestrador único que atualiza todo o site
│   └── download_raw_data.py # Download massivo de dados brutos para o Data Lake local
├── requirements.txt      # Dependências Python (requests, beautifulsoup4, etc.)
└── README.md
```

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
