# Writing Guide

Como escrever o SKILL.md e as referências: tom, estrutura e progressive disclosure.

## Tom e voz

- **Terceira pessoa imperativa** — a skill instrui o agente: "Execute", "Leia", "Verifique", "Registre". Nunca "eu faço" ou "você deve".
- **Passos numerados** — procedimento executável, não prosa.
- **Concreto > abstrato** — prefira "execute `dotnet test` e registre o exit code" a "valide a qualidade".
- Termos canônicos do domínio em inglês (nomes de refatorações, smells, padrões); texto explicativo na língua do usuário.

## Estrutura do SKILL.md (o cérebro)

1. **Intro de 1–3 linhas** — o que a skill garante (a promessa de valor).
2. **Quando usar** — triggers explícitos.
3. **Quando NÃO usar** — recusa e redirecionamento (o freio).
4. **Roteamento/modos** — se o domínio tem modos, tabela com quando usar cada um + qual referência carregar.
5. **Protocolo em passos** — o núcleo; passos numerados, com **gates** (pontos de verificação obrigatórios) entre fases.
6. **Regras não negociáveis** — o que nunca pode ser violado.
7. **Erros comuns a evitar** — modos de falha documentados do domínio.
8. **Referências** — links para os arquivos, cada um com 1 linha de descrição.

## Progressive disclosure na prática

- O SKILL.md cita o arquivo **quando** ele é necessário: "Se a stack é Python, leia [command-catalog](references/command-catalog.md) para os comandos".
- Referências a **um nível** — o agente lê o arquivo completo quando precisa.
- Arquivos longos (>100 linhas): **índice no topo** para navegação parcial.
- Código de exemplo e templates vão para `assets/` ou `references/`, não para o cérebro.

## Gate > checklist

- Transforme intenção em verificação: "certifique-se de que os testes passam" → "execute o comando; se exit != 0, reverta e refaça em passos menores".
- Use a fórmula: **condição → comando → ação em falha**. Ex.: "Teste falhou? Desfaça o último passo (git checkout) e reduza o tamanho do passo."
- Isso é o que separa uma skill operável de um ensaio.

## O padrão "mecânica ≠ diff final"

- Skills de processo devem descrever a **jornada verificável** (passos intermediários que terminam em estado bom), não só o resultado final.
- Ex.: para mover uma função: copiar → delegação → inline nos callers → remover, com verificação entre cada sub-passo.

## Qualidade de referência

- Cada referência tem um propósito único e nome descritivo (`equivalence-gates.md`, não `doc2.md`).
- Mantenha a terminologia consistente em toda a skill.
- Inclua checklist de verificação no final dos arquivos de procedimento.

## Armadilhas de escrita

- SKILL.md virando livro (detalhe no cérebro) — mova para referências.
- Passos sem gate (o agente avança sem verificar).
- Instruções em 1ª/2ª pessoa.
- Referências a 2 níveis.
- Código exemplo gigante no corpo — vira arquivo em `assets/`.