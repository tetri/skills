---
name: code-refactoring
description: Refatora código existente com segurança, preservando o comportamento observável, por meio de passos pequenos verificados por build e testes, gates mecânicos de equivalência (caracterização, golden master, typecheck por delta), ordenação por grafo de dependências e disciplina git reversível. Use quando o usuário pedir para melhorar, simplificar, reestruturar, renomear, extrair, mover ou limpar código sem mudar o que ele faz.
license: MIT
compatibility: Windows/PowerShell, git; agnóstica de linguagem
metadata:
  categoria: engenharia-de-software
  fontes: Fowler-Refactoring-2ed, refactoring.guru, RefactorAssist/SWE-Refactor-2026
  status: publicado
---

# Code Refactoring

Refatoração é modificar a estrutura interna do software **sem alterar o comportamento observável**, encadeando pequenos passos que preservam comportamento — cada um verificado. Esta skill é um **protocolo com gates**, não uma lista de boas intenções: todo passo de refatoração passa por verificação mecânica antes de avançar.

## Quando usar

- O usuário pede para "melhorar", "simplificar", "limpar", "reestruturar", "renomear", "extrair", "mover", "deduplicar" código existente mantendo o comportamento.
- Refatoração preparatória: o código atrapalha a adição de uma feature ou a correção de um bug — refatore a causa antes de implementar.
- Refatoração para compreensão: o usuário precisa entender código obscuro.
- Reduzir dívida técnica em área que será tocada (regra do acampamento: deixe melhor do que encontrou).
- Code review: o autor e o revisor refatoram juntos a zona revisada.

## Quando NÃO usar (recuse e redirecione)

- O usuário quer mudar comportamento, adicionar feature ou corrigir lógica — isso é funcionalidade, não refatoração. Nunca misture nos mesmos commits (dois chapéus).
- Reescrever do zero é claramente mais barato que refatorar (código morto, descontinuado ou sem requisitos estáveis).
- O alvo é uma API publicada, formato serializado ou contrato externo sem plano de migração (expand-contract).
- Não há rede de segurança (build + testes) e o risco de tocar o código não é aceito — sem testes não se refatora com segurança.
- O alvo é hot path de produção e não há como medir desempenho antes/depois.

## Classificação: selecione o modo

Passo 1 — classifique o pedido e carregue a referência indicada. Todos os modos seguem o mesmo protocolo; muda a referência e o tamanho do passo.

| Modo | Aplicar quando | Carregar |
| --- | --- | --- |
| `refactor-local` | Um símbolo/função/arquivo, escopo pequeno, baixo risco (rename, extract local) | [safety-protocol](references/safety-protocol.md) + [equivalence-gates](references/equivalence-gates.md) |
| `refactor-scoped` | Vários arquivos, uma responsabilidade, contrato explícito de arquivos | [dependency-ordering](references/dependency-ordering.md) + [git-discipline](references/git-discipline.md) |
| `refactor-legacy` | Código antigo sem testes ou cobertura fraca | [equivalence-gates](references/equivalence-gates.md) + [protected-files](references/protected-files.md) |
| `refactor-migration` | Mover/migrar preservando API (move module, swap de biblioteca, split phase) | [dependency-ordering](references/dependency-ordering.md) + [equivalence-gates](references/equivalence-gates.md) |

## Protocolo obrigatório (todos os modos)

### Gate 0 — Baseline (antes de tocar qualquer arquivo)

1. Determine os comandos de verificação da stack em [command-catalog](references/command-catalog.md): build/typecheck, testes, lint, dead-code.
2. Confirme `git status` limpo. Rode build + testes e registre o estado **VERDE**. Nunca refatore com a barra vermelha.
3. Se houver typechecker, rode-o e guarde o resultado como **baseline**. Gates são medidos por **delta** (o que mudou com você), nunca por valor absoluto — erro pré-existente não pode ser atribuído à sua mudança.
4. Cobertura fraca na área-alvo? Não avance sem rede de segurança: caracterização ou golden master ([equivalence-gates](references/equivalence-gates.md)).

### Contrato de mudança

5. Defina o conjunto de arquivos que a mudança pode tocar. Tudo fora dele é intocável.
6. Marque como **PROTEGIDOS** arquivos gerados, infra, schemas e wrappers load-bearing na área ([protected-files](references/protected-files.md)) — não os altere sem justificativa explícita e aprovação.
7. Estime o blast radius: quem importa/chama o que será alterado ([dependency-ordering](references/dependency-ordering.md)). Arquivo com muitos importadores exige plano de decomposição antes de ser tocado.

