# Severity and Report

Classificação e formato de saída da revisão. O relatório é o entregável: **conclusões com evidência**, pronto para o autor agir.

## Escala de severidade

| Severidade | Definição | Exemplo |
| --- | --- | --- |
| `blocker` | Impede merge: mudança de comportamento não intencional, quebra de build/teste introduzida, bug real, teste adulterado, arquivo protegido alterado | Lógica mudada em "refactor"; wrapper de auth removido; expectativa de teste alterada |
| `major` | Funciona mas errado em caminhos/condições: edge case não tratado, segurança enfraquecida, out-of-scope, commit tangled | Condição nova não coberta; mudança em arquivo fora do escopo |
| `minor` | Melhorável sem mudar o resultado: nome confuso, duplicação pequena, estilo inconsistente, claim sem evidência | Nome que não comunica; comentário stale |
| `nit` | Cosméticos: formatação, typos, sugestão de estilo | Espaço em branco |

## Anatomia de um achado

```
[BLOCKER] test-helper.ts:42 — teste adulterado
  Antes: expect(result).toEqual([1,2,3])
  Depois: expect(result).toEqual([1,2,2])
  Evidência: git diff -- test-helper.ts (linhas 40-45)
  Impacto: o teste passa a aceitar o comportamento novo; o caminho antigo deixou de ser validado
  Correção: restaurar a expectativa ou, se a mudança de comportamento é intencional, mover para commit de feature
```

## Formato do relatório

### Cabeçalho
- Escopo revisado (base..head, arquivos).
- Comandos executados (baseline e delta) com resultado.
- Claims da mudança declaradas pelo autor.

### Achados
- Lista ordenada por severidade (blocker → nit).
- Cada um com: localização `arquivo:linha`, evidência, impacto, correção.

### Verdict
- `Aprovado` — nenhum blocker, gates executados, linha de falsificação vazia.
- `Aprovado com ressalvas` — majors/minors que não impedem merge mas devem ser tratados em follow-up.
- `Reprovado` — 1+ blocker.

### Não verificados
- Seção explícita: claims que não puderam ser verificadas e por quê.

## Regras do relatório

1. **Evidência > opinião:** toda conclusão cita comando+saída ou linha de diff. "Ficou mais limpo" não é achado; "renomeou `x` para `y` sem atualizar 3 callers" é.
2. **Nenhuma correção inline:** reporte, não conserte. O autor corrige; o revisor reverifica.
3. **Delta declarado:** erros pré-existentes listados separadamente como "baseline", não como achados da mudança.
4. **Revisão de refatoração:** inclua a linha de falsificação (o teste que provaria mudança de comportamento). Se foi possível escrevê-la, o diff falhou no gate.
5. **Tamanho:** blockers/majors com profundidade; nits agrupados em um bloco, sem parágrafo individual.

## Checklist de relatório

- [ ] Escopo e base definidos
- [ ] Comandos de baseline e delta executados e citados
- [ ] Achados com `arquivo:linha` + evidência + impacto + correção
- [ ] Severidade aplicada
- [ ] Verdict claro (Aprovado / Ressalvas / Reprovado)
- [ ] Seção "não verificado" preenchida honestamente