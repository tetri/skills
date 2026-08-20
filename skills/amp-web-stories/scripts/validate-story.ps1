<#
.SYNOPSIS
  Gate determinístico de Web Story AMP: valida markup essencial e roda o validador oficial AMP.

.DESCRIPTION
  Executa os gates do protocolo amp-web-stories:
    1. Estrutura do documento (doctype, <html amp>, charset, viewport, boilerplate)
    2. Self-canonical byte-a-byte vs a URL fornecida (ou presença do tag)
    3. <amp-story> como único filho de <body> + runtime/componente no <head>
    4. Metadados obrigatórios (standalone, title, publisher, publisher-logo-src, poster-portrait-src)
    5. Validação autoritativa com o validador oficial AMP (amphtml-validator via npx)
  Exit 0 = todos os gates passaram. Exit != 0 = gate reprovado (mensagem explica qual).

.EXAMPLE
  & .\validate-story.ps1 -Story .\story.html -Canonical "https://site.com/stories/my-story"

.EXAMPLE
  & .\validate-story.ps1 -Story .\story.html
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Story,

    [string]$Canonical
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Story)) {
    Write-Host "[FAIL] arquivo não encontrado: $Story" -ForegroundColor Red
    exit 1
}

$html = Get-Content -LiteralPath $Story -Raw

function Invoke-Gate {
    param([string]$Name, [scriptblock]$Body)
    try {
        & $Body
        Write-Host "[PASS] $Name" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAIL] $Name - $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Gate 1 - estrutura do documento
Invoke-Gate "estrutura: documento AMP básico" {
    if ($html -notmatch '(?i)<!doctype\s+html>') { throw "faltando <!doctype html>." }
    if ($html -notmatch '<html[^>]*\b(amp|⚡)\b') { throw "<html> sem o atributo amp (ou ⚡)." }
    if ($html -notmatch '(?i)<meta[^>]*charset') { throw "faltando <meta charset>." }
    if ($html -notmatch '(?i)<meta[^>]*name="viewport"') { throw "faltando <meta viewport>." }
    if ($html -notmatch 'amp-boilerplate') { throw "faltando amp-boilerplate (página pisca e pode falhar validação)." }
}

# Gate 2 - self-canonical
Invoke-Gate "canonical: self-referencing da story" {
    $link = [regex]::Match($html, '(?i)<link[^>]*rel=["'']canonical["''][^>]*>|(?i)<link[^>]*rel=["'']canonical["'']')
    if (-not $link.Success) { throw "faltando <link rel=canonical> no head." }

    $href = [regex]::Match($link.Value, '(?i)href=["'']([^"'']+)["'']')
    if (-not $href.Success) { throw "<link rel=canonical> sem href." }

    if ($Canonical) {
        if ($href.Groups[1].Value -ne $Canonical) {
            throw "canonical href [$($href.Groups[1].Value)] difere da URL servida [$Canonical]. Deve ser byte-a-byte (protocolo, trailing slash, query, www)."
        }
    }
}

# Gate 3 - amp-story único filho do body + runtime no head
Invoke-Gate "estrutura: amp-story como único filho do body" {
    if ($html -notmatch '(?s)<body[^>]*>\s*<amp-story\b') { throw "<amp-story> não é o primeiro elemento do <body>." }
    if ($html -notmatch '(?s)</amp-story>\s*</body>') { throw "</amp-story> não precede </body> (a story deve ser o único filho do body)." }
    if ($html -notmatch '<script[^>]*custom-element="amp-story"[^>]*src="https://cdn\.ampproject\.org/v0/amp-story') {
        throw "faltando <script custom-element=amp-story> do runtime no head."
    }
}

# Gate 4 - metadados obrigatórios
Invoke-Gate "metadados: atributos obrigatórios do amp-story" {
    $tag = [regex]::Match($html, '(?s)<amp-story\b[^>]*>')
    if (-not $tag.Success) { throw "<amp-story> não encontrado." }

    foreach ($attr in @('standalone', 'title=', 'publisher=', 'publisher-logo-src=', 'poster-portrait-src=')) {
        if ($tag.Value -notmatch [regex]::Escape($attr)) { throw "atributo obrigatório ausente: $attr." }
    }
}

# Gate 5 - validador oficial AMP
Invoke-Gate "validação autoritativa: amphtml-validator" {
    & npx --yes amphtml-validator $Story
    if ($LASTEXITCODE -ne 0) { throw "validador oficial AMP reprovou a story (exit $LASTEXITCODE)." }
}

Write-Host ""
Write-Host "Story VÁLIDA: todos os gates passaram." -ForegroundColor Green
exit 0