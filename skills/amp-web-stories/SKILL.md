---
name: amp-web-stories
description: Cria, aprimora e avalia Web Stories AMP no estado da arte de 2026 — sem vantagem de ranking no Google e com valor real em UX on-site. Use quando o usuário quiser criar uma história visual full-screen (Web Story) no padrão open web (amp-story), corrigir uma story existente que falha na validação AMP/Google (self-canonical, metadados, limite de caracteres) ou decidir se o formato AMP/Web Stories compensa para o caso dele.
license: MIT
compatibility: Windows/PowerShell, bash, Node.js (para o gate de validação)
metadata:
  categoria: web-publishing
  fontes: amp.dev (about/stories, visual_story, amp-story), developers.google.com/amp, Google Search Central (enable-web-stories, validate-amp), SearchEngineLand/SearchEngineJournal 2026-07-01
  status: publicado
---

# AMP Web Stories

Web Stories (antes AMP Stories) é o caso de uso vivo do AMP em 2026: histórias visuais full-screen, tap-through, indexáveis e com URL própria — parte do open web, sem aprisionamento a plataforma. Esta skill é um **protocolo com gates**, não uma lista de componentes: decide primeiro se o formato compensa (estado da arte), depois cria com markup válido e metadados corretos, e **prova** a validade com o validador oficial AMP antes de publicar.

## Quando usar

- O usuário quer criar uma Web Story (história visual, imagens/vídeo/GIF + texto por página) para publicar no próprio site.
- Corrigir/validar uma story existente que falha na validação AMP ou Google (erro de self-canonical, metadados, rich results, limite de caracteres).
- Avaliar se AMP/Web Stories é a escolha certa para o caso de negócio antes de investir produção.
- Migrar para fora de AMP (retirada) em site legado que já não justifica o formato.

## Quando NÃO usar (recuse e redirecione)

- O objetivo é **tráfego SEO externo fora de EUA/Índia/Brasil** ou "subir no ranking com AMP": AMP não tem vantagem de ranking desde 2021 e os destaques de Discover encolheram. Redirecione para performance nativa (Core Web Vitals: LCP, INP, CLS) + conteúdo otimizado.
- Página comum (artigo não-visual): AMP de sites não é mais recomendado; use HTML moderno com CDN/edge cache, AVIF e JS adiado.
- AMP para E-mail: é outro produto (runtime e regras próprios, vivo no Gmail) — não misture com web AMP.
- O usuário não aceita o custo de manutenção do formato (template AMP + template canônico) — sem orçamento de manutenção, recuse o modo `create`.

## Classificação: selecione o modo

Passo 1 — classifique o pedido e carregue a referência indicada. Todos os modos seguem o mesmo protocolo; muda o gate inicial.

| Modo | Aplicar quando | Carregar |
| --- | --- | --- |
| `evaluate` | Decidir se Web Stories/AMP vale o investimento para o caso | [amp-state-of-the-art](references/amp-state-of-the-art.md) |
| `create` | Construir uma Web Story nova do zero | [amp-story-spec](references/amp-story-spec.md) + [content-guidelines](references/content-guidelines.md) |
| `improve` | Corrigir story existente que falha validação/rich results | [amp-story-spec](references/amp-story-spec.md) + [validation-tooling](references/validation-tooling.md) |
| `retire` | Remover AMP do site com segurança (sem quebrar SEO) | [amp-state-of-the-art](references/amp-state-of-the-art.md) |

## Protocolo obrigatório (todos os modos)

### Gate 0 — Decisão de investimento (evaluate)

1. Faça a avaliação honesta do estado da arte ([amp-state-of-the-art](references/amp-state-of-the-art.md)): Web Stories NÃO impulsiona ranking; o valor é engajamento/UX on-site e conteúdo visual indexável.
2. Registre a resposta para: público geográfico (Discover forte em EUA, Índia, Brasil), objetivo (tráfego externo vs retenção on-site), e orçamento de manutenção.
3. Tráfego externo é o KPI? Recuse `create` e redirecione para performance nativa. Retenção/UX é o KPI? Avance.
4. Modo `retire`: liste as URLs AMP ativas (padrão `/amp/`, `?amp=1`, `?output=amp`), canonicals e backlinks indexados ANTES de tocar qualquer template.

### Gate 1 — Contrato de conteúdo

5. Cada página da story: **máximo 180 caracteres de texto** na maioria das páginas (elegibilidade para rich results); narração em frases curtas de 1–2 sentenças.
6. **Arco narrativo completo**: a story deve satisfazer o interesse nativamente — proibido cliffhanger teaser que empurra para fora ("continue lendo" como única conclusão).
7. Mídias: raster (`.jpg`/`.png`/`.gif`) nas dimensões mínimas; nada de SVG/EPS em poster/logo. Cobertura: poster 3:4, logo 1:1.

