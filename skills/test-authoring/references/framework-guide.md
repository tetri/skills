# Framework Guide

Frameworks de teste e comandos por stack. Use para o Gate 0 (baseline) e o Gate 2 (verificação) da skill test-authoring.

## .NET / C#

- **xUnit** (padrão moderno), **NUnit**, **MSTest**.
- Comando: `dotnet test` (toda a solução) ou `dotnet test <proj>`.
- Asserções: `Assert.Equal`, `Assert.Throws<T>` (xUnit), `Assert.True/False`.
- Golden: `Verify` (Verify.MSTest/xUnit/NUnit) — snapshot files versionados.
- Fuzz: `Microsoft.NETCore.App` + `FluentAssertions`; ou `FsCheck` (property-based).

## TypeScript / JavaScript

- **Vitest** (rápido, TS nativo), **Jest** (ecossistema maior).
- Comando: `vitest run`, `jest --ci`.
- Asserções: `expect(x).toEqual(...)`, `expect(fn).toThrow()`.
- Golden/snapshot: `expect(x).toMatchSnapshot()` (Jest) ou `vitest` snapshot.
- Fuzz: `fast-check` (property-based).
- Cobertura: `vitest --coverage`, `jest --coverage`.

## Python

- **pytest** (padrão), **unittest** (stdlib).
- Comando: `pytest -q` ou `python -m pytest`.
- Asserções: `assert x == y`, `pytest.raises(SomeError)`.
- Golden: `pytest-regressions` (num_regression/file_regression/image_regression) ou `pytest-snapshot`.
- Fuzz: `hypothesis` (property-based).
- Cobertura: `pytest --cov` (pytest-cov).

## Go

- **testing** (stdlib), **testify** (assert), **golang.org/x/tools** para table-driven.
- Comando: `go test ./...` ou `go test ./<pkg>/...`.
- Golden: `golden` package (gotest.tools) ou arquivos `.golden`.
- Fuzz: fuzzing nativo (`FuzzXxx` + `go test -fuzz`).
- Cobertura: `go test -cover ./...`.

## Rust

- **built-in** (`#[test]`, `#[cfg(test)]`).
- Comando: `cargo test`.
- Asserções: `assert_eq!`, `assert!`, `#[should_panic]`.
- Golden: `insta` (snapshot testing) — revisão de snapshots via `cargo insta review`.
- Fuzz: `proptest` (property-based) ou `cargo-fuzz`.

## Java

- **JUnit 5** (padrão), **TestNG**.
- Comando: `mvn -q test` ou `./gradlew test`.
- Asserções: `assertEquals`, `assertThrows`, `assertThat` (AssertJ/Hamcrest).
- Golden: `AssertJ` + `ApprovalTests` (approval testing).
- Fuzz: `jqwik` (property-based).
- Cobertura: `mvn jacoco:report`, `./gradlew jacocoTestReport`.

## PowerShell

- **Pester 5**.
- Comando: `Invoke-Pester`.
- Asserções: `Should -Be`, `Should -Throw`.
- Cobertura: `Invoke-Pester -CodeCoverage`.

## Regras transversais

- Rode a suíte **rápida** na área tocada a cada passo; a suíte completa pelo menos uma vez por dia.
- Todo teste novo: injete a falha e confirme que falha (Gate de sensibilidade).
- Snapshot/golden files são **versionados** e sua alteração exige revisão — são contrato.
- Se a stack não está na lista, determine o comando padrão do ecossistema (test runner oficial) e declare o delta no relatório.