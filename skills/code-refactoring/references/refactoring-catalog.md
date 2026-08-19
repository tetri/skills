# Refactoring Catalog

As 61 refatorações de Fowler (2ª ed.) por categoria, no formato do catálogo: **faz (motivação) + mecânica segura**. Regra de ouro: siga a **mecânica**, não o diff final — cada passo intermediário preserva comportamento e termina verde. Nomes em inglês (canônicos), com o equivalente em português.

> **Mecânica ≠ diff final.** O diff mostra o antes/depois e apaga os estados seguros intermediários; a mecânica mostra a sequência de transformações elementares. Nunca emita o diff final como plano de execução.

## Grupo 1 — Primeiro conjunto (cap. 6)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Extract Function (Extrair função) | Cria função nomeada para um fragmento, substituindo-o pela chamada | Identifique variáveis: não-modificadas → parâmetros; modificada e usada depois → retorno (leve inicialização para dentro); **remova variáveis locais antes de extrair** (Replace Temp with Query/Inline); aninhe quando conveniente; compile-test-commit |
| Inline Function (Internalizar função) | Substitui chamada pelo corpo; remove indireção ociosa | Copie o corpo no call site; ajuste variáveis/retornos; remova a função; compile-test-commit (um caller por vez) |
| Extract Variable (Extrair variável) | Nomeia expressão complexa | Extraia a expressão; dê nome expressivo; substitua usos; compile-test-commit |
| Inline Variable (Internalizar variável) | Remove variável de nome = expressão | Substitua a variável pela expressão; remova a declaração; compile-test-commit |
| Change Function Declaration (Mudar declaração de função) | Renomeia/altera assinatura | **Dois passos**: 1) adicionar nova forma e usar no corpo; 2) remover a forma antiga (ou renomear callers via search); nunca deixe dois nomes no mesmo commit |
| Encapsulate Variable (Encapsular variável) | Protege variável global/amplamente usada | Crie getter/setter com mesmo nome (nome antigo como passagem); migre leituras→getter, escritas→setter; remova a variável; compile-test-commit |
| Rename Variable (Renomear variável) | Melhora nome de variável | Renomeie com ferramenta (IDE/LSP); verifique usos via `rg`; compile-test-commit |
| Introduce Parameter Object (Introduzir objeto de parâmetros) | Agrupa parâmetros co-ocorrentes | Extraia classe de dados; adicione objeto como parâmetro; migre callers um a um; remova parâmetros antigos |
| Combine Functions into Class (Combinar funções em classe) | Agrupa funções que compartilham estado/dados | Crie classe; mova funções (Move Function); passe dados como campos; compile-test-commit |
| Combine Functions into Transform (Combinar funções em transformação) | Agrupa em uma transformação imutável de dados | Crie função transformadora; mova lógica; trate dados como imutáveis |
| Split Phase (Separar em fases) | Divide processamento em fases com estrutura intermediária | Extraia a 2ª fase em função; crie objeto intermediário vazio; **popule campos um a um** (compile-test-commit cada); mova funções para trabalhar só com o objeto; extraia a 1ª fase |

## Grupo 2 — Encapsulamento (cap. 7)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Encapsulate Record (Encapsular registro) | Esconde estrutura de dados | Crie classe com acesso encapsulado; migre leituras/escritas; remova acesso direto |
| Encapsulate Collection (Encapsular coleção) | Protege coleção de mutação externa | Retorne cópia/somente-leitura; adicione métodos de modificação; migre callers |
| Replace Primitive with Object (Substituir primitivo por objeto) | Eleva primitivo a tipo de domínio | Crie classe; substitua usos; mova comportamento |
| Replace Temp with Query (Substituir variável temporária por consulta) | Remove temporária; calcula via função | Extraia o lado direito da atribuição em função; compile-test-commit; Inline Variable; compile-test-commit |
| Extract Class (Extrair classe) | Divide classe grande em duas | Defina as responsabilidades; crie nova classe; mova campos/funções (um por vez); relacione; compile-test-commit |
| Inline Class (Internalizar classe) | Une classe que não se sustenta | Mova campos/funções para a classe absorvente; remova a classe; compile-test-commit |
| Hide Delegate (Ocultar delegação) | Esconde o objeto delegado | Crie método no cliente que delega; migre callers; remova exposição |
| Remove Middle Man (Remover intermediário) | Elimina classe que só delega | Faça callers chamarem o delegado diretamente; remova o intermediário |
| Substitute Algorithm (Substituir algoritmo) | Troca algoritmo por outro equivalente | Prepare o algoritmo de substituição (slides/extrações); escreva o novo; compare com o antigo (fuzz/golden master); remova o antigo |

