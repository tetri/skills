---
name: test-authoring
description: Cria testes focados em rede de segurança — caracterização, golden master, testes diferenciais e de borda — garantindo que cada teste falha quando deve falhar. Use quando for escrever testes para código existente, criar a rede de segurança antes de refatorar, ou cobrir áreas de risco e caminhos de borda.
license: MIT
compatibility: Windows/PowerShell, git; agnóstica de linguagem
metadata:
  categoria: engenharia-de-software
  status: publicado
---

# Test Authoring

Testes são um **detector de bugs**, não uma formalidade de cobertura. O objetivo desta skill é criar uma rede de segurança que (a) captura o comportamento atual de código existente e (b) falha quando o comportamento muda. Um teste que não falha quando deveria falhar não vale nada.

## Quando usar

- Antes de refatorar código existente sem cobertura (a rede de segurança da refatoração).
- O usuário pede "testes para esse código", "cobrir essa função", "testes de caracterização" ou "golden master".
- Garantir que uma mudança não alterou comportamento (teste diferencial).
- Cobrir caminhos de borda e áreas de risco de uma feature.

## Quando NÃO usar

- O usuário quer testes de funcionalidade nova que ainda não existe — use TDD (teste primeiro) e outra skill.
- O usuário quer "100% de cobertura" como fim em si — oriente a risco, não a métrica.
- Código cujo comportamento desejado é desconhecido e não observável — defina comportamento com o usuário primeiro.

## Escolha o tipo de teste

| Situação | Tipo | Carregar |
| --- | --- | --- |
| Código existente, sem testes, comportamento desconhecido | [Caracterização](references/characterization.md) | 1º |
| Código com saída observável estável (CLI, serialização, geração) | [Golden master](references/golden-master.md) | 2º |
| Preciso provar equivalência antes/depois de mudança | [Teste diferencial](references/golden-master.md) | 3º |
| Cobrir lógica nova, bordas e risco | [Design de teste](references/test-design.md) | 4º |

## Workflow

### Gate 0 — Mapear seams e comportamento

1. Identifique as **linhas de junção** (seams): pontos onde o código pode ser exercitado sem dependências impossíveis (funções puras, métodos públicos, entrada/saída de processo). Para legado, isso pode exigir mudança mínima (passar valores, extrair função pura) — faça em passo separado e justifique.
2. Determine o comportamento observável: o que entra, o que sai, que efeitos colaterais existem.
3. Registre a baseline de verificação (rodar a suíte existente; ver [framework-guide](references/framework-guide.md)).

### Gate 1 — Criar a rede

4. **Caracterização:** escreva teste com expectativa placeholder → substitua pelo valor real produzido → **injetar uma falha** (`* 2`) e confirme que o teste falha → remova a falha. Teste verde, mas provado sensível ([characterization](references/characterization.md)).
5. **Golden master:** capture saídas reais para entradas representativas como ground truth, com casos de borda (coleção vazia, zero, negativo, string vazia, nulo) ([golden-master](references/golden-master.md)).
6. **Bordas e risco:** além do caminho feliz, cubra o que pode dar errado — "desempenhe o papel de inimigo do seu código".

### Gate 2 — Verificação

7. Rode a suíte completa. **Todo teste deve falhar quando deve falhar** — verifique com falha injetada em pelo menos um teste novo de cada tipo.
8. Fixture nova por teste; uma verificação (asserção) principal por teste ([test-design](references/test-design.md)).
9. Testes rápidos (segundos) e totalmente automatizados — roda-se com a mesma facilidade do build.

## Regras não negociáveis

- Teste que não falha quando deve falhar = teste inútil. Sempre injete a falha e prove.
- Testes documentam o comportamento ATUAL. Se o comportamento desejado é diferente, é mudança de produto — converse antes de "corrigir" o teste.
- Oriente a risco: áreas complexas e bordas primeiro; getters/setters triviais não precisam de teste.
- Nunca escreva teste que depende de outro (ordem de execução, fixture compartilhada mutável).
- Prefira testes incompletos a nenhum teste — "é melhor escrever e executar testes incompletos do que não executar testes completos".

## Erros comuns a evitar

- Copiar a lógica do código para o teste (mesma variável, mesmo erro — o teste nunca falharia).
- Testar só o caminho feliz.
- Fixture compartilhada mutável (placa de Petri de bugs intermitentes).
- Múltiplas asserções no mesmo teste (falha na 1ª esconde a informação das demais).
- Golden master não determinístico (ordem de dicionário, timestamps, paths) sem normalização.

## Referências

- [characterization](references/characterization.md) — testes de caracterização (Feathers) passo a passo
- [golden-master](references/golden-master.md) — golden master e testes diferenciais
- [test-design](references/test-design.md) — orientação a risco, bordas, fixture, asserção única
- [framework-guide](references/framework-guide.md) — frameworks e comandos por stack