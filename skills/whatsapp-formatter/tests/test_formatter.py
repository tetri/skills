"""
Testes unitários para o WhatsApp Formatter.
Execute com: python -m pytest tests/test_formatter.py -v
"""

import pytest
from whatsapp_formatter import (
    WhatsAppFormatter,
    WhatsAppStyle,
    bold, italic, strikethrough, monospace, inline_code,
    bullet_list, numbered_list, block_quote, combine,
    format_message, validate_format, get_format_errors, strip_formatting
)


class TestBasicStyles:
    """Testes para estilos básicos."""

    def test_bold(self):
        assert bold("texto") == "*texto*"
        assert bold("") == ""
        assert bold("Olá mundo") == "*Olá mundo*"

    def test_italic(self):
        assert italic("texto") == "_texto_"
        assert italic("") == ""
        assert italic("Olá mundo") == "_Olá mundo_"

    def test_strikethrough(self):
        assert strikethrough("texto") == "~texto~"
        assert strikethrough("") == ""
        assert strikethrough("Olá mundo") == "~Olá mundo~"

    def test_monospace(self):
        assert monospace("texto") == "```texto```"
        assert monospace("") == ""
        assert monospace("code()") == "```code()```"

    def test_inline_code(self):
        assert inline_code("texto") == "`texto`"
        assert inline_code("") == ""
        assert inline_code("print(x)") == "`print(x)`"


class TestLists:
    """Testes para listas."""

    def test_bullet_list_default(self):
        items = ["Item 1", "Item 2"]
        result = bullet_list(items)
        assert result == "- Item 1\n- Item 2"

    def test_bullet_list_asterisk(self):
        items = ["Item 1", "Item 2"]
        result = bullet_list(items, marker="*")
        assert result == "* Item 1\n* Item 2"

    def test_bullet_list_indent(self):
        items = ["Item 1"]
        result = bullet_list(items, indent=1)
        assert result == "  - Item 1"

    def test_bullet_list_empty(self):
        assert bullet_list([]) == ""

    def test_numbered_list_default(self):
        items = ["Passo 1", "Passo 2"]
        result = numbered_list(items)
        assert result == "1. Passo 1\n2. Passo 2"

    def test_numbered_list_start(self):
        items = ["Passo 1"]
        result = numbered_list(items, start=5)
        assert result == "5. Passo 1"

    def test_numbered_list_indent(self):
        items = ["Item"]
        result = numbered_list(items, indent=1)
        assert result == "  1. Item"

    def test_numbered_list_empty(self):
        assert numbered_list([]) == ""

    def test_invalid_marker(self):
        with pytest.raises(ValueError):
            bullet_list(["item"], marker="#")


class TestBlockQuote:
    """Testes para citação de bloco."""

    def test_block_quote_simple(self):
        result = block_quote("Citação")
        assert result == "> Citação"

    def test_block_quote_multiline(self):
        result = block_quote("Linha 1\nLinha 2")
        assert result == "> Linha 1\n> Linha 2"

    def test_block_quote_indent(self):
        result = block_quote("Texto", indent=1)
        assert result == "  > Texto"

    def test_block_quote_empty(self):
        assert block_quote("") == ""


class TestCombinations:
    """Testes para combinações de estilos."""

    def test_bold_italic(self):
        result = combine("texto", ["bold", "italic"])
        assert result == "*_texto_*"

    def test_bold_strikethrough(self):
        result = combine("texto", ["bold", "strikethrough"])
        assert result == "*~texto~*"

    def test_triple_combination(self):
        result = combine("texto", ["bold", "italic", "strikethrough"])
        assert result == "*_~texto~_*"

    def test_inline_code_combinable(self):
        result = combine("funcao()", ["bold", "inline_code"])
        assert result == "*`funcao()`*"

    def test_monospace_not_combinable(self):
        with pytest.raises(ValueError, match="não pode ser combinado"):
            combine("texto", ["monospace", "bold"])

    def test_monospace_not_combinable_with_italic(self):
        with pytest.raises(ValueError, match="não pode ser combinado"):
            combine("texto", ["monospace", "italic"])

    def test_empty_styles(self):
        assert combine("texto", []) == "texto"

    def test_empty_text(self):
        assert combine("", ["bold", "italic"]) == ""

    def test_invalid_style(self):
        with pytest.raises(ValueError, match="Estilo desconhecido"):
            combine("texto", ["invalid_style"])

    def test_enum_styles(self):
        result = combine("texto", [WhatsAppStyle.BOLD, WhatsAppStyle.ITALIC])
        assert result == "*_texto_*"


