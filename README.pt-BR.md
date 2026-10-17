# Skills

[Read in English](README.md)

Skills para o [Claude](https://claude.com) (Claude Code, Claude Desktop e
claude.ai), escritas por Sidney da Silva Pereira Bissoli. Cada pasta é uma
skill: um `SKILL.md` com as instruções que o Claude segue, mais os scripts e as
referências que ela usa. A maioria está em português.

| Skill | O que faz |
|---|---|
| [docx-revisao](docx-revisao/) | Revisa `.docx` no texto e nos comentários, sempre numa cópia: o texto vai pelo servidor MCP do Word; os comentários (ler, criar, levar para versões parecidas, reautorar) vão pelo motor OOXML próprio, que confere cada âncora antes de gravar. |
| [docx-tabelas-validadas](docx-tabelas-validadas/) | Extrai para CSV as tabelas de anexos de pesquisa em `.docx`, lendo cada célula duas vezes por caminhos independentes e conferindo somas, marginais e base amostral antes de qualquer análise. |
| [literature-review-academic-ptbr](literature-review-academic-ptbr/) | Revisões de literatura acadêmica em português para saúde coletiva, ciências sociais, metodologia e políticas públicas, com toda referência verificada (DOI, metadados) e nada inventado. |
| [r-package-dev](r-package-dev/) | Desenvolvimento moderno de pacotes R no Windows (usethis, testthat, roxygen2, Air, GitHub Actions): criação, ciclo de desenvolvimento, checagem completa e release. |

[`scripts/`](scripts/) guarda utilitários compartilhados entre projetos, não é
uma skill: `restore-libc.mjs` devolve os campos `libc` que o `npm install` no
Windows apaga do `package-lock.json`.

## Como instalar uma skill

- **Claude Code:** copie (ou ligue) a pasta da skill em `~/.claude/skills/`. No
  Windows, use uma junction (`New-Item -ItemType Junction`); o `ln -s` do Git
  Bash copia a pasta em vez de ligá-la.
- **claude.ai / Claude Desktop:** compacte a pasta da skill com o `SKILL.md` na
  raiz do zip e envie em Configurações > Capacidades > Skills.

## Licença

MIT (`LICENSE` na raiz, repetido em cada pasta para que uma skill copiada sozinha o leve junto).
