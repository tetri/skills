# Dependency Ordering

Ordenar os passos de refatoração pelo **grafo de dependências**, não pela ordem textual ou estética. Refatorar folhas (sem dependentes) antes de raízes (muitos importadores) mantém o código compilável a cada passo e localiza erros.

## Construir o grafo

1. Liste os símbolos a tocar e os arquivos que os referenciam.
2. Para cada arquivo-alvo, conte os **importadores** (quem o importa/usa):
   - TypeScript: `import`/`require`/dynamic `import()`.
   - Python: `import`/`from ... import`/`__import__`.
   - Go/Rust/Java/.NET: declarações de import/package/using.
   - Use `rg '<nome-do-modulo>|<símbolo>' --type <lang>` + LSP references para confirmar.
3. Use `git log -S'<símbolo>'` para achar usos históricos que o estático não vê.
4. Registre a lista de **callers** de cada símbolo alterado (é a sua worklist de verificação).

## Regras de ordenação

- **Folhas primeiro:** refatore arquivos/módulos sem dependentes (fan-out 0) antes dos que são importados.
- **Fan-out crescente:** dos menores importadores para os maiores. Nunca comece pela raiz de alto fan-out.
- **"Conte os callers primeiro":**
  - 0 callers → candidato a exclusão/remoção (ver dead-code em equivalence-gates).
  - 1 caller → candidato a inline (se o nível de indireção não justifica).
  - 2–3 callers → avalie; refatore com os callers no contrato.
  - 4+ callers → NÃO refatore em um passo; exige plano de decomposição e contratos de arquivos.
- **Barreira de fan-out:** arquivo com fan-out acima do limite prático (defina: >5 importadores) só pode ser tocado com plano explícito de passos e contrato de arquivos aprovado.

## Blast radius

- Blast radius = tamanho da superfície afetada (arquivos a alterar + arquivos que dependem deles e precisam ser verificados).
- >5 arquivos → modo `refactor-scoped`/`refactor-migration` obrigatório, com plano em fases.
- Estime verificando: mudança de assinatura, move de módulo e troca de abstração propagam para todos os importadores.
- Rote o tamanho:
  - 1 arquivo / baixo risco → `refactor-local`.
  - Vários arquivos / uma responsabilidade → `refactor-scoped`.
  - Migração com muitos consumidores → `refactor-migration` + expand-contract.

## Contrato de arquivos

- Defina o conjunto exato de arquivos que a mudança pode tocar (o "contrato").
- O gate `git diff --name-only` só pode listar arquivos do contrato — zero diff fora dele.
- Para mudanças de assinatura/API: o contrato inclui TODOS os callers que serão atualizados no mesmo commit (renomear símbolo e deixar caller antigo = código quebrado).

## Dependências implícitas (o que o estático não vê)

Verifique explicitamente antes de mover/excluir:

- Imports dinâmicos (`import(variable)`, `require(variable)`, `__import__`, `eval`).
- Reflection (`getattr`, `Invoke`, `ServiceLoader`, DI containers, registros de plugins).
- Glob de arquivos / convenção de nomes (frameworks que carregam por path).
- Arquivos gerados e manifests que referenciam símbolos (`.proto`, migrations, IaC, index/barrel exports).
- Configuração que injeta implementações (XML/JSON de DI).

Se qualquer dependência implícita referenciar o símbolo, inclua o arquivo no contrato ou preserve o símbolo.

## Sequência típica para split/move (exemplo)

1. Folhas de menor fan-out (pure functions, data classes).
2. Mover função → criar delegação no local antigo → inline nos callers (Move Function em passos).
3. Migrar callers em lotes (mantendo shim/facade de transição).
4. Remover shim/facade apenas quando zero callers restarem (verifique com `rg`).
5. Re-exports: remova só depois de migrar todos os imports (nunca no mesmo passo da migração).