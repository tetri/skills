"""
WhatsApp Message Formatter - Implementação principal
Formata mensagens seguindo rigorosamente os padrões oficiais do WhatsApp.
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum


class WhatsAppStyle(Enum):
    """Estilos de formatação suportados pelo WhatsApp."""
    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    MONOSPACE = "monospace"
    INLINE_CODE = "inline_code"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    BLOCK_QUOTE = "block_quote"


# Mapeamento de estilos para símbolos do WhatsApp
STYLE_SYMBOLS = {
    WhatsAppStyle.BOLD: ("*", "*"),
    WhatsAppStyle.ITALIC: ("_", "_"),
    WhatsAppStyle.STRIKETHROUGH: ("~", "~"),
    WhatsAppStyle.MONOSPACE: ("```", "```"),
    WhatsAppStyle.INLINE_CODE: ("`", "`"),
    WhatsAppStyle.BULLET_LIST: ("- ", ""),
    WhatsAppStyle.NUMBERED_LIST: ("", ""),  # Handled specially
    WhatsAppStyle.BLOCK_QUOTE: ("> ", ""),
}

# Ordem de prioridade para combinação (LIFO - Last In, First Out)
# Estilos que abrem por último devem fechar primeiro
STYLE_PRECEDENCE = [
    WhatsAppStyle.BOLD,
    WhatsAppStyle.ITALIC,
    WhatsAppStyle.STRIKETHROUGH,
    WhatsAppStyle.INLINE_CODE,
    WhatsAppStyle.MONOSPACE,
]

# Monoespaçado NÃO pode ser combinado com outros estilos
NON_COMBINABLE = {WhatsAppStyle.MONOSPACE}


@dataclass
class FormatRule:
    """Regra de validação de formatação."""
    pattern: str
    description: str
    is_error: bool = True


VALIDATION_RULES = [
    FormatRule(
        pattern=r"\*[ \t]+[^*\n]+[ \t]+\*",
        description="Espaços entre asteriscos e texto no negrito",
    ),
    FormatRule(
        pattern=r"_[ \t]+[^_\n]+[ \t]+_",
        description="Espaços entre underscores e texto no itálico",
    ),
    FormatRule(
        pattern=r"~[ \t]+[^~\n]+[ \t]+~",
        description="Espaços entre tils e texto no tachado",
    ),
    FormatRule(
        pattern=r"```[ \t]+[^`\n]+[ \t]+```",
        description="Espaços entre acentos graves triplos e texto no monoespaçado",
    ),
    FormatRule(
        pattern=r"`[ \t]+[^`\n]+[ \t]+`",
        description="Espaços entre acentos graves simples e texto no código embutido",
    ),
    FormatRule(
        pattern=r"^-\S(?!.*-\s)",
        description="Falta espaço após hífen em lista com marcadores",
    ),
    FormatRule(
        pattern=r"^\*\S(?![^\n]*\*)",
        description="Falta espaço após asterisco em lista com marcadores",
    ),
    FormatRule(
        pattern=r"^\d+\.\S",
        description="Falta espaço após número em lista numerada",
        is_error=True,
    ),
    FormatRule(
        pattern=r"^>\S",
        description="Falta espaço após '>' em citação de bloco",
    ),
]


class WhatsAppFormatter:
    """
    Formatador principal para mensagens do WhatsApp.
    Garante formatação 100% compatível com o WhatsApp oficial.
    """

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self._validation_cache: dict[str, bool] = {}

    # ==================== Estilos Básicos ====================

    def bold(self, text: str) -> str:
        """Aplica negrito: *texto*"""
        if not text:
            return ""
        self._validate_no_spaces(text, "*")
        return f"*{text}*"

    def italic(self, text: str) -> str:
        """Aplica itálico: _texto_"""
        if not text:
            return ""
        self._validate_no_spaces(text, "_")
        return f"_{text}_"

    def strikethrough(self, text: str) -> str:
        """Aplica tachado: ~texto~"""
        if not text:
            return ""
        self._validate_no_spaces(text, "~")
        return f"~{text}~"

    def monospace(self, text: str) -> str:
        """Aplica monoespaçado (3 acentos graves): ```texto```"""
        if not text:
            return ""
        self._validate_no_spaces(text, "`", triple=True)
        return f"```{text}```"

    def inline_code(self, text: str) -> str:
        """Aplica código embutido (1 acento grave): `texto`"""
        if not text:
            return ""
        self._validate_no_spaces(text, "`")
        return f"`{text}`"

    # ==================== Estruturas ====================

    def bullet_list(
        self,
        items: List[str],
        marker: str = "-",
        indent: int = 0
    ) -> str:
        """
        Cria lista com marcadores.
        marker: "-" ou "*"
        indent: níveis de indentação (cada nível = 2 espaços)
        """
        if not items:
            return ""
        if marker not in ("-", "*"):
            raise ValueError("Marcador deve ser '-' ou '*'")

        prefix = "  " * indent + f"{marker} "
        return "\n".join(f"{prefix}{item}" for item in items)

    def numbered_list(
        self,
        items: List[str],
        start: int = 1,
        indent: int = 0
    ) -> str:
        """Cria lista numerada: 1. item"""
        if not items:
            return ""

        prefix_base = "  " * indent
        return "\n".join(
            f"{prefix_base}{i}. {item}"
            for i, item in enumerate(items, start=start)
        )

    def block_quote(self, text: str, indent: int = 0) -> str:
        """Cria citação de bloco: > texto"""
        if not text:
            return ""

        prefix = "  " * indent + "> "
        # Preserva quebras de linha dentro da citação
        lines = text.split("\n")
        return "\n".join(f"{prefix}{line}" for line in lines)

    # ==================== Combinação de Estilos ====================

    def combine(self, text: str, styles: List[Union[str, WhatsAppStyle]]) -> str:
        """
        Combina múltiplos estilos na ordem correta (LIFO).
        Ex: combine("texto", ["bold", "italic"]) -> "*_texto_*"
        """
        if not text:
            return ""
        if not styles:
            return text

        # Converte strings para enum
        style_enums = []
        for s in styles:
            if isinstance(s, str):
                try:
                    style_enums.append(WhatsAppStyle(s.lower()))
                except ValueError:
                    raise ValueError(f"Estilo desconhecido: {s}")
            else:
                style_enums.append(s)

        # Valida combinações proibidas
        if WhatsAppStyle.MONOSPACE in style_enums and len(style_enums) > 1:
            raise ValueError(
                "Monoespaçado (```) não pode ser combinado com outros estilos. "
                "Use inline_code (`) para código embutido combinável."
            )

        # Ordena por precedência (menor índice = abre primeiro)
        style_enums.sort(key=lambda s: STYLE_PRECEDENCE.index(s) if s in STYLE_PRECEDENCE else 999)

        # Aplica abertura na ordem, fechamento na ordem inversa (LIFO)
        opens = "".join(STYLE_SYMBOLS[s][0] for s in style_enums)
        closes = "".join(STYLE_SYMBOLS[s][1] for s in reversed(style_enums))

        return f"{opens}{text}{closes}"

    # ==================== Formatação de Templates ====================

    def format_message(self, template: str, **kwargs) -> str:
        """
        Formata template com placeholders.
        Placeholders: {bold:chave}, {italic:chave}, {code:chave}, etc.
        """
        result = template

        # Processa placeholders com formatação
        patterns = {
            r"\{bold:(\w+)\}": lambda m: self.bold(kwargs.get(m.group(1), "")),
            r"\{italic:(\w+)\}": lambda m: self.italic(kwargs.get(m.group(1), "")),
            r"\{strikethrough:(\w+)\}": lambda m: self.strikethrough(kwargs.get(m.group(1), "")),
            r"\{monospace:(\w+)\}": lambda m: self.monospace(kwargs.get(m.group(1), "")),
            r"\{code:(\w+)\}": lambda m: self.inline_code(kwargs.get(m.group(1), "")),
            r"\{(\w+)\}": lambda m: str(kwargs.get(m.group(1), "")),
        }

        for pattern, replacer in patterns.items():
            result = re.sub(pattern, replacer, result)

        return result

    def format_response(
        self,
        title: str = "",
        body: str = "",
        details: Optional[List[str]] = None,
        code_snippet: str = "",
        footer: str = "",
        title_style: str = "bold",
    ) -> str:
        """Formata resposta padrão estruturada."""
        parts = []

        if title:
            style_func = getattr(self, title_style.lower(), self.bold)
            parts.append(style_func(title))

        if body:
            parts.append(body)

        if details:
            parts.append(self.bullet_list(details))

        if code_snippet:
            parts.append(self.inline_code(code_snippet))

        if footer:
            parts.append(footer)

        return "\n\n".join(filter(None, parts))

    # ==================== Validação ====================

    def validate_format(self, text: str) -> bool:
        """
        Valida se a formatação está correta.
        Retorna True se válido, False se houver erros.
        """
        if text in self._validation_cache:
            return self._validation_cache[text]

        errors = self.get_format_errors(text)
        is_valid = len(errors) == 0
        self._validation_cache[text] = is_valid
        return is_valid

    def get_format_errors(self, text: str) -> List[str]:
        """Retorna lista de erros de formatação encontrados."""
        errors = []

        for rule in VALIDATION_RULES:
            matches = re.findall(rule.pattern, text, re.MULTILINE)
            if matches:
                errors.append(f"{rule.description}: {matches[:3]}")

        # Verifica balanceamento de símbolos
        balance_errors = self._check_balance(text)
        errors.extend(balance_errors)

        # Verifica combinações inválidas
        combo_errors = self._check_invalid_combinations(text)
        errors.extend(combo_errors)

        return errors

    def _check_balance(self, text: str) -> List[str]:
        """Verifica se símbolos de abertura/fechamento estão balanceados."""
        errors = []
        pairs = [
            ("*", "*", "negrito"),
            ("_", "_", "itálico"),
            ("~", "~", "tachado"),
            ("```", "```", "monoespaçado"),
            ("`", "`", "código embutido"),
        ]

        for open_sym, close_sym, name in pairs:
            count = text.count(open_sym)
            if count % 2 != 0:
                errors.append(f"Símbolos de {name} desbalanceados: {count} ocorrências")

        return errors

    def _check_invalid_combinations(self, text: str) -> List[str]:
        """Verifica combinações inválidas (ex: monoespaçado com outros)."""
        errors = []

        # Monoespaçado não deve conter outros símbolos de formatação dentro
        monospace_blocks = re.findall(r"```.+?```", text, re.DOTALL)
        for block in monospace_blocks:
            inner = block[3:-3]
            if any(sym in inner for sym in ["*", "_", "~", "`"]):
                errors.append("Monoespaçado contém outros símbolos de formatação (inválido)")

        return errors

    def _validate_no_spaces(self, text: str, symbol: str, triple: bool = False) -> None:
        """Valida se não há espaços entre símbolo e texto."""
        if not self.strict_mode:
            return

        if triple:
            if text.startswith(" ") or text.endswith(" "):
                raise ValueError(f"Monoespaçado não deve ter espaços nas extremidades: '{text}'")
        else:
            if text.startswith(" ") or text.endswith(" "):
                raise ValueError(f"Formatação não deve ter espaços nas extremidades: '{text}'")

    # ==================== Utilitários ====================

    def strip_formatting(self, text: str) -> str:
        """Remove toda formatação WhatsApp do texto."""
        # Remove monoespaçado (3 acentos graves)
        text = re.sub(r"```.+?```", lambda m: m.group(0)[3:-3], text, flags=re.DOTALL)
        # Remove código embutido (1 acento grave)
        text = re.sub(r"`(.+?)`", r"\1", text)
        # Remove negrito
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        # Remove itálico
        text = re.sub(r"_(.+?)_", r"\1", text)
        # Remove tachado
        text = re.sub(r"~(.+?)~", r"\1", text)
        # Remove citações
        text = re.sub(r"^> ", "", text, flags=re.MULTILINE)
        # Remove marcadores de lista
        text = re.sub(r"^[\-\*]\s+", "", text, flags=re.MULTILINE)
        # Remove numeração de lista
        text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

        return text

    def preview(self, text: str) -> str:
        """
        Gera preview de como a mensagem será renderizada (para debug).
        Substitui símbolos por marcações visuais.
        """
        preview = text
        preview = preview.replace("*", "⟪B⟫").replace("_", "⟪I⟫").replace("~", "⟪S⟫")
        preview = preview.replace("```", "⟪M⟫").replace("`", "⟪C⟫")
        preview = preview.replace("> ", "⟪Q⟫ ").replace("- ", "⟪L⟫ ")
        return preview


# ==================== Funções de Conveniência (Module-level) ====================

# Instância singleton para uso direto
_default_formatter = WhatsAppFormatter(strict_mode=True)


def bold(text: str) -> str:
    return _default_formatter.bold(text)


def italic(text: str) -> str:
    return _default_formatter.italic(text)


def strikethrough(text: str) -> str:
    return _default_formatter.strikethrough(text)


def monospace(text: str) -> str:
    return _default_formatter.monospace(text)


def inline_code(text: str) -> str:
    return _default_formatter.inline_code(text)


def bullet_list(items: List[str], marker: str = "-", indent: int = 0) -> str:
    return _default_formatter.bullet_list(items, marker, indent)


def numbered_list(items: List[str], start: int = 1, indent: int = 0) -> str:
    return _default_formatter.numbered_list(items, start, indent)


def block_quote(text: str, indent: int = 0) -> str:
    return _default_formatter.block_quote(text, indent)


def combine(text: str, styles: List[Union[str, WhatsAppStyle]]) -> str:
    return _default_formatter.combine(text, styles)


def format_message(template: str, **kwargs) -> str:
    return _default_formatter.format_message(template, **kwargs)


def validate_format(text: str) -> bool:
    return _default_formatter.validate_format(text)


def get_format_errors(text: str) -> List[str]:
    return _default_formatter.get_format_errors(text)


def strip_formatting(text: str) -> str:
    return _default_formatter.strip_formatting(text)


# ==================== Exportações ====================

__all__ = [
    "WhatsAppFormatter",
    "WhatsAppStyle",
    "FormatRule",
    "bold",
    "italic",
    "strikethrough",
    "monospace",
    "inline_code",
    "bullet_list",
    "numbered_list",
    "block_quote",
    "combine",
    "format_message",
    "validate_format",
    "get_format_errors",
    "strip_formatting",
]