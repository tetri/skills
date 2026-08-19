---
name: skill-creator
description: Cria Agent Skills no padrão de mercado (Anthropic) com diferencial real, seguindo um protocolo de pesquisa, análise de lacunas, design e validação. Use quando for criar uma nova skill, reestruturar uma existente ou avaliar se uma skill do repositório está no padrão.
license: MIT
compatibility: agnóstica
metadata:
  categoria: meta
  status: publicado
---

# Skill Creator

Criar uma skill "notável" não é escrever um arquivo — é seguir um **protocolo**: pesquisar a fonte canônica do domínio, mapear o que já existe, encontrar a lacuna, desenhar com progressive disclosure e validar contra a especificação. Este skill codifica o processo usado para criar a `code-refactoring`.

## Quando usar

- O usuário pede para criar uma nova skill, "fazer uma skill sobre X".
- Reestruturar/avaliar uma skill existente do repositório.
- Qualquer skill que vai entrar no repositório de skills.

## Quando NÃO usar

- O usuário quer usar uma skill existente (não criar).
- Ajuste pontual de uma skill em produção (use edição direta).

## Fases do protocolo

### Fase 1 — Escopo e pesquisa

1. **Defina o domínio e o público** (para quem, que agentes).
2. **Pesquise as fontes canônicas** do tema ([research-protocol](references/research-protocol.md)): livros/artigos de referência, documentação oficial, páginas especializadas. Priorize fontes primárias sobre blogs genéricos.
3. **Mapeie as skills existentes** sobre o tema (GitHub, marketplaces): o que fazem, como estruturam, onde falham.

### Fase 2 — Gap analysis

4. Identifique o **diferencial substantivo**: o que as skills existentes NÃO fazem e que os dados empíricos (artigos de pesquisa, postmortems) mostram ser necessário ([gap-analysis](references/gap-analysis.md)).
5. Documente os modos de falha reais do domínio — a skill deve combatê-los explicitamente.

### Fase 3 — Design

6. Desenhe o **cérebro (SKILL.md)**: quando usar, quando NÃO usar, roteamento de modos, protocolo em passos, regras não negociáveis, erros comuns.
7. Defina as **referências** (1 nível de profundidade) que serão carregadas sob demanda. Regra: SKILL.md < 500 linhas; detalhe vai para as referências ([writing-guide](references/writing-guide.md)).
8. Decida se há **script determinístico** — uma ferramenta executável (CLI) que automatiza um gate da skill é um forte diferencial.

### Fase 4 — Escrita

9. Escreva em **terceira pessoa imperativa**, com passos numerados e procedimentos claros.
10. Nomes canônicos em inglês para termos de domínio; texto na língua do usuário.
11. Referencie os arquivos com **caminhos relativos com `/`**, um nível de profundidade.

### Fase 5 — Validação

12. Valide contra a especificação ([validation](references/validation.md)): frontmatter (nome = pasta, regex, description ≤ 1024), SKILL.md < 500 linhas, links resolvendo, profundidade.
13. Valide com `skills-ref` (agentskills.io) quando disponível.
14. **Teste a skill com requests reais** — a prova final é o agente seguir o protocolo em um caso real.
15. Atualize o índice do repositório (README) e a documentação de contribuição.

## Regras de mercado (resumo)

- `name`: 1–64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`, idêntico à pasta.
- `description`: 1–1024 chars, terceira pessoa, "o quê + quando usar". É o único metadado de roteamento.
- Estrutura: `SKILL.md` + `references/` + `scripts/` + `assets/` (opcionais).
- Progressive disclosure: carregar sob demanda; nada de README/CHANGELOG dentro da skill.
- "Mecânica ≠ diff final": o SKILL.md descreve o processo verificável, não só o resultado ([writing-guide](references/writing-guide.md)).

## Checklist final

- [ ] Fonte canônica pesquisada e citada no frontmatter (`metadata.fontes`)
- [ ] Skills existentes mapeadas (gap documentado)
- [ ] Diferencial substantivo definido (não é mais uma lista do mesmo)
- [ ] SKILL.md < 500 linhas
- [ ] `name` válido e idêntico à pasta
- [ ] `description` com o quê + quando, ≤ 1024 chars
- [ ] Referências a 1 nível, caminhos `/`
- [ ] Script determinístico incluído se aplicável
- [ ] Validada (`skills-ref`) e testada com request real

## Referências

- [skill-format](references/skill-format.md) — especificação do formato Agent Skills
- [research-protocol](references/research-protocol.md) — como pesquisar o domínio
- [gap-analysis](references/gap-analysis.md) — como achar o diferencial
- [writing-guide](references/writing-guide.md) — como escrever (progressive disclosure, tom, estrutura)
- [validation](references/validation.md) — checklist de validação e testes