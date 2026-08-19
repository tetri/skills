<#
.SYNOPSIS
  Gate determinístico de refatoração: valida o contrato de diff e o estado de verificação.

.DESCRIPTION
  Executa os gates do protocolo code-refactoring:
    1. Árvore de trabalho estava limpa? (baseline)
    2. O diff de trabalho respeita o contrato (só arquivos do escopo)?
    3. Os comandos de verificação (build/typecheck/testes) passam?
  Exit 0 = todos os gates passaram. Exit != 0 = gate reprovado (mensagem explica qual).

.EXAMPLE
  & .\verify-refactor.ps1 -Scope "src/A.cs,src/B.cs" -BuildCmd "dotnet build" -TestCmd "dotnet test"

.EXAMPLE
  & .\verify-refactor.ps1 -Scope "src" -CheckCmd "tsc --noEmit", "vitest run"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Scope,

    [string]$BuildCmd,
    [string]$TypeCheckCmd,
    [string]$TestCmd,
    [string[]]$CheckCmd = @(),

    [switch]$FailOnUncommittedBaseline
)

$ErrorActionPreference = 'Stop'

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

# Gate 1 - baseline limpa
Invoke-Gate "baseline: arvore de trabalho limpa" {
    $status = git status --porcelain
    if ($status) {
        if ($FailOnUncommittedBaseline) {
            throw "Arvore de trabalho suja antes de refatorar. Commite ou reverta primeiro.`n$status"
        }
        Write-Host "  (aviso) arvore suja; o contrato sera avaliado sobre o diff de trabalho." -ForegroundColor Yellow
    }
}

# Gate 2 - contrato de diff
Invoke-Gate "contrato: diff respeita o escopo '$Scope'" {
    $allowed = @($Scope -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    if ($allowed.Count -eq 0) { throw "Escopo vazio." }

    $changed = @(git diff --name-only --diff-filter=ACDMR)
    $violations = @($changed | Where-Object {
        $f = $_
        -not ($allowed | Where-Object { $f -like "$_*" -or $f -eq $_ })
    })
    if ($violations.Count -gt 0) {
        throw "Arquivos fora do contrato alterados: $($violations -join ', '). Reverta com: git checkout -- <arquivo>"
    }
    Write-Host "  arquivos no diff: $($changed.Count) - $($changed -join ', ')" -ForegroundColor Gray
}

# Gate 3 - verificacao (delta por baseline)
$baselineLog = Join-Path $env:TEMP "verify-refactor-baseline.log"
if (Test-Path $baselineLog) {
    $baseline = Get-Content $baselineLog -Raw
} else {
    $baseline = $null
}

function Invoke-Verify {
    param([string]$Label, [string]$Cmd)
    if (-not $Cmd) { return }
    Write-Host "  [$Label] executando: $Cmd" -ForegroundColor Gray
    $out = & { Invoke-Expression $Cmd } 2>&1
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        $out | Select-Object -First 40
        throw "[$Label] falhou (exit $code)."
    }
    Write-Host "  [$Label] OK (exit 0)" -ForegroundColor Green
}

Invoke-Gate "verificacao: build/typecheck/testes" {
    Invoke-Verify "build" $BuildCmd
    Invoke-Verify "typecheck" $TypeCheckCmd
    Invoke-Verify "testes" $TestCmd
    foreach ($c in $CheckCmd) { Invoke-Verify "check" $c }
}

# Gate 4 - delta de typecheck (se baseline salvo existir e typecheck for fornecido)
if ($TypeCheckCmd -and $baseline -and ($null -ne (git diff --name-only))) {
    Invoke-Gate "delta: nenhum erro NOVO de typecheck vs baseline" {
        $cur = & { Invoke-Expression $TypeCheckCmd } 2>&1
        $curCode = $LASTEXITCODE
        if ($curCode -ne 0) {
            $novos = @($cur | Where-Object { $_ -and ($baseline -notmatch [regex]::Escape($_.Trim())) })
            if ($novos.Count -gt 0) {
                throw "Erros novos de typecheck introduzidos:`n$($novos -join "`n")"
            }
            Write-Host "  (aviso) erros de typecheck iguais aos da baseline - nao atribuidos a esta mudanca." -ForegroundColor Yellow
        }
    }
}

Write-Host "TODOS OS GATES PASSARAM." -ForegroundColor Green
exit 0