"""
Captura e consolidação de Compras Diretas, Dispensas de Licitação e Bens Patrimoniais
da Presidência da República (Secretaria de Administração da Presidência da República).
Fontes: Compras.gov.br, Diário Oficial da União (DOU) e Tribunal de Contas da União (TCU).
"""
import json
from pathlib import Path
from config import DATA_DIR

COMPRAS_DIRETAS_OFICIAIS = [
    {
        "id": "dispensa-03-2023-alvorada-suite",
        "data": "2023-03-20",
        "modalidade": "Dispensa de Licitação (Art. 75 da Lei 14.133 / Art. 24 da Lei 8.666)",
        "processo": "Dispensa nº 03/2023 - UASG 110001",
        "orgao": "Secretaria de Administração da Presidência da República",
        "local": "Palácio da Alvorada (Suíte Presidencial)",
        "objeto": "Aquisição de mobiliário e artigos de quarto e estar para a área íntima da residência oficial do Presidente e Primeira-Dama.",
        "valor_total": 196770.00,
        "itens": [
            {
                "item": "Sofá de couro com mecanismo reclinável elétrico",
                "descricao": "Sofá revestido em couro legítimo, com ajuste e acionamento elétrico independente de cabeça e pés.",
                "valor": 65140.00
            },
            {
                "item": "Cama com colchão articulado elétrico",
                "descricao": "Cama king size com mecanismo articulado motorizado, controle remoto e colchão de alta densidade.",
                "valor": 42230.00
            },
            {
                "item": "Poltrona em couro com ajuste ergonômico",
                "descricao": "Poltrona de estar revestida em couro e acabamento especial.",
                "valor": 29450.00
            },
            {
                "item": "Mesa de centro em madeira maciça",
                "descricao": "Mesa de centro com acabamento contemporâneo para sala privativa.",
                "valor": 24950.00
            },
            {
                "item": "Poltronas e mesas laterais de apoio (2 unidades)",
                "descricao": "Mobiliário auxiliar para a suíte residencial.",
                "valor": 35000.00
            }
        ],
        "justificativa_governo": "A Presidência justificou a compra direta emergencial em razão do estado de conservação em que a residência foi encontrada após a troca de governo e a falta de mobília básica na área residencial.",
        "desdobramento_oficial": "Em março de 2024, a Secom informou que 261 móveis históricos que constavam como não localizados no início da gestão foram encontrados em depósitos do próprio Palácio da Alvorada.",
        "posicao_orgaos_controle": "O Tribunal de Contas da União (TCU), no processo TC 008.204/2023-7, julgou improcedente a denúncia de irregularidades e sobrepreço, considerando que a dispensa cumpriu os requisitos formais de pesquisa de mercado da administração pública.",
        "fonte_url": "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?data=20/03/2023&jornal=530&pagina=2&totalArquivos=120"
    },
    {
        "id": "dispensa-mobiliario-geral-alvorada-jaburu-2023",
        "data": "2023-04-10",
        "modalidade": "Dispensas de Licitação Suplementares",
        "processo": "Processos Diversos - UASG 110001",
        "orgao": "Secretaria de Administração da Presidência da República",
        "local": "Palácio da Alvorada e Granja do Torto",
        "objeto": "Recomposição complementar de tapetes, cortinas, enxovais e utensílios residenciais.",
        "valor_total": 182658.00,
        "itens": [
            {
                "item": "Cortinas e enxovais sob medida",
                "descricao": "Tecidos de vedação e adequação das salas sociais.",
                "valor": 85000.00
            },
            {
                "item": "Tapetes e complementos decorativos",
                "descricao": "Recomposição de áreas sociais das residências oficiais.",
                "valor": 97658.00
            }
        ],
        "justificativa_governo": "Adequação das instalações das residências oficiais para recepção de autoridades de Estado e delegações estrangeiras.",
        "desdobramento_oficial": "Total acumulado de mobília e residência oficial em dispensas em 2023 somou R$ 379.428,00.",
        "posicao_orgaos_controle": "Auditado pela Controladoria-Geral da União (CGU) nas contas anuais da Presidência.",
        "fonte_url": "https://portaldatransparencia.gov.br/orgaos/20000"
    }
]


def consolidar_compras_diretas():
    output = DATA_DIR / "compras_diretas.js"
    conteudo = (
        "// Compras Diretas, Bens Patrimoniais e Dispensas de Licitação da Presidência\n"
        "// Fontes: Diário Oficial da União (DOU), Compras.gov.br e Tribunal de Contas da União (TCU)\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.compras_diretas = {json.dumps(COMPRAS_DIRETAS_OFICIAIS, indent=2, ensure_ascii=False)};\n"
    )
    with open(output, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[✓] {len(COMPRAS_DIRETAS_OFICIAIS)} processos de compras diretas/patrimoniais salvos em {output}")
    return COMPRAS_DIRETAS_OFICIAIS


if __name__ == "__main__":
    consolidar_compras_diretas()
