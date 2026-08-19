# Skills — Repositório de Agent Skills

<p align="center">
  <a href="https://skills.sh/tetri/skills"><img src="https://skills.sh/b/tetri/skills" alt="Instalações no skills.sh"></a>
</p>

Repositório de **Agent Skills** no padrão da [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) (pasta + `SKILL.md`), compatível com Claude Code, opencode, Cursor e outros agentes que seguem a especificação.

## Estrutura

```
.
├── skills/                 # Skills (uma pasta por skill)
│   └── <skill-name>/
│       ├── SKILL.md        # Metadados + instruções (< 500 linhas)
│       ├── references/     # Docs complementares (1 nível de profundidade)
│       ├── scripts/        # Scripts executáveis determinísticos
│       └── assets/         # Templates e arquivos estáticos
├── template/               # Esqueleto para criar novas skills
├── CONTRIBUTING.md         # Regras do padrão + checklist
└── README.md
```

## Skills

| Skill | Descrição | Status |
| --- | --- | --- |
| [code-refactoring](skills/code-refactoring/) | Refatoração segura com gates mecânicos de equivalência, grafo de dependências e disciplina git reversível | Publicado |
| [code-review](skills/code-review/) | Revisão adversarial com evidências mecânicas e caça a mudanças de comportamento mascaradas | Publicado |
| [test-authoring](skills/test-authoring/) | Criação de rede de segurança: caracterização, golden master, testes de borda | Publicado |
| [skill-creator](skills/skill-creator/) | Protocolo de criação de skills notáveis (pesquisa, gap analysis, escrita, validação) | Publicado |

## Instalação (symlink)

Cada skill é uma pasta autocontida. Instale criando um link simbólico para o diretório de skills do agente.

### Diretórios de destino

- **Claude Code** — global `~/.claude/skills/`, projeto `.claude/skills/`
- **opencode** — global `~/.config/opencode/skills/`, `~/.claude/skills/` ou `~/.agents/skills/`; projeto `.opencode/skills/`, `.claude/skills/` ou `.agents/skills/`
- **Cursor** — `~/.cursor/skills/` ou `.cursor/skills/`

### Windows (PowerShell)

```powershell
# Junction não exige admin (recomendado). Alternativa: -ItemType SymbolicLink (exige Dev Mode/admin)
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\<skill-name>" -Target "D:\tetri\skills\skills\<skill-name>"
```

### macOS / Linux (bash)

```bash
ln -s "$PWD/skills/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

> Para instalar todas as skills de uma vez, repita o comando para cada pasta em `skills/`.

## Validar uma skill

Use o validador da especificação **`skills-ref`** (agentskills.io) para conferir conformidade com o padrão Agent Skills.

## Licença

MIT — veja [LICENSE](LICENSE).