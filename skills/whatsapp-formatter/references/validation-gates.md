# Validation Gates — Gates de Validação Mecânicos

Gates executáveis que impedem mensagens inválidas de serem emitidas. Cada gate tem: **condição → verificação → ação em falha**.

## Gate 1 — Espaçamento (regex)

**Condição**: símbolo de formatação não deve ter espaços/tabs entre ele e o texto.

| Estilo | Regex de detecção | Erro retornado |
| --- | --- | --- |
| Negrito | `\*[ \t]+[^*\n]+[ \t]+\*` | "Espaços entre asteriscos e texto no negrito" |
| Itálico | `_[ \t]+[^_\n]+[ \t]+_` | "Espaços entre underscores e texto no itálico" |
| Tachado | `~[ \t]+[^~\n]+[ \t]+~` | "Espaços entre tils e texto no tachado" |
| Monoespaçado | `````[ \t]+[^`\n]+[ \t]+``` `` | "Espaços entre acentos graves triplos e texto no monoespaçado" |
| Código embutido | `` `[ \t]+[^`\n]+[ \t]+` `` | "Espaços entre acentos graves simples e texto no código embutido" |
| Lista marcadores | `^[-\*][^\s]` | "Falta espaço após marcador em lista" |
| Lista numerada | `^\d+\.[^\s]` | "Falta espaço após número em lista numerada" |
| Citação bloco | `^>[^\s]` | "Falta espaço após '>' em citação de bloco" |

**Ação em falha**: Rejeite a mensagem. Retorne lista de erros com trecho problemático.

## Gate 2 — Balanceamento de símbolos

**Condição**: cada símbolo de abertura deve ter fechamento correspondente (contagem par).

| Símbolo | Verificação | Erro se ímpar |
| --- | --- | --- |
| `*` | `count('*') % 2 == 0` | "Símbolos de negrito desbalanceados: N ocorrências" |
| `_` | `count('_') % 2 == 0` | "Símbolos de itálico desbalanceados: N ocorrências" |
| `~` | `count('~') % 2 == 0` | "Símbolos de tachado desbalanceados: N ocorrências" |
| `` ``` `` | `count('```') % 2 == 0` | "Símbolos de monoespaçado desbalanceados: N ocorrências" |
| `` ` `` | `count('`') % 2 == 0` | "Símbolos de código embutido desbalanceados: N ocorrências" |

**Ação em falha**: Rejeite. Indique qual símbolo está desbalanceado e contagem.

## Gate 3 — Monoespaçado isolado

**Condição**: blocos `` ``` ``` `` não contêm outros símbolos de formatação.

**Verificação**:
```python
monospace_blocks = re.findall(r"```.+?```", text, re.DOTALL)
for block in monospace_blocks:
    inner = block[3:-3]  # remove ``` ```
    if any(sym in inner for sym in ["*", "_", "~", "`"]):
        return False, "Monoespaçado contém outros símbolos de formatação (inválido)"
```

**Ação em falha**: Rejeite. Sugira usar código embutido (`` ` ``) se precisa combinar.

## Gate 4 — Ordem LIFO em combinações

**Condição**: ao combinar estilos, fechamento deve ser inverso da abertura.

**Verificação**: A API `combine()` garante isso automaticamente. Se usuário concatenar manualmente, valide:

```python
# Padrão correto LIFO para bold+italic
expected = "*_texto_*"
# Padrão incorreto
wrong = "*_texto*_"
```

**Ação em falha**: Rejeite. Explique: "Primeiro a abrir = último a fechar. Use `combine(texto, ['bold', 'italic'])`.

## Gate 5 — Estrutura de listas e citações

**Condição**: listas e citações seguem padrão de linha.

| Tipo | Padrão válido | Padrão inválido |
| --- | --- | --- |
| Bullet list | `^- .+$` (multilinha) | `^-` sem texto, `-item` |
| Numbered list | `^\d+\. .+$` | `1.item`, `1.` sem texto |
| Block quote | `^> .+$` | `>texto`, `>` sem texto |

**Ação em falha**: Rejeite com erro específico por linha.

## Pipeline de validação completo

```python
def validate_message(text: str) -> ValidationResult:
    errors = []
    
    # Gate 1: Espaçamento
    errors.extend(check_spacing(text))
    
    # Gate 2: Balanceamento
    errors.extend(check_balance(text))
    
    # Gate 3: Monoespaçado isolado
    errors.extend(check_monospace_isolation(text))
    
    # Gate 4: LIFO (apenas se detectar combinação manual)
    errors.extend(check_lifo_order(text))
    
    # Gate 5: Estrutura listas/citações
    errors.extend(check_structure(text))
    
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors
    )
```

## Saída de erro padronizada

```json
{
  "valid": false,
  "errors": [
    {
      "gate": "spacing",
      "style": "bold",
      "message": "Espaços entre asteriscos e texto no negrito",
      "snippet": "* bold *",
      "fix": "Remova espaços: *texto* não * texto *"
    },
    {
      "gate": "balance",
      "style": "italic",
      "message": "Símbolos de itálico desbalanceados: 3 ocorrências",
      "snippet": "_início _meio fim",
      "fix": "Adicione underscore de fechamento ou remova o extra"
    }
  ]
}
```

## Integração com agente

```python
# No agente, ANTES de emitir mensagem WhatsApp:
result = validate_format(mensagem_pronta)
if not result.valid:
    # Não emita — regenere ou corrija
    for err in result.errors:
        logger.warning(f"Gate {err.gate} falhou: {err.message} | Trecho: {err.snippet}")
    # Tente auto-correção simples
    mensagem_corrigida = auto_fix(mensagem_pronta, result.errors)
    # Re-valide
    if validate_format(mensagem_corrigida).valid:
        emit(mensagem_corrigida)
    else:
        raise ValidationError("Mensagem não pode ser corrigida automaticamente")
else:
    emit(mensagem_pronta)
```

## Checklist de validação (para revisão manual)

- [ ] Gate 1: Nenhum espaço entre símbolo e texto
- [ ] Gate 2: Todos os símbolos balanceados (pares)
- [ ] Gate 3: Monoespaçado isolado (sem `*`, `_`, `~`, `` ` `` internos)
- [ ] Gate 4: Combinações seguem LIFO (use API `combine()`)
- [ ] Gate 5: Listas e citações têm espaço após marcador