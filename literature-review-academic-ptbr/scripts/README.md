# Scripts da skill `literature-review-academic-ptbr`

Hard gates de verificação executados localmente via Claude Code ou
CLI. Não embarcados no zip de distribuição (Claude.ai e Claude
Desktop não executam Python). Versionados no repositório da skill
para rastro deliberativo, mas operados fora do runtime da skill.

## Estado atual

Subset prioritário da Fase 4 (Frente 3 do roadmap v3.4) implementado
em 2026-04-25:

- `doi_verify.py` — verificação de existência e consistência de DOI
  via CrossRef com fallback OpenAlex.
- `bib_consistency.py` — verificação bidirecional de citações no
  texto contra entradas em `.bib`.

Componentes adiados da §(iii) do `_phase2-handoff.md` (registrados na
Sub-31.5 da decisão 31 do `_changelog.md`): `style_formatter.py`,
`openalex_search.py` standalone, demais utilitários de descoberta.

## Requisitos

- Python 3.12 ou superior. Validado em 3.14.3.
- venv fora do repositório da skill (ex.: `$HOME\venvs\litreview`).

## Setup

Em PowerShell, a partir da raiz da skill (caminhos relativos a ela):

```powershell
# Criar venv (uma vez)
python -m venv $HOME\venvs\litreview

# Ativar venv (a cada sessão)
$HOME\venvs\litreview\Scripts\Activate.ps1

# Instalar dependências fixadas (verificação de hashes ativa)
pip install -r scripts\requirements.txt --require-hashes
```

Para desativar a venv: `deactivate`.

## Atualização de versões

`requirements.in` é o arquivo declarativo (fonte da verdade
editada por humanos, com bounds mínimos); `requirements.txt` é o
**lockfile gerado** por `uv pip compile` com versões pinadas e
hashes SHA256 para integridade de cadeia de suprimentos. Nunca
edite `requirements.txt` manualmente.

Para acrescentar, remover ou alterar bound de uma dependência:

```powershell
# 1. Editar scripts\requirements.in
# 2. Recompilar o lockfile com hashes
uv pip compile scripts\requirements.in `
    -o scripts\requirements.txt `
    --generate-hashes

# 3. Validar reprodutibilidade na venv
pip uninstall -r scripts\requirements.txt -y
pip install -r scripts\requirements.txt --require-hashes

# 4. Conferir que pip freeze coincide com as versoes do lockfile
pip freeze
```

`uv` está listado em `requirements.in` como dependência de
toolchain — instalado na venv junto com as bibliotecas de runtime.

## doi_verify.py

Verifica DOIs de uma bateria de referências contra CrossRef (com
fallback OpenAlex). Retorna um dos seis estados por referência:

| Estado | Significado |
|---|---|
| `OK` | DOI resolve e metadados batem com o esperado acima do threshold de fuzzy matching |
| `MISMATCH` | DOI resolve mas metadados divergem (subtipo Sub-30.2 do `_changelog.md`) |
| `NOT_FOUND` | DOI não resolve em CrossRef nem em OpenAlex |
| `NO_DOI` | Referência sem DOI fornecido |
| `RETRACTED` | DOI resolve mas a publicação está marcada como retratada |
| `ERROR` | Falha de rede, timeout ou erro de API |

### Uso

Bateria de teste empírico (Suíte A — sete casos do Teste 03 + um
caso sintético de retratação):

```powershell
python scripts\doi_verify.py `
    --cases scripts\tests\teste03_doi_verify_cases.json `
    --output relatorio.md
```

Verificação de um `.bib` arbitrário:

```powershell
python scripts\doi_verify.py `
    --bib referencias.bib `
    --output relatorio.json
```

A flag `--output` aceita `.md` (relatório legível) ou `.json`
(estruturado para pipeline). Padrão: `.md` em stdout se omitida.

## bib_consistency.py

Verifica consistência bidirecional entre citações no texto-fonte e
entradas no `.bib`. Retorna um dos quatro estados por elemento:

| Estado | Significado |
|---|---|
| `OK` | Citação e entrada `.bib` correspondem em ambas as direções |
| `ORPHAN_CITATION` | Citação no texto sem entrada correspondente no `.bib` |
| `UNCITED_REFERENCE` | Entrada no `.bib` não é referenciada em nenhuma citação |
| `APUD_ONLY` | Citação aparece exclusivamente via apud sem entrada primária (granularidade documentada na docstring do script) |

### Uso

Bateria de teste empírico (Suíte B — quatro casos do Teste 03 + um
caso sintético `UNCITED_REFERENCE`):

```powershell
python scripts\bib_consistency.py `
    --suite scripts\tests\teste03_bib_consistency_fixtures `
    --output relatorio.md
```

Verificação de par texto + `.bib` arbitrário:

```powershell
python scripts\bib_consistency.py `
    --text capitulo.md `
    --bib referencias.bib `
    --output relatorio.json
```

Aceita `.md` ou `.docx` no `--text`.

## Bateria de teste

Fixtures derivadas do Teste 03 (Fase A.7.2; ground truth v2.0)
materializam o princípio metodológico canonizado pela Sub-31.4:
exemplares canonizados de testes da skill viram suite de regressão
permanente dos scripts.

```powershell
# Suíte A — doi_verify.py
python scripts\doi_verify.py --cases scripts\tests\teste03_doi_verify_cases.json

# Suíte B — bib_consistency.py
python scripts\bib_consistency.py --suite scripts\tests\teste03_bib_consistency_fixtures
```

Critério de pronto de cada suíte: todos os casos retornam o estado
esperado conforme §4.2.1 e §4.2.2 do plano canônico
(documento de deliberação da Frente 3, mantido fora deste repositório).
Falha em qualquer caso = pendência registrada antes de fechar.

## Zotero MCP

Setup do Zotero MCP no Claude Desktop (Sub-31.3) documentado em
[`SETUP-ZOTERO-MCP.md`](SETUP-ZOTERO-MCP.md) neste mesmo diretório.
Cobre a opção canônica pela API local, sequência de instalação,
estado canônico do bloco `mcpServers`, ativação tardia da busca
semântica e restauração em caso de falha.

## Convenções operacionais

- Comentários em código Python em inglês.
- Paralelismo via `concurrent.futures.ThreadPoolExecutor` (analogia
  ao padrão `--transfers 16 --checkers 32` do rclone).
- User-Agent CrossRef com e-mail de contato (`mailto`) conforme a
  etiqueta da API. O padrão é o e-mail do autor; quem usar a skill
  pode definir a variável de ambiente `CROSSREF_MAILTO` com o próprio.
- Arquivos `.json` e `.md` editados ou criados em UTF-8 sem BOM.