## Grupo 3 — Movendo recursos (cap. 8)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Move Function (Mover função) | Move função para o contexto certo (Feature Envy) | Copie a lógica para o destino; adapte referências; compile para checar sintaxe; transforme a original em **delegação**; compile-test-commit; Inline Function; compile-test-commit |
| Move Field (Mover campo) | Move campo para a classe que o usa mais | Declare no destino; adapte acessos; compile-test-commit (migre leituras e escritas separadamente) |
| Move Statements into Function (Mover instruções para uma função) | Move trecho do caller para dentro da função | Identifique trecho não usado pelo caller; mova; compile-test-commit |
| Move Statements to Callers (Mover instruções para os callers) | Extrai trecho que só alguns callers usam | Copie para os callers que precisam; remova da função; compile-test-commit |
| Replace Inline Code with Function Call (Substituir código internalizado por chamada) | Deduplica trecho inline | Extraia o trecho em função; substitua usos; compile-test-commit |
| Slide Statements (Deslocar instruções) | Aproxima instruções relacionadas | Verifique se o deslocamento não muda efeitos (dependências de dados/efeitos); mova; compile-test-commit |
| Split Loop (Dividir laço) | Separa responsabilidades de um laço | Copie o laço; remova a responsabilidade de cada cópia; compile-test-commit (geralmente seguido de Extract Function) |
| Replace Loop with Pipeline (Substituir laço por pipeline) | Converte laço imperativo em filter/map/reduce | Construa o pipeline equivalente; compare saídas (golden master); remova o laço |
| Remove Dead Code (Remover código morto) | Elimina código sem usos | Verifique usos (texto + dinâmicos — ver equivalence-gates); remova; compile-test-commit; nunca remova sem a verificação de usos dinâmicos |

## Grupo 4 — Organizando dados (cap. 9)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Split Variable (Separar variável) | Divide variável com múltiplos papéis | Renomeie a primeira atribuição; ajuste usos; repita por papel; compile-test-commit |
| Rename Field (Renomear campo) | Melhora nome de campo | Renomeie com ferramenta (IDE); atualize usos; compile-test-commit |
| Replace Derived Variable with Query (Substituir variável derivada por consulta) | Elimina estado derivado redundante | Extraia cálculo em função; substitua leituras; remova escritas de sincronização; compile-test-commit |
| Change Reference to Value (Mudar referência para valor) | Torna objeto imutável/valor | Torne campos imutáveis; mude comparações para igualdade por valor; compile-test-commit |
| Change Value to Reference (Mudar valor para referência) | Compartilha instância única | Crie registry/factory; garanta identidade única; atualize callers; compile-test-commit |

## Grupo 5 — Simplificando condicionais (cap. 10)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Decompose Conditional (Decompor condicional) | Extrai condição e branches em funções nomeadas | Extraia a condição; extraia cada branch; compile-test-commit |
| Consolidate Conditional Expression (Consolidar expressão condicional) | Une condicionais com mesma consequência | Verifique ausência de efeitos colaterais; combine com OR/AND; extraia se necessário |
| Replace Nested Conditional with Guard Clauses (Substituir condicional aninhada por cláusulas de guarda) | Aplana casos especiais antes do fluxo principal | Introduza cláusulas de guarda para casos excepcionais; remova aninhamento; compile-test-commit |
| Replace Conditional with Polymorphism (Substituir condicional por polimorfismo) | Troca switch/cascata por subtipos | Prepare a hierarquia (Replace Type Code with Subclasses); **mova um case por vez** para a subclasse (compile-test-commit cada); deixe "lápide" (`throw` na superclasse); remova o condicional quando vazio |
| Introduce Special Case (Introduzir caso especial) | Encapsula tratamento de caso nulo/especial | Crie subclasse/classe de caso especial; mova comportamento do `if` para ela; remova a condicional |
| Introduce Assertion (Introduzir asserção) | Documenta/valida suposição de estado | Adicione asserção no ponto de entrada/saída; compile-test-commit |

