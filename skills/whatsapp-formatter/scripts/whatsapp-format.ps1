<#
.SYNOPSIS
    WhatsApp Formatter CLI - Valida e formata mensagens para WhatsApp

.DESCRIPTION
    Script determinístico para validar e formatar mensagens WhatsApp via linha de comando.
    Implementa os gates de validação mecânicos da skill whatsapp-formatter.
    
    Gates verificados:
    - Gate 1: Espaçamento (regex)
    - Gate 2: Balanceamento de símbolos
    - Gate 3: Monoespaçado isolado
    - Gate 4: Ordem LIFO em combinações
    - Gate 5: Estrutura de listas e citações

.PARAMETER Validate
    Valida uma mensagem e retorna resultado estruturado (JSON).

.PARAMETER Message
    Mensagem a validar (usado com -Validate).

.PARAMETER Format
    Formata uma mensagem usando template + parâmetros.

.PARAMETER Template
    Template com placeholders (ex: "{bold:titulo} {italic:sub}").

.PARAMETER Params
    Hashtable com valores para placeholders (ex: @{titulo="Título"; sub="Sub"}).

.PARAMETER InputFile
    Arquivo com mensagem a validar (uma mensagem por linha ou JSON).

.PARAMETER OutputFile
    Arquivo para salvar resultado (JSON).

.PARAMETER Strict
    Modo estrito (padrão: $true). Lança exceção em validação falhada.

.EXAMPLE
    .\whatsapp-format.ps1 -Validate -Message "*bold* _italic_"
    # Valida mensagem simples

.EXAMPLE
    .\whatsapp-format.ps1 -Validate -Message "* bold *" -Strict:$false
    # Valida sem lançar exceção, retorna JSON com erros

.EXAMPLE
    .\whatsapp-format.ps1 -Format -Template "{bold:title} - {code:cmd}" -Params @{title="Deploy"; cmd="npm run deploy"}
    # Formata template com parâmetros

.EXAMPLE
    .\whatsapp-format.ps1 -Validate -InputFile "mensagens.txt" -OutputFile "resultados.json"
    # Valida arquivo em lote

.EXAMPLE
    .\whatsapp-format.ps1 -Validate -Message (Get-Content "msg.txt" -Raw)
    # Valida conteúdo de arquivo
#>

[CmdletBinding(DefaultParameterSetName='Validate')]
param(
    [Parameter(ParameterSetName='Validate', Mandatory=$true)]
    [switch]$Validate,

    [Parameter(ParameterSetName='Validate', Mandatory=$false)]
    [string]$Message,

    [Parameter(ParameterSetName='Format', Mandatory=$true)]
    [switch]$Format,

    [Parameter(ParameterSetName='Format', Mandatory=$true)]
    [string]$Template,

    [Parameter(ParameterSetName='Format', Mandatory=$true)]
    [hashtable]$Params,

    [Parameter(ParameterSetName='Validate', Mandatory=$false)]
    [string]$InputFile,

    [Parameter(ParameterSetName='Validate', Mandatory=$false)]
    [string]$OutputFile,

    [Parameter(Mandatory=$false)]
    [bool]$Strict = $true
)

# Importa o módulo Python (requer skills/whatsapp-formatter instalado)
function Import-WhatsAppFormatter {
    try {
        # Tenta importar via Python
        $pythonCmd = "python -c \"import sys; sys.path.insert(0, r'$PSScriptRoot\..\src'); from whatsapp_formatter import validate_format, get_format_errors, format_message, WhatsAppFormatter; print('OK')\""
        $result = Invoke-Expression $pythonCmd
        if ($result -eq "OK") {
            return $true
        }
    } catch {
        Write-Error "Falha ao importar whatsapp_formatter. Instale com: pip install -e $PSScriptRoot\.."
        return $false
    }
}

function Validate-Message {
    param(
        [string]$Text,
        [bool]$StrictMode
    )
    
    $escaped = $Text -replace '"', '\"' -replace "`n", '\n' -replace "`r", ''
    $pythonCmd = @"
import sys
sys.path.insert(0, r'$PSScriptRoot\..\src')
from whatsapp_formatter import validate_format, get_format_errors

text = \"\"\"$escaped\"\"\"
valid = validate_format(text)
errors = get_format_errors(text) if not valid else []
import json
print(json.dumps({"valid": valid, "errors": errors}, ensure_ascii=False))
"@

    try {
        $result = python -c $pythonCmd
        return $result | ConvertFrom-Json
    } catch {
        Write-Error "Erro ao executar validação Python: $_"
        return @{valid=$false; errors=@("Erro interno: $_")}
    }
}

function Format-Template {
    param(
        [string]$TemplateText,
        [hashtable]$Parameters
    )
    
    # Converte hashtable para dict Python
    $paramsJson = $Parameters | ConvertTo-Json -Compress -Depth 5
    $escapedTemplate = $TemplateText -replace '"', '\"' -replace "`n", '\n' -replace "`r", ''
    
    $pythonCmd = @"
import sys
sys.path.insert(0, r'$PSScriptRoot\..\src')
from whatsapp_formatter import format_message
import json

template = \"\"\"$escapedTemplate\"\"\"
params = $paramsJson
result = format_message(template, **params)
print(result)
"@

    try {
        $result = python -c $pythonCmd
        return $result
    } catch {
        Write-Error "Erro ao executar formatação Python: $_"
        return $null
    }
}

function Process-BatchFile {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [bool]$StrictMode
    )
    
    $lines = Get-Content $InputPath -Raw
    $messages = $lines -split "`r?`n" | Where-Object { $_ -and $_ -notmatch '^\s*#' }
    
    $results = @()
    foreach ($msg in $messages) {
        $validation = Validate-Message -Text $msg -StrictMode $StrictMode
        $results += @{
            message = $msg
            valid = $validation.valid
            errors = $validation.errors
        }
    }
    
    $output = @{
        total = $results.Count
        valid = ($results | Where-Object { $_.valid }).Count
        invalid = ($results | Where-Object { -not $_.valid }).Count
        results = $results
    } | ConvertTo-Json -Depth 5 -Compress
    
    if ($OutputPath) {
        $output | Set-Content -Path $OutputPath -Encoding UTF8
        Write-Host "Resultados salvos em: $OutputPath"
    } else {
        Write-Host $output
    }
}

# Main
if (-not (Import-WhatsAppFormatter)) {
    exit 1
}

if ($PSCmdlet.ParameterSetName -eq 'Validate') {
    if ($InputFile) {
        Process-BatchFile -InputPath $InputFile -OutputPath $OutputFile -StrictMode $Strict
    } elseif ($Message) {
        $result = Validate-Message -Text $Message -StrictMode $Strict
        $json = $result | ConvertTo-Json -Depth 5 -Compress
        
        if ($OutputFile) {
            $json | Set-Content -Path $OutputFile -Encoding UTF8
        } else {
            Write-Host $json
        }
        
        if ($Strict -and -not $result.valid) {
            Write-Error "Validação falhou: $($result.errors -join '; ')"
            exit 1
        }
    } else {
        Write-Error "Forneça -Message ou -InputFile para validação"
        exit 1
    }
}
elseif ($PSCmdlet.ParameterSetName -eq 'Format') {
    $formatted = Format-Template -TemplateText $Template -Parameters $Params
    if ($formatted) {
        if ($OutputFile) {
            $formatted | Set-Content -Path $OutputFile -Encoding UTF8
        } else {
            Write-Host $formatted
        }
    } else {
        exit 1
    }
}