# ⭐️ Trabalhômetro

Painel independente e 100% estático que reúne **dados públicos oficiais** sobre os atos, entregas, gastos e viagens da Presidência da República (3º Mandato).

🌐 **Site no ar:** [https://jeferson-guedes.github.io/trabalhometro/](https://jeferson-guedes.github.io/trabalhometro/)

Cada indicador e dado exibido possui link direto para sua respectiva fonte oficial, sem qualquer juízo editorial — apenas transparência e números.

---

## 📌 Funcionalidades

- **Cartão Corporativo (CPGF):** Gastos mensais consolidados diretamente dos Dados Abertos da Controladoria-Geral da União (CGU / Portal da Transparência), com contagem de transações e gráfico temporal interativo.
- **Viagens Oficiais:** Mapa mundial interativo (Leaflet) com destinos nacionais e internacionais da Presidência da República, datas, motivos e coordenadas.
- **Entregas e Programas:** Catálogo interativo com busca rápida e links para a legislação, Novo PAC e diário oficial de programas sancionados (Bolsa Família, Pé-de-Meia, Minha Casa Minha Vida, Reforma Tributária, Desenrola, etc.).
- **Transparência Total:** Sem intermediários nem banco de dados dinâmico — dados compilados e abertos em JavaScript.

---

## 🎨 Design System

Interface inspirada na identidade visual e estética do **Partido dos Trabalhadores (PT)**:
- Paleta oficial em tons de vermelho (`#D71920`, `#FF333D`) e branco puro sobre fundo dark moderno.
- Elementos com a estrela clássica (★) no logotipo e cabeçalhos.
- Visual refinado com *glassmorphism*, responsividade total e alta legibilidade.

---

## 📂 Estrutura do Projeto

```text
trabalhometro/
├── index.html            # Página estática única (roda direto no navegador)
├── assets/
│   ├── style.css         # Design system PT, modo escuro, gráficos e mapa
│   └── app.js            # Lógica dos componentes, busca e interatividade
├── data/
│   ├── meta.js           # Metadados de atualização e contadores
│   ├── gastos.js         # Gastos reais do Cartão Corporativo (CGU)
│   ├── viagens.js        # Deslocamentos oficiais e coordenadas
│   └── entregas.js       # Entregas, leis e programas governamentais
├── scripts/
│   ├── config.py         # Configurações gerais, rotas e coordenadas
│   ├── fetch_cartao.py   # Coleta e consolidação de gastos no Portal da Transparência
│   ├── fetch_viagens_oficiais.py # Consolidação de viagens oficiais
│   ├── fetch_entregas.py # Catálogo de entregas e atos sancionados
│   └── update_all.py     # Orquestrador único de atualização
├── requirements.txt      # Dependências Python (requests, beautifulsoup4, etc.)
└── README.md
```

---

## 🔄 Como atualizar os dados (Python)

Para rodar a rotina de atualização dos dados oficiais:

```bash
# 1. Ativar o ambiente virtual e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Executar o script orquestrador
python3 scripts/update_all.py
```

O script baixa e consolida automaticamente os extratos mensais oficiais do CPGF, as viagens e entregas, gerando os novos arquivos em `data/*.js` com cache inteligente.

---

## 📄 Fontes de Dados Públicas

- [Portal da Transparência — Cartões de Pagamento (CPGF)](https://portaldatransparencia.gov.br/cartoes)
- [Portal da Transparência — Viagens a Serviço](https://portaldatransparencia.gov.br/viagens)
- [Presidência da República — Agenda Oficial](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica)
- [Casa Civil — Novo PAC](https://www.gov.br/casacivil/pt-br/novopac)
- [Obrasgov.br](https://www.gov.br/obrasgov)
- [Presidência da República — Legislação](https://www.planalto.gov.br/legislacao)

---

## ⚖️ Licença

Projeto independente de código aberto sob licença MIT.
