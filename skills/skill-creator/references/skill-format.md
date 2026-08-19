# Skill Format

Especificação do padrão Agent Skills (Anthropic) — as regras rígidas que qualquer skill do repositório deve cumprir.

## Estrutura de diretório

```
skill-name/
├── SKILL.md              # Obrigatório: metadados + instruções (< 500 linhas)
├── references/           # Opcional: documentação carregada sob demanda
├── scripts/              # Opcional: CLIs determinísticos (executáveis)
└── assets/               # Opcional: templates, arquivos estáticos
```

- Nome da pasta: minúsculas + hífens (kebab-case), sem `--` consecutivos.
- Caminhos relativos resolvem a partir da raiz da skill; use **`/`**, nunca `\`.
- Regras: sem `README.md`/`CHANGELOG.md`/guia de instalação dentro da skill.

## Frontmatter

### Obrigatórios

- `name` — 1–64 caracteres; somente letras minúsculas, números e hífens; sem hífens consecutivos; **idêntico ao nome da pasta**. Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`. Não pode conter "anthropic"/"claude" nem tags XML.
- `description` — 1–1024 caracteres; terceira pessoa; descreve **o que** a skill faz e **quando usar** (triggers). Sem tags XML.

### Opcionais

- `license` — MIT, Apache-2.0, CC-BY-4.0, etc.
- `compatibility` — ambiente/agentes testados (≤ 500 chars).
- `metadata` — mapa chave-valor livre (autor, versão, status, fontes, categorias).

## Corpo do SKILL.md

- **< 500 linhas** (ótimo: 100–300).
- O SKILL.md é o **cérebro** (navegação + procedimento de alto nível); o detalhe mora em arquivos referenciados.
- Referências **um nível de profundidade** a partir do SKILL.md (nunca `references/subdir/file.md` para os arquivos citados).
- Arquivos de referência com mais de 100 linhas: **índice (table of contents)** no topo.
- Instruções em **terceira pessoa imperativa**: "Execute o script...", "Leia `references/x.md`...".
- Passos numerados, workflflows com etapas claras, checklist de verificação ao final.

## Progressive disclosure

- Níveis: (1) nome+descrição pré-carregados; (2) SKILL.md lido quando a skill é ativada; (3) referências/scripts lidos/executados sob demanda.
- Custo zero de contexto até o arquivo ser realmente lido — use isso para bundar material rico (catálogos, schemas, exemplos) sem inchar o cérebro.
- Instrua o agente **quando** ler cada arquivo ("Para erros específicos, leia `references/errors.md`").

## Descrições eficazes

- Terceira pessoa, nunca "Eu" ou "Você".
- Inclua o quê + quando + trigers negativos quando útil ("Não use para X").
- Seja específica; termos-chave do domínio ajudam o roteamento.

## Erros comuns

- `name` ≠ pasta.
- SKILL.md gigante (detalhe empurrado para dentro do cérebro).
- Referência a 2 níveis de profundidade.
- Caminho com `\`.
- Instruções em 1ª pessoa.
- README/CHANGELOG dentro da skill.