### Gate 2 — Markup válido ([amp-story-spec](references/amp-story-spec.md))

8. Estrutura AMP válida: `<!doctype html>`, `<html amp>` (ou `⚡`), `<meta charset>`, viewport AMP, boilerplate AMP, runtime `v0.js` e o script `custom-element="amp-story"` no `<head>`.
9. `<amp-story>` é o **único filho de `<body>`**. Atributos obrigatórios: `standalone`, `title`, `publisher`, `publisher-logo-src`, `poster-portrait-src`.
10. **Self-canonical**: `link rel="canonical"` deve apontar byte-a-byte para a própria URL da story (protocolo, barra final, query, `www`). Stories NÃO usam o padrão AMP→canônico de páginas comuns — não aponte o canônico para a página do artigo.

### Gate 3 — Metadados e structured data

11. Poster e logo dentro das regras ([amp-story-spec](references/amp-story-spec.md)): `publisher-logo-src` 1:1 ≥ 96×96, fundo não transparente; `poster-portrait-src` 3:4 ≥ 640×853 (landscape 4:3 ≥ 853×640, square 1:1 ≥ 640×640).
12. Adicione JSON-LD (Article/NewsArticle) — os atributos do `amp-story` complementam, não substituem, o structured data.

### Gate 4 — Validação mecânica (provar, não acreditar)

13. Rode o **gate determinístico** [validate-story.ps1](../scripts/validate-story.ps1) na story: markup essencial + self-canonical + metadados + validador oficial AMP (`amphtml-validator`). Exit 0 obrigatório.
14. Confirme no Google: AMP Test e, se aplicável, Rich Results Test (structured data) ([validation-tooling](references/validation-tooling.md)). Story que falha validação não é publicável.

### Gate 5 — Publicação e indexação

15. A story deve estar acessível a Googlebot: sem `noindex`, sem bloqueio no robots.txt, URL na sitemap (e linkada de páginas do site).
16. Bookend (`amp-story-bookend`) com related links e compartilhamento — a story deve engajar e navegar para dentro do site.
17. Modo `retire`: após remover AMP, **301 redirects** de cada URL AMP para a canônica, repair de canonicals e sitemaps, monitorar Search Console por 2–4 semanas ([amp-state-of-the-art](references/amp-state-of-the-art.md)).

## Regras não negociáveis

- Avaliação primeiro: nunca criar AMP/Web Story sem Gate 0 explícito (o formato não compra tráfego externo).
- Self-canonical é obrigatório e byte-a-byte — erro de canonical invalida a story no Google (requisito intencional da plataforma, não bug).
- Texto por página ≤ 180 caracteres na maioria das páginas; arco narrativo completo, sem cliffhanger.
- Nunca aponte o canônico da story para a página do artigo, mesmo com `amp-story-player` na página não-AMP.
- Validação mecânica é condição de publicação: story inválida não vai para produção.
- Mídia de poster/logo em raster (`.jpg`/`.png`/`.gif`), nunca SVG/EPS; logo com fundo sólido.

## Erros comuns a evitar (modos de falha documentados)

- Vender Web Stories como canal de tráfego orgânico em mercados sem destaque no Discover (EUA/Índia/Brasil) — expectativa errada desde o Gate 0.
- Self-canonical apontando para o artigo ou para URL derivada de config estática (trailing slash, `www`, `?param`) — erro `amp-story canonical` que invalida a story.
- Canonical injetado via JS client-side (useEffect) — Googlebot lê o HTML cru; injete no SSR/SSG.
- Mais de 180 caracteres por página — story perde elegibilidade de rich result.
- Teaser com cliffhanger ("continue lendo") — política de spam suprime o domínio.
- Poster derivado do primeiro frame do vídeo (não representativo) — use frame representativo.
- Ignorar que o AMP Cache deixou de servir páginas (2026-07-01) e continuar otimizando para ele.
- Manter páginas AMP comuns sem benefício — dívida de manutenção sem retorno; considere `retire`.
- Publicar story sem rodar o gate determinístico.

## Referências

- [amp-state-of-the-art](references/amp-state-of-the-art.md) — status do AMP em 2026: fim do cache no Google, sem vantagem de ranking, Core Web Vitals, quando usar/retirar
- [amp-story-spec](references/amp-story-spec.md) — markup obrigatório, componentes (amp-story, amp-story-page, amp-story-grid-layer, bookend, player), metadados e self-canonical
- [content-guidelines](references/content-guidelines.md) — políticas de conteúdo, limites de texto, monetização (story ads, affiliate), structured data
- [validation-tooling](references/validation-tooling.md) — validador oficial, AMP Test, Rich Results, Search Console e erros comuns
- [validate-story.ps1](../scripts/validate-story.ps1) — gate determinístico: markup essencial + self-canonical + metadados + validador oficial AMP