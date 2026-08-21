# API Reference — API Python para Agentes

Instalação: `pip install -e skills/whatsapp-formatter` (src layout)

## Importação

```python
from whatsapp_formatter import (
    WhatsAppFormatter,
    bold, italic, strikethrough, monospace, inline_code,
    bullet_list, numbered_list, block_quote, combine,
    format_message, validate_format, get_format_errors, strip_formatting
)
```

## Funções de estilo (module-level)

Todas aceitam `str`, retornam `str` formatado. Validação `strict_mode=True` por padrão.

| Função | Sintaxe WhatsApp | Exemplo |
| --- | --- | --- |
| `bold(text)` | `*text*` | `bold("Importante")` → `*Importante*` |
| `italic(text)` | `_text_` | `italic("Ênfase")` → `_Ênfase_` |
| `strikethrough(text)` | `~text~` | `strikethrough("Errado")` → `~Errado~` |
| `monospace(text)` | `` ```text``` `` | `monospace("code()")` → `` ```code()``` `` |
| `inline_code(text)` | `` `text` `` | `inline_code("print(x)")` → `` `print(x)` `` |

### Comportamento
- String vazia → retorna `""`
- Levanta `ValueError` se `strict_mode=True` e houver espaços nas extremidades
- Não valida conteúdo interno (ex: quebras de linha)

## Funções de estrutura

### `bullet_list(items, marker="-", indent=0)`
Cria lista com marcadores.
```python
bullet_list(["Item 1", "Item 2"])
# "- Item 1\n- Item 2"

bullet_list(["Item 1"], marker="*", indent=1)
# "  * Item 1"
```
- `marker`: `"-"` ou `"*"` (levanta `ValueError` se outro)
- `indent`: níveis de indentação (2 espaços por nível)

### `numbered_list(items, start=1, indent=0)`
Cria lista numerada.
```python
numbered_list(["Passo 1", "Passo 2"], start=1)
# "1. Passo 1\n2. Passo 2"

numbered_list(["Item"], start=5, indent=1)
# "  5. Item"
```

### `block_quote(text, indent=0)`
Cria citação de bloco. Preserva quebras de linha.
```python
block_quote("Citação importante")
# "> Citação importante"

block_quote("Linha 1\nLinha 2")
# "> Linha 1\n> Linha 2"
```

## Combinação de estilos

### `combine(text, styles)`
Combina múltiplos estilos na ordem LIFO correta.

```python
combine("Texto", ["bold", "italic"])
# "*_Texto_*"

combine("Texto", ["bold", "strikethrough"])
# "*~Texto~*"

combine("Texto", ["bold", "italic", "strikethrough"])
# "*_~Texto~_*"

combine("funcao()", ["bold", "inline_code"])
# "*`funcao()`*"
```

**Parâmetros**:
- `text: str` — texto a formatar
- `styles: List[Union[str, WhatsAppStyle]]` — lista de estilos

**Estilos válidos**: `"bold"`, `"italic"`, `"strikethrough"`, `"monospace"`, `"inline_code"` (ou enum `WhatsAppStyle`)

**Erros**:
- `ValueError` se `monospace` combinado com outros estilos
- `ValueError` se estilo desconhecido

**Regra**: Monoespaçado (`` ``` ``) é isolado. Use `inline_code` (`` ` ``) para código combinável.

## Templates com placeholders

### `format_message(template, **kwargs)`
Processa template com placeholders formatados.

**Placeholders suportados**:
| Placeholder | Função aplicada |
| --- | --- |
| `{bold:chave}` | `bold(kwargs["chave"])` |
| `{italic:chave}` | `italic(kwargs["chave"])` |
| `{strikethrough:chave}` | `strikethrough(kwargs["chave"])` |
| `{monospace:chave}` | `monospace(kwargs["chave"])` |
| `{code:chave}` | `inline_code(kwargs["chave"])` |
| `{chave}` | `str(kwargs["chave"])` (sem formatação) |

**Exemplo**:
```python
template = """
{bold:titulo}

{italic:subtitulo}

{code:comando}
"""

result = format_message(template,
    titulo="BEM-VINDO",
    subtitulo="Sistema WhatsApp",
    comando="python main.py"
)
# Resultado:
# *BEM-VINDO*
#
# _Sistema WhatsApp_
#
# `python main.py`
```

**Chaves faltando**: retorna string vazia para aquele placeholder.

## Classe WhatsAppFormatter

