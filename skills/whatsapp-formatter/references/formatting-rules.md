# Formatting Rules — Regras Canônicas de Formatação WhatsApp

Fonte: [WhatsApp FAQ](https://faq.whatsapp.com/general/chats/how-to-format-your-messages) + atualizações de Fevereiro 2024 (listas, citações, código embutido).

## Tabela completa de estilos

| Estilo | Símbolo abertura | Símbolo fechamento | Exemplo entrada | Renderiza no WhatsApp | Disponível desde |
| --- | --- | --- | --- | --- | --- |
| **Negrito** | `*` | `*` | `*importante*` | **importante** | 2017 |
| **Itálico** | `_` | `_` | `_ênfase_` | _ênfase_ | 2017 |
| **Tachado** | `~` | `~` | `~errado~` | ~~errado~~ | 2017 |
| **Monoespaçado** | `` ``` `` | `` ``` `` | `` ```código()``` `` | `código()` | 2017 |
| **Código embutido** | `` ` `` | `` ` `` | `` `print(x)` `` | `print(x)` | 2024 |
| **Lista com marcadores** | `- ` | (fim de linha) | `- item 1\n- item 2` | • item 1<br>• item 2 | 2024 |
| **Lista numerada** | `1. ` | (fim de linha) | `1. passo\n2. passo` | 1. passo<br>2. passo | 2024 |
| **Citação de bloco** | `> ` | (fim de linha) | `> cita isso` | > cita isso | 2024 |

## Combinações permitidas

| Combinação | Sintaxe correta (LIFO) | Sintaxe incorreta | Observação |
| --- | --- | --- | --- |
| Negrito + Itálico | `*_texto_*` | `*_texto*_` | Fecha itálico antes do negrito |
| Negrito + Tachado | `*~texto~*` | `*~texto*~` | Fecha tachado antes do negrito |
| Negrito + Itálico + Tachado | `*_~texto~_*` | qualquer outra ordem | LIFO estrito |
| Negrito + Código embutido | `*` `texto` `*` | `*` `texto` `*` | Código embutido combina |
| Itálico + Código embutido | `_` `texto` `_` | `_` `texto` `_` | Código embutido combina |

## Combinações PROIBIDAS

| Combinação | Por que falha | Alternativa |
| --- | --- | --- |
| Monoespaçado + Negrito | Monoespaçado ignora formatação interna | Use código embutido: `` `*negrito*` `` |
| Monoespaçado + Itálico | Mesmo motivo | Use código embutido: `` `_itálico_` `` |
| Monoespaçado + Tachado | Mesmo motivo | Use código embutido: `` `~tachado~` `` |
| Monoespaçado + Código embutido | Redundante e conflita | Use apenas monoespaçado ou apenas inline code |

## Ordem de precedência (para combinação)

Ao combinar estilos, a API aplica na ordem de **precedência crescente** (menor = abre primeiro):

1. **Negrito** (`*`) — menor precedência, abre primeiro
2. **Itálico** (`_`)
3. **Tachado** (`~`)
4. **Código embutido** (`` ` ``)
5. **Monoespaçado** (`` ``` ``) — maior precedência, NÃO combina

Exemplo: `combine("texto", ["bold", "italic", "strikethrough"])`
1. Abre negrito (`*`)
2. Abre itálico (`_`)
3. Abre tachado (`~`)
4. Fecha tachado (`~`)
5. Fecha itálico (`_`)
6. Fecha negrito (`*`)
**Resultado**: `*_~texto~_*`

## Regras de sintaxe (validadas automaticamente)

### Espaçamento (regra #1 de falha)

| Estilo | Correto | Incorreto (não renderiza) |
| --- | --- | --- |
| Negrito | `*texto*` | `* texto *`, `*texto *`, `* texto*` |
| Itálico | `_texto_` | `_ texto _`, `_texto _`, `_ texto_` |
| Tachado | `~texto~` | `~ texto ~`, `~texto ~`, `~ texto~` |
| Monoespaçado | `` ```texto``` `` | `` ``` texto ``` ``, `` ```texto ``` `` |
| Código embutido | `` `texto` `` | `` ` texto ` ``, `` `texto ` `` |
| Lista marcadores | `- item` | `-item`, `-  item` (dois espaços OK mas não padrão) |
| Lista numerada | `1. item` | `1.item`, `1.  item` |
| Citação bloco | `> texto` | `>texto`, `>  texto` |

### Balanceamento de símbolos

- Cada símbolo de abertura **deve** ter fechamento correspondente.
- Contagem de `*` deve ser par.
- Contagem de `_` deve ser par.
- Contagem de `~` deve ser par.
- Contagem de `` ``` `` deve ser par (3 acentos graves = 1 par).
- Contagem de `` ` `` deve ser par.

### Monoespaçado — isolamento estrito

- Conteúdo dentro de `` ``` ``` `` **não pode** conter `*`, `_`, `~`, `` ` ``.
- Se conter, validação falha: "Monoespaçado contém outros símbolos de formatação".

## Compatibilidade por plataforma

| Plataforma | Negrito | Itálico | Tachado | Monoespaçado | Inline Code | Listas | Citações |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Android | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| iOS | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Web | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Desktop | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mac | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Windows | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*Todas as plataformas usam a mesma sintaxe. Listas, citações e inline code lançados em Fev/2024 requerem app atualizado.*

## Exemplos de uso real

### Confirmação de pedido
```text
*✅ Pedido Confirmado!*

> Seu pedido #12345 foi recebido.

*Detalhes:*
- Produto: `Notebook Pro 15`
- Quantidade: `1`
- Total: *R$ 4.999,00*
- Entrega: _3-5 dias úteis_

_Acompanhe em: rastreio.exemplo.com_
```

### Instruções técnicas
```text
*🔧 Instruções*
1. Execute `npm install`
2. Rode `npm test`
3. Verifique ```logs/```
```

### Relatório estruturado
```text
*📊 Relatório - 20/08/2026*
- Processados: `1,234` pedidos
- Receita: *R$ 45.670,00*
- Taxa: `98.5%`

> Sistema operando normalmente.
```

## Checklist rápido (antes de emitir)

- [ ] Zero espaços entre símbolo e texto
- [ ] Todos os símbolos balanceados (pares)
- [ ] Monoespaçado não contém `*`, `_`, `~`, `` ` ``
- [ ] Listas têm espaço após `-` ou `*`
- [ ] Listas numeradas têm espaço após `N.`
- [ ] Citações têm espaço após `>`
- [ ] Combinações seguem LIFO (use `combine()` da API)
- [ ] Não combinou monoespaçado com outros estilos