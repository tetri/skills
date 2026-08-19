# Code Smells

Os 24 "maus cheiros" (Fowler 2ª ed. + refactoring.guru). Formato: **detecção → tratamentos → quando ignorar**. Use para diagnosticar; o tratamento sempre passa por uma refatoração do [refactoring-catalog](refactoring-catalog.md) com a mecânica segura. O campo "quando ignorar" é o freio anti-super-refatoração.

## 1. Nome misterioso (Mysterious Name)

- **Detecção:** nomes que não comunicam o quê/porquê; você quebra a cabeça para entender.
- **Tratamento:** Change Function Declaration, Rename Variable, Rename Field. Não achar um bom nome é sinal de problema mais profundo.
- **Quando ignorar:** nunca — nomes são a matéria-prima da clareza.

## 2. Código duplicado (Duplicated Code)

- **Detecção:** mesma estrutura em 2+ lugares; cada mudança exige atualizar todas as cópias.
- **Tratamento:** Extract Function; Slide Statements antes (para aproximar fragmentos); Pull Up Method (subclasses).
- **Quando ignorar:** casos raros em que fundir tornaria o código menos intuitivo.

## 3. Função longa (Long Function)

- **Detecção:** funções grandes; a sensação de "preciso comentar" indica onde extrair.
- **Tratamento:** Extract Function; Replace Temp with Query / Introduce Parameter Object / Preserve Whole Object (se temporárias/parâmetros atrapalham); Replace Function with Command (casos pesados); Decompose Conditional; Replace Conditional with Polymorphism; Split Loop.
- **Quando ignorar:** loops com efeitos desprezíveis não exigem split imediato.

## 4. Lista longa de parâmetros (Long Parameter List)

- **Detecção:** assinaturas confusas, muitos parâmetros.
- **Tratamento:** Replace Parameter with Query; Preserve Whole Object; Introduce Parameter Object; Remove Flag Argument (flags); Combine Functions into Class (valores compartilhados).
- **Quando ignorar:** API pública estável onde mudar a assinatura é mais caro que o ganho.

## 5. Dados globais (Global Data)

- **Detecção:** estado modificável em qualquer ponto da base (inclui variáveis de classe e singletons).
- **Tratamento:** Encapsulate Variable como primeiro passo; limitar escopo movendo para classe/módulo.
- **Quando ignorar:** pequenas doses controladas; cresce exponencialmente em risco.

## 6. Dados mutáveis (Mutable Data)

- **Detecção:** atualizações com consequências inesperadas; dados derivados mantidos à mão.
- **Tratamento:** Encapsulate Variable; Split Variable; Slide Statements + Extract Function (separar efeitos); Separate Query from Modifier; Remove Setting Method; Replace Derived Variable with Query; Combine Functions into Class/Transform; Change Reference to Value.
- **Quando ignorar:** performance legítima (memoização) pode exigir estado mutável — documente.

## 7. Alteração divergente (Divergent Change)

- **Detecção:** o mesmo módulo muda por motivos diferentes (novo banco muda 3 funções; novo instrumento muda outras 4).
- **Tratamento:** Split Phase; Move Function; Extract Function antes de mover; Extract Class.
- **Quando ignorar:** módulos pequenos onde a divisão fragmenta sem ganho.

## 8. Cirurgia com rifle (Shotgun Surgery)

- **Detecção:** uma mudança exige pequenas alterações em várias classes.
- **Tratamento:** Move Function/Field; Combine Functions into Class/Transform; Split Phase; Inline Class (reunir primeiro, extrair depois).
- **Quando ignorar:** nunca — é o odor inverso do anterior e sinal de acoplamento espalhado.

## 9. Inveja de recursos (Feature Envy)

- **Detecção:** função fala mais com dados de outra classe que com a própria (meia dúzia de getters).
- **Tratamento:** Move Function (coloque a função com os dados); Extract Function da parte invejosa e mova.
- **Quando ignorar:** estratégias conscientes (Strategy, Visitor, Self Delegation).

## 10. Agrupamentos de dados (Data Clumps)

- **Detecção:** os mesmos 3–4 dados andando juntos (campos, parâmetros). Teste: apague um deles — os demais fazem sentido?
- **Tratamento:** Extract Class (campos); Introduce Parameter Object / Preserve Whole Object (assinaturas); depois cace Feature Envy para povoar a classe.
- **Quando ignorar:** raro; o clump é a pista de um conceito de domínio faltando.

## 11. Obsessão por primitivos (Primitive Obsession)

- **Detecção:** int/string para conceitos de domínio (moeda, telefone, CPF — "stringly typed").
- **Tratamento:** Replace Primitive with Object; Replace Type Code with Subclasses + Replace Conditional with Polymorphism; Extract Class / Introduce Parameter Object (grupos).
- **Quando ignorar:** primitivos para valores sem comportamento próprio são aceitáveis.

## 12. Switches repetidos (Repeated Switches)

