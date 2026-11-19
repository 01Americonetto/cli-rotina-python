import argparse
import json
from datetime import datetime
from pathlib import Path

ARQUIVO_DADOS = Path(__file__).parent / "rotina.json"


def carregar_tarefas() -> list[dict]:
    if not ARQUIVO_DADOS.exists():
        return []
    with ARQUIVO_DADOS.open("r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas: list[dict]) -> None:
    with ARQUIVO_DADOS.open("w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)


def proximo_id(tarefas: list[dict]) -> int:
    if not tarefas:
        return 1
    return max(item["id"] for item in tarefas) + 1


def adicionar_tarefa(titulo: str, categoria: str) -> None:
    tarefas = carregar_tarefas()
    nova = {
        "id": proximo_id(tarefas),
        "titulo": titulo.strip(),
        "categoria": categoria.strip().lower(),
        "concluida": False,
        "criada_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tarefas.append(nova)
    salvar_tarefas(tarefas)
    print(f"[OK] Tarefa #{nova['id']} adicionada em '{nova['categoria']}': {nova['titulo']}")


def listar_tarefas(apenas_pendentes: bool = False, categoria: str | None = None) -> None:
    tarefas = carregar_tarefas()

    if apenas_pendentes:
        tarefas = [t for t in tarefas if not t["concluida"]]
    if categoria:
        cat_alvo = categoria.strip().lower()
        tarefas = [t for t in tarefas if t["categoria"] == cat_alvo]

    if not tarefas:
        print("Nenhuma tarefa encontrada com esse filtro.")
        return

    for t in tarefas:
        status = "[x]" if t["concluida"] else "[ ]"
        print(f"{status} #{t['id']} | ({t['categoria']}) {t['titulo']} — {t['criada_em']}")


def concluir_tarefa(tarefa_id: int) -> None:
    tarefas = carregar_tarefas()
    for t in tarefas:
        if t["id"] == tarefa_id:
            t["concluida"] = True
            salvar_tarefas(tarefas)
            print(f"[OK] Tarefa #{tarefa_id} marcada como concluída.")
            return
    print(f"[!] Tarefa #{tarefa_id} não encontrada.")


def remover_tarefa(tarefa_id: int) -> None:
    tarefas = carregar_tarefas()
    novas = [t for t in tarefas if t["id"] != tarefa_id]
    if len(novas) == len(tarefas):
        print(f"[!] Tarefa #{tarefa_id} não encontrada.")
        return
    salvar_tarefas(novas)
    print(f"[OK] Tarefa #{tarefa_id} removida.")


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rotina",
        description="CLI simples para organizar tarefas e rotina diária em JSON.",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # add
    p_add = subparsers.add_parser("add", help="Adiciona uma nova tarefa")
    p_add.add_argument("titulo", help="Descrição ou título da tarefa")
    p_add.add_argument("-c", "--categoria", default="geral", help="Categoria (ex.: estudo, treino, projeto)")

    # list
    p_list = subparsers.add_parser("list", help="Lista as tarefas")
    p_list.add_argument("-p", "--pendentes", action="store_true", help="Mostra apenas tarefas pendentes")
    p_list.add_argument("-c", "--categoria", help="Filtra por categoria")

    # done
    p_done = subparsers.add_parser("done", help="Marca uma tarefa como concluída")
    p_done.add_argument("id", type=int, help="ID da tarefa")

    # remove
    p_rm = subparsers.add_parser("remove", help="Remove uma tarefa pelo ID")
    p_rm.add_argument("id", type=int, help="ID da tarefa")

    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    if args.comando == "add":
        adicionar_tarefa(args.titulo, args.categoria)
    elif args.comando == "list":
        listar_tarefas(apenas_pendentes=args.pendentes, categoria=args.categoria)
    elif args.comando == "done":
        concluir_tarefa(args.id)
    elif args.comando == "remove":
        remover_tarefa(args.id)


if __name__ == "__main__":
    main()