# CLI de Rotina em Python

Ferramenta de linha de comando (CLI) simples em Python para organizar tarefas e rotina diária, salvando os dados localmente em `rotina.json` (ignorado pelo Git via `.gitignore`).

## Funcionalidades

- **Adicionar tarefa (`add`):** cria uma tarefa com título e categoria opcional (`geral` por padrão).
- **Listar tarefas (`list`):** exibe todas as tarefas ou filtra por pendentes (`-p`) e categoria (`-c`).
- **Concluir tarefa (`done`):** marca uma tarefa como concluída pelo `ID`.
- **Remover tarefa (`remove`):** exclui uma tarefa pelo `ID`.

## Como executar no Windows (PowerShell)

```powershell
$py = "$env:APPDATA\uv\python\cpython-3.15.2-windows-x86_64-none\python.exe"
& $py rotina.py add "Revisar código e subir no Git" -c estudos
& $py rotina.py add "Treino físico e alongamento" -c treino
& $py rotina.py list -p
& $py rotina.py done 1
& $py rotina.py list
```

## Estrutura do projeto

```text
cli-rotina/
├── .gitignore
├── README.md
└── rotina.py
```