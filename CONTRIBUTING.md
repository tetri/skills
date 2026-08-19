# Contribuindo

Guia para criar e manter skills neste repositório seguindo o padrão **Agent Skills** (Anthropic).

## Criar uma nova skill

1. Copie `template/` para `skills/<skill-name>/`.
2. Defina o frontmatter (`name`, `description` e opcionais).
3. Escreva o `SKILL.md` enxuto e mova detalhes para `references/`.
4. Adicione a skill à tabela do `README.md`.
5. Valide com `skills-ref`.

## Regras do padrão

### Frontmatter

- `name` — 1 a 64 caracteres; somente letras minúsculas, números e hífens; sem `--` consecutivos; **idêntico ao nome da pasta**.
  - Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `description` — 1 a 1024 caracteres; em **terceira pessoa**; descreve **o que** a skill faz e **quando usar** (sem termos reservados nem tags XML).
- Opcionais: `license`, `compatibility`, `metadata` (chave-valor).

### Corpo do SKILL.md

- Menos de **500 linhas**.
- **Progressive disclosure**: o SKILL.md é o "cérebro"; detalhes ficam em arquivos referenciados.
- Referências **um nível de profundidade** a partir do SKILL.md.
- Caminhos **relativos** com **`/`** (nunca `\`).
- Instruções em **terceira pessoa imperativa** (ex.: "Execute o script...", "Leia `references/guide.md`").
- Passos numerados e workflow com etapas claras.

### Estrutura interna

| Pasta | Uso |
| --- | --- |
| `references/` | Documentação, cheatsheets, exemplos (carregados sob demanda) |
| `scripts/` | Scripts pequenos e determinísticos (CLIs executáveis, não bibliotecas) |
| `assets/` | Templates e arquivos estáticos |

- **Não** incluir `README.md`, `CHANGELOG.md` ou guias de instalação dentro da skill.
- Arquivos de referência com mais de 100 linhas devem ter **índice (table of contents)** no topo.

## Checklist final

- [ ] `name` válido e idêntico ao nome da pasta
- [ ] `description` específica, em terceira pessoa, com o quê e quando usar
- [ ] SKILL.md < 500 linhas
- [ ] Referências a um nível de profundidade
- [ ] Caminhos relativos com `/`
- [ ] Sem arquivos de documentação de repo dentro da skill
- [ ] Passa na validação do `skills-ref`
- [ ] Testada com requests reais