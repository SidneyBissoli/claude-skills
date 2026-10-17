# CLAUDE.md — contexto automático para sessões futuras

Arquivo lido pelo Claude Code ao abrir este repositório. Aqui vão só os
pontos de entrada; o detalhe vive nos arquivos-fonte.

## Visão geral

Skill que redige revisões de literatura acadêmica em pt-BR para quatro
domínios: saúde coletiva; ciências sociais e humanidades; metodologia e
psicometria; políticas públicas. Opera como redator assistido sobre corpus
curado — nunca como bibliotecário a partir de memória paramétrica. Defende
contra erros bibliográficos classificados pela **taxonomia v2** em três
dimensões hierárquicas condicionais — Existência, Objeto do erro, Natureza
do erro (desenho operacional em `references/_taxonomy-v2-design.md`).

## Estado atual

Fase 1 do MVP concluída. Fase A do roadmap de refatoração taxonômica em
curso; última subfase fechada registrada no `_changelog.md`. Subfases
A.4 em diante refatoram módulos derivados em `references/`.

## Arquivos críticos para contexto

- `SKILL.md` — regras inegociáveis, glossário de termos operacionais, fluxo
  obrigatório (instância de generate-critique-refine) e política de
  carregamento condicional dos módulos de `references/`.
- `references/_taxonomy-v2-design.md` — taxonomia canônica em três
  dimensões hierárquicas condicionais (Existência, Objeto, Natureza),
  árvore decisória, protocolo de verificação em seis passos, casos
  limítrofes.
- `references/_changelog.md` — decisões arquiteturais da Fase 1, em ordem
  de consequência, cada uma com justificativa.
- `references/_phase2-handoff.md` — pendências em formato
  Objetivo/Inputs/Critério/Risco; fonte da verdade para a Fase 2.
- `references/_master-guide.md` — base estratégica e empírica da skill
  (engenharia de prompt, verificação externa de DOI, taxas de fabricação
  documentadas na literatura revisada por pares).
- `<memory>/MEMORY.md` — índice de memórias operacionais ativas do Claude
  Code entre sessões; lido automaticamente no início de cada conversa.

## Convenções operacionais

- Ler `_changelog.md` antes de qualquer alteração significativa em
  `SKILL.md` ou em `references/`.
- Regenerar o zip de distribuição com listagem explícita dos arquivos
  (nunca wildcard `*`); auditar a estrutura antes do upload para garantir
  `SKILL.md` na raiz do zip, sem pasta envolvente.
- Propagar edições do `SKILL.md` aos dois ambientes separadamente
  (Claude.ai web e Claude Desktop); não há sincronização automática.
- Git commit descritivo a cada marco (decisão arquitetural nova, módulo
  fechado, correção de regra).
- Glossário do `SKILL.md` é autocontido em vocabulário: termo novo criado
  em arquivo de `references/` só entra após adicionar entrada
  correspondente ao glossário — evitar órfãos operacionais (decisão
  registrada no changelog).
- Claude Desktop exige invocação explícita para ações de sistema de
  arquivos, mesmo com Filesystem MCP configurado: prompts que envolvem
  arquivos locais devem nomear a ferramenta MCP ou usar linguagem
  inequívoca de ação em disco (ex.: "usando o filesystem MCP, liste…",
  "leia o arquivo X", "abra em disco…"). Essa invocação vem antes da ação
  bibliográfica específica em contextos de uso da skill.
- **Divisão de papéis entre agentes.** Execução operacional (edição de
  arquivos da skill, Git, commits, testes, push) em Claude Code.
  Auditoria, sugestão e produção de documentos acadêmicos em Claude no
  navegador — não edita arquivos da skill diretamente. Escopo,
  validação de decisões e ponte entre as duas instâncias com Sidney
  Bissoli, designer do projeto. Convenção estabelecida em A.1.7 após
  desvio observado em A.1.5 e A.1.6.