### Loop de passo seguro

8. Aplique **uma** transformação do [refactoring-catalog](references/refactoring-catalog.md) por vez, seguindo a **mecânica** — nunca emita o diff final como plano de execução. Cada passo intermediário preserva comportamento e termina executável.
9. Verifique imediatamente: compile/typecheck + testes + gate de equivalência aplicável. Pequenas modificações e testes depois de cada modificação é a essência do processo.
10. Falhou? Desfaça o passo (reverta ao último commit bom) e refaça em passos **menores** — não insista no passo grande.
11. Commit local a cada passo verde ([git-discipline](references/git-discipline.md)). Um commit = uma mudança lógica de refatoração. **Nunca** adicione funcionalidade nem modifique testes para "passar" — testes mudam só para acomodar mudança de interface.
12. Bug descoberto no caminho? Registre, termine a refatoração e corrija em commit separado — jamais inline (anti-tangle).

### Gate final — Equivalência (antes de concluir)

13. Prove equivalência; não confie em testes verdes (cerca de 1 em 5 refactors não-equivalentes passa na suíte existente):
    - `git diff` mostra apenas arquivos do contrato (zero diff fora do contrato).
    - Rename/move puro: confirme no grafo que todos os pontos de uso foram atualizados (go-to-definition ou busca estrutural).
    - Mudança estrutural: rode golden master / fuzzing diferencial / comparação AST quando aplicável ([equivalence-gates](references/equivalence-gates.md)).
    - Gate de falsificação: escreva a linha que provaria que o comportamento mudou. Se não conseguir, o passo é grande demais.
14. Delta de typecheck: nenhum erro NOVO vs baseline. Erros pré-existentes ficam documentados, não são "consertados" na refatoração.
15. Hot path: registre baseline de benchmark antes e compare depois, ou adie a refatoração para fora do hot path.
16. Relatório final: o que foi refatorado, quantos passos, comandos executados, artefatos de equivalência gerados.

## Regras não negociáveis

- Dois chapéus: funcionalidade e refatoração nunca no mesmo passo.
- Nunca refatore com a barra vermelha.
- Comportamento observável é a lei — bugs percebidos continuam presentes (exceto latentes).
- Mecânica ≠ diff final: planeje passos intermediários verificáveis, cada um terminando verde.
- Reversão é o caminho padrão: reverta ao último commit bom e refaça menor.
- Não refatore código que não precisa ser modificado ("um código feio que funciona como API pode permanecer feio").
- A refatoração se justifica pelo argumento econômico, nunca por moral de "código limpo".

## Erros comuns a evitar (modos de falha documentados)

- Refatorar em larga escala de uma vez — mudanças irrelevantes e inconsistências crescem com o tamanho do passo.
- Renomear símbolo e perder call sites — atualize o grafo; renomeie por ferramenta determinística quando disponível.
- "Melhorar" comportamento durante a refatoração — mudar lógica é funcionalidade.
- Apagar "dead code" sem procurar usos dinâmicos (imports dinâmicos, reflection, DI containers) — já deletou arquivos críticos reais.
- Modificar a fonte da verdade (backend, `.proto`, Terraform) para fazer testes passarem.
- Remover wrapper load-bearing (auth, validação) como "limpeza".
- Usar gate por valor absoluto em vez de delta (baseline falsamente verde).
- Deixar a refatoração mais lenta no hot path sem medir.

## Referências

- [safety-protocol](references/safety-protocol.md) — definição, dois chapéus, quando/não refatorar, YAGNI, desempenho
- [equivalence-gates](references/equivalence-gates.md) — caracterização, golden master, fuzzing diferencial, delta, falsificação
- [command-catalog](references/command-catalog.md) — comandos de build/typecheck/teste/lint/dead-code por stack + limites de cada ferramenta
- [dependency-ordering](references/dependency-ordering.md) — grafo de dependências, blast radius, ordem de passos
- [git-discipline](references/git-discipline.md) — commits refactor-only, undo points, revert, anti-tangle
- [smells](references/smells.md) — 24 smells: detecção + tratamentos + quando ignorar
- [refactoring-catalog](references/refactoring-catalog.md) — 61 refatorações por categoria: motivação + mecânica segura
- [protected-files](references/protected-files.md) — gerados, infra, schemas, wrappers load-bearing, formatos serializados
- [verify-refactor.ps1](../scripts/verify-refactor.ps1) — gate determinístico de contrato de diff + verde de verificação