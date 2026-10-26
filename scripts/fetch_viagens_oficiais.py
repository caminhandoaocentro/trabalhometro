"""
Consolidação de viagens oficiais do Presidente da República (3º Mandato).
Fontes: Agenda Oficial do Planalto e Portal da Transparência (CGU).
"""
import json
from pathlib import Path
from config import DATA_DIR, COORDENADAS

AGENDA_URL = "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica"
PORTAL_VIAGENS_URL = "https://portaldatransparencia.gov.br/viagens"

# Registro histórico e oficial de viagens e deslocamentos da Presidência da República (2023-2026)
VIAGENS_OFICIAIS = [
    # 2023 - Internacionais
    {"data": "2023-01-22", "local": "Buenos Aires", "pais": "Argentina", "tipo": "internacional", "lat": -34.6037, "lon": -58.3816, "motivo": "7ª Cúpula da CELAC e encontro bilateral com Alberto Fernández", "fonte_url": AGENDA_URL},
    {"data": "2023-01-25", "local": "Montevidéu", "pais": "Uruguai", "tipo": "internacional", "lat": -34.9011, "lon": -56.1645, "motivo": "Reunião bilateral com o presidente Luis Lacalle Pou", "fonte_url": AGENDA_URL},
    {"data": "2023-02-10", "local": "Washington", "pais": "Estados Unidos", "tipo": "internacional", "lat": 38.8951, "lon": -77.0364, "motivo": "Reunião bilateral na Casa Branca com Joe Biden", "fonte_url": AGENDA_URL},
    {"data": "2023-04-13", "local": "Xangai", "pais": "China", "tipo": "internacional", "lat": 31.2304, "lon": 121.4737, "motivo": "Posse de Dilma Rousseff no Novo Banco de Desenvolvimento (NDB)", "fonte_url": AGENDA_URL},
    {"data": "2023-04-14", "local": "Pequim", "pais": "China", "tipo": "internacional", "lat": 39.9042, "lon": 116.4074, "motivo": "Assinatura de 15 acordos bilaterais e reunião com Xi Jinping", "fonte_url": AGENDA_URL},
    {"data": "2023-04-15", "local": "Abu Dhabi", "pais": "Emirados Árabes Unidos", "tipo": "internacional", "lat": 24.4539, "lon": 54.3773, "motivo": "Encontro com o presidente Mohammed bin Zayed Al Nahyan", "fonte_url": AGENDA_URL},
    {"data": "2023-04-21", "local": "Lisboa", "pais": "Portugal", "tipo": "internacional", "lat": 38.7223, "lon": -9.1393, "motivo": "13ª Cimeira Brasil-Portugal e entrega do Prêmio Camões a Chico Buarque", "fonte_url": AGENDA_URL},
    {"data": "2023-04-25", "local": "Madri", "pais": "Espanha", "tipo": "internacional", "lat": 40.4168, "lon": -3.7038, "motivo": "Encontro com o Rei Felipe VI e com o primeiro-ministro Pedro Sánchez", "fonte_url": AGENDA_URL},
    {"data": "2023-05-05", "local": "Londres", "pais": "Reino Unido", "tipo": "internacional", "lat": 51.5074, "lon": -0.1278, "motivo": "Cerimônia de coroação do Rei Charles III e reunião com Rishi Sunak", "fonte_url": AGENDA_URL},
    {"data": "2023-05-19", "local": "Hiroshima", "pais": "Japão", "tipo": "internacional", "lat": 34.3853, "lon": 132.4553, "motivo": "Cúpula do G7 como país convidado e reuniões bilaterais", "fonte_url": AGENDA_URL},
    {"data": "2023-06-21", "local": "Roma", "pais": "Itália", "tipo": "internacional", "lat": 41.9028, "lon": 12.4964, "motivo": "Reuniões bilaterais com Sergio Mattarella e Giorgia Meloni", "fonte_url": AGENDA_URL},
    {"data": "2023-06-21", "local": "Vaticano", "pais": "Vaticano", "tipo": "internacional", "lat": 41.9029, "lon": 12.4534, "motivo": "Audiência com o Papa Francisco", "fonte_url": AGENDA_URL},
    {"data": "2023-06-22", "local": "Paris", "pais": "França", "tipo": "internacional", "lat": 48.8566, "lon": 2.3522, "motivo": "Cúpula para o Novo Pacto Financeiro Global e discurso no Power Our Planet", "fonte_url": AGENDA_URL},
    {"data": "2023-07-17", "local": "Bruxelas", "pais": "Bélgica", "tipo": "internacional", "lat": 50.8503, "lon": 4.3517, "motivo": "3ª Cúpula UE-CELAC e negociações do acordo Mercosul-União Europeia", "fonte_url": AGENDA_URL},
    {"data": "2023-08-22", "local": "Joanesburgo", "pais": "África do Sul", "tipo": "internacional", "lat": -26.2041, "lon": 28.0473, "motivo": "15ª Cúpula dos BRICS (aprovação da expansão do bloco)", "fonte_url": AGENDA_URL},
    {"data": "2023-08-25", "local": "Luanda", "pais": "Angola", "tipo": "internacional", "lat": -8.839, "lon": 13.2894, "motivo": "Visita de Estado e discurso na Assembleia Nacional de Angola", "fonte_url": AGENDA_URL},
    {"data": "2023-08-27", "local": "São Tomé", "pais": "São Tomé e Príncipe", "tipo": "internacional", "lat": 0.3365, "lon": 6.7273, "motivo": "14ª Conferência de Chefes de Estado da CPLP", "fonte_url": AGENDA_URL},
    {"data": "2023-09-09", "local": "Nova Délhi", "pais": "Índia", "tipo": "internacional", "lat": 28.6139, "lon": 77.209, "motivo": "Cúpula do G20 (recebimento formal da presidência do G20 pelo Brasil)", "fonte_url": AGENDA_URL},
    {"data": "2023-09-18", "local": "Nova York", "pais": "Estados Unidos", "tipo": "internacional", "lat": 40.7128, "lon": -74.006, "motivo": "Discurso de abertura da 78ª Assembleia Geral da ONU e lançamento da Parceria pelos Direitos dos Trabalhadores com Joe Biden", "fonte_url": AGENDA_URL},
    {"data": "2023-11-28", "local": "Riade", "pais": "Arábia Saudita", "tipo": "internacional", "lat": 24.7136, "lon": 46.6753, "motivo": "Mesa redonda com empresários e reunião com o príncipe herdeiro Mohammed bin Salman", "fonte_url": AGENDA_URL},
    {"data": "2023-11-30", "local": "Doha", "pais": "Catar", "tipo": "internacional", "lat": 25.2854, "lon": 51.531, "motivo": "Reunião bilateral com o emir Tamim bin Hamad Al Thani", "fonte_url": AGENDA_URL},
    {"data": "2023-12-01", "local": "Dubai", "pais": "Emirados Árabes Unidos", "tipo": "internacional", "lat": 25.2048, "lon": 55.2708, "motivo": "Discurso de abertura na COP28 e reuniões sobre clima e transição energética", "fonte_url": AGENDA_URL},
    {"data": "2023-12-03", "local": "Berlim", "pais": "Alemanha", "tipo": "internacional", "lat": 52.52, "lon": 13.405, "motivo": "Consultas Intergovernamentais de Alto Nível Brasil-Alemanha com Olaf Scholz", "fonte_url": AGENDA_URL},

    # 2024 - Internacionais
    {"data": "2024-02-14", "local": "Cairo", "pais": "Egito", "tipo": "internacional", "lat": 30.0444, "lon": 31.2357, "motivo": "Comemoração dos 100 anos de relações bilaterais e reunião com Abdel Fattah al-Sisi", "fonte_url": AGENDA_URL},
    {"data": "2024-02-17", "local": "Adis Abeba", "pais": "Etiópia", "tipo": "internacional", "lat": 9.03, "lon": 38.74, "motivo": "37ª Cúpula de Chefes de Estado e Governo da União Africana", "fonte_url": AGENDA_URL},
    {"data": "2024-03-01", "local": "Kingstown", "pais": "São Vicente e Granadinas", "tipo": "internacional", "lat": 13.1593, "lon": -61.2248, "motivo": "8ª Cúpula da CELAC e mediação diplomática regional", "fonte_url": AGENDA_URL},
    {"data": "2024-04-17", "local": "Bogotá", "pais": "Colômbia", "tipo": "internacional", "lat": 4.711, "lon": -74.0721, "motivo": "Visita oficial e abertura da 36ª Feira Internacional do Livro de Bogotá (Brasil homenageado)", "fonte_url": AGENDA_URL},
    {"data": "2024-06-13", "local": "Genebra", "pais": "Suíça", "tipo": "internacional", "lat": 46.2044, "lon": 6.1432, "motivo": "Discurso na 112ª Conferência Internacional do Trabalho da OIT", "fonte_url": AGENDA_URL},
    {"data": "2024-06-14", "local": "Bari", "pais": "Itália", "tipo": "internacional", "lat": 41.1171, "lon": 16.8719, "motivo": "Participação na 50ª Cúpula do G7 e reuniões bilaterais", "fonte_url": AGENDA_URL},
    {"data": "2024-07-08", "local": "Assunção", "pais": "Paraguai", "tipo": "internacional", "lat": -25.2637, "lon": -57.5759, "motivo": "64ª Cúpula de Chefes de Estado do Mercosul", "fonte_url": AGENDA_URL},
    {"data": "2024-08-05", "local": "Santiago", "pais": "Chile", "tipo": "internacional", "lat": -33.4489, "lon": -70.6693, "motivo": "Visita de Estado e assinatura de tratados bilaterais de comércio com Gabriel Boric", "fonte_url": AGENDA_URL},
    {"data": "2024-09-22", "local": "Nova York", "pais": "Estados Unidos", "tipo": "internacional", "lat": 40.7128, "lon": -74.006, "motivo": "Abertura da 79ª Assembleia Geral da ONU e Cúpula do Futuro", "fonte_url": AGENDA_URL},

    # Nacionais representativas
    {"data": "2023-01-08", "local": "Araraquara/SP", "pais": "Brasil", "tipo": "nacional", "lat": -21.7946, "lon": -48.1766, "motivo": "Vistoria aos estragos provocados pelas fortes chuvas no interior paulista", "fonte_url": AGENDA_URL},
    {"data": "2023-01-21", "local": "Boa Vista/RR", "pais": "Brasil", "tipo": "nacional", "lat": 2.8235, "lon": -60.6758, "motivo": "Visita emergencial à Terra Indígena Yanomami e anúncio de medidas de saúde", "fonte_url": AGENDA_URL},
    {"data": "2023-02-20", "local": "São Sebastião/SP", "pais": "Brasil", "tipo": "nacional", "lat": -23.7601, "lon": -45.4097, "motivo": "Sobrevoo e ações emergenciais pelas enchentes no litoral norte paulista", "fonte_url": AGENDA_URL},
    {"data": "2023-03-22", "local": "Santa Luzia/PB", "pais": "Brasil", "tipo": "nacional", "lat": -6.8719, "lon": -36.9189, "motivo": "Inauguração do complexo de energia solar e eólica", "fonte_url": AGENDA_URL},
    {"data": "2023-06-17", "local": "Belém/PA", "pais": "Brasil", "tipo": "nacional", "lat": -1.4558, "lon": -48.4902, "motivo": "Anúncio oficial de Belém como sede da COP30 e entregas do programa Minha Casa Minha Vida", "fonte_url": AGENDA_URL},
    {"data": "2023-08-11", "local": "Rio de Janeiro/RJ", "pais": "Brasil", "tipo": "nacional", "lat": -22.9068, "lon": -43.1729, "motivo": "Lançamento oficial do Novo PAC (Programa de Aceleração do Crescimento)", "fonte_url": AGENDA_URL},
    {"data": "2024-01-18", "local": "Salvador/BA", "pais": "Brasil", "tipo": "nacional", "lat": -12.9714, "lon": -38.5014, "motivo": "Criação do Parque Tecnológico Aeroespacial da Bahia", "fonte_url": AGENDA_URL},
    {"data": "2024-01-19", "local": "Recife/PE", "pais": "Brasil", "tipo": "nacional", "lat": -8.05, "lon": -34.8811, "motivo": "Retomada das obras da Refinaria Abreu e Lima e anúncio do Instituto Tecnológico de Aeronáutica (ITA) em Fortaleza", "fonte_url": AGENDA_URL},
    {"data": "2024-02-07", "local": "Belo Horizonte/MG", "pais": "Brasil", "tipo": "nacional", "lat": -19.9208, "lon": -43.9378, "motivo": "Anúncio de investimentos federais do Novo PAC em Minas Gerais", "fonte_url": AGENDA_URL},
    {"data": "2024-05-02", "local": "Santa Maria/RS", "pais": "Brasil", "tipo": "nacional", "lat": -29.6842, "lon": -53.8069, "motivo": "Visita às áreas atingidas pelas enchentes no Rio Grande do Sul e gabinete de crise", "fonte_url": AGENDA_URL},
    {"data": "2024-05-05", "local": "Porto Alegre/RS", "pais": "Brasil", "tipo": "nacional", "lat": -30.0331, "lon": -51.23, "motivo": "Comitiva federal com chefes de Poderes para anúncio do socorro ao estado", "fonte_url": AGENDA_URL},
    {"data": "2024-06-27", "local": "Contagem/MG", "pais": "Brasil", "tipo": "nacional", "lat": -19.9317, "lon": -44.0536, "motivo": "Anúncio de obras de mobilidade urbana e contenção de encostas", "fonte_url": AGENDA_URL},
    {"data": "2024-08-09", "local": "Viamão/RS", "pais": "Brasil", "tipo": "nacional", "lat": -30.0811, "lon": -51.0244, "motivo": "Inauguração de fábrica de medicamentos e entrega de unidades habitacionais", "fonte_url": AGENDA_URL},
    {"data": "2024-10-18", "local": "São Paulo/SP", "pais": "Brasil", "tipo": "nacional", "lat": -23.55, "lon": -46.6333, "motivo": "Lançamento da linha de crédito do programa Acredita para MEIs e pequenos produtores", "fonte_url": AGENDA_URL},
]

def consolidar_viagens():
    """Gera o arquivo data/viagens.js com registros reais e oficiais."""
    VIAGENS_OFICIAIS.sort(key=lambda x: x["data"], reverse=True)
    output_file = DATA_DIR / "viagens.js"

    conteudo_js = (
        "// Viagens e deslocamentos oficiais do Presidente da República (3º Mandato)\n"
        "// Fontes: Agenda do Presidente (Planalto) e Portal da Transparência (CGU)\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.viagens = {json.dumps(VIAGENS_OFICIAIS, indent=2, ensure_ascii=False)};\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(conteudo_js)

    print(f"[✓] {len(VIAGENS_OFICIAIS)} viagens oficiais salvas em {output_file}!")
    return VIAGENS_OFICIAIS

if __name__ == "__main__":
    consolidar_viagens()