- **Sandbox do Claude Code para edições de configuração de sistema.**
  Quando uma tarefa delegada ao Claude Code envolve edição de arquivo
  fora do sandbox do filesystem MCP do Claude Code (`%APPDATA%`,
  `Program Files`, configs de sistema, profile global), o Claude Code
  não consegue verificar substantivamente o resultado da edição —
  depende do exit code e do output do subprocesso (ferramentas como
  `zotero-mcp setup`, instaladores de MCP servers, scripts de
  configuração), que pode reportar sucesso baseado em expectativa em
  vez de inspeção do arquivo. Mitigação: classificar a tarefa antes
  de delegar. Edições dentro do sandbox → delegação direta. Edições
  fora do sandbox → escolher entre (a) Sidney edita manualmente
  desde o início; (b) Claude navegador edita via seu próprio sandbox
  e Sidney copia o arquivo de volta; (c) Claude Code propõe diff
  textual que Sidney aplica e verifica. Convenção fechada na Fase 4
  / Frente 3 a partir de caso reflexivo (ver seção "Casos reflexivos
  sobre a operação da skill").
- **Ciclo de revisão para tarefas arquiteturalmente substantivas.**
  Tarefas de consequência arquitetural — canonização de variante,
  refinamento de taxonomia, execução de bloco arquitetural — seguem o
  padrão execução → síntese estruturada → avaliação por Claude
  navegador via Sidney → veredito (aprovação integral, aprovação com
  ajustes, reprovação com justificativa) → nova rodada se aplicável.
  O Claude Code produz síntese estruturada redigida de modo que o
  Claude navegador consiga avaliar o resultado sem precisar abrir os
  arquivos da skill; o Claude navegador avalia e retorna veredito via
  Sidney, que é o decisor final e intermediador. Convenção fechada
  na Fase A.7 Bloco A, cujo ciclo completo (execução → aprovação com
  cinco ajustes → aprovação integral) está registrado em
  `<pasta-de-referencias>\skill-development\research\fase-A7-sintese-execucao-bloco-A.md`.

## Casos reflexivos sobre a operação da skill

Observações empíricas em que a skill, operando sobre material que
testa a própria skill, manifestou os vetores de risco que ela
cataloga. Úteis como exemplos didáticos em refinamentos futuros e como
reforço operacional das regras da skill. Distintos de **convenções
operacionais** (orientação sobre como trabalhar) e de **decisões
arquiteturais** (que vivem no `_changelog.md`).

### Skill manifestando o risco que cataloga — caso §4.2 reflexivo (Teste 03 / Fase A.7.2)

Manifestação. Durante o Papel 2 do Teste 03 (2026-04-25), em ambiente
**Claude Desktop Incognito**, a skill detectou pastiche stricto sensu
da referência fabricada Magnani (2011) corretamente — mas, ao
identificar a obra-fonte real do pastiche (Magnani 2005, "Os
circuitos dos jovens urbanos"), atribuiu erradamente o veículo da
obra-fonte: afirmou que a obra foi publicada em
*Horizontes Antropológicos*, quando o veículo correto é
***Tempo Social*** v.17 n.2, 2005. Erro periférico, que não invalida
a detecção do pastiche, mas é exemplo de intrusão da própria memória
paramétrica do agente operando sob a skill.

Mecanismo. Intrusão da memória paramétrica do agente subjacente,
exatamente o vetor contra o qual o §4.2 do
`hallucination-prevention-checklist.md` alerta. A memória paramétrica
acertou no nível diagnóstico (reconheceu o pastiche e identificou a
obra-fonte real) mas errou no detalhe de metadado (veículo da
obra-fonte) — assinatura típica de intrusão paramétrica em conteúdo
canônico.

Significado. A skill, operando sobre material que testa a própria
skill, manifestou o vetor de risco que ela cataloga. O caso é
reflexivo no sentido forte: a skill é tanto observadora quanto
exemplar do fenômeno descrito.

Lição operacional. **Verificação ativa deve sempre exceder a
memória paramétrica do agente.** Mesmo quando a memória paramétrica
acerta na detecção primária (identifica o pastiche), pode errar nos
detalhes (atribui o veículo errado). §(xii) é o protocolo de
fechamento desse vetor, não um detalhe opcional. A regra nominal
"verificação ativa de conceitos-âncora canônicos mobilizados via
apud" do `epistemic-tagging-rules.md` (§8 — incorporada pela decisão
de fechamento da Frente 2) endereça vetores cognatos a este caso.

Referência cruzada. Ground truth v2.0 do Teste 03 §3.3 e §5.3:
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`.
Decisão de fechamento da Frente 2 do roadmap v3.4 (subdecisão sobre
caso reflexivo) no `_changelog.md`.

### Claude Code reportando edição fora do sandbox sem inspeção do arquivo (Frente 3 / Fase 4)

Manifestação. Durante a §5.4 da execução da Frente 3 (2026-04-25),
o Claude Code rodou `zotero-mcp setup --skip-semantic-search` para
adicionar entrada `zotero` ao `claude_desktop_config.json` em
`%APPDATA%\Claude\`. O relato consolidado afirmou edição
bem-sucedida — apresentou diff de seis linhas adicionadas em
`mcpServers`, confirmou encoding UTF-8 sem BOM preservado, estado
canônico do `mcpServers` documentado em
`scripts/SETUP-ZOTERO-MCP.md`. Inspeção subsequente pelo Claude
navegador (com filesystem MCP em outro sandbox) sobre cópia trazida
manualmente por Sidney revelou que o config no disco **não** continha
a entrada `zotero` — apenas a entrada `filesystem` pré-existente.

Mecanismo. O filesystem MCP do Claude Code é restrito a três
pastas locais do usuário (pesquisa, programação e a pasta de
skills); `%APPDATA%\Claude\` está fora desse
sandbox. O Claude Code rodou o subprocesso `zotero-mcp setup` com
permissões de usuário (subprocesso opera fora do sandbox MCP), mas
**não conseguiu ler o arquivo modificado** para verificar a edição.
Inferiu o estado pós-setup a partir do exit code e do output
capturado, não da inspeção direta do arquivo. O `zotero-mcp setup`
v0.3.0 falhou silenciosamente em persistir a edição no caminho
esperado — causa raiz não diagnosticada conclusivamente; possível
bug em cp1252 análogo ao do `setup-info` ou outro. O relato do
Claude Code refletiu o que o setup deveria ter feito segundo a
documentação, não o que efetivamente fez no disco.

Significado. O Claude Code (subagente confiável da skill)
manifestou vetor cognato ao §4.2 — relato baseado em expectativa,
não em inspeção. Análogo cognato à intrusão de memória paramétrica
do §4.2 reflexivo: a skill cataloga o vetor para o agente
principal; aqui o vetor manifesta-se na cadeia de delegação. O
caso é reflexivo no mesmo sentido forte: o Claude Code, executando
trabalho sob a skill, manifestou exatamente o tipo de erro que a
skill instrui o agente principal a evitar.

Lição operacional. **Verificação ativa precisa exceder o relato
de quem executou — incluindo o relato do próprio Claude Code.**
Quando a delegação cruza o sandbox do filesystem MCP do Claude
Code, a inspeção substantiva precisa vir de fora — Sidney
diretamente ou Claude navegador via cópia manual. A convenção
operacional "Sandbox do Claude Code para edições de configuração
de sistema" (seção "Convenções operacionais" deste arquivo) é a
formalização desta lição.

Referência cruzada. `scripts/SETUP-ZOTERO-MCP.md` (procedimento
canônico, com ressalva de verificação substantiva); síntese de
execução da Frente 3 a ser produzida em §5.9 do prompt de
abertura da Frente
(`<pasta-de-referencias>\skill-development\research\fase-4-sintese-execucao-frente-3.md`,
seção "Casos reflexivos manifestados durante a execução");
`_changelog.md` decisão 31 (fechamento da Frente 3).

## Pendências ativas

Fonte da verdade: `references/_phase2-handoff.md`. Em aberto:

- **(i)** Módulos de domínio (`domain-public-health/`,
  `domain-social-sciences/`, `domain-methodology-psychometry/`,
  `domain-public-policy/`).
- **(ii)** Templates de matriz de síntese em `assets/` (genérico mais
  uma variante por domínio).
- **(iii)** [RESOLVIDA PARCIALMENTE pela Frente 3 — `doi_verify.py` e
  `bib_consistency.py` implementados; `style_formatter.py` e demais
  componentes adiados — ver `_phase2-handoff.md` §(iii) Resolução parcial
  e `_changelog.md` decisão 31.]
- **(iv)** Módulos `bibliographic-styles/` específicos (Vancouver, ABNT
  6023/10520, APA 7).
- **(v)** [RESOLVIDA em A.4 — ver `_phase2-handoff.md` §(v)]
- **(vi)** Passo 6 do `SKILL.md`: colunas obrigatórias ainda não
  listadas (`data_ultima_verificacao`, `risco_verificacao`,
  `fonte_desambiguacao`).
- **(vii)** Memórias ativas em `<memory>/MEMORY.md` a resolver antes
  de empilhar novas.

## Como retomar trabalho

1. Ler `_changelog.md` e `_phase2-handoff.md` inteiros antes de propor
   mudanças arquiteturais ou priorizar pendência.
2. Ler `SKILL.md` inteiro se a mudança envolver regras inegociáveis,
   fluxo obrigatório ou glossário.
3. Não improvisar decisão arquitetural: escolha que afete mais de um
   arquivo precisa ser consultada contra o changelog (para não contradizer
   decisão viva) e registrada como decisão nova antes do merge.
4. Ao resolver memória ou pendência, registrar a decisão no
   `_changelog.md` antes de remover o rastro do `MEMORY.md` ou marcar
   pendência como concluída.
