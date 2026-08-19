# Evidence Gates

Toda claim da revisão deve ser verificada **mecanicamente**. Esta página lista os comandos por stack e o princípio do delta. Se não existe comando que prove a claim, a claim não está aprovada — está "em aberto".

## Princípio do delta

- Gate por **delta**, nunca por valor absoluto: compare a saída do comando na baseline (antes da mudança) com o depois.
- Erro pré-existente na baseline ≠ erro da mudança.
- Typechecker só cobre o programa que ele vê — arquivos fora do `tsconfig`/projeto respondem "phantom"; não use como prova para arquivos fora do grafo compilado.
- Testes verdes ≠ equivalência: a suíte deixa passar ~1 em 5 refactors não-equivalentes.

## Comandos por stack

### .NET / C#

| Claim | Comando |
| --- | --- |
| Builda | `dotnet build` |
| Testes passam | `dotnet test` |
| Typecheck/análise | `dotnet build` (analyzers); `dotnet format analyzers --verify-no-changes` |
| Rename completo | LSP references / IDE rename; `rg '<símbolo>'` |

### TypeScript / JavaScript

| Claim | Comando |
| --- | --- |
| Typecheck | `tsc --noEmit` |
| Testes | `vitest run` / `jest --ci` |
| Dead code | `knip` / `ts-prune` (e ainda assim busque usos dinâmicos) |
| Rename completo | LSP references; `rg` |

### Python

| Claim | Comando |
| --- | --- |
| Typecheck | `pyright` / `mypy` |
| Testes | `pytest -q` |
| Lint | `ruff check .` |
| Dead code | `vulture` (com allowlist) |

### Go / Rust / Java

| Claim | Go | Rust | Java |
| --- | --- | --- | --- |
| Compila | `go build ./...` | `cargo check` | `mvn -q compile` / `./gradlew compileJava` |
| Testes | `go test ./...` | `cargo test` | `mvn -q test` / `./gradlew test` |
| Vet | `go vet ./...` | `cargo clippy` | `spotbugs`/`checkstyle` |

### PowerShell

| Claim | Comando |
| --- | --- |
| Lint | `Invoke-ScriptAnalyzer -Path .` |
| Testes | `Invoke-Pester` |

## Gates de revisão (o que executar na prática)

1. **Build/typecheck com delta:** rode na baseline (se disponível) e depois da mudança; aponte erros NOVOS.
2. **Suíte de testes na área tocada:** rode a suíte; compare o resultado com a baseline.
3. **Teste específico do caminho:** para mudanças de lógica, rode o teste que exercita aquele caminho e confirme que falharia se a lógica estivesse errada (injete falha mentalmente).
4. **Contrato de diff:** `git diff --name-only` só deve listar arquivos do escopo declarado.
5. **Equivalência declarada:** exija o artefato (caracterização, golden master, fuzz diferencial) ou rode-o. "Confie em mim" não é gate.
6. **Renames:** LSP references / busca estrutural (`ast-grep`, `comby`) — zero caller órfão.

## Limites que você deve declarar no relatório

| Ferramenta | Cobre | NÃO cobre |
| --- | --- | --- |
| Testes | Comportamento exercitado | Não testado, desempenho, integração real |
| Typechecker | Contratos de tipo do programa que ele vê | Lógica, arquivos fora do programa |
| Linter | Higiene estática | Equivalência |
| Dead-code estático | Referências léxicas | Imports dinâmicos, reflection, DI |
| Golden master | Saídas capturadas | Caminhos não capturados |
| Benchmarks | Caminho medido | Ambientes não medidos |

Se o revisor não consegue executar um gate (ex.: sem ambiente), o relatório deve dizer "NÃO VERIFICADO" para aquela claim — nunca "provavelmente OK".