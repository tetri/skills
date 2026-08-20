# AMP State of the Art (2026)

O que um agente precisa saber para **avaliar** (e não só construir) AMP em 2026. O formato não é o que era; decisões informadas evitam o modo de falha mais caro: investir onde não há retorno.

## Cronologia (por que o formato mudou)

| Ano | Evento |
| --- | --- |
| 2016 | AMP lançado; obrigatório para o carrossel Top Stories |
| 2018 | Pico de adoção; cresce a crítica sobre controle da Google (URL, cache) |
| 2021 | Google **remove a obrigatoriedade** de AMP no Top Stories; aposenta o ícone do raio; Core Web Vitals vira o sinal primário de performance |
| 2024-03 | INP substitui FID como Core Web Vital |
| 2024-02 | Google **remove o ícone dedicado de Web Stories** na busca de Imagens |
| 2025 | Downloads do plugin AMP caem ~80% do pico |
| **2026-07-01** | Google **deixa de servir AMP pelo AMP Cache** na Pesquisa: usuário vai direto à página AMP hospedada no domínio do publisher. Removidos das docs: AMP viewer, AMP Cache e signed exchanges |

## O que mudou em 01/07/2026 (mudança operacional, não de ranking)

- Resultado AMP na Pesquisa leva à **página AMP do publisher**, não à versão do cache/AMP viewer.
- Não há mais necessidade de atualizar o cache nem configurar **signed exchanges** (SXG).
- **Ranking inalterado**: conteúdo AMP continua rankeando como qualquer página. Fim do privilégio de entrega, não do suporte ao formato.
- A Google afirmou que continua suportando o formato open source `amphtml`.

## Posição da Google em 2026

- AMP está **"supported"** mas **não é recomendado nem exigido** para nenhum recurso da Pesquisa.
- Sem vantagem de ranking, sem carrossel exclusivo, sem ícone dedicado.
- O que valia em 2016 (velocidade comprada com controle do seu código/URL) hoje se obtém com performance nativa: **Core Web Vitals (LCP, INP, CLS)**, AVIF, edge caching em CDN, JS adiado.

## Web Stories: o caso de uso vivo

- Web Stories (ex-AMP Stories) é o formato visual full-screen sobre o componente `amp-story`.
- **Ainda suportado e indexável**: pode aparecer como resultado único na Pesquisa e como card no Discover (destaque mais provável em **EUA, Índia e Brasil**).
- Desde 2024 a visibilidade de superfície encolheu (sem ícone em Imagens, carrosséis de Discover reduzidos).
- **Valor estratégico atual**: ativo de UX/engajamento on-site e conteúdo visual indexável — **não** é canal de aquisição de tráfego externo na maioria dos mercados.

## Quando usar cada coisa

| Cenário | Recomendação |
| --- | --- |
| Story visual para engajamento on-site | **Sim** — Web Story válida + validada |
| KPI = tráfego orgânico externo fora de EUA/Índia/Brasil | **Não** — performance nativa + conteúdo |
| Página comum (artigo, produto, landing) | **Não** — HTML moderno + CWV + CDN |
| E-mail interativo (RSVP, formulário no inbox) | **AMP for Email** — produto separado, runtime próprio, vivo no Gmail; não confundir com web AMP |
| Site legado com AMP sem benefício | **Retirada planejada** (modo `retire`) |

## Retirada segura de AMP (modo `retire`)

1. **Inventário**: liste URLs AMP indexadas (`/amp/`, `?amp=1`, `?output=amp`) via Search Console (relatório de indexação), sitemaps e logs. O maior risco de SEO é esquecer variante de URL e deixar 404 indexado por semanas.
2. **Canonicals**: remova `rel="amphtml"`; garanta que cada página tenha canonical self-referencing. Nunca canônicos apontando para versão AMP.
3. **301 redirects**: cada URL AMP → canônica definitiva (inclusive variante `?amp=1`).
4. **Sitemap**: ressubmeta a sitemap limpa no Search Console.
5. **Monitoramento**: acompanhe Search Console (crawling/indexação) e erros de rastreamento por 2–4 semanas.

## Restrições técnicas do AMP (relevantes para avaliar)

- **Sem JavaScript customizado síncrono** — limita conversões, formulários e integrações complexas.
- **CSS inline limitado a 75 KB**.
- O "instantâneo" histórico veio do cache/pré-render da Google — não é propriedade intrínseca do formato.
- Manter AMP exige **dois templates** (AMP + canônico): custo de manutenção real.

## Fontes

- Google Search Central — AMP documentation update (2026-07-01): AMP Search Central, "Enable Web Stories on Google", "Validate your AMP content"
- SearchEngineLand / SearchEngineJournal / Search Roundtable (2026-07-01/02) — Google ends cache-served AMP pages in Search
- wppoland.com (2026-07) — "Is Google AMP dead in 2026?"
- Netolink (2026-05) — "Google Web Stories: The Updated Strategic Guide"
- GitHub community discussion #199472 — `amp-story canonical error` (self-canonical é requisito intencional)