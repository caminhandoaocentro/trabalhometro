"""
Integração com a API REST oficial do Portal da Transparência (CGU) para Viagens.
Utiliza a chave cadastrada em .env (chave-api-dados).
"""
import os
import re
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from config import DATA_DIR, CACHE_DIR, COORDENADAS, ORGAO_SUPERIOR_PRESIDENCIA
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TRANSPARENCIA_API_KEY", "").strip()
BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
CACHE_API_VIAGENS = CACHE_DIR / "api_viagens"
CACHE_API_VIAGENS.mkdir(exist_ok=True)


def extrair_destino_do_texto(texto: str) -> str:
    """Extrai cidade/UF ou país mencionado no motivo da viagem oficial."""
    texto_upper = texto.upper()

    # Busca padrão Cidade/UF (ex: SALVADOR/BA, RECIFE/PE, RIO DE JANEIRO/RJ)
    match = re.search(r'([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]{3,20})/([A-Z]{2})', texto_upper)
    if match:
        cidade = match.group(1).strip().title()
        uf = match.group(2).strip().upper()
        return f"{cidade}/{uf}"

    # Busca em coordenadas conhecidas
    for nome in COORDENADAS:
        cidade_base = nome.split("/")[0].split("(")[0].strip()
        if cidade_base.upper() in texto_upper:
            return nome

    return "Brasília/DF"


def buscar_viagens_mes_api(ano: int, mes: int) -> list[dict]:
    """Busca viagens a serviço da Presidência da República para um mês via API."""
    if not API_KEY:
        print("[-] TRANSPARENCIA_API_KEY não configurada.")
        return []

    cache_file = CACHE_API_VIAGENS / f"{ano}{mes:02d}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Calcula primeiro e último dia do mês
    dt_inicio = datetime(ano, mes, 1)
    if mes == 12:
        dt_fim = datetime(ano + 1, 1, 1) - timedelta(days=1)
    else:
        dt_fim = datetime(ano, mes + 1, 1) - timedelta(days=1)

    headers = {
        "chave-api-dados": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "dataIdaDe": dt_inicio.strftime("%d/%m/%Y"),
        "dataIdaAte": dt_fim.strftime("%d/%m/%Y"),
        "dataRetornoDe": dt_inicio.strftime("%d/%m/%Y"),
        "dataRetornoAte": dt_fim.strftime("%d/%m/%Y"),
        "codigoOrgao": ORGAO_SUPERIOR_PRESIDENCIA,
        "pagina": 1
    }

    try:
        r = requests.get(f"{BASE_URL}/viagens", headers=headers, params=params, timeout=20)
        if r.status_code != 200:
            print(f"[-] Erro na API para {ano}/{mes:02d}: {r.status_code}")
            return []

        dados = r.json()
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return dados
    except Exception as e:
        print(f"[-] Falha na requisição {ano}/{mes:02d}: {e}")
        return []


def processar_viagens_api(limite_meses: int = 12) -> list[dict]:
    """
    Percorre os meses recentes da Presidência e consolida destinos únicos com dados da API.
    """
    if not API_KEY:
        return []

    hoje = datetime.now()
    viagens_consolidadas = []
    chaves_vistas = set()

    print(f"[*] Consultando API de Viagens da CGU (últimos {limite_meses} meses)...")

    ano = hoje.year
    mes = hoje.month

    for _ in range(limite_meses):
        print(f" -> Consultando {ano}/{mes:02d}...")
        itens = buscar_viagens_mes_api(ano, mes)

        for item in itens:
            v_info = item.get("viagem", {})
            motivo = v_info.get("motivo", "")
            dt_inicio = item.get("dataInicioAfastamento", "")
            tipo_viagem = item.get("tipoViagem", "Nacional").lower()
            val_total = item.get("valorTotalViagem", 0.0)

            if not dt_inicio:
                continue

            destino = extrair_destino_do_texto(motivo)
            chave = (dt_inicio, destino)
            if chave in chaves_vistas:
                continue
            chaves_vistas.add(chave)

            # Coordenadas
            lat, lon = COORDENADAS.get(destino, COORDENADAS.get("Brasília/DF", (-15.79, -47.88)))
            is_int = "internacional" in tipo_viagem or ("/" not in destino and "DF" not in destino)

            viagens_consolidadas.append({
                "data": dt_inicio,
                "local": destino,
                "pais": "Internacional" if is_int else "Brasil",
                "tipo": "internacional" if is_int else "nacional",
                "lat": lat,
                "lon": lon,
                "motivo": motivo[:120] if motivo else "Viagem oficial a serviço da Presidência",
                "valor": val_total,
                "fonte_url": f"https://portaldatransparencia.gov.br/viagens/{item.get('id')}"
            })

        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        time.sleep(0.3)

    return viagens_consolidadas


if __name__ == "__main__":
    viagens = processar_viagens_api(6)
    print(f"[✓] {len(viagens)} viagens extraídas via API oficial da CGU!")
