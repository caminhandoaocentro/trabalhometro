"""
Catálogo oficial de entregas, programas e leis sancionadas pela Presidência.
Fontes: Planalto Legislação, Casa Civil (Novo PAC) e Obrasgov.br.
"""
import json
from pathlib import Path
from config import DATA_DIR

LEGISLACAO_URL = "https://www.planalto.gov.br/legislacao"
NOVOPAC_URL = "https://www.gov.br/casacivil/pt-br/novopac"
AGENCIA_GOV_URL = "https://agenciagov.ebc.com.br"

ENTREGAS_OFICIAIS = [
    {
        "data": "2023-03-02",
        "titulo": "Novo Bolsa Família (MP 1.164 / Lei 14.601)",
        "area": "Social",
        "uf": "BR",
        "valor": 600.0,
        "descricao": "Reformulação do programa de transferência de renda com benefício mínimo de R$ 600 mais R$ 150 por criança de até 6 anos e acompanhamento escolar e vacinal.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14601.htm"
    },
    {
        "data": "2023-07-13",
        "titulo": "Retomada do Minha Casa, Minha Vida (Lei 14.620)",
        "area": "Habitação",
        "uf": "BR",
        "valor": 13700000000,
        "descricao": "Retomada da Faixa 1 para famílias com renda de até R$ 2.640, subsídios ampliados e prioridade para mulheres chefes de família.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14620.htm"
    },
    {
        "data": "2023-08-11",
        "titulo": "Lançamento do Novo PAC",
        "area": "Infraestrutura",
        "uf": "BR",
        "valor": 1700000000000,
        "descricao": "Plano de investimentos públicos e privados em transição ecológica, energia, cidades sustentáveis, ferrovias, portos e saúde.",
        "fonte_url": NOVOPAC_URL
    },
    {
        "data": "2023-10-03",
        "titulo": "Programa Desenrola Brasil (Lei 14.690)",
        "area": "Economia",
        "uf": "BR",
        "valor": 53000000000,
        "descricao": "Renegociação de dívidas bancárias e de consumo para milhões de famílias com descontos médios de 83% e teto para juros do rotativo.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14690.htm"
    },
    {
        "data": "2023-12-20",
        "titulo": "Promulgação da Reforma Tributária sobre o Consumo (EC 132)",
        "area": "Economia",
        "uf": "BR",
        "valor": None,
        "descricao": "Simplificação de 5 tributos (PIS, Cofins, IPI, ICMS e ISS) no IVA Dual (CBS e IBS) e isenção da cesta básica nacional.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm"
    },
    {
        "data": "2024-01-16",
        "titulo": "Criação do Programa Pé-de-Meia (Lei 14.818)",
        "area": "Educação",
        "uf": "BR",
        "valor": 7100000000,
        "descricao": "Poupança e incentivo financeiro para permanência e conclusão de estudantes do ensino médio público inscritos no CadÚnico.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14818.htm"
    },
    {
        "data": "2024-03-07",
        "titulo": "Seleção das Obras do Novo PAC Seleções",
        "area": "Infraestrutura",
        "uf": "BR",
        "valor": 65200000000,
        "descricao": "Mais de 6,7 mil obras em saúde, educação e esporte selecionadas para municípios de todos os estados do país.",
        "fonte_url": NOVOPAC_URL
    },
    {
        "data": "2024-04-22",
        "titulo": "Lançamento do Programa Acredita (Lei 14.995)",
        "area": "Economia",
        "uf": "BR",
        "valor": 30000000000,
        "descricao": "Crédito orientado para MEIs, microempresas e empreendedores do CadÚnico, além de renegociação de dívidas com Procred360.",
        "fonte_url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14995.htm"
    },
    {
        "data": "2024-07-10",
        "titulo": "Universalização do Farmácia Popular (Absorventes e 100% Gratuito no Bolsa Família)",
        "area": "Saúde",
        "uf": "BR",
        "valor": None,
        "descricao": "Distribuição gratuita de absorventes pelo Programa Dignidade Menstrual e ampliação de gratuidade em remédios para asma, diabetes e hipertensão.",
        "fonte_url": "https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular"
    },
    {
        "data": "2024-08-28",
        "titulo": "Pacto Nacional pela Retomada de Obras da Educação",
        "area": "Educação",
        "uf": "BR",
        "valor": 3800000000,
        "descricao": "Retomada de creches, escolas e quadras poliesportivas paralisadas ou inacabadas em todo o território nacional.",
        "fonte_url": "https://www.gov.br/mec/pt-br/assuntos/noticias/2024/agosto/governo-retoma-obras-da-educacao"
    }
]

def consolidar_entregas():
    ENTREGAS_OFICIAIS.sort(key=lambda x: x["data"], reverse=True)
    output_file = DATA_DIR / "entregas.js"

    conteudo_js = (
        "// Entregas, programas e leis oficiais da Presidência da República (3º Mandato)\n"
        "// Fontes: Planalto Legislação, Casa Civil (Novo PAC) e Ministérios\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.entregas = {json.dumps(ENTREGAS_OFICIAIS, indent=2, ensure_ascii=False)};\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(conteudo_js)

    print(f"[✓] {len(ENTREGAS_OFICIAIS)} entregas oficiais salvas em {output_file}!")
    return ENTREGAS_OFICIAIS

if __name__ == "__main__":
    consolidar_entregas()
