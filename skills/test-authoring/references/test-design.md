# Test Design

Princípios de design de testes: orientação a risco, caminhos de borda, higiene de fixture e asserção única. Base: Fowler (Refactoring cap. 4).

## Orientação a risco, não a cobertura

- Testes são para **encontrar bugs**. Priorize onde o código é complexo e onde um erro seria caro (regras de negócio, cálculos, integrações, fronteiras de dados).
- Não teste getters/setters triviais ("tão simples que é pouco provável que eu encontre bugs ali").
- "É melhor escrever e executar testes incompletos do que não executar testes completos" — teste demais desanima e leva a teste de menos.
- Cobertura só identifica áreas NÃO testadas, não qualidade. A métrica certa: "se alguém introduzir um defeito aqui, algum teste falhará?"

## Caminhos de borda e limites

- Caminho feliz não basta. Pense ativamente em como causar falha: **coleção vazia, zero, negativos, string vazia, nulo, limite de tamanho**.
- Testes de limite frequentemente revelam perguntas de domínio: demanda negativa faz sentido? O setter deveria validar?
- "Desempenhe o papel de um inimigo para o seu código" — se você forçar a falha, o teste prova que detecta.

## Estrutura do teste

- **Arrange-Act-Assert** (given-when-then): monte o estado, execute a ação, verifique.
- **Uma verificação principal por teste** — o teste falha na primeira verificação e esconde informação. Agrupe apenas asserções intimamente conectadas (mesmo resultado sob diferentes ângulos).
- **Fixture nova por teste** (`beforeEach`/`setup`): compartilhar fixture mutável é "uma placa de Petri preparada para um dos piores bugs de teste" — testes interagem, falhas intermitentes não-determinísticas conforme a ordem.
- Fature o fixture padrão em `beforeEach`; mantenha os testes enxutos.

## Verificação de que o teste funciona

- **Injete uma falha** no código (`* 2`, condição invertida) e confirme que o teste falha. Remova a falha.
- Teste que nunca falhou por si só não é evidência — o verde pode ser "verde que não verifica nada".

## Bugs

- Ao receber bug: escreva primeiro o teste que **expõe o bug** (falha reproduzida), depois corrija e veja o teste passar. O teste vira regressão permanente.
- Um erro de framework (exceção no setup) é "erro", não falha de asserção — decisão: se a entrada vem de fonte confiável da mesma base, validação extra pode ser duplicação; se vem de fora (JSON externo), validações devem existir e ser testadas.

## Ritmo

- Execute os testes que exercitam o código em que você trabalha a cada poucos minutos; a suíte completa ao menos uma vez por dia.
- Testes devem ser **rápidos** (segundos) e **automatizados** — rodar deve ser tão fácil quanto compilar.

## Checklist

- [ ] Áreas de risco cobertas (não apenas caminho feliz)
- [ ] Bordas: vazio, zero, negativo, nulo, string vazia
- [ ] Uma asserção principal por teste
- [ ] Fixture nova por teste
- [ ] Falha injetada provada em pelo menos um teste
- [ ] Testes rápidos e automatizados