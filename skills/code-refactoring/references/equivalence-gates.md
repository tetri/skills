# Equivalence Gates

O diferencial central desta skill: **provar** equivalência de comportamento em vez de confiar em testes verdes. Dados empíricos (2026): 19–35% dos refactors de LLM são funcionalmente não-equivalentes e **~21% passam na suíte existente**. Testes verdes são condição necessária, não suficiente.

## Princípio do delta

- Gates por **delta**, nunca por valor absoluto. Registre a baseline ANTES (typecheck, testes, linters) e meça a diferença depois da sua mudança.
- Erro pré-existente na baseline não pode ser atribuído à sua mudança, nem "consertado" na refatoração (consertar é funcionalidade).
- "Baseline falsamente verde": suíte verde escondendo typecheck quebrado é comum; o gate absoluto acusaria sua mudança por erro que não é seu.
- Typechecker só cobre o programa que ele vê — arquivos fora do grafo compilado podem responder "phantom" (não confie no typechecker para arquivos que não estão no projeto dele).

## Rede de segurança antes de tocar código (refactor-legacy)

Se a área-alvo tem cobertura fraca, crie rede de segurança ANTES de refatorar. Prioridade:

1. **Caracterização (Feathers):** testes que capturam o comportamento atual sem assumir o que "deveria ser". Passos:
   - Encontre as linhas de junção (seams) para exercitar o código.
   - Escreva teste com valor esperado placeholder.
   - Substitua pelo valor real produzido pelo código.
   - **Injete uma falha** (ex.: `* 2`) e confirme que o teste falha — todo teste deve falhar quando deve falhar.
   - Remova a falha; o teste fica verde como rede de segurança.
2. **Golden master:** capture outputs reais (console, arquivos, estado, logs) para entradas representativas e guarde como ground truth. "1 byte de diferença = rejeita". Execute antes e depois de cada passo.
   - Inclua casos de borda: coleção vazia, zero, negativos, string vazia, nulo.
3. **Fuzzing diferencial:** gere entradas (aleatórias ou por propriedade) e compare saídas da versão antiga vs nova. Mais forte que snapshot para lógica densa.

## Gates mecânicos por tipo de mudança

| Mudança | Gate principal | Gate complementar |
| --- | --- | --- |
| Rename de símbolo | Grafo de usos atualizado (go-to-definition em todos os callers) | Renomear por ferramenta (IDE, ast-grep, jscodeshift, rope) quando possível |
| Move (função/módulo) | Todos os callers apontam para o novo local | `git log -S` para achar usos históricos; busca por imports/requires |
| Extract (função/método) | Diff da chamada + testes | Comparação estrutural (AST) da lógica extraída |
| Inline | Diff do call site + testes | Falsificação: nenhum comportamento novo |
| Troca de algoritmo | Fuzzing diferencial / golden master | Caracterização prévia |
| Divisão de fase | Golden master das saídas das fases | Imutabilidade dos dados intermediários |
| Substituir condicional por polimorfismo | Executar todos os branches/tipos | Caracterização por caso |

## Gate de falsificação

Para cada passo, escreva a **linha de teste (ou condição) que provaria que o comportamento mudou**. Se não conseguir escrevê-la, o passo é grande demais — divida.

Exemplo: ao extrair uma função, a linha de falsificação é um teste que compara a chamada antiga vs nova com os mesmos argumentos e espera resultados idênticos.

## Zero diff fora do contrato

- `git diff --name-only` deve listar apenas os arquivos do contrato (definidos no passo 5 do SKILL.md).
- Arquivo fora do contrato alterado → reverta (`git checkout --`) imediatamente.
- Verifique também imports órfãos, declarações stale e exports mortos após o passo (limpeza pós-refactor é parte da equivalência, não decoração).

## Limites de cada gate (o que ele NÃO cobre)

| Ferramenta | Cobre | NÃO cobre |
| --- | --- | --- |
| Testes de unidade | Comportamento exercitado | Comportamento não testado; desempenho; integração real |
| Typechecker | Contratos de tipo | Lógica; arquivos fora do programa; comportamento em runtime |
| Linter | Higiene estática | Equivalência; desempenho |
| Dead-code estático | Símbolos sem referência léxica | Imports dinâmicos, reflection, DI, carregamento por string |
| Golden master | Saídas capturadas | Caminhos não capturados; ordem não determinística |
| Fuzzing diferencial | Entradas geradas | Casos que o gerador não alcança |
| Benchmarks | Desempenho do caminho medido | Plataformas/ambientes não medidos |

## Hot path e desempenho

- Se o alvo está no hot path: registre benchmark baseline antes (profiler, script de timing) e compare depois. CI normalmente não mede "slower" — refactor correto pode ficar 2× mais lento (guard clause derrotando cache, dataclass quebrando fast path).
- Refatorações que mudam estrutura de dados, iteração, cache ou locks exigem verificação de desempenho obrigatória.

## Dead-code: protocolo de exclusão

Nunca remova símbolo como "dead code" sem:
1. Busca textual completa (nome + nomes derivados: `Foo`, `foo`, `fooFactory`).
2. Busca por usos dinâmicos: imports dinâmicos, `require(variable)`, `__import__`, reflection (`getattr`, `eval`, DI containers, registros de plugins, glob de arquivos).
3. Confirmação de que nenhum arquivo gerado ou manifest (`.proto`, migrations, IaC) referencia o símbolo.
4. Remoção em commit próprio; se houver dúvida, mantenha com comentário de justificativa.