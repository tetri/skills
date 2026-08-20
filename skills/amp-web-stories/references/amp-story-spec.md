# AMP Story Spec

Markup obrigatório e componentes para uma Web Story válida. O validador AMP e o Google exigem estes pontos exatos — "olha só, funciona no browser" não basta.

## Requisitos de markup (regras do validator)

1. `<!doctype html>` no início do documento.
2. `<html amp>` (ou `<html ⚡>`).
3. No `<head>`, obrigatório (além do padrão AMP):
   - `<meta charset="utf-8">`
   - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`
   - runtime: `<script async src="https://cdn.ampproject.org/v0.js"></script>`
   - componente: `<script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>` — **terceiro filho do `<head>`**
   - boilerplate AMP (`amp-boilerplate` / `amp-story` style) — sem ele a página pisca e pode falhar validação
   - `<link rel="canonical">` apontando **para a própria story**
4. `<amp-story>` é o **único filho de `<body>`** (o documento é uma story, não uma página que embute story).

## `<amp-story>` — atributos

| Atributo | Exigência | Detalhe |
| --- | --- | --- |
| `standalone` | **obrigatório** | marca documento como story standalone |
| `title` | obrigatório | título da story (usado em previews) |
| `publisher` | obrigatório | nome do publisher |
| `publisher-logo-src` | obrigatório | logo 1:1, ≥ 96×96, raster, fundo não transparente |
| `poster-portrait-src` | obrigatório | capa 3:4, mín. 640×853, raster |
| `poster-landscape-src` / `poster-square-src` | opcional | 4:3 mín. 853×640 / 1:1 mín. 640×640 |
| `supports-landscape` | opcional | habilita orientação landscape + experiência desktop full-bleed |
| `desktop-aspect-ratio` | opcional | ex.: `"16:9"` — ratios aceitos incluem `4:3` e `3:4` |
| `live-story` / `data-poll-interval` | opcional | atualização ao vivo |

## Hierarquia da página

```
<amp-story ...>
  <amp-story-page id="pagina-1">          ← id obrigatório e único (usado no fragmento de URL)
    <amp-story-grid-layer template="vertical">   ← templates: vertical, horizontal, fill, thirds
      <amp-img src="..." width="266" height="340" layout="responsive"></amp-img>
    </amp-story-grid-layer>
    <!-- camadas empilhadas de baixo para cima (a última do DOM fica no topo) -->
  </amp-story-page>
  <amp-story-bookend src="related-links.json"></amp-story-bookend>
</amp-story>
```

- **`<amp-story-page>`**: `id` obrigatório (único); `auto-advance-after` opcional (tempo, ex. `"3s"`, ou `id` de um elemento de vídeo — avança quando o vídeo termina); `background-audio` opcional (URI de áudio tocado enquanto a página está visível).
- **`<amp-story-grid-layer>`**: `template` obrigatório — `vertical` (layout de coluna), `horizontal`, `fill` (mídia preenchendo a camada), `thirds` (três seções). Camadas são empilhadas bottom-up: a primeira no DOM fica no fundo.
- **`<amp-story-bookend>`**: `src` aponta para endpoint JSON com `related` (links relacionados) e `share-providers` — é onde se adiciona navegação para dentro do site e compartilhamento. Também pode ser inline.
- **`<amp-story-player>`**: componente para **embutir** a story em páginas não-AMP (não substitui a story canônica).

## Self-canonical (regra que mais derruba stories)

Diferente de páginas AMP comuns (AMP → canônico + canônico → `rel="amphtml"`), a story é **o próprio canônico**. Requisito intencional da plataforma — não há exceção.

O `href` do canonical deve ser **byte-a-byte idêntico** à URL servida:
- protocolo idêntico (`https` vs `http`)
- presença/ausência de **trailing slash** idêntica
- **sem query params** adicionados/removidos (`?id=1`)
- domínio idêntico (`www` vs sem `www`)

Erros comuns em stacks dinâmicos (Next.js/React):
- Canonical vindo de campo de CMS / `process.env.SITE_URL` / config estática em vez da rota resolvida → pode divergir (ex.: env de staging vazando).
- `trailingSlash: true` no config sem barra no canonical (ou vice-versa).
- Canonical injetado só client-side (`useEffect`) → Googlebot lê o HTML cru antes do JS. Injete no SSR/SSG (server-rendered).

## Mídia

- Poster e logo **raster**: `.jpg`, `.png`, `.gif`. Evite vetores (`.svg`, `.eps`); evite GIF animado para logo.
- Logo: ≥ 96×96, quadrado perfeito, fundo sólido (não transparente), uma logo consistente por marca.
- Poster de vídeo: use frame **representativo** (o primeiro frame frequentemente não é).
- Layout responsivo: sempre dimensões explícitas + `layout="responsive"` em `amp-img`/`amp-video`.

## Fontes

- amp.dev — Create your first Web Story (visual_story)
- amp.dev — Component: `<amp-story>` (extensions/amp-story/amp-story.md)
- amp.dev — Component: `<amp-story-page>` (extensions/amp-story/amp-story-page.md)
- Google Search Central — Enable Web Stories on Google