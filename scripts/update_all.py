"""
Orquestrador central de atualização de todos os dados do Trabalhômetro.
Executa a captura de cartões, viagens (API CGU + Agenda oficial) e entregas.
"""
from datetime import datetime
import json
from pathlib import Path
from config import DATA_DIR
import fetch_cartao
import fetch_viagens_oficiais
import fetch_viagens_api
import fetch_novopac
import fetch_entregas
import export_datasets


def atualizar_tudo():
    print("=" * 65)
    print("⭐️ TRABALHÔMETRO — Atualização com API Oficial do Portal da Transparência")
    print("=" * 65)

    # 1. Gastos (Cartão Corporativo CPGF)
    print("\n[1/4] Atualizando Gastos do Cartão Corporativo...")
    gastos = fetch_cartao.atualizar_gastos()

    # 2. Viagens (API Oficial da CGU + Viagens de Estado/Internacionais)
    print("\n[2/4] Atualizando Viagens Oficiais...")
    viagens_api = fetch_viagens_api.processar_viagens_api(limite_meses=12)
    viagens_estado = fetch_viagens_oficiais.VIAGENS_OFICIAIS

    # Mescla sem duplicidade
    todas_viagens = []
    vistos = set()

    for v in viagens_api + viagens_estado:
        chave = (v.get("data"), v.get("local"))
        if chave in vistos:
            continue
        vistos.add(chave)
        todas_viagens.append(v)

    todas_viagens.sort(key=lambda x: x.get("data", ""), reverse=True)

    output_viagens = DATA_DIR / "viagens.js"
    conteudo_viagens = (
        "// Viagens oficiais da Presidência da República\n"
        "// Fontes: API do Portal da Transparência (CGU) e Agenda Oficial do Planalto\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.viagens = {json.dumps(todas_viagens, indent=2, ensure_ascii=False)};\n"
    )
    with open(output_viagens, "w", encoding="utf-8") as f:
        f.write(conteudo_viagens)
    print(f"[✓] {len(todas_viagens)} viagens oficiais consolidadas com sucesso em {output_viagens}!")

    # 3. Novo PAC Transparência
    print("\n[3/4] Atualizando Dados Oficiais do Novo PAC...")
    pac_dados = fetch_novopac.extrair_dados_novopac()

    # 4. Entregas e Reformas
    print("\n[4/4] Atualizando Entregas Oficiais...")
    entregas = fetch_entregas.consolidar_entregas()

    # 4. Metadados
    hoje_fmt = datetime.now().strftime("%d/%m/%Y às %H:%M")
    paises_visitados = len(set(v.get("pais") for v in todas_viagens if v.get("tipo") == "internacional"))
    meta = {
        "atualizado_em": hoje_fmt,
        "exemplo": False,
        "total_meses_gastos": len(gastos),
        "total_viagens": len(todas_viagens),
        "total_paises": paises_visitados,
        "total_entregas": len(entregas)
    }

    meta_file = DATA_DIR / "meta.js"
    conteudo_meta = (
        "// Metadados de atualização do Trabalhômetro\n"
        "window.DADOS = window.DADOS || {};\n"
        f"window.DADOS.meta = {json.dumps(meta, indent=2, ensure_ascii=False)};\n"
    )
    with open(meta_file, "w", encoding="utf-8") as f:
        f.write(conteudo_meta)

    print(f"\n[✓] Sucesso! Metadados consolidados em {meta_file} ({hoje_fmt})")
    print(f"    - Gastos: {len(gastos)} meses oficiais")
    print(f"    - Viagens: {len(todas_viagens)} destinos catalogados ({paises_visitados} países)")
    print(f"    - Entregas: {len(entregas)} atos e obras oficiais")

    # 5. Exportação aberta (CSV + JSON)
    print("\n[5/5] Gerando exportações públicas (data/export/)...")
    export_datasets.exportar_todos()
    print("=" * 65)


if __name__ == "__main__":
    atualizar_tudo()
