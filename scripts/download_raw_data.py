"""
Script de Download Massivo e Arquivamento de Dados Brutos (Data Lake Local).
Filtra especificamente os dados da Presidência da República (2023 - 2026).
Salva em: data/raw/
"""
import io
import os
import csv
import json
import time
import zipfile
import requests
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from config import (
    DATA_DIR,
    ORGAO_SUPERIOR_PRESIDENCIA,
    ANO_INICIO,
    MES_INICIO
)

load_dotenv()

API_KEY = os.getenv("TRANSPARENCIA_API_KEY", "").strip()
BASE_API = "https://api.portaldatransparencia.gov.br/api-de-dados"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

RAW_DIR = DATA_DIR / "raw"
RAW_CPGF = RAW_DIR / "cpgf"
RAW_VIAGENS = RAW_DIR / "viagens"
RAW_DESPESAS = RAW_DIR / "despesas"
RAW_NOVOPAC = RAW_DIR / "novopac"

for d in [RAW_CPGF, RAW_VIAGENS, RAW_DESPESAS, RAW_NOVOPAC]:
    d.mkdir(parents=True, exist_ok=True)


def obter_meses_mandato() -> list[tuple[int, int]]:
    """Gera lista de tuplas (ano, mes) de 01/2023 até o mês corrente."""
    hoje = datetime.now()
    lista = []
    ano, mes = ANO_INICIO, MES_INICIO
    while (ano < hoje.year) or (ano == hoje.year and mes <= hoje.month):
        lista.append((ano, mes))
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1
    return lista


# =========================================================================
# 1. Download Bruto do Cartão Corporativo (CPGF)
# =========================================================================
def baixar_raw_cpgf():
    print("\n" + "=" * 60)
    print("📦 [1/3] BAIXANDO DADOS BRUTOS DO CARTÃO CORPORATIVO (CPGF)")
    print("=" * 60)

    meses = obter_meses_mandato()
    total_linhas_presidencia = 0

    for ano, mes in meses:
        cod_mes = f"{ano}{mes:02d}"
        dest_csv = RAW_CPGF / f"CPGF_Presidencia_{cod_mes}.csv"

        if dest_csv.exists() and dest_csv.stat().st_size > 100:
            print(f" [✓] {cod_mes} já arquivado localmente ({dest_csv.name})")
            continue

        url = f"https://portaldatransparencia.gov.br/download-de-dados/cpgf/{cod_mes}"
        print(f" [↓] Baixando pacote {cod_mes}...")
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    continue
                conteudo_zip = resp.read()
        except Exception as e:
            print(f"  [-] Mês {cod_mes} não disponível no Portal: {e}")
            continue

        try:
            linhas_filtradas = []
            header = None

            with zipfile.ZipFile(io.BytesIO(conteudo_zip)) as z:
                csv_nome = z.namelist()[0]
                with z.open(csv_nome) as f:
                    reader = csv.DictReader(io.TextIOWrapper(f, encoding="latin1"), delimiter=";")
                    header = reader.fieldnames

                    for row in reader:
                        orgao_sup = row.get("CÓDIGO ÓRGÃO SUPERIOR", "").strip()
                        orgao = row.get("CÓDIGO ÓRGÃO", "").strip()
                        if orgao_sup == ORGAO_SUPERIOR_PRESIDENCIA or orgao == "20101":
                            linhas_filtradas.append(row)

            if linhas_filtradas and header:
                with open(dest_csv, "w", encoding="utf-8", newline="") as out_f:
                    writer = csv.DictWriter(out_f, fieldnames=header, delimiter=";")
                    writer.writeheader()
                    writer.writerows(linhas_filtradas)

                qtd = len(linhas_filtradas)
                total_linhas_presidencia += qtd
                print(f"  [✓] Salvo {dest_csv.name}: {qtd} transações brutas da Presidência.")
        except Exception as e:
            print(f"  [-] Erro ao processar CSV {cod_mes}: {e}")

    print(f"\n[✓] CPGF Concluído! Arquivos salvos em: {RAW_CPGF}")


