# Golden Master

Golden master (também chamado de approval/snapshot test) captura a saída real de um sistema para entradas representativas e a usa como **ground truth**: qualquer diferença rejeita a mudança. É a verificação mais forte de equivalência de comportamento para refatoração.

## Quando usar

- Saída observável e estável: CLI, geração de arquivos, serialização, relatórios, transformações de dados.
- Refatoração de lógica densa onde caracterização unidade-a-unidade seria frágil.
- Provar equivalência antes/depois (teste diferencial).

## Como construir

1. **Selecione entradas representativas:** casos reais de produção + bordas (vazio, zero, negativos, nulo, string vazia). Quanto mais caminhos do código, mais forte o golden master.
2. **Capture a saída real** (stdout, arquivo, estrutura serializada) e salve como golden (commitado no repo).
3. **Normalize o não determinístico:** timestamps, GUIDs, ordem de dicionário, caminhos absolutos, timezones. Substitua por placeholders estáveis ANTES de comparar — senão o golden "flaky" é inútil.
4. **Injete falha para provar:** mude o código trivialmente e confirme que o golden master falha; reverta.
5. **Diferencial (before/after):** para refatoração, capture a saída da versão atual, faça a mudança, compare. "1 byte de diferença = rejeita."

## Estrutura de comparação

- Compare byte a byte (ou estrutura canonizada) — nunca "contém" ou aproximado.
- Guarde o golden em arquivo versionado; a alteração do golden exige revisão explícita (é uma mudança de contrato).
- Se a saída é grande, compare com diff (`git diff --no-index`) e reporte apenas a primeira divergência + contagem.

## Quando é frágil

- Saída com ordem não determinística (coleções): canonize (ordene, serialize com chaves ordenadas).
- Saída dependente de ambiente (locale, path): normalize ou rode no ambiente padrão do CI.
- Saída com conteúdo binário: hash sha256 do binário como golden.

## Relação com fuzzing diferencial

- Golden master usa entradas fixas; **fuzzing diferencial** gera entradas (aleatórias/propriedade) e compara saídas da versão nova vs antiga no mesmo processo.
- Use fuzz quando o espaço de entradas é amplo e a lógica densa; use golden quando a saída é um artefato estável.

## Checklist

- [ ] Entradas representativas + bordas
- [ ] Não determinismo normalizado
- [ ] Golden versionado
- [ ] Falha injetada → falhou → revertida
- [ ] Antes/depois comparado byte a byte