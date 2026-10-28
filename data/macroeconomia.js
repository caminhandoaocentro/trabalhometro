// Diagnóstico Macroeconômico: Custo de Vida vs. Motores do PIB (2023-2026)
// Fontes: IBGE (Contas Nacionais, PNAD Contínua), Banco Central (Copom, Focus), Receita Federal e IPEA.
window.DADOS = window.DADOS || {};
window.DADOS.macroeconomia = {
  diagnostico: {
    titulo: "Diagnóstico: O Paradoxo do Custo de Vida e os Motores do PIB",
    subtitulo: "Por que as manchetes comemoram menor desemprego e PIB em alta, mas o cidadão comum e as empresas sentem a vida cada vez mais cara?",
    tese: "O crescimento econômico recente foi impulsionado pelo consumo das famílias e aumento de gastos públicos (estímulo de demanda), mas a capacidade produtiva das fábricas e da infraestrutura (oferta) não acompanhou no mesmo ritmo. Para sustentar a alta das despesas sem cortar gastos, o governo optou pela arrecadação recorde de impostos. O resultado foi a necessidade de manter a taxa de juros básica (Selic) em dois dígitos para conter a inflação, gerando crédito caro, encarecendo a produção e corroendo o poder de compra da classe trabalhadora."
  },
  termometro_indicadores: [
    {
      indicador: "Taxa de Desemprego",
      valor: "6,5%",
      sub: "Mínima histórica em quase 10 anos",
      status: "positivo",
      icone: "📉",
      detalhe: "Queda na taxa de desocupação (IBGE/PNAD), mas com vagas predominantemente concentradas no setor de serviços de baixa remuneração e informalidade.",
      fonte_nome: "IBGE · PNAD Contínua",
      fonte_url: "https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pesquisa-nacional-por-amostra-de-domicilios-continua-trimestral.html"
    },
    {
      indicador: "Crescimento do PIB",
      valor: "~3,0%",
      sub: "Média anual acumulada",
      status: "positivo",
      icone: "📊",
      detalhe: "Puxado pela injeção da PEC da Transição (R$ 170 bi), pagamento de precatórios (R$ 90 bi), consumo das famílias e exportações do agronegócio e petróleo.",
      fonte_nome: "IBGE · Contas Nacionais",
      fonte_url: "https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9300-contas-nacionais-trimestrais.html"
    },
    {
      indicador: "Taxa de Juros (Selic)",
      valor: "10,75% a 12%+",
      sub: "Dois dígitos / Juro real mais alto do mundo",
      status: "alerta",
      icone: "🏦",
      detalhe: "Banco Central mantém juros restritivos para conter a pressão inflacionária provocada pelo déficit público e pela alta da dívida do governo.",
      fonte_nome: "Banco Central do Brasil · Copom",
      fonte_url: "https://www.bcb.gov.br/controleinflacao/taxaselic"
    },
    {
      indicador: "Arrecadação Federal",
      valor: "> R$ 2,3 Tri",
      sub: "Recorde histórico de tributos",
      status: "alerta",
      icone: "💸",
      detalhe: "Aumento da carga efetiva sobre o consumo diário (combustíveis, compras internacionais de até US$ 50, IOF e reoneração da folha de pagamento).",
      fonte_nome: "Receita Federal · Relatórios Mensais",
      fonte_url: "https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/arrecadacao"
    },
    {
      indicador: "Taxa de Investimento (FBCF)",
      valor: "16,5%",
      sub: "Do PIB (abaixo do necessário de 22%-25%)",
      status: "critico",
      icone: "🏭",
      detalhe: "A Formação Bruta de Capital Fixo (fábricas, portos, máquinas e tecnologia) segue estagnada, caracterizando um crescimento puxado por consumo e não por capacidade produtiva.",
      fonte_nome: "IPEA / IBGE · Indicador FBCF",
      fonte_url: "https://www.ipea.gov.br/cartadacojuntura/index.php/tag/formacao-bruta-de-capital-fixo/"
    },
    {
      indicador: "Dívida Bruta da União",
      valor: "~78% a 80%",
      sub: "Do PIB (trajetória de elevação contínua)",
      status: "critico",
      icone: "📈",
      detalhe: "Aumento do endividamento público para bancar a expansão de despesas obrigatórias, gerando desconfiança fiscal e encarecendo os juros futuros.",
      fonte_nome: "Banco Central · Estatísticas Fiscais",
      fonte_url: "https://www.bcb.gov.br/estatisticas/estatisticasfiscais"
    }
  ],
  eixos_analiticos: [
    {
      id: "demanda_vs_oferta",
      icone: "⚡",
      titulo: "1. O Motor do PIB: Consumo Imediato vs. Capacidade Produtiva",
      o_que_o_governo_fez: "Injetou liquidez imediata com a PEC da Transição (R$ 170 bi a mais de gastos em 2023), quitação de R$ 90 bi em precatórios autorizados pelo STF, aumento real do salário mínimo e ampliação do Bolsa Família e Pé-de-Meia.",
      o_efeito_no_bolso: "Famílias de menor renda gastam todo o recurso na sobrevivência diária, o que aqueceu o comércio e os serviços locais. Porém, como a Taxa de Investimento (FBCF) ficou estagnada em apenas 16,5% do PIB (sem novas fábricas e grandes obras de oferta imediata), a demanda bateu no teto de capacidade, pressionando os preços para cima em vez de baratear o custo de vida."
    },
    {
      id: "arrecadacao_recorde",
      icone: "📦",
      titulo: "2. A Conta Fiscal: Arrecadação Recorde e o Recuo da 'Taxa das Blusinhas' em 2026",
      o_que_o_governo_fez: "Para fechar as contas sem cortar gastos públicos, a União buscou arrecadação recorde (> R$ 2,3 trilhões/ano). Em 2024, aprovou a 'Taxa das Blusinhas' de 20% sobre compras até US$ 50 (Lei 14.902/2024), além de impostos sobre combustíveis e IOF. No entanto, em 2026 (ano eleitoral), diante de forte desgaste político, o governo e o Congresso recuaram e zeraram novamente a alíquota federal de 20% (sancionada em setembro de 2026, gerando ação da CNI e CNC no STF pela ADI 7.973).",
      o_efeito_no_bolso: "A criação inicial da taxa das blusinhas encareceu importações populares em até 44% (com ICMS) por dois anos, penalizando jovens e classe média. A queda do imposto federal em 2026 aliviou o comércio exterior popular às vésperas da eleição, mas o custo tributário estrutural do país (combustíveis, encargos da folha e ICMS estadual) continuou pressionando as empresas e o custo de vida nas prateleiras."
    },
    {
      id: "juros_altos",
      icone: "💳",
      titulo: "3. A Armadilha dos Juros: Crédito Sufocado e Dívida Pública",
      o_que_o_governo_fez: "Com déficit primário contínuo e a Dívida Bruta da União subindo rumo a 78%-80% do PIB, o risco fiscal percebido pelo mercado aumentou significativamente.",
      o_efeito_no_bolso: "Para evitar que a inflação disparasse, o Banco Central manteve a taxa Selic em dois dígitos (10,75% a 12%+), resultando em uma das taxas de juros reais mais altas do planeta. Isso torna o financiamento habitacional e de veículos proibitivo, encarece o cheque especial e o cartão de crédito e encarece o capital de giro das empresas, que repassam o custo financeiro para as prateleiras."
    },
    {
      id: "qualidade_emprego",
      icone: "👷",
      titulo: "4. A Qualidade do Emprego: Baixo Desemprego vs. Renda Real Espremida",
      o_que_o_governo_fez: "O governo comemorou a taxa de desemprego mais baixa em anos (queda para ~6,5%), puxada por contratações em serviços e programas de inclusão.",
      o_efeito_no_bolso: "Apesar do aumento no número de pessoas ocupadas, as vagas geradas estão fortemente concentradas em faixas de 1 a 2 salários mínimos, com alta pejotização e informalidade. Ao mesmo tempo, a inflação acumulada de alimentos, energia elétrica, planos de saúde e aluguéis neutralizou a sensação de ganho de renda da classe média e das famílias trabalhadoras."
    }
  ],
  conclusao_desenvolvimentista: "O país cresceu nos últimos anos empurrado por despesa pública e consumo, e não por um choque de investimentos e produtividade. Um projeto desenvolvimentista sustentável exige baratear o custo sistêmico do país (energia barata, logística ferroviária, corte de desperdícios da burocracia e juros civilizados) para que o crescimento se traduza em conforto real e poder de compra para as famílias."
};
