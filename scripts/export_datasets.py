"""
Utilitário de Exportação de Dados do Trabalhômetro.
Converte as bases consolidadas para JSON e CSV limpos em `data/export/`,
permitindo que pesquisadores, jornalistas e desenvolvedores utilizem
os dados diretamente em Python (Pandas), R, Excel ou APIs.
"""
import csv
import json
import re
from pathlib import Path
from config import DATA_DIR

EXPORT_DIR = DATA_DIR / "export"


def extrair_json_de_js(js_path: Path) -> any:
    """Lê um arquivo .js que atribui window.DADOS.xxx = {...} e extrai o objeto JSON."""
    texto = js_path.read_text(encoding="utf-8")
    # Busca a primeira ocorrência de '=' e pega até o final antes de ';'
    match = re.search(r"window\.DADOS(?:\.[a-zA-Z0-9_]+)?\s*=\s*(.+?);\s*$", texto, re.DOTALL)
    if match:
        bloco = match.group(1).strip()
        try:
            return json.loads(bloco)
        except Exception:
            # Caso seja JS puro com chaves não aspeadas (ex: avaliacao.js), usamos fallback seguro
            pass

    # Fallback usando node para avaliar JS com precisão
    import subprocess
    cmd = ["node", "-e", f"const fs = require('fs'); const window = {{}}; eval(fs.readFileSync('{js_path}', 'utf8')); console.log(JSON.stringify(Object.values(window.DADOS)[0]));"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def exportar_todos():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 65)
    print("📦 Exportando Datasets Consolidados (JSON + CSV)...")
    print("=" * 65)

    # 1. Gastos (CPGF)
    gastos_js = DATA_DIR / "gastos.js"
    if gastos_js.exists():
        gastos = extrair_json_de_js(gastos_js)
        # Salva JSON
        (EXPORT_DIR / "gastos.json").write_text(json.dumps(gastos, indent=2, ensure_ascii=False), encoding="utf-8")
        # Salva CSV
        with open(EXPORT_DIR / "gastos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["mes", "ano", "valor", "transacoes"])
            for g in gastos:
                mes = g.get("mes", "")
                ano = mes.split("-")[0] if "-" in mes else ""
                writer.writerow([mes, ano, g.get("valor", 0), g.get("transacoes", 0)])
        print(f"[✓] Gastos exportados: {len(gastos)} meses -> data/export/gastos.json & gastos.csv")

    # 2. Viagens
    viagens_js = DATA_DIR / "viagens.js"
    if viagens_js.exists():
        viagens = extrair_json_de_js(viagens_js)
        # Salva JSON
        (EXPORT_DIR / "viagens.json").write_text(json.dumps(viagens, indent=2, ensure_ascii=False), encoding="utf-8")
        # Salva CSV
        with open(EXPORT_DIR / "viagens.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["data", "tipo", "local", "pais", "uf", "motivo", "lat", "lng", "fonte"])
            for v in viagens:
                writer.writerow([
                    v.get("data", ""),
                    v.get("tipo", ""),
                    v.get("local", ""),
                    v.get("pais", ""),
                    v.get("uf", ""),
                    v.get("motivo", ""),
                    v.get("lat", ""),
                    v.get("lng", ""),
                    v.get("fonte", "")
                ])
        print(f"[✓] Viagens exportadas: {len(viagens)} registros -> data/export/viagens.json & viagens.csv")

    # 3. Entregas e Reformas
    entregas_js = DATA_DIR / "entregas.js"
    if entregas_js.exists():
        entregas = extrair_json_de_js(entregas_js)
        # Salva JSON
        (EXPORT_DIR / "entregas.json").write_text(json.dumps(entregas, indent=2, ensure_ascii=False), encoding="utf-8")
        # Salva CSV
        with open(EXPORT_DIR / "entregas.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ano", "data", "titulo", "tipo", "uf", "investimento", "descricao", "fonte_url"])
            for e in entregas:
                writer.writerow([
                    e.get("ano", ""),
                    e.get("data", ""),
                    e.get("titulo", ""),
                    e.get("tipo", ""),
                    e.get("uf", ""),
                    e.get("investimento", ""),
                    e.get("descricao", ""),
                    e.get("fonte_url", "")
                ])
        print(f"[✓] Entregas exportadas: {len(entregas)} atos -> data/export/entregas.json & entregas.csv")

    # 4. Novo PAC
    novopac_js = DATA_DIR / "novopac.js"
    if novopac_js.exists():
        pac = extrair_json_de_js(novopac_js)
        (EXPORT_DIR / "novopac.json").write_text(json.dumps(pac, indent=2, ensure_ascii=False), encoding="utf-8")
        with open(EXPORT_DIR / "novopac_fontes.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["fonte", "valor", "percentual"])
            for fo in pac.get("fontes_financiamento", []):
                writer.writerow([fo.get("fonte", ""), fo.get("valor", ""), fo.get("percentual", "")])
        print(f"[✓] Novo PAC exportado -> data/export/novopac.json & novopac_fontes.csv")

    # 5. Avaliação Desenvolvimentista
    avaliacao_js = DATA_DIR / "avaliacao.js"
    if avaliacao_js.exists():
        avaliacao = extrair_json_de_js(avaliacao_js)
        (EXPORT_DIR / "avaliacao.json").write_text(json.dumps(avaliacao, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[✓] Avaliação exportada -> data/export/avaliacao.json")

    # 6. Metadados
    meta_js = DATA_DIR / "meta.js"
    if meta_js.exists():
        meta = extrair_json_de_js(meta_js)
        (EXPORT_DIR / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[✓] Metadados exportados -> data/export/meta.json")

    print(f"\n[✓] Exportação completa com sucesso em {EXPORT_DIR}")


if __name__ == "__main__":
    exportar_todos()