Instância configurável (útil para `strict_mode=False` ou reuse).

```python
fmt = WhatsAppFormatter(strict_mode=True)
fmt.bold("texto")           # Mesmo que bold("texto")
fmt.combine("x", ["bold"])  # Mesmo que combine("x", ["bold"])
```

### `format_response(title, body, details, code_snippet, footer, title_style="bold")`
Gera resposta estruturada padrão para agentes.

```python
fmt = WhatsAppFormatter()
resp = fmt.format_response(
    title="📋 Relatório",
    body="Processamento concluído.",
    details=["1.234 registros", "0 erros", "Tempo: 2.3s"],
    code_snippet="resultado = processar(lote)",
    footer="Digite *AJUDA* para comandos"
)
# *📋 Relatório*
#
# Processamento concluído.
#
# - 1.234 registros
# - 0 erros
# - Tempo: 2.3s
#
# `resultado = processar(lote)`
#
# Digite *AJUDA* para comandos
```

**Parâmetros** (todos opcionais):
- `title: str` — título (aplica `title_style`)
- `body: str` — corpo da mensagem
- `details: List[str]` — lista de detalhes (usa `bullet_list`)
- `code_snippet: str` — trecho de código (usa `inline_code`)
- `footer: str` — rodapé
- `title_style: str` — `"bold"`, `"italic"`, `"strikethrough"`, `"monospace"`, `"inline_code"`

## Validação

### `validate_format(text) -> bool`
Retorna `True` se formatação válida, `False` caso contrário. Usa cache interno.

```python
validate_format("*bold* _italic_")  # True
validate_format("* bold *")         # False
```

### `get_format_errors(text) -> List[str]`
Retorna lista de erros legíveis (mesma lógica do `validate_format` sem cache).

```python
get_format_errors("* bold *")
# ["Espaços entre asteriscos e texto no negrito: ['* bold *']"]
```

### `strip_formatting(text) -> str`
Remove **toda** formatação WhatsApp, retorna texto puro.

```python
strip_formatting("*Negrito* _Itálico_ ~Tachado~ `Código` ```Mono``` > Citação\n- Item")
# "Negrito Itálico Tachado Código Mono Citação\nItem"
```

**Remove**: negrito, itálico, tachado, monoespaçado, código embutido, blockquote, bullet list, numbered list.

## Enum WhatsAppStyle

```python
from whatsapp_formatter import WhatsAppStyle

WhatsAppStyle.BOLD
WhatsAppStyle.ITALIC
WhatsAppStyle.STRIKETHROUGH
WhatsAppStyle.MONOSPACE
WhatsAppStyle.INLINE_CODE
WhatsAppStyle.BULLET_LIST
WhatsAppStyle.NUMBERED_LIST
WhatsAppStyle.BLOCK_QUOTE
```

Útil para type hints e validação estática.

## Exemplo completo: Agente respondendo status de pedido

```python
from whatsapp_formatter import WhatsAppFormatter, bold, inline_code, monospace, italic

class PedidoAgent:
    def __init__(self):
        self.fmt = WhatsAppFormatter()
    
    def status_pedido(self, pedido: dict) -> str:
        return self.fmt.format_response(
            title=f"📦 Pedido #{pedido['id']}",
            body=f"Status: {bold(pedido['status'])}",
            details=[
                f"Produto: {inline_code(pedido['produto'])}",
                f"Previsão: {italic(pedido['eta'])}",
                f"Rastreio: {monospace(pedido['rastreio'])}"
            ],
            footer="Dúvidas? Digite *AJUDA*"
        )
    
    def erro(self, msg: str) -> str:
        return f"{bold('❌ Erro')}\n\n{msg}\n\nTente novamente ou digite *AJUDA*"

# Uso
agent = PedidoAgent()
print(agent.status_pedido({
    "id": "BR-2024-001",
    "status": "Enviado",
    "produto": "iPhone 15",
    "eta": "2 dias úteis",
    "rastreio": "BR123456789BR"
}))
```

## Dicas de uso para agentes

1. **Sempre valide antes de emitir**: `if not validate_format(msg): regenerate()`
2. **Use `combine()` para múltiplos estilos**: garante LIFO correto
3. **Use `format_response()` para respostas padronizadas**: consistente, testável
4. **Prefira `inline_code` a `monospace`**: combina com outros estilos
5. **`strip_formatting()` para logs/processamento**: remove ruído visual