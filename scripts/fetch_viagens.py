"""
Coleta de viagens oficiais da Presidência da República
no Portal da Transparência (Dados Abertos).
"""
import io
import json
import csv
import zipfile
import urllib.request
from datetime import datetime
from pathlib import Path
from config import (
    DATA_DIR,
    CACHE_DIR,
    COORDENADAS,
    ORGAO_SUPERIOR_PRESIDENCIA,
    ANO_INICIO
)

VIAGENS_CACHE_DIR = CACHE_DIR / "viagens"
VIAGENS_CACHE_DIR.mkdir(exist_ok=True)

USER_AGENT = "Trabalhometro/1.0 (+https://jeferson-guedes.github.io/trabalhometro/)"
URL_FONTE_VIAGENS = "https://portaldatransparencia.gov.br/viagens"


def obter_coordenadas(destino: str) -> tuple[float, float, str, str]:
    """
    Retorna (lat, lon, pais, tipo) para um determinado destino.
    """
    destino_clean = destino.strip()

    # Busca exata
    if destino_clean in COORDENADAS:
        lat, lon = COORDENADAS[destino_clean]
        is_int = "/" not in destino_clean and "(DF)" not in destino_clean and "Brasil" not in destino_clean
        return lat, lon, "Internacional" if is_int else "Brasil", "internacional" if is_int else "nacional"

    # Busca parcial por nome de cidade ou UF
    for nome, (lat, lon) in COORDENADAS.items():
        if nome.split("/")[0].lower() in destino_clean.lower():
            is_int = "/" not in nome and "DF" not in nome
            return lat, lon, "Internacional" if is_int else "Brasil", "internacional" if is_int else "nacional"

    # Fallback padrão: Brasília
    lat, lon = COORDENADAS["Brasília/DF"]
    return lat, lon, "Brasil", "nacional"


def processar_ano_viagens(ano: int) -> list[dict]:
    """Baixa e processa o arquivo de viagens da Presidência da República para um ano."""
    cache_file = VIAGENS_CACHE_DIR / f"{ano}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    url = f"https://portaldatransparencia.gov.br/download-de-dados/viagens/{ano}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            if resp.status != 200:
                return []
            content = resp.read()
    except Exception as e:
        print(f"[-] Viagens {ano} não disponíveis ou erro: {e}")
        return []

    viagens = []
    vistos = set()

    try:
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            # Arquivo de viagens
            nome_csv = None
            for n in z.namelist():
                if "Viagem" in n:
                    nome_csv = n
                    break

            if not nome_csv:
                return []

            with z.open(nome_csv) as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="latin1"), delimiter=";")
                for row in reader:
                    orgao = row.get("Código do órgão superior", "").strip()
                    if orgao != ORGAO_SUPERIOR_PRESIDENCIA:
                        continue

                    destinos_raw = row.get("Destinos", "").strip()
                    data_inicio = row.get("Período - Data de início", "").strip()
                    motivo = row.get("Motivo", "").strip()
                    num_prop = row.get("Número da Proposta (PCDP)", "").strip()

                    if not destinos_raw or not data_inicio:
                        continue

                    # Converte data DD/MM/AAAA para AAAA-MM-DD
                    try:
                        dt = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
                    except Exception:
                        dt = data_inicio

                    # Divide múltiplos destinos se houver
                    destinos_lista = [d.strip() for d in destinos_raw.split("-") if d.strip()]
                    if not destinos_lista:
                        destinos_lista = [destinos_raw]

                    for dest in destinos_lista[:2]:  # pega os principais
                        chave = (dt, dest, motivo[:30])
                        if chave in vistos:
                            continue
                        vistos.add(chave)

                        lat, lon, pais, tipo = obter_coordenadas(dest)

                        viagens.append({
                            "data": dt,
                            "local": dest,
                            "pais": pais,
                            "tipo": tipo,
                            "lat": lat,
                            "lon": lon,
                            "motivo": motivo[:120] if motivo else "Viagem oficial a serviço",
                            "processo": num_prop,
                            "fonte_url": URL_FONTE_VIAGENS
                        })

        if viagens:
            # Ordena por data mais recente
            viagens.sort(key=lambda x: x["data"], reverse=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(viagens, f, indent=2, ensure_ascii=False)

        return viagens

    except Exception as e:
        print(f"[-] Erro ao ler CSV de viagens do ano {ano}: {e}")
        return []


def atualizar_viagens():
    """Consolida as viagens de todos os anos do mandato e salva em data/viagens.js."""
    ano_atual = datetime.now().year
    todas = []

    for ano in range(ANO_INICIO, ano_atual + 1):
        print(f"[*] Processando viagens de {ano}...")
        viagens_ano = processar_ano_viagens(ano)
        todas.extend(viagens_ano)

    # Ordena por data decrescente
    todas.sort(key=lambda x: x["data"], reverse=True)

    # Limita às últimas 150 viagens para não sobrecarregar o mapa e a lista
    selecionadas = todas[:150]

    output_file = DATA_DIR / "viagens.js"
    conteudo_js = (
        "// Viagens oficiais da Presidência da República\n"
        "// Fonte: Portal da Transparência (CGU)\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.viagens = {json.dumps(selecionadas, indent=2, ensure_ascii=False)};\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(conteudo_js)

    print(f"[✓] {len(selecionadas)} viagens consolidadas em {output_file}!")
    return selecionadas


if __name__ == "__main__":
    atualizar_viagens()
