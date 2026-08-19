# Safety Protocol

Fundamento conceitual do skill (Fowler, Refactoring 2ª ed.). Definições, princípios e o protocolo de passo seguro.

## Definições (Fowler)

- **Refatoração (substantivo):** modificação da estrutura interna do software para torná-lo mais fácil de compreender e menos custoso de alterar, **sem alterar o comportamento observável**.
- **Refatorar (verbo):** reestruturar o software aplicando uma série de refatorações, sem alterar o comportamento observável.
- Refatoração ≠ reestruturação genérica: é a aplicação de **pequenos passos que preservam comportamento**, encadeados até produzir uma grande mudança.
- Sinal de que alguém NÃO estava refatorando: "se o código apresentou falhas durante dias enquanto 'refatorava', não era refatoração". O código nunca fica muito tempo em estado quebrado; pode-se parar a qualquer momento.
- Comportamento observável é deliberadamente flexível: o código deve fazer exatamente o mesmo; **interfaces podem mudar** (com migração de callers); características de desempenho podem mudar; **bugs percebidos continuam presentes** (exceto os latentes).

## Dois chapéus (Kent Beck)

- **Chapéu de funcionalidade:** não alterar código existente; adicionar recursos; avaliar progresso acrescentando testes e fazendo-os passar.
- **Chapéu de refatoração:** não acrescentar funcionalidades; reestruturar; **não acrescentar testes** (a menos que descubra caso novo); mudar testes somente para acomodar mudança de interface.
- Troque de chapéu frequentemente (às vezes em 10 minutos), sempre ciente de qual chapéu está usando. Nunca no mesmo commit.

## Quando refatorar

- **Regra dos Três** (Don Roberts): 1ª vez você faz; 2ª vez duplica e torce o nariz; 3ª vez refatora.
- **Preparatória (melhor momento):** logo antes de adicionar feature ou corrigir bug. "Refatore antes para tornar fácil a mudança, depois faça a fácil mudança" (Beck). Refatorar a causa de um bug aumenta a chance de o bug não voltar.
- **Para compreensão:** se você precisa pensar para entender, refatore para tornar o entendimento aparente. O insight está na mente (volátil) — **persista-o de volta no código** (Cunningham). Código mais claro facilita compreensão, gerando insights mais profundos (ciclo positivo).
- **Coleta de lixo:** código que funciona mal — mudança simples faça já; maior anote e faça depois. Regra do acampamento: deixe a base mais saudável do que encontrou, em pequenas doses.
- **Oportunista > planejada:** a maior parte da refatoração é oportunista, parte do fluxo normal. Refatoração planejada é rara (áreas negligenciadas ou esforço orquestrado).
- **Code review:** refatorar lado a lado com o autor; revisão solitária de PR "não funciona muito bem".
- **Troca de biblioteca em longo prazo:** Branch by Abstraction (migrar via abstração, nunca corte brusco).

## Quando NÃO refatorar

- Código confuso que **não precisa ser modificado** — se funciona como API, pode permanecer feio. Só refatore se precisar entender/altera-lo.
- Quando **reescrever é mais barato** — decisão de julgamento; muitas vezes só se descobre tentando um pouco.
- **Dono do código / API publicada:** renomeie mantendo a declaração antiga como passagem deprecada; prefira propriedade de equipe.
- **Branches longos:** integração frequente (trunk-based, ≥1x/dia) é compatível com refatoração; branches de semanas geram conflitos **semânticos** que o VCS não detecta.

## Problemas conhecidos

- **Percepção de atraso:** pouca refatoração é muito mais comum que refatoração demais. Justifique economicamente, nunca por moral.
- **Testes ausentes:** autotestabilidade é pré-requisito. Alternativa: refatorações automatizadas comprovadamente seguras (ex.: Extract Method por ferramenta) limitam o cardápio mas permitem atuar em bases grandes sem cobertura.
- **Legado sem testes:** refatorar sem testes é "risco necessário" — use linhas de junção (seams) para inserir testes (Feathers).
- **Bancos de dados:** cada mudança pequena + script de migração versionado; **expand-contract** (adicionar campo → atualizar leituras/escritas → remover antigo), nunca renomear/alterar coluna de uma vez.

## YAGNI vs refatoração

- Flexibilidade especulativa custa: complica o caso atual e erra o alvo se o requisito mudar.
- Estratégia: implemente somente o necessário **agora**, mas com design excelente para esse caso; adapte por refatoração quando a compreensão mudar.
- Só antecipe flexibilidade se refatorar depois for **significativamente** mais difícil.
- YAGNI não é não pensar em arquitetura — é outro estilo de incorporá-la. Refatoração é o que torna o YAGNI viável.

## Desempenho

- Ignore desempenho durante a refatoração. Se a refatoração introduzir lentidão, termine o refactoring e **otimize depois**, guiado por profiler.
- Se o alvo está no hot path: meça antes/depois (baseline de benchmark), ou adie. Otimização é guiada por profiler, nunca por especulação ("faça medições, não especule").
- Código bem fatorado é o pré-requisito para otimizar: "escreva software ajustável primeiro, depois ajuste".

## Protocolo de passo seguro (resumo operacional)

1. Pré-condição: testes robustos e verdes para a área (ou rede de segurança equivalente).
2. Uma única refatoração do catálogo por vez, seguindo a mecânica.
3. Compile/typecheck.
4. Teste imediatamente — o erro fica localizado no último passo (poucas linhas).
5. Commit local verde.
6. Falhou e não resolve rápido → restore do último bom commit → refaça em passos menores.
7. Tamanho do passo: quanto mais complicada a situação, **menores** os passos.

## Checklist de comportamento

- [ ] Nenhuma funcionalidade adicionada
- [ ] Nenhum teste modificado (exceto interface)
- [ ] Suíte verde a cada passo
- [ ] Bugs percebidos permanecem presentes
- [ ] Cada passo terminou compilável/executável
- [ ] Cada passo tem commit próprio