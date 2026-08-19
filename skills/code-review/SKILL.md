---
name: code-review
description: Revisa código com rigor adversarial e evidências mecânicas, caçando mudanças de comportamento mascaradas, violações de contrato, riscos de segurança e commits tangled em diffs e pull requests. Use quando o usuário pedir revisão de código, PR, MR, diff, ou validação de uma mudança feita por IA ou humano.
license: MIT
compatibility: Windows/PowerShell, git; agnóstica de linguagem
metadata:
  categoria: engenharia-de-software
  status: publicado
---

# Code Review

Revisão é um processo de **descoberta de defeitos com evidência**, não de aprovação por leitura. O revisor é um **advogado do diabo**: o objetivo é provar que a mudança está errada — e, se não conseguir, o código está aprovado. Toda opinião deve ser acompanhada de evidência mecânica (comando executado, diff, teste rodado).

## Quando usar

- O usuário pede revisão de um PR/MR, diff, commit ou mudança recente.
- Validação de mudança gerada por IA (a revisão é o gate de segurança de código produzido por agente).
- Revisão de refatoração: confirmar que comportamento foi preservado ([comportamento](references/behavior-detection.md)).
- Preparação para merge: caçar tangled commits, arquivos fora do contrato, testes adulterados.

## Quando NÃO usar

- O usuário quer você para implementar/alterar código (isso é outra skill).
- Revisão de arquitetura ampla sem diff específico (use a skill de arquitetura quando existir).
- Code review de "estilo" puro sem escopo definido — defina o diff antes.

## Modos de revisão

| Modo | Aplicar quando | Ênfase |
| --- | --- | --- |
| `review-refactor` | A mudança se apresenta como refatoração | Comportamento preservado? (behavior-detection) |
| `review-ai` | Mudança gerada por IA (session/repo) | Hallucination, renames inconsistentes, shims, dead-code errado |
| `review-standard` | Feature/fix comum | Correção, segurança, testes, contrato |

## Protocolo de revisão

### Gate 0 — Contexto e baseline

1. Identifique o escopo: base vs branch (`git merge-base`), ou o diff exato (`git diff <base>..<head>`).
2. Registre a baseline de verificação da stack ([evidence-gates](references/evidence-gates.md)): build/typecheck/testes. Review com suíte quebrada = a mudança em revisão é suspeita, mas erros pré-existentes são **delta**, não atribuição.
3. Liste os arquivos fora do contrato natural da mudança (o que a mudança diz que faz vs o que toca).

### Gate 1 — Leitura adversarial do diff

4. Leia o diff **com contexto**: `git diff`, `git blame -L` para saber por que o código existe, `git log -S'<símbolo>'` para mudanças históricas ([diff-analysis](references/diff-analysis.md)).
5. Para cada arquivo, pergunte: a mudança faz só o que diz? Há alteração em arquivo não relacionado (out-of-scope)?
6. Para cada símbolo renomeado/movido: **todos** os callers foram atualizados? (use LSP references / busca estrutural — um caller perdido quebra o build ou, pior, silenciosamente).
7. Caça ativa de comportamento mascarado ([behavior-detection](references/behavior-detection.md)): lógica alterada sob pretexto de "limpeza", wrapper load-bearing removido, formato serializado mudado, valor mágico alterado.

### Gate 2 — Verificação mecânica das claims

8. Para cada claim da mudança ("isto é equivalente", "isto é dead code", "isto é não-load-bearing"), execute a verificação correspondente em [evidence-gates](references/evidence-gates.md). Claim sem verificação executada = claim não aprovada.
9. Rode build/typecheck/testes e compare com baseline (delta). Teste que foi **modificado** na mudança é um red flag prioritário — o autor pode estar ajustando a fonte de verdade.
10. Rode a suíte na área tocada; se a mudança alega equivalência, exija o artefato (caracterização/golden master/fuzz) ou rode-o você.

### Gate 3 — Verdict por mudança

11. Classifique cada achado por severidade ([severity-and-report](references/severity-and-report.md)): `blocker` (impede merge), `major`, `minor`, `nit`.
12. Cada achado leva: localização (arquivo:linha), evidência (comando/linha de diff), impacto (o que quebra), sugestão de correção.
13. Aprovação final só quando: nenhum blocker, evidências executadas, e a resposta à "o que este diff pode quebrar silenciosamente?" é vazia.

## Regras não negociáveis

- Opinião sem evidência não conta. Toda afirmação = comando + saída ou linha de diff.
- Gates por delta: erro pré-existente não é culpa da mudança; erro novo é.
- Red flags automáticos: teste modificado, arquivo fora do escopo, commit misto (feature+refactor), remoção de wrapper/validação, mudança em schema/infra sem migração.
- Nunca "conserte" o código durante a revisão — reporte.
- Revisão de refatoração: o revisor deve tentar escrever a linha de falsificação (provar mudança de comportamento). Se não conseguir, aprova.

## Erros comuns a evitar

- Aprovar pela leitura fluida ("it reads correctly") — erros de renaming e imports órfãos só aparecem com verificação mecânica.
- Não olhar o diff fora do `git diff --stat` (mudanças em arquivos que você não esperava).
- Aceitar "as mudanças de teste são para acomodar a interface" sem verificar que o teste continua testando a MESMA coisa.
- Tratar todo código aparentemente morto como removível — imports dinâmicos, reflection e DI escondem usos reais.

## Referências

- [diff-analysis](references/diff-analysis.md) — como ler o diff com contexto (base, blame, log -S, out-of-scope)
- [behavior-detection](references/behavior-detection.md) — caça a mudanças de comportamento mascaradas
- [evidence-gates](references/evidence-gates.md) — verificação mecânica de claims por stack + delta
- [severity-and-report](references/severity-and-report.md) — classificação de severidade e formato do relatório