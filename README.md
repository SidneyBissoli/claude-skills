# Skills

[Leia em português](README.pt-BR.md)

Agent skills for [Claude](https://claude.com) (Claude Code, Claude Desktop and
claude.ai), written by Sidney da Silva Pereira Bissoli. Each folder is one
skill: a `SKILL.md` with the instructions Claude follows, plus the scripts and
references it uses. Most skills are written in Brazilian Portuguese.

| Skill | What it does |
|---|---|
| [docx-revisao](docx-revisao/) | Reviews `.docx` files, both text and comments, always on a copy: text goes through the Word MCP server; comments (read, create, move between similar documents, re-author) go through its own OOXML engine, which checks every anchor before saving. |
| [docx-tabelas-validadas](docx-tabelas-validadas/) | Extracts tables from `.docx` survey annexes to CSV, reading each cell twice by independent routes and checking sums, marginals and sample base before any analysis. |
| [literature-review-academic-ptbr](literature-review-academic-ptbr/) | Academic literature reviews in Portuguese for public health, social sciences, methodology and public policy, with every reference verified (DOI, metadata) and nothing invented. |
| [r-package-dev](r-package-dev/) | Modern R package development on Windows (usethis, testthat, roxygen2, Air, GitHub Actions): scaffolding, the development cycle, a full quality gate and release. |

[`scripts/`](scripts/) holds utilities shared across projects, not a skill:
`restore-libc.mjs` puts back the `libc` fields that `npm install` on Windows
strips from `package-lock.json`.

## Installing a skill

- **Claude Code:** copy (or link) the skill folder into `~/.claude/skills/`.
  On Windows, use a junction (`New-Item -ItemType Junction`); `ln -s` in Git
  Bash copies the folder instead of linking it.
- **claude.ai / Claude Desktop:** zip the skill folder with `SKILL.md` at the
  root of the zip and upload it under Settings > Capabilities > Skills.

## License

MIT, per skill (see the `LICENSE` file in each folder).
