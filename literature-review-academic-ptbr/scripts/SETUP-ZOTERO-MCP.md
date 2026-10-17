# Setup do Zotero MCP no Claude Desktop

Configura o servidor MCP `zotero-mcp` (pacote pipx
`zotero-mcp-server`) para que o Claude Desktop consiga consultar a
biblioteca Zotero local via Better BibTeX. Componente operacional da
Sub-31.3 do `references/_changelog.md`.

## Pré-requisitos

- Zotero 7 instalado (Fase 0.3 do roadmap; já presente).
- Better BibTeX configurado (Fase 0.3; já presente). Citation key
  canônica: `auth.lower + year + title.lower.select(1,1).lower`.
- API local do Zotero habilitada em **Settings → Advanced →
  "Allow other applications on this computer to communicate with
  Zotero"**. Endpoint local: `http://localhost:23119/`.
- `pipx` instalado e em PATH.

## Modo de operação canônico — API local

A skill adota como variante canônica a **API local** do Zotero
(default da v0.3.0 do `zotero-mcp-server`). Razões:

- Better BibTeX já está configurado e expõe metadados Zotero por
  vias locais; a API local conversa naturalmente com ele.
- Zero credenciais persistidas no `claude_desktop_config.json` —
  nenhuma API key exposta em arquivo versionado ou em logs.
- Caminho operacional mais simples: nenhuma operação de portal
  Zotero (zotero.org/settings/keys) necessária.
- Custo: Zotero precisa estar rodando a cada uso da skill no Claude
  Desktop. O custo é compatível com o uso já estabelecido (Better
  BibTeX também exige Zotero aberto).

A variante alternativa **Web API** (`zotero-mcp setup --no-local
--api-key K --library-id L --library-type {user,group}`) fica
adiada para frente futura, com critério de reabertura: cenário de
operação multi-máquina, Zotero remoto, ou demanda explícita de uso
sem Zotero rodando localmente.

## Sequência de instalação (validada em 2026-04-25)

1. **`pipx install zotero-mcp-server`** — executar no terminal do
   usuário. Instala o executável em
   `%USERPROFILE%\.local\bin\zotero-mcp.exe` (Windows) ou
   `~/.local/bin/zotero-mcp` (macOS/Linux). Confirmação:

   ```powershell
   pipx list
   # package zotero-mcp-server 0.3.0, installed using Python 3.13.9
   #     - zotero-mcp.exe
   ```

2. **Backup do `claude_desktop_config.json`**:

   ```powershell
   Copy-Item `
       "$env:APPDATA\Claude\claude_desktop_config.json" `
       "$env:APPDATA\Claude\claude_desktop_config.backup-pre-zotero-mcp-2026-04-25.json"
   ```

3. **Verificação UTF-8 sem BOM** do config existente. Convenção
   operacional crítica herdada da decisão de Filesystem MCP da Fase
   2; o `zotero-mcp setup` precisa preservá-la.

4. **Setup com API local + skip semantic search**:

   ```powershell
   zotero-mcp setup --skip-semantic-search
   ```

   A flag `--skip-semantic-search` adia o índice semântico para
   ativação tardia (ver "Semantic search — ativação tardia"
   abaixo). Aderente ao princípio just-in-time.

5. **Verificações pós-setup, antes do reinício do Claude Desktop**:
   - encoding do `claude_desktop_config.json` continua UTF-8 sem
     BOM (verificado);
   - entrada `filesystem` MCP existente intocada (verificado);
   - entrada `zotero` MCP nova presente, formato pipx (`command`
     aponta para o caminho absoluto de `zotero-mcp.exe`, p. ex.
     `C:\\Users\\<usuario>\\.local\\bin\\zotero-mcp.exe`,
     com `env: {"ZOTERO_LOCAL": "true"}`);
   - preferências do Claude Desktop intocadas (cowork tasks,
     sidebar, etc.).

6. **Reinício do Claude Desktop** — Quit completo via system tray
   (não apenas fechar a janela). Necessário para o Claude Desktop
   carregar o novo `mcpServers`.

7. **Teste funcional**: prompt `quantos itens tenho no Zotero?` no
   Claude Desktop deve retornar um número real (não erro de
   configuração).

## Estado canônico do bloco `mcpServers` após setup

```json
"zotero": {
  "command": "C:\\Users\\<usuario>\\.local\\bin\\zotero-mcp.exe",
  "env": {
    "ZOTERO_LOCAL": "true"
  }
}
```

Notar que o padrão difere do `cmd /c npx` usado pelo Filesystem MCP:
o Zotero MCP é um executável `.exe` instalado diretamente via pipx,
sem necessidade do wrapper `npx`. Caminho absoluto com `\\`
escapados em JSON, conforme convenção; trocar `C:\\Users\\<usuario>` pelo valor de
`%USERPROFILE%` na sua máquina. O JSON não expande variáveis de
ambiente, por isso o caminho vai por extenso.

## Semantic search — ativação tardia

A Frente 3 propositadamente adia a configuração do índice de busca
semântica. Para ativar quando demanda real surgir (Fase 5 — módulo
de domínio prioritário, ou Fase 6 — primeiro projeto real), executar:

```powershell
zotero-mcp setup --semantic-config-only
```

Em seguida, popular o índice:

```powershell
zotero-mcp update-db
```

Verificar o estado:

```powershell
zotero-mcp db-status
zotero-mcp db-inspect
```

## Limitações conhecidas

- **Bug `zotero-mcp setup-info` no Windows cp1252**: o subcomando
  informativo (`zotero-mcp setup-info`) quebra com
  `UnicodeEncodeError: 'charmap' codec can't encode character
  '\U0001f527'` (emoji 🔧) em terminais cp1252 (Anaconda Prompt
  default, PowerShell 5). Bug upstream da v0.3.0. Não bloqueia o
  `setup` em si, apenas o subcomando informativo. Mitigação:
  executar em PowerShell 7+ com
  `$OutputEncoding = [System.Text.UTF8Encoding]::new()` ou aceitar
  como limitação cosmética. Não exige correção em escopo da
  Frente 3.

## Restauração em caso de falha

Se o setup quebrar algo (`filesystem` MCP disruptado, encoding
incorreto, sintaxe JSON inválida), restaurar via:

```powershell
Copy-Item `
    "$env:APPDATA\Claude\claude_desktop_config.backup-pre-zotero-mcp-2026-04-25.json" `
    "$env:APPDATA\Claude\claude_desktop_config.json" `
    -Force
```

Reaplicar a entrada `zotero` manualmente seguindo o "Estado canônico
do bloco `mcpServers`" acima.
