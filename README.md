# Skills — Repositório de Agent Skills

<p align="center">
  <a href="https://skills.sh/tetri/skills"><img src="https://skills.sh/b/tetri/skills" alt="Instalações no skills.sh"></a>
</p>

Repositório de **Agent Skills** no padrão da [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) (pasta + `SKILL.md`), compatível com Claude Code, opencode, Cursor e outros agentes que seguem a especificação.

## Skills

| Skill | Descrição | skills-ref | Gen Agent Trust Hub | Socket | Snyk |
| --- | --- | --- | --- | --- | --- |
| [code-refactoring](skills/code-refactoring/) | Refatoração segura com gates mecânicos de equivalência, grafo de dependências e disciplina git reversível | Pass | Pass (SAFE) | Pass | Pass (LOW) |
| [code-review](skills/code-review/) | Revisão adversarial com evidências mecânicas e caça a mudanças de comportamento mascaradas | Pass | Pass (SAFE) | Pass | Warn (MEDIUM) — [W011](https://skills.sh/tetri/skills/code-review/security/snyk) |
| [test-authoring](skills/test-authoring/) | Criação de rede de segurança: caracterização, golden master, testes de borda | Pass | Pass (SAFE) | Pass | Pass (LOW) |
| [skill-creator](skills/skill-creator/) | Protocolo de criação de skills notáveis (pesquisa, gap analysis, escrita, validação) | Pass | Pass (SAFE) | Pass | Pass (LOW) |
| [amp-web-stories](skills/amp-web-stories/) | Histórias visuais full-screen (Web Stories AMP) com gate determinístico de validação e avaliação de estado da arte | Pass | — | — | — |

Verificações: `skills-ref` valida a conformidade com o padrão Agent Skills; os demais são [security audits](https://skills.sh/audits) do skills.sh. O aviso do Snyk em `code-review` (W011, "Third-party content exposure detected — indirect prompt injection risk") é uma flag genérica de scanner para skills que instruem o agente a analisar conteúdo externo (diffs e PRs de terceiros) — risco inerente à atividade de revisão, não uma vulnerabilidade da skill. A `amp-web-stories` ainda não foi publicada no skills.sh (audits pendentes).

## Instalação

Cada skill é uma pasta autocontida. Instale criando um link simbólico para o diretório de skills do agente.

- **Claude Code** — global `~/.claude/skills/`, projeto `.claude/skills/`
- **opencode** — global `~/.claude/skills/` ou `~/.agents/skills/`; projeto `.claude/skills/` ou `.agents/skills/`
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

## Licença

MIT — veja [LICENSE](LICENSE).