#!/usr/bin/env python3
"""
WhatsApp Formatter CLI - Valida e formata mensagens para WhatsApp
Script Python determinístico para uso em automação/CI/CD
"""

import sys
import json
import argparse
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from whatsapp_formatter import (
    validate_format,
    get_format_errors,
    format_message,
    WhatsAppFormatter,
    bold, italic, strikethrough, monospace, inline_code,
    bullet_list, numbered_list, block_quote, combine
)


def validate_message(text: str) -> dict:
    """Valida uma mensagem e retorna resultado estruturado."""
    valid = validate_format(text)
    errors = get_format_errors(text) if not valid else []
    return {
        "valid": valid,
        "errors": errors
    }


def format_template(template: str, params: dict) -> str:
    """Formata template com parâmetros."""
    return format_message(template, **params)


def process_batch_file(input_path: Path, output_path: Path = None, strict: bool = True) -> dict:
    """Processa arquivo com múltiplas mensagens (uma por linha)."""
    content = input_path.read_text(encoding='utf-8')
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
    
    results = []
    for msg in lines:
        validation = validate_message(msg)
        results.append({
            "message": msg,
            "valid": validation["valid"],
            "errors": validation["errors"]
        })
    
    output = {
        "total": len(results),
        "valid": sum(1 for r in results if r["valid"]),
        "invalid": sum(1 for r in results if not r["valid"]),
        "results": results
    }
    
    if output_path:
        output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"Resultados salvos em: {output_path}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    
    return output


def main():
    parser = argparse.ArgumentParser(
        description="WhatsApp Formatter CLI - Valida e formata mensagens WhatsApp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s validate -m "*bold* _italic_"
  %(prog)s validate -m "* bold *" --no-strict
  %(prog)s format -t "{bold:title} - {code:cmd}" -p '{"title":"Deploy","cmd":"npm run deploy"}'
  %(prog)s batch -i mensagens.txt -o resultados.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Valida uma mensagem')
    validate_parser.add_argument('-m', '--message', help='Mensagem a validar')
    validate_parser.add_argument('-i', '--input-file', type=Path, help='Arquivo com mensagens (uma por linha)')
    validate_parser.add_argument('-o', '--output-file', type=Path, help='Arquivo para salvar resultado JSON')
    validate_parser.add_argument('--no-strict', action='store_true', help='Não lança exceção em falha')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Formata template com parâmetros')
    format_parser.add_argument('-t', '--template', required=True, help='Template com placeholders')
    format_parser.add_argument('-p', '--params', required=True, help='Parâmetros JSON (ex: \'{"title":"X"}\')')
    format_parser.add_argument('-o', '--output-file', type=Path, help='Arquivo para salvar resultado')
    
    # Batch command (alias para validate com arquivo)
    batch_parser = subparsers.add_parser('batch', help='Valida arquivo em lote')
    batch_parser.add_argument('-i', '--input-file', required=True, type=Path, help='Arquivo de entrada')
    batch_parser.add_argument('-o', '--output-file', type=Path, help='Arquivo de saída JSON')
    batch_parser.add_argument('--no-strict', action='store_true', help='Não lança exceção em falha')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'validate':
            if args.input_file:
                result = process_batch_file(args.input_file, args.output_file, strict=not args.no_strict)
            elif args.message:
                result = validate_message(args.message)
                output = json.dumps(result, ensure_ascii=False)
                if args.output_file:
                    args.output_file.write_text(output, encoding='utf-8')
                else:
                    print(output)
                
                if not args.no_strict and not result["valid"]:
                    sys.stderr.write(f"Validação falhou: {'; '.join(result['errors'])}\n")
                    sys.exit(1)
            else:
                parser.error("Forneça --message ou --input-file para validação")
        
        elif args.command == 'format':
            params = json.loads(args.params)
            formatted = format_template(args.template, params)
            if args.output_file:
                args.output_file.write_text(formatted, encoding='utf-8')
            else:
                print(formatted)
        
        elif args.command == 'batch':
            result = process_batch_file(args.input_file, args.output_file, strict=not args.no_strict)
    
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Erro JSON nos parâmetros: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Erro: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()