# Content Guidelines (Web Stories)

Políticas de conteúdo que decidem se a story aparece como rich result e se o domínio é suprimido. Cumprir estas regras é condição do Gate 1 do protocolo.

## Limite de texto: 180 caracteres

- A **maioria das páginas** deve ter no máximo **180 caracteres** de texto. Exceder desqualifica a story de rich results.
- Escreva em frases curtas (1–2 sentenças por página), otimizadas para leitura em telas mobile.
- Texto legível sobre mídia: use overlay de gradiente (ex.: preto transparente) para garantir contraste.

## Arco narrativo completo (proibido cliffhanger)

- A story deve satisfazer o interesse **dentro dela** — narrativa standalone com início, meio e fim.
- **Proibido** usar páginas como teaser para empurrar clique externo ("3 slides + botão continue lendo"). A política de spam do Google suprime domínios que manipulam o formato para tráfego de baixo valor.
- O bookend (links relacionados) é o mecanismo legítimo para navegação de continuação e compartilhamento.

## Aspect ratios e formatos

- Capa/poster: **3:4** (portrait) é o caso padrão; landscape 4:3 e square 1:1 para os atributos correspondentes.
- Logo do publisher: **1:1**, ≥ 96×96, raster, fundo não transparente.
- Imagens e vídeos expandem para preencher a tela; sempre dimensões explícitas + `layout="responsive"`.

## Mídia por página

- Imagens, vídeos e GIFs são livres; escolha o formato conforme rede e browser do usuário.
- Áudio por página é opcional (`background-audio`) para narração ou música ambiente.
- Vídeo: considere `auto-advance-after` apontando para o `id` do vídeo (avança quando termina) para experiência lean-back.

## Monetização

- **Story Ads**: anúncios full-screen de uma página dentro da story — suportados por Google Ad Manager e DV360 (beta). Templates oficiais em amp.dev/documentation/templates.
- **Affiliate links**: o publisher pode colocar outlinks de afiliados em páginas orgânicas da story.
- O bookend também recebe links de compartilhamento social.

## Structured data (JSON-LD)

- Os atributos de metadados do `amp-story` **complementam**, não substituem, o structured data.
- Recomendado: JSON-LD de `Article`/`NewsArticle` na página (validar com Rich Results Test).

## Requisito de indexação

- URL da story na sitemap e linkada de páginas do site.
- Sem `noindex`; sem bloqueio no robots.txt.
- Canonical self-referencing obrigatório (byte-a-byte).
- Confirmar indexação com URL Inspection Tool.

## Fontes

- Google Search Central — Enable Web Stories on Google (content policies)
- Google — Spam policies (teaser/cliffhanger, conteúdo de baixo valor)
- amp.dev — Web Stories (about/stories): benefícios, monetização, editors
- Netolink (2026-05) — limitações e melhores práticas de Web Stories em 2026