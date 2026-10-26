# ⭐️ Trabalhômetro

Painel independente e 100% estático que reúne **dados públicos oficiais** sobre os atos, entregas, gastos e viagens da Presidência da República.

Cada indicador e dado exibido possui link direto para sua respectiva fonte original oficial, sem juízo editorial — apenas números e transparência.

---

## 📌 Funcionalidades

- **Cartão Corporativo (CPGF):** Gastos mensais detalhados e gráficos interativos com link para o Portal da Transparência.
- **Viagens Oficiais:** Mapa interativo (Leaflet) com destinos nacionais e internacionais, datas, motivos e links da agenda oficial.
- **Entregas e Ações:** Catálogo com filtro e busca de obras, programas e atos públicos entregues.
- **Transparência Total:** Todas as fontes e metodologias abertas e acessíveis.

---

## 🎨 Design System

Interface construída com a identidade visual e estética do **Partido dos Trabalhadores (PT)**:
- Paleta oficial em tons de vermelho (`#D71920`, `#FF333D`) e branco puro.
- Elementos de destaque com a estrela característica (★).
- Estilo moderno em modo escuro com *glassmorphism* e alta legibilidade.

---

## 📂 Estrutura do Projeto

```text
trabalhometro/
├── index.html         # Página estática única (funciona direto no navegador)
├── assets/
│   ├── style.css      # Estilização completa e responsiva
│   └── app.js         # Lógica do painel, filtros, mapa e busca
├── data/
│   ├── meta.js        # Data de atualização e metadados
│   ├── gastos.js      # Dados de gastos (cartão corporativo)
│   ├── viagens.js     # Dados de viagens oficiais e coordenadas
│   └── entregas.js    # Dados de obras e programas entregues
└── README.md
```

---

## 🚀 Como executar

Por ser 100% estático (sem necessidade de servidor ou build):
1. Basta clonar o repositório.
2. Dar duplo clique ou abrir o arquivo `index.html` em qualquer navegador.

```bash
open index.html
```

---

## 📄 Fontes de Dados Públicas

- [Portal da Transparência — Cartões de Pagamento](https://portaldatransparencia.gov.br/cartoes)
- [Portal da Transparência — Viagens a Serviço](https://portaldatransparencia.gov.br/viagens)
- [Presidência da República — Agenda Oficial](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica)
- [Casa Civil — Novo PAC](https://www.gov.br/casacivil/pt-br/novopac)
- [Obrasgov.br](https://www.gov.br/obrasgov)
- [Legislação Presidencial](https://www.planalto.gov.br/legislacao)

---

## ⚖️ Licença

Projeto independente de código aberto sob licença MIT.
