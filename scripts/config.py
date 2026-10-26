"""
Configurações do Trabalhômetro para captura de dados oficiais.
"""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / ".cache"

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Órgãos oficiais da Presidência da República no SIAFI / CGU
ORGAO_SUPERIOR_PRESIDENCIA = "20000"
ORGAO_VINCULADO_PRESIDENCIA = "20101"

# Início do 3º mandato de Lula
ANO_INICIO = 2023
MES_INICIO = 1

# Chave opcional da API do Portal da Transparência (se vazia, usa os Dados Abertos diretos)
TRANSPARENCIA_API_KEY = os.getenv("TRANSPARENCIA_API_KEY", "").strip()

# Coordenadas conhecidas para capitais, grandes cidades e destinos frequentes
COORDENADAS = {
    # Brasil
    "Brasília/DF": (-15.793889, -47.882778),
    "Brasília (DF)": (-15.793889, -47.882778),
    "São Paulo/SP": (-23.55, -46.6333),
    "Rio de Janeiro/RJ": (-22.9068, -43.1729),
    "Salvador/BA": (-12.9714, -38.5014),
    "Recife/PE": (-8.05, -34.8811),
    "Fortaleza/CE": (-3.7172, -38.5434),
    "Belo Horizonte/MG": (-19.9208, -43.9378),
    "Porto Alegre/RS": (-30.0331, -51.23),
    "Curitiba/PR": (-25.4284, -49.2733),
    "Manaus/AM": (-3.119, -60.0217),
    "Belém/PA": (-1.4558, -48.4902),
    "Goiânia/GO": (-16.6869, -49.2648),
    "São Luís/MA": (-2.5307, -44.3068),
    "Maceió/AL": (-9.6658, -35.7353),
    "Natal/RN": (-5.7945, -35.211),
    "Teresina/PI": (-5.0892, -42.8016),
    "João Pessoa/PB": (-7.115, -34.8631),
    "Aracaju/SE": (-10.9472, -37.0731),
    "Cuiabá/MT": (-15.6014, -56.0979),
    "Campo Grande/MS": (-20.4697, -54.6201),
    "Vitória/ES": (-20.3155, -40.3128),
    "Florianópolis/SC": (-27.5954, -48.548),
    "Porto Velho/RO": (-8.7619, -63.9039),
    "Rio Branco/AC": (-9.9749, -67.8243),
    "Macapá/AP": (0.0389, -51.0664),
    "Boa Vista/RR": (2.8235, -60.6758),
    "Palmas/TO": (-10.2491, -48.3243),
    "Campinas/SP": (-22.9056, -47.0608),
    "Santos/SP": (-23.9608, -46.3336),
    "São Bernardo do Campo/SP": (-23.6939, -46.565),
    "Foz do Iguaçu/PR": (-25.5161, -54.5854),
    "Santarém/PA": (-2.4431, -54.7083),

    # Internacionais
    "Buenos Aires": (-34.6037, -58.3816),
    "Montevidéu": (-34.9011, -56.1645),
    "Washington": (38.8951, -77.0364),
    "Nova York": (40.7128, -74.006),
    "Pequim": (39.9042, 116.4074),
    "Xangai": (31.2304, 121.4737),
    "Lisboa": (38.7223, -9.1393),
    "Madri": (40.4168, -3.7038),
    "Londres": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Roma": (41.9028, 12.4964),
    "Vaticano": (41.9029, 12.4534),
    "Hiroshima": (34.3853, 132.4553),
    "Joanesburgo": (-26.2041, 28.0473),
    "Luanda": (-8.839, 13.2894),
    "São Tomé": (0.3365, 6.7273),
    "Nova Délhi": (28.6139, 77.209),
    "Dubai": (25.2048, 55.2708),
    "Berlim": (52.52, 13.405),
    "Riade": (24.7136, 46.6753),
    "Doha": (25.2854, 51.531),
    "Cairo": (30.0444, 31.2357),
    "Adis Abeba": (9.03, 38.74),
    "Kingstown": (13.1593, -61.2248),
    "Bogotá": (4.711, -74.0721),
    "Genebra": (46.2044, 6.1432),
    "Santiago": (-33.4489, -70.6693),
    "Assunção": (-25.2637, -57.5759),
}