class TestFormatMessage:
    """Testes para formatação de templates."""

    def test_format_message_basic(self):
        template = "{bold:titulo} - {italic:sub}"
        result = format_message(template, titulo="Título", sub="Sub")
        assert result == "*Título* - _Sub_"

    def test_format_message_all_styles(self):
        template = "{bold:b} {italic:i} {strikethrough:s} {code:c}"
        result = format_message(template, b="B", i="I", s="S", c="C")
        assert result == "*B* _I_ ~S~ `C`"

    def test_format_message_missing_key(self):
        template = "{bold:existente} {italic:faltando}"
        result = format_message(template, existente="OK")
        assert result == "*OK* "

    def test_format_message_plain(self):
        template = "Olá {nome}!"
        result = format_message(template, nome="Mundo")
        assert result == "Olá Mundo!"


class TestFormatResponse:
    """Testes para resposta estruturada."""

    def test_format_response_full(self):
        fmt = WhatsAppFormatter()
        result = fmt.format_response(
            title="Título",
            body="Corpo",
            details=["Item 1", "Item 2"],
            code_snippet="code()",
            footer="Rodapé"
        )
        assert "*Título*" in result
        assert "Corpo" in result
        assert "- Item 1" in result
        assert "`code()`" in result
        assert "Rodapé" in result

    def test_format_response_minimal(self):
        fmt = WhatsAppFormatter()
        result = fmt.format_response(title="Apenas título")
        assert result == "*Apenas título*"

    def test_format_response_custom_title_style(self):
        fmt = WhatsAppFormatter()
        result = fmt.format_response(title="Título", title_style="italic")
        assert result == "_Título_"


class TestValidation:
    """Testes para validação."""

    def test_valid_format(self):
        assert validate_format("*bold* _italic_ ~strike~ `code`") is True
        assert validate_format("Texto simples") is True
        assert validate_format("- Item 1\n- Item 2") is True
        assert validate_format("1. Item\n2. Item") is True
        assert validate_format("> Citação") is True

    def test_invalid_spaces_bold(self):
        assert validate_format("* texto *") is False
        errors = get_format_errors("* texto *")
        assert any("negrito" in e.lower() for e in errors)

    def test_invalid_spaces_italic(self):
        assert validate_format("_ texto _") is False
        errors = get_format_errors("_ texto _")
        assert any("itálico" in e.lower() for e in errors)

    def test_invalid_spaces_strikethrough(self):
        assert validate_format("~ texto ~") is False
        errors = get_format_errors("~ texto ~")
        assert any("tachado" in e.lower() for e in errors)

    def test_invalid_spaces_monospace(self):
        assert validate_format("``` texto ```") is False
        errors = get_format_errors("``` texto ```")
        assert any("monoespaçado" in e.lower() for e in errors)

    def test_invalid_spaces_inline_code(self):
        assert validate_format("` texto `") is False
        errors = get_format_errors("` texto `")
        assert any("código embutido" in e.lower() for e in errors)

    def test_invalid_bullet_list_space(self):
        assert validate_format("-Item") is False
        errors = get_format_errors("-Item")
        assert any("marcadores" in e.lower() for e in errors)

    def test_invalid_numbered_list_space(self):
        assert validate_format("1.Item") is False
        errors = get_format_errors("1.Item")
        assert any("numerada" in e.lower() for e in errors)

    def test_invalid_block_quote_space(self):
        assert validate_format(">Citação") is False
        errors = get_format_errors(">Citação")
        assert any("citação" in e.lower() for e in errors)

    def test_unbalanced_symbols(self):
        assert validate_format("*texto") is False
        errors = get_format_errors("*texto")
        assert any("desbalanceados" in e.lower() for e in errors)

    def test_monospace_with_inner_formatting(self):
        assert validate_format("```*texto*```") is False
        errors = get_format_errors("```*texto*```")
        assert any("monoespaçado contém" in e.lower() for e in errors)


