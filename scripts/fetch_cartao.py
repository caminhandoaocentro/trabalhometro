"""
Coleta de gastos do Cartão de Pagamento do Governo Federal (CPGF)
da Presidência da República no Portal da Transparência.
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
    ORGAO_SUPERIOR_PRESIDENCIA,
    ANO_INICIO,
    MES_INICIO
)

CPGF_CACHE_DIR = CACHE_DIR / "cpgf"
CPGF_CACHE_DIR.mkdir(exist_ok=True)

USER_AGENT = "Trabalhometro/1.0 (+https://caminhandoaocentro.github.io/trabalhometro/)"
URL_FONTE_CARTOES = "https://portaldatransparencia.gov.br/cartoes"


def extrair_total_mes(ano_mes: str) -> dict | None:
    """
    Baixa o CSV de Dados Abertos do CPGF para o ano_mes (ex: '202301')
    e totaliza os gastos da Presidência da República.
    """
    cache_file = CPGF_CACHE_DIR / f"{ano_mes}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    url = f"https://portaldatransparencia.gov.br/download-de-dados/cpgf/{ano_mes}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return None
            content = resp.read()
    except Exception as e:
        print(f"[-] Mês {ano_mes} não disponível ou erro no download: {e}")
        return None

    try:
        total = 0.0
        qtd = 0
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="latin1"), delimiter=";")
                for row in reader:
                    orgao_sup = row.get("CÓDIGO ÓRGÃO SUPERIOR", "").strip()
                    orgao = row.get("CÓDIGO ÓRGÃO", "").strip()
                    if orgao_sup == ORGAO_SUPERIOR_PRESIDENCIA or orgao == "20101":
                        val_raw = row.get("VALOR TRANSAÇÃO", "").replace(".", "").replace(",", ".").strip()
                        try:
                            val = float(val_raw)
                            total += val
                            qtd += 1
                        except ValueError:
                            pass

        resultado = {
            "mes": f"{ano_mes[:4]}-{ano_mes[4:]}",
            "valor": round(total, 2),
            "transacoes": qtd,
            "fonte_url": URL_FONTE_CARTOES
        }

        # Salva em cache se tiver dados
        if qtd > 0:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=2)

        return resultado

    except Exception as e:
        print(f"[-] Erro ao processar ZIP do mês {ano_mes}: {e}")
        return None


def obter_lista_meses() -> list[str]:
    """Gera lista de meses no formato 'AAAAMM' de 2023 até o mês corrente."""
    hoje = datetime.now()
    meses = []
    ano = ANO_INICIO
    mes = MES_INICIO
    while (ano < hoje.year) or (ano == hoje.year and mes <= hoje.month):
        meses.append(f"{ano}{mes:02d}")
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1
    return meses


def atualizar_gastos():
    """Percorre os meses e gera o arquivo data/gastos.js com os dados reais."""
    meses = obter_lista_meses()
    print(f"[*] Processando {len(meses)} meses do CPGF (2023 em diante)...")

    gastos = []
    for am in meses:
        print(f" -> Verificando {am}...")
        res = extrair_total_mes(am)
        if res and res.get("valor", 0) > 0:
            gastos.append({
                "mes": res["mes"],
                "valor": res["valor"],
                "transacoes": res.get("transacoes", 0),
                "fonte_url": res["fonte_url"]
            })

    output_file = DATA_DIR / "gastos.js"
    conteudo_js = (
        "// Dados oficiais do Cartão Corporativo (CPGF) da Presidência da República\n"
        "// Fonte: Portal da Transparência (CGU)\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.gastos = {json.dumps(gastos, indent=2, ensure_ascii=False)};\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(conteudo_js)

    print(f"[✓] {len(gastos)} meses consolidados com sucesso em {output_file}!")
    return gastos


if __name__ == "__main__":
    atualizar_gastos()
