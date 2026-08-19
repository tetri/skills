# Gap Analysis

Como transformar pesquisa em uma skill com **diferencial substantivo** — o oposto de "mais uma lista do mesmo".

## O que é diferencial substantivo

Não é estilo nem volume. É: **uma capacidade que as skills existentes não oferecem e que os dados empíricos do domínio mostram ser necessária**. Três testes:

1. **Teste da lacuna:** "as skills existentes fazem X? Não? Então X é candidato." Se todas fazem X, X é baseline, não diferencial.
2. **Teste da necessidade:** "os dados do domínio (pesquisa, postmortems, falhas documentadas) mostram que X é necessário?" Ex.: 21% dos refactors não-equivalentes passam na suíte → "gates mecânicos de equivalência" é necessário.
3. **Teste da executabilidade:** "X pode ser um procedimento verificável na skill?" (passos, comandos, gates). Se é só intenção ("seja cuidadoso"), não é um gate.

## Padrão típico das skills genéricas (o que evitar)

- Lista do inventário do domínio (smells, padrões, técnicas) sem protocolo.
- Instrução vaga: "refatore passo a passo", "rode os testes", "seja consistente".
- Fase de análise + fase de aplicação sem gates entre elas.
- Checklist moral sem verificação mecânica.

## Onde procurar o gap

| Fonte | O que revela |
| --- | --- |
| Dados empíricos (papers, postmortems) | O que realmente falha na prática (ex.: dead-code removido errado, teste adulterado, rename perdendo callers) |
| Limites das ferramentas | O que a ferramenta-padrão NÃO cobre (ex.: typechecker não vê arquivos fora do programa) |
| Skills existentes | O que todas ignoram em comum |
| O próprio domínio | Regras de exceção que ninguém formaliza (ex.: "quando ignorar o smell") |

## Formato do entregável de gap

```
DOMÍNIO: code-refactoring
GAP: gates mecânicos de equivalência
EVIDÊNCIA: 21% dos refactors não-equivalentes passam na suíte (fuzz diferencial, 2026)
EXISTENTES: 14 skills mapeadas — nenhuma combina caracterização obrigatória + grafo + delta + reversão
DIFERENCIAL: protocolo com gates (caracterização, golden master, typecheck por delta, falsificação, contrato de diff, git reversível)
```

## Anti-padrões do processo

- Escolher o diferencial por "gosto" ou tendência (ex.: "vamos focar em padrões de design") sem evidência de lacuna.
- Diferenciar pela quantidade de conteúdo (a skill mais longa não é a melhor).
- Ignorar o "quando NÃO usar" (o freio é parte do diferencial de qualidade).
- Criar skill sem script determinístico quando o domínio permite um gate executável (scripts são diferenciais raros e valiosos).

## Checklist

- [ ] Gap declarado em uma frase
- [ ] Evidência empírica citada
- [ ] Confirmado que skills existentes não cobrem
- [ ] Gap é traduzível em passos/gates verificáveis
- [ ] "Quando não usar" definido como contrapeso do diferencial