class TestStripFormatting:
    """Testes para remoção de formatação."""

    def test_strip_basic(self):
        text = "*Negrito* _Itálico_ ~Tachado~ `Código`"
        result = strip_formatting(text)
        assert result == "Negrito Itálico Tachado Código"

    def test_strip_monospace(self):
        text = "```mono```"
        result = strip_formatting(text)
        assert result == "mono"

    def test_strip_block_quote(self):
        text = "> Citação"
        result = strip_formatting(text)
        assert result == "Citação"

    def test_strip_lists(self):
        text = "- Item 1\n- Item 2\n1. Numero"
        result = strip_formatting(text)
        assert result == "Item 1\nItem 2\nNumero"

    def test_strip_mixed(self):
        text = "*Título*\n> Citação\n- Item\n`code`"
        result = strip_formatting(text)
        assert "Título" in result
        assert "Citação" in result
        assert "Item" in result
        assert "code" in result


class TestWhatsAppFormatterClass:
    """Testes da classe WhatsAppFormatter."""

    def test_instance_creation(self):
        fmt = WhatsAppFormatter()
        assert fmt.strict_mode is True

    def test_instance_strict_false(self):
        fmt = WhatsAppFormatter(strict_mode=False)
        assert fmt.strict_mode is False

    def test_methods_delegate_to_functions(self):
        fmt = WhatsAppFormatter()
        assert fmt.bold("x") == bold("x")
        assert fmt.italic("x") == italic("x")
        assert fmt.strikethrough("x") == strikethrough("x")
        assert fmt.monospace("x") == monospace("x")
        assert fmt.inline_code("x") == inline_code("x")
        assert fmt.bullet_list(["x"]) == bullet_list(["x"])
        assert fmt.numbered_list(["x"]) == numbered_list(["x"])
        assert fmt.block_quote("x") == block_quote("x")
        assert fmt.combine("x", ["bold"]) == combine("x", ["bold"])


class TestEdgeCases:
    """Testes de casos extremos."""

    def test_special_characters(self):
        assert bold("🎉 Emoji") == "*🎉 Emoji*"
        assert italic("Café 🍵") == "_Café 🍵_"
        assert monospace("café") == "```café```"

    def test_newlines_in_formatting(self):
        # WhatsApp não suporta quebras dentro de formatação inline
        # Mas o formatter não deve quebrar
        result = bold("Linha 1\nLinha 2")
        assert result == "*Linha 1\nLinha 2*"

    def test_nested_lists(self):
        # Current implementation applies same indent to all items
        result = bullet_list(["Pai", "Filho"], indent=1)
        assert "  - Pai" in result
        assert "  - Filho" in result
        
        # For true nesting, caller must handle indentation manually
        result2 = bullet_list(["Pai", "  Filho"], indent=0)
        assert "- Pai" in result2
        assert "-   Filho" in result2

    def test_preview_method(self):
        fmt = WhatsAppFormatter()
        preview = fmt.preview("*bold* _italic_")
        assert "⟪B⟫" in preview
        assert "⟪I⟫" in preview


class TestIntegrationScenarios:
    """Testes de cenários de integração real."""

    def test_welcome_message(self):
        fmt = WhatsAppFormatter()
        msg = fmt.format_response(
            title="🎉 Bem-vindo!",
            body="Obrigado por se cadastrar.",
            details=["Acesse sua conta", "Configure perfil"],
            footer="Digite *AJUDA*"
        )
        assert validate_format(msg) is True

    def test_order_confirmation(self):
        fmt = WhatsAppFormatter()
        msg = f"""{fmt.bold('✅ Confirmado')}
{fmt.block_quote('Pedido #123 processado')}
{fmt.bullet_list([f'Item: {fmt.inline_code("Produto")}', f'Valor: {fmt.bold("R$ 100")}'])}"""
        assert validate_format(msg) is True

    def test_technical_instructions(self):
        fmt = WhatsAppFormatter()
        msg = f"""{fmt.bold('🔧 Instruções')}
{fmt.numbered_list([
    f'Execute {fmt.inline_code("npm install")}',
    f'Rode {fmt.inline_code("npm test")}',
    f'Verifique {fmt.monospace("logs/")}'
])}"""
        assert validate_format(msg) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])