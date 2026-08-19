# Research Protocol

Como pesquisar um domínio antes de escrever a skill. O objetivo: **encontrar a fonte canônica e os dados empíricos** — a skill notável nasce da pesquisa, não do chute.

## Ordem de pesquisa

1. **Fontes canônicas do domínio** — o livro/artigo/curso de referência (ex.: para refatoração, Fowler; para testes, Feathers; para arquitetura, Fowler/Evans).
2. **Documentação oficial e especificações** — o que o mercado usa como padrão (ex.: especificação Agent Skills).
3. **Páginas especializadas consolidadas** — sites que organizam o domínio de forma operacional (ex.: refactoring.guru).
4. **Skills existentes** — GitHub/marketplaces: `"SKILL.md <tema>"`, `"claude skill <tema>"`, `"agent skills <tema>"`.
5. **Dados empíricos recentes** — artigos de pesquisa (arXiv), postmortems de engenharia, relatos de falha de agentes no domínio.

## Técnicas

- Use busca + leitura de páginas-chave; para conteúdo grande (livros/EPUBs), extraia e faça distilação por partes.
- Liste o **índice/TOC** da fonte canônica — é o mapa do domínio (categorias, inventário, nomes).
- Para cada skill existente: nome, URL, estrutura, forças, fraquezas.
- Colete **modos de falha documentados** (como agentes/humanos erram neste domínio) — serão os "erros comuns a evitar" da skill.

## Distilação

Para cada fonte, produza (mentalmente ou em notas):

1. **Definições** — conceitos-chave com a redação canônica.
2. **Princípios** — regras que governam o domínio.
3. **Inventário** — lista completa de itens (smells, padrões, refatorações, comandos).
4. **Procedimentos** — passos executáveis (mecânica).
5. **Regras de exceção** — quando NÃO fazer (o freio anti-superaplicação).
6. **Fatos empíricos** — números e achados de pesquisa.

## Critérios de parada

- Você tem a fonte canônica identificada + inventário completo do domínio.
- Você viu pelo menos 3 skills existentes do tema (ou confirmou que não existem).
- Você tem 3+ modos de falha documentados do domínio.
- Você sabe qual é a lacuna que sua skill vai preencher.

## Armadilhas

- Parar no primeiro artigo de blog genérico (falta a fonte canônica).
- Ignorar skills existentes (você vai recriar o que já existe).
- Ignorar dados empíricos (a skill vira opinião, não protocolo).
- Copiar estrutura de uma skill existente sem o gap (reproduz a mediocridade).