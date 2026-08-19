# Diff Analysis

Como ler um diff como um investigador, não como um leitor.

## Antes do diff

1. **Escopo:** determine a base (`git merge-base <base> <head>` ou `git diff <base>..<head>`).
2. **Estatística primeiro:** `git diff --stat` revela o tamanho e a distribuição. Diff pequeno em muitos arquivos = suspeito (tangled). Arquivo não esperado no stat = primeiro achado.
3. **Nome do commit:** `git log --oneline <base>..<head>` — commits mistos (feature + refactor + fix no mesmo commit) são um achado por si.

## Lendo o diff com contexto

- `git diff <base>..<head>` — o conteúdo; leia **linha de contexto** para entender o antes/depois real.
- `git blame -L <inicio>,<fim> <arquivo>` — por que o código existe. Código antigo que está sendo alterado merece mais atenção (pode ser load-bearing).
- `git log -S'<símbolo>' -- <path>` — quando um símbolo foi introduzido e por quem.
- `git show <commit> -- <arquivo>` — o que cada commit individual fez (para diffs grandes, revise por commit).

## Padrões de diff suspeitos

| Padrão | Sinal | Ação |
| --- | --- | --- |
| Out-of-scope | Mudança em arquivo não relacionado à claim do PR | Achado major/blocker se altera comportamento |
| Teste modificado junto com código | O teste passou a esperar algo diferente | Verifique se o teste testa a MESMA coisa; se mudou expectativa, comportamento mudou |
| Reformat em massa junto com lógica | Linhas reformatadas escondem mudanças reais | Separe com `git diff -w` para ver só lógica |
| Rename + edição no mesmo hunk | Renomear e mudar corpo no mesmo passo | Quebra o "invariante móvel" — exija evidência de equivalência |
| Arquivo grande de uma vez | >200 linhas em um hunk | Provável refactor grande demais; divida |
| Remoção + adição não pareadas | Wrapper/símbolo some sem equivalente novo | Caçar usos dinâmicos antes de aceitar |
| Mudança em `.proto`/schema/migration/Terraform | Formato/contrato alterado | Requer expand-contract e aprovação |

## Ferramentas de leitura

- `git diff --word-diff` — para ver mudanças finas dentro de linhas longas.
- `git diff --stat -- <path>` — confirmar o que um arquivo sofreu.
- `git diff -w --ignore-all-space` — isolar mudanças reais de formatação.
- `rg '<símbolo>'` — verificar todos os usos de um símbolo alterado.
- LSP go-to-definition/references — confirmar callers de um símbolo renomeado/movido.

## Checklist

- [ ] `git diff --stat` analisado antes do conteúdo
- [ ] Commits individuais revisados (`git log`/`git show`)
- [ ] `git blame` usado para código antigo alterado
- [ ] Arquivos fora do escopo identificados
- [ ] `git diff -w` usado para separar formatação de lógica
- [ ] Usos de símbolos renomeados verificados por busca/LSP