## Grupo 6 — Refatorando APIs (cap. 11)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Separate Query from Modifier (Separar consulta de modificador) | Divide função que retorna e altera | Extraia a consulta pura; faça o modificador retornar void; atualize callers; compile-test-commit |
| Parameterize Function (Parametrizar função) | Une funções que só variam em valor | Adicione parâmetro; substitua constantes por parâmetro; remova duplicações |
| Remove Flag Argument (Remover argumento de flag) | Elimina boolean/flag de assinatura | Extraia uma função por valor do flag; mova a condicional para dentro de cada; atualize callers |
| Preserve Whole Object (Preservar objeto inteiro) | Passa objeto em vez de vários campos | Adicione parâmetro objeto; ajuste corpo para usá-lo; remova campos individuais |
| Replace Parameter with Query (Substituir parâmetro por consulta) | Remove parâmetro derivável | Adicione getter/consulta; use no corpo; remova o parâmetro; atualize callers |
| Replace Query with Parameter (Substituir consulta por parâmetro) | Injeta valor em vez de consultar | Adicione parâmetro; use no corpo; remova a consulta; atualize callers |
| Remove Setting Method (Remover método de escrita) | Torna campo imutável após construção | Remova o setter; atualize inicialização; compile-test-commit |
| Replace Constructor with Factory Function (Substituir construtor por função de factory) | Substitui construção por função nomeada | Crie a factory; migre chamadas; restrinja o construtor; compile-test-commit |
| Replace Function with Command (Substituir função por comando) | Converte função complexa em objeto com método executável | Crie classe; mova função como método; mova variáveis para campos; compile-test-commit |
| Replace Command with Function (Substituir comando por função) | Inverte o acima quando o objeto não se sustenta | Extraia o método; mova campos para parâmetros; remova a classe |

## Grupo 7 — Lidando com herança (cap. 12)

| Refatoração | Faz | Mecânica segura |
| --- | --- | --- |
| Pull Up Method (Subir método) | Move método duplicado para a superclasse | Verifique identidade/diferenças; mova o corpo; ajuste referências; compile-test-commit |
| Pull Up Field (Subir campo) | Move campo para a superclasse | Declare na superclasse; remova das subclasses; compile-test-commit |
| Pull Up Constructor Body (Subir corpo do construtor) | Unifica construção | Extraia corpo comum; chame super(); compile-test-commit |
| Push Down Method (Descer método) | Move método para a subclasse certa | Movimente o método; remova da superclasse; compile-test-commit |
| Push Down Field (Descer campo) | Move campo para a subclasse certa | Movimente o campo; remova da superclasse; compile-test-commit |
| Replace Type Code with Subclasses (Substituir código de tipos por subclasses) | Transforma campo discriminador em subtipos | Crie subclasses; mova um case/branch por vez (compile-test-commit cada); remova o campo de tipo |
| Remove Subclass (Remover subclasse) | Elimina subclasse sem valor | Mova comportamento para a superclasse; remova a subclasse; compile-test-commit |
| Extract Superclass (Extrair superclasse) | Cria superclasse com comportamento comum | Identifique o comum; crie superclasse; mova campos/métodos; compile-test-commit |
| Collapse Hierarchy (Condensar hierarquia) | Une superclasse e subclasse que não se distinguem | Mova o que resta; remova uma das classes; compile-test-commit |
| Replace Subclass with Delegate (Substituir subclasse por delegação) | Troca herança por composição | Crie classe delegada; mova método como delegado; ajuste instanciação; remova a subclasse |
| Replace Superclass with Delegate (Substituir superclasse por delegação) | Troca herança pela composição do pai | Crie campo com a superclasse; substitua chamadas herdadas por delegação; remova a herança |

## Seleção da refatoração certa

1. **Diagnostique** o smell ([smells.md](smells.md)) — não escolha a refatoração pela estética.
2. **Menor refatoração primeiro**: Extract/Inline Variable e Rename antes de mover classes.
3. **Pensar nos efeitos**: mudanças de assinatura/API propagam para callers (dependency-ordering).
4. **Inversas**: conheça o par (Inline é a inversa de Extract; Remove Middle Man de Hide Delegate) — escolha pelo equilíbrio, não pelo gosto.
5. **Sequências clássicas** (da 2ª ed., usadas no cap. 1): Split Loop → Slide Statements → Extract Function → Inline Variable; Replace Temp with Query → Inline Variable; Replace Type Code with Subclasses → Replace Conditional with Polymorphism.