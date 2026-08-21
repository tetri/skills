---
name: whatsapp-formatter
description: Formata mensagens para WhatsApp com validação automática de sintaxe, gates de verificação (espaços, balanceamento, combinações inválidas) e API para agentes de IA. Use quando um agente precisar emitir mensagens prontas para copiar/colar no WhatsApp (negrito, itálico, listas, citações, código, monoespaçado).
license: MIT
compatibility: Windows/PowerShell, Python 3.10+, agnóstica de plataforma
metadata:
  categoria: comunicacao
  fontes: WhatsApp-FAQ-2024, TechTudo-2024, G1-WhatsApp-Formatacao-2024
  status: publicado
---

# WhatsApp Formatter

Garante que agentes de IA emitam mensagens **100% compatíveis** com a formatação nativa do WhatsApp (Android, iOS, Web, Desktop). A skill combina **regras canônicas** da documentação oficial com **gates de validação mecânicos** que impedem erros silenciosos (espaços, símbolos desbalanceados, monoespaçado combinado).

## Quando usar

- Um agente precisa responder no formato WhatsApp (chatbots, assistentes, automações).
- Formatar relatórios, confirmações, instruções técnicas, lembretes para WhatsApp.
- Validar se uma mensagem já formatada está correta antes de enviar.
- Remover formatação WhatsApp para processamento de texto puro.

## Quando NÃO usar

- Formatação para outras plataformas (Slack usa `*bold*`, Discord usa `**bold**`, Telegram usa HTML/Markdown).
- Mensagens que não serão enviadas via WhatsApp.
- Criar formatação visual complexa (tabelas, imagens, botões) — WhatsApp não suporta.

## Modos de operação

| Modo | Quando aplicar | Carregar referência |
| --- | --- | --- |
| `format-message` | Agente precisa construir mensagem do zero | [formatting-rules](references/formatting-rules.md) + [api-reference](references/api-reference.md) |
| `validate-message` | Verificar mensagem existente antes de enviar | [validation-gates](references/validation-gates.md) |
| `strip-formatting` | Remover formatação para processar texto | [api-reference](references/api-reference.md) |
| `combine-styles` | Aplicar múltiplos estilos com ordem LIFO correta | [formatting-rules](references/formatting-rules.md) |

## Protocolo obrigatório

### Gate 0 — Conhecer as regras canônicas (antes de formatar)

1. **Leia [formatting-rules](references/formatting-rules.md)** — tabela completa de símbolos, combinações permitidas/proibidas, ordem LIFO.
2. **Memorize os 5 erros fatais**: espaços entre símbolo e texto, símbolos desbalanceados, monoespaçado combinado, lista sem espaço após marcador, citação sem espaço após `>`.

### Gate 1 — Formatar com API (modo `format-message`)

3. Use funções da API em [api-reference](references/api-reference.md): `bold()`, `italic()`, `bullet_list()`, `combine()`, `format_message()`, `WhatsAppFormatter.format_response()`.
4. **Nunca concatene símbolos manualmente** — use a API para garantir ordem LIFO e validação.
5. Para respostas estruturadas de agentes, use `WhatsAppFormatter.format_response()` com `title`, `body`, `details`, `code_snippet`, `footer`.

### Gate 2 — Validar antes de emitir (modo `validate-message`)

6. Execute `validate_format(mensagem)` — retorna `True`/`False`.
7. Se `False`, execute `get_format_errors(mensagem)` para lista de erros acionáveis.
8. **Não emita mensagem inválida** — corrija ou regere.

### Gate 3 — Script determinístico (para automação/CI)

9. Use `scripts/whatsapp-format.ps1` para validar/formatar via CLI:
   ```powershell
   .\scripts/whatsapp-format.ps1 -Validate -Message "*bold* _italic_"
   .\scripts/whatsapp-format.ps1 -Format -Template "{bold:title}" -Params @{title="Título"}
   ```

## Regras não negociáveis

- **Zero espaços** entre símbolo e texto: `*texto*` ✓ | `* texto *` ✗ (não renderiza).
- **Ordem LIFO**: primeiro a abrir = último a fechar. `*_texto_*` ✓ | `*_texto*_` ✗.
- **Monoespaçado isolado**: ``` `texto` ``` NÃO combina com `*`, `_`, `~`, `` ` ``. Use `` `texto` `` (inline code) para combinar.
- **Listas e citações exigem espaço**: `- item` ✓ | `-item` ✗. `> texto` ✓ | `>texto` ✗.
- **Universal**: mesmo símbolo funciona em Android, iOS, Web, Desktop, Mac, Windows.

## Erros comuns a evitar (modos de falha documentados)

- Espaço após asterisco: `* negrito *` → WhatsApp ignora formatação.
- Esquecer fechamento: `*início` → renderiza literal.
- Combinar monoespaçado: ``` `*negrito*` ``` → monoespaçado ignora asteriscos internos.
- Lista sem espaço: `-Item 1` → não vira bullet.
- Citação sem espaço: `>Citação` → não vira blockquote.
- Ordem errada em combinação: `*_texto*_` → itálico "vaza" para fora.
- Assumir que `_` é sublinhado → no WhatsApp `_texto_` = itálico (sublinhado não existe nativo).

## Referências

- [formatting-rules](references/formatting-rules.md) — Tabela completa de símbolos, combinações, precedência, plataformas
- [validation-gates](references/validation-gates.md) — Regras de validação, padrões regex, mensagens de erro
- [api-reference](references/api-reference.md) — API Python completa: funções, classe, parâmetros, exemplos
- [scripts/whatsapp-format.ps1](scripts/whatsapp-format.ps1) — CLI PowerShell para validar/formatar em automação
- [scripts/whatsapp-format.py](scripts/whatsapp-format.py) — CLI Python para validar/formatar em automação/CI
- [assets/templates.json](assets/templates.json) — Templates prontos para casos de uso comuns