- **Detecção:** a mesma condicional switch/cascata if/else em lugares diferentes.
- **Tratamento:** Replace Conditional with Polymorphism (após Replace Type Code with Subclasses/State).
- **Quando ignorar:** a condicional é simples e os casos não crescem.

## 13. Laços (Loops)

- **Detecção:** loops imperativos onde pipelines (filter/map/reduce) mostram melhor o processamento.
- **Tratamento:** Replace Loop with Pipeline.
- **Quando ignorar:** loops com efeitos colaterais múltiplos ou performance de hot path.

## 14. Elemento ocioso (Lazy Element)

- **Detecção:** função/classe que não agrega estrutura (nome = corpo; classe de uma função; "ia crescer e não cresceu").
- **Tratamento:** Inline Function; Inline Class; Collapse Hierarchy (herança).
- **Quando ignorar:** indireção que ainda comunica intenção (nomes expressivos).

## 15. Generalidade especulativa (Speculative Generality)

- **Detecção:** hooks, parâmetros e casos especiais para "um dia precisaremos"; os únicos usuários são os testes.
- **Tratamento:** Collapse Hierarchy; Inline Function/Class; Change Function Declaration (remover parâmetros não usados); Remove Dead Code.
- **Quando ignorar:** extensões planejadas com requisito conhecido — mas não especule.

## 16. Campo temporário (Temporary Field)

- **Detecção:** campo definido só em certas circunstâncias; objeto "incompleto".
- **Tratamento:** Extract Class (lar das órfãs); Move Function para a nova classe; Introduce Special Case (estado inválido).
- **Quando ignorar:** raro; é sinal de objeto parcial.

## 17. Cadeias de mensagens (Message Chains)

- **Detecção:** cliente navega por `getThis().getThat().getOther()`.
- **Tratamento:** Hide Delegate (cuidado: cada intermediário vira Middle Man); melhor: Extract Function + Move Function para dentro da cadeia.
- **Quando ignorar:** navegação que é o próprio domínio (ex.: APIs de dados).

## 18. Intermediário (Middle Man)

- **Detecção:** metade dos métodos da classe só delega.
- **Tratamento:** Remove Middle Man; Inline Function (métodos triviais); Replace Superclass/Subclass with Delegate.
- **Quando ignorar:** delegar esconde acoplamento legítimo (Hide Delegate é o equilíbrio).

## 19. Trocas escusas (Insider Trading)

- **Detecção:** módulos cochicham demais; subclasses sabem demais do pai.
- **Tratamento:** Move Function/Field; criar 3º módulo para interesses comuns; Hide Delegate; Replace Subclass/Superclass with Delegate.
- **Quando ignorar:** nunca — é acoplamento excessivo.

## 20. Classe grande (Large Class)

- **Detecção:** campos demais; prefixos/sufixos comuns sugerem componentes; clientes que usam subconjuntos.
- **Tratamento:** Extract Class; Extract Superclass; Replace Type Code with Subclasses.
- **Quando ignorar:** classes de dados imutáveis grandes (registros) podem ser legítimas.

## 21. Classes alternativas com interfaces diferentes (Alternative Classes with Different Interfaces)

- **Detecção:** classes intercambiáveis que não têm protocolos iguais.
- **Tratamento:** Change Function Declaration (igualar); Move Function (até os protocolos coincidirem); Extract Superclass (se duplicar).
- **Quando ignorar:** integrações externas que não compensa unificar.

## 22. Classe de dados (Data Class)

- **Detecção:** campos + getters/setters e nada mais; comportamento no lugar errado. Exceção nobre: registro de resultado **imutável** (ex.: estrutura intermediária do Split Phase).
- **Tratamento:** Encapsulate Record (campos públicos); Remove Setting Method; Move Function para dentro; Extract Function quando não der para mover tudo.
- **Quando ignorar:** DTOs/registros imutáveis de fronteira são aceitáveis e comuns.

## 23. Herança recusada (Refused Bequest)

- **Detecção:** subclasse ignora parte do que herdou. Recusar implementação é ok; recusar interface é problema. "Nove de cada dez vezes não vale a pena eliminar."
- **Tratamento:** Push Down Method/Field (para classe irmã); Replace Subclass/Superclass with Delegate (se recusa interface).
- **Quando ignorar:** na maioria dos casos, o odor é sutil e não vale o custo.

## 24. Comentários (Comments)

- **Detecção:** comentários explicando "o que" em vez de "porquê" — são desodorantes de código ruim.
- **Tratamento:** Extract Function (comentário explica um bloco); Change Function Declaration (renomear); Introduce Assertion (regras de estado). Comentários bons explicam o *porquê* e sinalizam incerteza.
- **Quando ignorar:** comentários de contexto histórico, decisões e avisos de risco são bem-vindos.

## Priorização prática

1. Odores de acoplamento (7, 8, 19) e dados (5, 6) → mais caros de corrigir depois.
2. Duplicação (2) e nomes (1) → maior ROI imediato.
3. Especulação (15) e ociosos (14) → remova apenas na área que já está no contrato.
4. Nunca refatore smell fora da área-alvo do pedido, a menos que seja o pedido.