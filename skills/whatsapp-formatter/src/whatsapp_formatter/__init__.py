"""
WhatsApp Formatter - Formatação nativa para mensagens WhatsApp
Baseado na documentação oficial do WhatsApp (2024)
"""

from .formatter import (
    WhatsAppFormatter,
    WhatsAppStyle,
    bold,
    italic,
    strikethrough,
    monospace,
    inline_code,
    bullet_list,
    numbered_list,
    block_quote,
    combine,
    format_message,
    validate_format,
    get_format_errors,
    strip_formatting,
)

__version__ = "1.0.0"
__author__ = "OpenCode Skills"
__license__ = "MIT"

__all__ = [
    "WhatsAppFormatter",
    "WhatsAppStyle",
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