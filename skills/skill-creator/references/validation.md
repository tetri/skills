# Validation

Como validar uma skill antes de considerá-la pronta. Executável e objetivo — roda-se em cada skill do repositório.

## 1. Validação estrutural (automatizável)

| Verificação | Regra | Como checar |
| --- | --- | --- |
| Pasta = nome | `name` idêntico ao diretório | Comparar regex `^[a-z0-9]+(-[a-z0-9]+)*$` contra o nome e o diretório |
| Description | 1–1024 chars, terceira pessoa | Medir e ler |
| SKILL.md < 500 linhas | limite do cérebro | `(Get-Content SKILL.md).Count` |
| Referências a 1 nível | nenhum caminho `../references/x/sub.md` ou similar | Listar links e validar existência |
| Caminhos com `/` | nunca `\` | Grep por `\` em links |
| Links resolvem | todo link relativo existe | Extrair links do SKILL.md e Test-Path |
| Sem docs de repo na skill | sem README.md/CHANGELOG.md dentro da pasta da skill | Listar arquivos |

## 2. Validação de conformidade (skills-ref)

- Use o validador oficial da especificação **`skills-ref`** (agentskills.io) quando disponível no ambiente.
- Corrija tudo que ele apontar antes de publicar.

## 3. Validação de conteúdo

- **Frontmatter completo:** license, compatibility, metadata (status, fontes) presentes.
- **Quando usar / quando não usar** presentes no SKILL.md.
- **Gates verificáveis:** todo "certifique-se" tem comando ou condição acionável.
- **Referências citadas no corpo** — nenhum arquivo órfão (referência que o SKILL.md nunca cita) e nenhum link morto.
- **Erros comuns a evitar** baseados em modos de falha documentados (não opinião).

## 4. Validação funcional (teste real)

A prova final: **simule o agente executando a skill**.

1. Peça a um agente que carregue a skill e execute um request real do domínio.
2. Verifique se ele seguiu o protocolo na ordem (gates respeitados, referências carregadas).
3. Verifique se os comandos/scripts da skill funcionam no ambiente-alvo (Windows/PowerShell, etc.).
4. Procure "execution blockers": a linha exata onde a skill o força a adivinhar porque a instrução é ambígua.
5. Corrija os pontos ambíguos e repita.

## 5. Publicação

- Atualize o índice (README) com a skill e status.
- Atualize CONTRIBUTING.md se o padrão mudou.
- Commit com mensagem convencional (`feat(skills): adiciona <skill-name>`).

## Checklist final

- [ ] `skills-ref` passa (ou regras estruturais validadas manualmente)
- [ ] SKILL.md < 500 linhas
- [ ] Todos os links resolvem, 1 nível, `/`
- [ ] Sem arquivos órfãos de referência
- [ ] Teste real executado com agente
- [ ] README atualizado