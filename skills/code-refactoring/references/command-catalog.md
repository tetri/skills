# Command Catalog

Comandos determinísticos por stack para o Gate 0 (baseline), o loop de passo seguro e o Gate final. Para cada stack: o que rodar, o que a ferramenta cobre e — criticamente — **o que ela NÃO cobre**. Prefira sempre a ferramenta determinística ao invés de "confiar no olho" do modelo.

## .NET / C#

| Etapa | Comando |
| --- | --- |
| Build | `dotnet build` (ou `dotnet build <proj>`) |
| Testes | `dotnet test` |
| Typecheck/análise | `dotnet build` + analyzers (`.editorconfig` com `dotnet_diagnostic` severities); `dotnet format analyzers` (seco) |
| Lint | `dotnet format --verify-no-changes` |
| Dead code | `dotnet build` com `EnableNETAnalyzers`; IDE/`dotnet-format`; `Microsoft.CodeAnalysis.NetAnalyzers` (CA1815 etc.). Ferramenta externa: `ReSharper`/`Roslynator` CLI |
| Rename | IDE rename (F2), Roslyn code action — use em vez de edição textual |

**Limites:** testes não cobrem comportamento não exercitado; typechecker não vê arquivos fora do projeto; nullable warnings (CS86xx) são gate de delta; reflection/DynamicInvoke não é visto por analisadores estáticos.

## TypeScript / JavaScript

| Etapa | Comando |
| --- | --- |
| Typecheck | `tsc --noEmit` (ou `npm run typecheck`) |
| Testes | `vitest run` / `jest --ci` / `npm test` |
| Lint | `eslint .` |
| Dead code | `knip` (imports/exports não usados); `ts-prune` |
| Rename | `tsc` + LSP go-to-definition; `ast-grep` para renames estruturais |

**Limites:** `tsc` só typechecka arquivos no projeto (phantom para arquivos fora do programa — nunca use como prova de arquivos fora do `tsconfig`); `knip` não vê imports dinâmicos, string paths ou `.vue/.svelte` sem config própria; testes não veem runtime de libs externas.

## Python

| Etapa | Comando |
| --- | --- |
| Typecheck | `pyright` ou `mypy --strict` (scoped) |
| Testes | `pytest -q` (ou `python -m pytest`) |
| Lint | `ruff check .` |
| Dead code | `vulture` (com allowlist de falsos positivos) |
| Rename | `python-rope` (AST-aware, resolve todos os callers), `ruff` ou `pyupgrade` para idioms |

**Limites:** `mypy` não rastreia dinâmica (`getattr`, `eval`, `__import__`, metaprogramação); `vulture` gera falsos positivos em entrypoints/registros — use allowlist; testes dinâmicos (parametrize) não são vistos por estáticos.

## Go

| Etapa | Comando |
| --- | --- |
| Build/check | `go build ./...` e `go vet ./...` |
| Testes | `go test ./...` (ou `go test ./<pkg>/...`) |
| Lint | `golangci-lint run` |
| Dead code | `go vet` (unreachable), `staticcheck` (SA), `deadcode` tool |

**Limites:** `go vet` cobre padrões conhecidos, não lógica; `go test ./...` compila todos os pacotes (bom para delta de compilação); reflection/`go:linkname`/`//go:build` dinâmicos não são vistos.

## Rust

| Etapa | Comando |
| --- | --- |
| Build/check | `cargo check` (rápido) e `cargo build` |
| Testes | `cargo test` |
| Lint | `cargo clippy -- -D warnings` |
| Dead code | `cargo clippy` (dead_code lint), `cargo udeps` (deps não usadas) |
| Rename | `rust-analyzer` LSP rename |

**Limites:** `cargo check` não executa; testes `#[ignore]`/feature-gated não rodam por padrão; macros e geração procedural não são vistos por estáticos.

## Java (Maven/Gradle)

| Etapa | Comando |
| --- | --- |
| Build/check | `mvn -q compile` / `./gradlew compileJava` |
| Testes | `mvn -q test` / `./gradlew test` |
| Lint | `spotbugs`, `checkstyle`, `pmd` |
| Dead code | `jdeps` (deps), `UCDetector`/IntelliJ inspection |
| Rename | IDE rename (refactoring engine) — use em vez de edição textual |

**Limites:** testes não cobrem paths não exercitados; reflection/SPI (`ServiceLoader`) não é visto por estáticos; toolchain (JDK version) afeta o build — use a versão do projeto.

## PowerShell

| Etapa | Comando |
| --- | --- |
| Lint | `Invoke-ScriptAnalyzer -Path .` (PSScriptAnalyzer) |
| Testes | `Invoke-Pester` (Pester 5) |
| Docs/parse | `[System.Management.Automation.Language.Parser]::ParseFile()` para AST |

**Limites:** PSScriptAnalyzer é heurístico; dynamic invocation (`& $cmd`, `Invoke-Expression`) não é rastreável; testes dependem do host.

## Git (base de todas as stacks)

| Etapa | Comando |
| --- | --- |
| Contrato de diff | `git diff --name-only` e `git diff --stat` |
| Reverter fora do contrato | `git checkout -- <arquivo>` |
| Achar usos históricos | `git log -S'<symbol>' --oneline -- <path>` |
| Estado da árvore | `git status --porcelain` |
| Blame (entender) | `git blame -L <range> <file>` |
| Desfazer passo | `git revert <commit>` ou `git checkout -- <file>` |
| Commit refactor-only | mensagem `refactor: <oque> (<refatoração>)` — nunca misturar |

## Busca estrutural (todas as stacks)

- `ast-grep` (`sg`) — busca/reescrita estrutural por padrões de AST.
- `comby` — reescrita textual com matching estruturado.
- `rg`/`grep -R` — usos textuais (inclui imports dinâmicos que estáticos perdem).
- LSP (`typescript-language-server`, `pyright-langserver`, `rust-analyzer`, etc.) — go-to-definition/references para confirmar call sites.

## Regra de ouro

Ferramenta determinística > inferência do modelo. Se existe ferramenta para o passo (rename, reescrita, verificação), use-a. O modelo planeja e orquestra; a ferramenta executa e prova.