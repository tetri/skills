# Behavior Detection

O coração da revisão de refatoração: **caçar mudanças de comportamento que se disfarçam de "limpeza"**, "simplificação", "dead code" ou "refactor". Dados empíricos: ~21% dos refactors de IA são não-equivalentes e passam na suíte; 13,7% adicionam funcionalidade disfarçada.

## As mudanças mascaradas mais comuns

| Máscara | O que esconde | Como detectar |
| --- | --- | --- |
| "Limpeza" | Wrapper load-bearing removido (`withAuth`, validação, logging) | `git blame` do wrapper; busque usos; pergunte "o que este wrapper protege?" |
| "Simplificação" | Lógica alterada (operador, ordem, default, `else` removido) | Compare antes/depois com `git diff -w`; isole os hunks de lógica |
| "Dead code removido" | Símbolo com usos dinâmicos (imports dinâmicos, reflection, DI, strings) | Busca textual + usos dinâmicos + manifests (`.proto`, IaC, migrations) |
| "Teste ajustado para interface" | Teste passou a aceitar comportamento diferente | Verifique se o teste testa a MESMA asserção; compare expectativa antiga vs nova |
| "Melhoria" | Bug consertado ou comportamento novo embutido no "refactor" | Busque branches/condições novas no diff; delta de lógica |
| "Reorganização" | Valores mágicos, constantes, tolerâncias alterados | Diff de literais; compare constantes antes/depois |
| "Migração" | Formato serializado/contrato alterado sem expand-contract | Diff em schema/API/DB; exija migração versionada |

## Sinal de comportamento (o teste da mudança)

Para cada hunk que toca lógica, responda:

1. **O que este código fazia?** (antes)
2. **O que faz agora?** (depois)
3. **A diferença é estrutural (renome, move, extração) ou comportamental (lógica)?**

Se a diferença é comportamental e a mudança se apresenta como refatoração → achado `blocker` (não é refatoração).

## Red flags de teste adulterado

- Teste modificado na mesma mudança que o código e a expectativa mudou.
- Teste que passou a usar valores diferentes (fake mais "permissivo").
- Teste deletado na mudança.
- Asserções removidas ou enfraquecidas (`toEqual` → `toBeTruthy`, `expect(...)` removida).
- Fixture que "simplificou" demais a ponto de não exercitar o caminho.

**Regra:** o teste que muda para acomodar mudança de **interface** é legítimo (e o teste continua validando o mesmo comportamento); o teste que muda para acomodar mudança de **comportamento** é admissão de mudança de comportamento.

## Ataque de falsificação

Para um diff de refatoração, o revisor deve escrever (ou exigir) a **linha que provaria mudança de comportamento**:

> "O teste/caminho que falharia se a semântica tivesse mudado é: `f(x) == f'(x)` para entradas `[...]`."

Se nenhuma linha de falsificação for possível, a mudança é ou trivial ou grande demais — peça mais evidência.

## Verificações para "é mesmo dead code?"

1. `rg '<nome>' <repo>` (nome + derivados: `Foo`, `foo`, `fooFactory`, `#foo`).
2. Usos dinâmicos: `import(variable)`, `require(variable)`, `__import__`, `eval`, `getattr`, DI containers, plugins, glob de arquivos, convenção de nomes de framework.
3. Manifests: `.proto`, migrations, IaC, index/barrel exports, config XML/JSON de DI.
4. Se há dúvida: **não** é dead code. Veredito: "manter, com justificativa" em vez de "remover".

## Checklist final de comportamento

- [ ] Nenhum hunk de lógica alterado sob pretexto de limpeza
- [ ] Nenhum valor mágico/constante/tolerância mudado
- [ ] Nenhum wrapper/validação removido sem prova de não-load-bearing
- [ ] Nenhum teste adulterado (expectativa mantida)
- [ ] Nenhum arquivo fora do escopo alterado
- [ ] Linha de falsificação escrita ou exigida para refactors