# =========================================================================
# 2. Download Bruto de Viagens a Serviço (API CGU)
# =========================================================================
def baixar_raw_viagens():
    print("\n" + "=" * 60)
    print("✈️ [2/3] BAIXANDO DADOS BRUTOS DE VIAGENS (API CGU)")
    print("=" * 60)

    if not API_KEY:
        print("[-] API_KEY não configurada. Pule para a próxima etapa.")
        return

    meses = obter_meses_mandato()
    headers = {"chave-api-dados": API_KEY, "Accept": "application/json"}

    for ano, mes in meses:
        cod_mes = f"{ano}{mes:02d}"
        dest_json = RAW_VIAGENS / f"Viagens_Presidencia_{cod_mes}.json"

        if dest_json.exists() and dest_json.stat().st_size > 10:
            print(f" [✓] {cod_mes} já arquivado localmente ({dest_json.name})")
            continue

        dt_inicio = datetime(ano, mes, 1)
        if mes == 12:
            dt_fim = datetime(ano + 1, 1, 1) - timedelta(days=1)
        else:
            dt_fim = datetime(ano, mes + 1, 1) - timedelta(days=1)

        params = {
            "dataIdaDe": dt_inicio.strftime("%d/%m/%Y"),
            "dataIdaAte": dt_fim.strftime("%d/%m/%Y"),
            "dataRetornoDe": dt_inicio.strftime("%d/%m/%Y"),
            "dataRetornoAte": dt_fim.strftime("%d/%m/%Y"),
            "codigoOrgao": ORGAO_SUPERIOR_PRESIDENCIA,
            "pagina": 1
        }

        print(f" [↓] Consultando API de Viagens {cod_mes}...")
        try:
            r = requests.get(f"{BASE_API}/viagens", headers=headers, params=params, timeout=20)
            if r.status_code == 200:
                dados = r.json()
                with open(dest_json, "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
                print(f"  [✓] Salvo {dest_json.name}: {len(dados)} processos de viagem.")
            else:
                print(f"  [-] Erro HTTP {r.status_code} para {cod_mes}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [-] Falha ao consultar viagens {cod_mes}: {e}")

    print(f"\n[✓] Viagens Concluídas! Arquivos salvos em: {RAW_VIAGENS}")


# =========================================================================
# 3. Download Bruto de Fornecedores e Pagamentos da Presidência (API CGU)
# =========================================================================
def baixar_raw_despesas():
    print("\n" + "=" * 60)
    print("💼 [3/3] BAIXANDO EXECUÇÃO DE DESPESAS E FAVORECIDOS (API CGU)")
    print("=" * 60)

    if not API_KEY:
        return

    meses = obter_meses_mandato()
    headers = {"chave-api-dados": API_KEY, "Accept": "application/json"}

    for ano, mes in meses[-12:]:  # Últimos 12 meses mais recentes
        cod_mes = f"{ano}{mes:02d}"
        dest_json = RAW_DESPESAS / f"Despesas_Favorecidos_{cod_mes}.json"

        if dest_json.exists():
            print(f" [✓] {cod_mes} já arquivado localmente ({dest_json.name})")
            continue

        m_str = f"{mes:02d}/{ano}"
        url = f"{BASE_API}/despesas/recursos-recebidos"
        params = {
            "codigoOrgao": ORGAO_SUPERIOR_PRESIDENCIA,
            "mesAnoInicio": m_str,
            "mesAnoFim": m_str,
            "pagina": 1
        }

        print(f" [↓] Baixando favorecidos de despesas {cod_mes}...")
        try:
            r = requests.get(url, headers=headers, params=params, timeout=20)
            if r.status_code == 200:
                dados = r.json()
                with open(dest_json, "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
                print(f"  [✓] Salvo {dest_json.name}: {len(dados)} fornecedores/favorecidos.")
            else:
                print(f"  [-] Status {r.status_code} para despesas {cod_mes}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [-] Erro despesas {cod_mes}: {e}")

    print(f"\n[✓] Despesas Concluídas! Arquivos salvos em: {RAW_DESPESAS}")


def executar_download_completo():
    inicio = time.time()
    print("🚀 INICIANDO DOWNLOAD MASSIVO DE DADOS BRUTOS DA PRESIDÊNCIA")
    print(f"Diretório destino: {RAW_DIR}")

    baixar_raw_cpgf()
    baixar_raw_viagens()
    baixar_raw_despesas()

    duracao = time.time() - inicio
    print("\n" + "=" * 65)
    print(f"🎉 DOWNLOAD CONCLUÍDO COM SUCESSO EM {duracao:.1f} SEGUNDOS!")
    print(f"Todos os dados brutos oficiais foram arquivados em: {RAW_DIR}")
    print("=" * 65)


if __name__ == "__main__":
    executar_download_completo()
