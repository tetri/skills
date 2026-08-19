# Git Discipline

A refatoração vive e morre na disciplina git: **undo points por commit**, commits **refactor-only**, reversão como caminho padrão. O git é a rede de segurança operacional da skill.

## Commits refactor-only

- Um commit = uma mudança lógica de refatoração. Nunca misture refatoração com feature/fix/cleanup (tangled refactoring é uma das maiores causas de falha medida em agentes).
- Padrão de mensagem: `refactor: <o que> (<refatoração do catálogo>)`
  - Ex.: `refactor: extrai cálculo de volume (Split Phase)`, `refactor: renomeia Play para Performance (Rename Variable)`.
- Se um bug for descoberto durante a refatoração: registre-o, continue, e corrija em commit separado (`fix:`), jamais inline no commit de refatoração.

## Undo points

- Commit local **a cada passo verde**. Isso torna a reversão trivial e o erro localizável no último passo.
- Protocolo de falha: `git revert <commit>` (ou `git checkout -- <file>` para o passo em andamento) → retorne ao último bom estado → refaça em passos menores.
- Antes de cada sessão: `git status --porcelain` limpo. Árvore suja = baseline incerto.

## Contrato de diff

- `git diff --name-only` deve listar apenas arquivos do contrato (definido no passo 5 do SKILL.md).
- Fora do contrato: `git checkout -- <arquivo>` imediatamente.
- `git diff --stat` deve ser proporcional ao passo — diff grande = passo grande demais.

## Git blame e histórico

- `git blame -L <range> <file>` para entender por que o código existe (evita remover código load-bearing sem saber).
- `git log -S'<símbolo>' -- <path>` para achar usos históricos e commits que introduziram o símbolo.
- `.git-blame-ignore-revs` para commits de refatoração mecânica (rename/format) que poluem o blame. Configure `blame.ignoreRevsFile`.

## Integração contínua (trunk-based)

- Branches longos geram conflitos **semânticos** que o VCS não detecta. Integre ≥1x/dia.
- Refatoração em feature branch longo = risco dobrado. Prefira refatorar na linha principal e rebase frequente.
- Para mudanças grandes em paralelo: worktrees + Branch by Abstraction (nunca corte brusco).

## Anti-tangle

- Nunca altere comportamento E estrutura no mesmo passo ("invariante móvel": nunca mude lógica e localização ao mesmo tempo).
- Sequência para mover código: Introduce → Redirect → Remove, com testes verdes em cada sub-passo:
  1. Introduza a nova versão (cópia) no destino.
  2. Redirecione callers um a um para o destino.
  3. Remova a versão antiga apenas quando zero callers restarem.
- Expansão-contração para estado persistente (DB, serialização): adicionar → dupla escrita → migrar leituras → remover. Nunca alterar o formato em um passo.

## Reversão como padrão

- Erro → reverta primeiro, discuta depois. Não "corrija em cima" do passo quebrado.
- Cada commit verde é um checkpoint seguro; nenhum trabalho se perde.
- Regra: se o passo não ficou verde após 2 tentativas, o problema é o tamanho do passo, não a sorte — divida.

## Checklist

- [ ] `git status --porcelain` limpo antes de começar
- [ ] Baseline verde registrada (build + testes)
- [ ] Um commit por passo verde, mensagem `refactor:`
- [ ] Zero diff fora do contrato
- [ ] Nenhuma mistura de funcionalidade/fix nos commits de refatoração
- [ ] `.git-blame-ignore-revs` atualizado para renames mecânicos