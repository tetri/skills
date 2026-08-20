# Validation Tooling

Como **provar** que uma Web Story é válida e indexável — e os erros que mais derrubam stories.

## Ferramentas

| Ferramenta | Uso | Quando |
| --- | --- | --- |
| `validate-story.ps1` (scripts da skill) | Gate determinístico local: markup essencial + self-canonical + metadados + validador oficial | Antes de publicar (obrigatório no protocolo) |
| `amphtml-validator` (npm, oficial) | Validação autoritativa da página contra as regras AMP | CLI; parte do gate determinístico |
| AMP Linter | Validação durante o desenvolvimento (mensagens acionáveis) | Em dev contínuo |
| Google AMP Test (validator.amp.dev / search.google.com/test/amp) | Confirmação oficial em URL pública | Pós-publicação |
| Rich Results Test | Structured data (JSON-LD) da story | Quando usar JSON-LD |
| Search Console — URL Inspection Tool | Status de indexação e validade AMP | Pós-publicação e no monitoramento |

## Gate determinístico (scripts/validate-story.ps1)

Valida: estrutura do documento → self-canonical (byte-a-byte vs a URL fornecida) → `amp-story` como único filho de `<body>` → runtime/componente no `<head>` → metadados obrigatórios (`standalone`, `title`, `publisher`, `publisher-logo-src`, `poster-portrait-src`) → validador oficial AMP.

```powershell
& .\validate-story.ps1 -Story .\story.html -Canonical "https://site.com/stories/my-story"
```

Exit 0 = todos os gates passaram; exit ≠ 0 = gate reprovado com a mensagem de qual falhou. Requer Node.js (o validador oficial roda via `npx`).

## Erros comuns de validação e correção

| Erro | Causa típica | Correção |
| --- | --- | --- |
| `amp-story canonical error` | Canonical não self-referencing (aponta para artigo, embutido via `amp-story-player`, ou URL divergente: trailing slash, `www`, query, protocolo) | Derivar o canonical da rota real servida, byte-a-byte (ver amp-story-spec.md) |
| Canonical ausente para o Googlebot | Tag injetada client-side (useEffect/hydration) | Gerar no SSR/SSG, no HTML cru |
| Story inválida (critical errors) | Boilerplate faltando, `<amp-story>` não é único filho de `<body>`, script do componente na posição errada | Corrigir estrutura (amp-story-spec.md) |
| Metadados de preview ausentes | Falta `publisher-logo-src` ou `poster-portrait-src` (ou tamanho/ratio errados) | Sizes oficiais: logo 1:1 ≥96×96; poster 3:4 ≥640×853 |
| Rich result desqualificado | Texto > 180 caracteres na maioria das páginas; arco narrativo incompleto | Encurtar texto; completar narrativa (content-guidelines.md) |
| Não indexada | `noindex`, robots.txt bloqueando, fora da sitemap, canônica duplicada | Liberar, linkar e submeter sitemap |

## Validação na Google (pós-publicação)

1. Passe a URL no AMP Test — válida a página e a exibição.
2. Se usou JSON-LD, valide com Rich Results Test.
3. Confirme indexação no URL Inspection Tool (Search Console); se não indexar: canonical, robots, sitemap, status code.
4. Acompanhe o status de indexação/sitemaps por 2–4 semanas após mudanças (especialmente no modo `retire`).

## Limites

- `amphtml-validator` valida regras AMP do documento local, não: indexação, elegibilidade de rich results, nem comportamento de runtime do navegador.
- A validação local não substitui o AMP Test da Google em URL pública.
- O validador não detecta violações de política de conteúdo (limite de caracteres, cliffhanger) — essas são verificadas pelo Gate 1 do protocolo.

## Fontes

- Google Search Central — Validate your AMP content; AMP status report; AMP Test / Rich Results Test
- amp.dev — Validate AMP pages; AMP validation errors; AMP Linter
- npm — `amphtml-validator` (official AMP HTML Validator CLI)