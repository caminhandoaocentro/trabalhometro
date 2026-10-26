"""
Orquestrador central de atualização de todos os dados do Trabalhômetro.
Executa a captura de cartões, viagens, entregas e atualiza data/meta.js.
"""
from datetime import datetime
import json
from pathlib import Path
from config import DATA_DIR
import fetch_cartao
import fetch_viagens_oficiais
import fetch_entregas


def atualizar_tudo():
    print("=" * 60)
    print("⭐️ TRABALHÔMETRO — Atualização de Dados Oficiais")
    print("=" * 60)

    # 1. Gastos (Cartão Corporativo)
    print("\n[1/3] Atualizando Gastos do Cartão Corporativo...")
    gastos = fetch_cartao.atualizar_gastos()

    # 2. Viagens
    print("\n[2/3] Atualizando Viagens Oficiais...")
    viagens = fetch_viagens_oficiais.consolidar_viagens()

    # 3. Entregas
    print("\n[3/3] Atualizando Entregas Oficiais...")
    entregas = fetch_entregas.consolidar_entregas()

    # 4. Metadados
    hoje_fmt = datetime.now().strftime("%d/%m/%Y às %H:%M")
    meta = {
        "atualizado_em": hoje_fmt,
        "exemplo": False,
        "total_meses_gastos": len(gastos),
        "total_viagens": len(viagens),
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

    print(f"\n[✓] Sucesso! Metadados atualizados em {meta_file} ({hoje_fmt})")
    print("=" * 60)


if __name__ == "__main__":
    atualizar_tudo()
