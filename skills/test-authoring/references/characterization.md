# Characterization Tests

Testes de caracterização (Michael Feathers) capturam o comportamento **atual** de código existente, sem presumir o que "deveria ser". São a rede de segurança de refatoração para código legado sem cobertura.

## Quando usar

- Código antigo/sem testes que será refatorado.
- Comportamento é desconhecido ou não documentado — o teste registra o que o código faz, não o que ele deveria fazer.
- Antes de qualquer mudança estrutural em área sem segurança.

## Passos

1. **Encontre os seams:** o ponto onde o código pode ser exercitado — função pura, método público, entrada/saída de CLI. Para código sem seam, crie um em passo separado (ex.: extrair a lógica pura de uma função com efeitos) — refatoração mínima e justificada, em commit próprio.
2. **Exercite com inputs representativos:** valores do mundo real + bordas (vazio, zero, negativo, nulo, string vazia).
3. **Escreva o teste com placeholder:** `Assert.That(statement(invoice), Is.EqualTo("???"))`.
4. **Rode e capture o valor real** produzido pelo código; substitua o placeholder.
5. **Injete uma falha:** mude o código (`* 2`, operador invertido) e confirme que o teste falha. Isso prova que o teste está amarrado ao comportamento, não ao acaso.
6. **Remova a falha.** O teste fica verde como rede de segurança.

## Regras

- O teste documenta o comportamento ATUAL. Se o comportamento parece "errado", registre a suspeita como achado, mas o teste preserva o atual — a correção é decisão de produto, não do teste.
- Não "melhore" o código enquanto escreve caracterização — escreva os testes, depois refatore (dois chapéus).
- Para você se enganar nos dois (código e teste) teria que errar do mesmo jeito em ambos — por isso a injetada de falha é obrigatória.

## Estrutura típica

- Um teste por cenário de entrada (não empilhe todos os casos em um teste).
- Nomeie pelo comportamento: `devolve_Total_Gravado_com_Play_Normal` — descreva a saída, não a intenção.
- Se o código não é determinístico (tempo, random, I/O), normalize ou use os mesmos valores capturados (ver golden-master).

## Limites

- Cobre o que os inputs representativos exercitam — caminhos não exercitados continuam descobertos.
- Código com efeitos colaterais externos (DB, rede) exige injeção/fake do seam, o que pode ser uma mini-refatoração — faça antes, em commit separado.
- Não detecta mudança de comportamento em caminhos que nenhum teste exercita.

## Checklist

- [ ] Seams identificados/criados em commit separado
- [ ] Inputs representativos + bordas
- [ ] Placeholder substituído por valor real
- [ ] Falha injetada → teste falhou → falha removida
- [ ] Testes verdes e rápidos