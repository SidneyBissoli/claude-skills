# Handoff operacional para Fase 2

Especificação executável das pendências listadas no `_changelog.md`. Cada
pendência estrutura-se em quatro campos: **Objetivo** (o que o artefato
deve fazer), **Inputs** (arquivos/decisões/módulos pré-requisitos),
**Critério de pronto** (como saber que terminou), **Risco conhecido**
(armadilha arquitetural identificada durante a Fase 1). As decisões
arquiteturais estão no `_changelog.md` e não se repetem aqui — quando um
campo depende de decisão já documentada, o handoff remete.

## (i) Módulos de domínio por área

**Objetivo.** Criar `references/domain-public-health/`,
`domain-social-sciences/`, `domain-methodology-psychometry/`,
`domain-public-policy/` com, em cada um, convenções de periódicos da área,
correntes teóricas a contrastar, fontes primárias específicas, e armadilhas
de conflação típicas do domínio. Carregados condicionalmente conforme
detecção de domínio no Passo 0.

**Inputs.** SKILL.md regra 3 (pares-gatilho canônicos por domínio, listados
com as correntes); guia-mestre seções 4 (MCPs por domínio) e 7 (convenções
por tipo de entregável); `author-disambiguation-universal.md` §7 (aponta
para estes módulos); `style-detection-heuristics.md` §2 (periódicos
listados por estilo, organizados por área).

**Critério de pronto.** Cada diretório `domain-*/` tem ao menos três
arquivos seguindo a nomenclatura proposta no SKILL.md (sobre `journal-
conventions-*.md`, `theoretical-currents-*.md`, `brazilian-*-sources.md`,
ou equivalentes). SKILL.md regra 3 remete aos pares-gatilho específicos
sem duplicar o conteúdo. Cross-references bidirecionais com
`author-disambiguation-universal.md` (desambiguação universal → domínio:
qual corrente cada autor ocupa) e com checklist §4.3 (contraste teórico
obrigatório).

**Risco conhecido.** Duplicação silenciosa com `author-disambiguation-
universal.md`. Fronteira a manter: o arquivo universal lista
sobrenomes-gatilho e protocolo de desambiguação; os módulos de domínio
listam autores-por-corrente teórica. Segundo risco: correntes teóricas
mudam de nomenclatura ao longo do tempo (o que era "análise de conteúdo
Bardin" nos anos 90 se desdobrou em variantes); prever um campo de
atualização dentro de cada `theoretical-currents-*.md`.

C1 do Bloco C da Fase A.7 mitiga parcialmente o risco de operação
silenciosa em temas sem módulo de domínio correspondente, ao exigir
declaração explícita de fronteira ortogonal no Passo 0 do SKILL.md
quando o tema estiver fora dos quatro domínios canônicos. A
declaração não substitui a implementação dos módulos — que permanece
objetivo de (i) —, mas torna auditável o estado "sem módulo" enquanto
a pendência não é resolvida.

## (ii) Templates de matriz de síntese em `assets/`

**Objetivo.** `synthesis_matrix_generic.xlsx` + variantes por domínio
(`_health.xlsx`, `_social.xlsx`, `_methods.xlsx`, `_policy.xlsx`) em
formato aberto por Excel/LibreOffice. Cada planilha é o artefato humano
que alimenta Claude durante a geração — matriz antes de prosa é regra
não-negociável do fluxo (SKILL.md passo 6).

**Inputs.** Colunas obrigatórias consolidadas pelo MVP: `chave_bibtex`,
`autores`, `ano`, `objeto`, `metodo`, `achado_principal`, `corrente_teorica`,
`trecho_verbatim`, `pagina`, `tag_tema`, `data_ultima_verificacao` (o
carimbo de confiança referido na decisão 12 do changelog), `risco_verificacao`
(estratificação para §5.2 do checklist), `fonte_desambiguacao` (registro do
critério usado em homônimos, §3 de `author-disambiguation`). A pendência
(vi) trata da propagação dessas três últimas colunas ao SKILL.md passo 6.

**Critério de pronto.** Arquivos `.xlsx` existem em `assets/`; cada um abre
sem erro; as 13 colunas obrigatórias aparecem em todos os templates;
variantes de domínio acrescentam colunas específicas (ex.: `desenho_estudo`,
`N`, `setting` em saúde; `corrente_teorica_secundaria`, `tradicao_nacional`
em social; `metodo_psicometrico`, `indicador_confiabilidade` em metodologia;
`esfera_regulatoria`, `ato_normativo` em políticas). SKILL.md passo 6 lista
cada template pelo nome.

**Risco conhecido.** Colunas obrigatórias precisam de versionamento. Se a
Fase 2 adicionar coluna nova (ex.: `status_retratacao`, quando pendência
(iii) for implementada), templates antigos ficam incompletos em projetos
em curso. Mitigação: sheet "versão" em cada planilha e script de migração
em `scripts/`.

**Relação com a Frente 3** (Fase 4 — Infraestrutura, subset prioritário,
fechada em 2026-04-25 pela decisão 31). Os scripts `doi_verify.py` e
`bib_consistency.py` produzidos pela Frente 3 retornam relatório em
`.json` ou `.md`, sem acoplamento estrutural com a matriz de síntese em
`.xlsx`; o fechamento da §(iii) parcial não força fechamento simultâneo
desta pendência. A integração entre matriz de síntese e scripts (consumo
da matriz como input dos scripts; ou propagação dos relatórios dos
scripts para colunas da matriz) é Frente 4+ candidata.

## (iii) Scripts Python de verificação

**Objetivo.** `doi_verify.py`, `bib_consistency.py`, `style_formatter.py`
como hard gate obrigatório antes de submissão (checklist §5.1). Demais
scripts do catálogo do SKILL.md (`zotero_extract`, `pubmed_search`,
`scielo_search`, `openalex_search`, `lexml_search`, `camara_senado_search`)
têm prioridade menor — são utilitários de descoberta, não de verificação.

**Inputs.** Decisão 4 do changelog (carimbo de confiança) e memória de
projeto `project_doi_verify_retraction_check.md` (estados de retorno
esperados, campos CrossRef `update-to`/`update-nature`, fallback OpenAlex
`is_retracted`). Protocolo de conversão de tags para citação em
epistemic-tagging §6 Fase 3 define o comportamento de `style_formatter.py`.
Templates de matriz da pendência (ii) definem o formato de entrada/saída.

**Critério de pronto.** Cada script passa em teste com BibTeX mínimo
(5-10 entradas bem-formadas + 1-2 quebradas de propósito). Docstring com
exemplos. Integração com Zotero via `pyzotero`. CLI aceita `.bib` e retorna
relatório em `.json` ou `.md`. `doi_verify.py` retorna os seis estados da
memória de projeto; `bib_consistency.py` identifica órfãos e faltantes;
`style_formatter.py` converte tags para Vancouver/ABNT/APA conforme o
estilo do entregável.

**Risco conhecido.** Limites de API (CrossRef pede User-Agent com e-mail;
OpenAlex tem rate-limit). Scripts respeitam, não contornam. Segundo risco:
detecção de retratação varia entre APIs — CrossRef usa `update-nature`,
OpenAlex usa `is_retracted`, PubMed usa `PublicationType="Retraction
Notice"`. Unificar na camada do script, não empurrar heterogeneidade para
o pesquisador. Terceiro risco: versões de `pyzotero` e CSL em evolução;
fixar dependências em `requirements.txt` ou `pyproject.toml`.

### Resolução parcial (2026-04-25)

Pendência **resolvida parcialmente** pela decisão 31 do `_changelog.md`
(fechamento da Frente 3 do roadmap v3.4 — Fase 4 — Infraestrutura
completa, subset prioritário). Subset prioritário implementado:

- **`scripts/doi_verify.py`** (Sub-31.1) — hard gate de verificação
  de DOI; seis estados de retorno (`OK`, `MISMATCH`, `NOT_FOUND`,
  `NO_DOI`, `RETRACTED`, `ERROR`); calibrado contra Silva & Lopes
  2020 (caso forte da Sub-30.2 — fabricação com identificador
  colidido); cobertura via Suíte A (8 de 8 casos passam).
- **`scripts/bib_consistency.py`** (Sub-31.2) — hard gate de
  verificação citação ↔ entrada bibliográfica; quatro estados
  (`OK`, `ORPHAN_CITATION`, `UNCITED_REFERENCE`, `APUD_ONLY`);
  cobertura via Suíte B (21 de 21 verificações passam através de 5
  sub-casos).
- **Zotero MCP** (Sub-31.3) — modo API local (`ZOTERO_LOCAL=true`,
  sem credenciais persistidas), integrado ao Claude Desktop; teste
  funcional de fechamento confirmou a contagem real de itens da
  biblioteca.
  Better BibTeX (Fase 0.3) permanece como fonte canônica de `.bib`.

**Componentes adiados explicitamente** (Sub-31.5 do `_changelog.md`):

- `style_formatter.py` — depende de §(iv) deste handoff
  (`bibliographic-styles/` específicos: Vancouver, ABNT, APA);
  criar antes dos módulos de estilo é programar contra superfície
  indefinida.
- `openalex_search.py` standalone — utilitário de descoberta;
  OpenAlex já entra como fallback interno do `doi_verify.py`,
  suficiente para o estado atual.
- PubMed MCP, Crossref MCP — utilitários de descoberta; HTTP direto
  via `requests` no `doi_verify.py` é suficiente para o hard gate.
- Demais utilitários (`zotero_extract`, `scielo_search`,
  `lexml_search`, `camara_senado_search`) — fora do hard gate;
  entrada por demanda dirigida.

**Critério de reabertura**: demanda de projeto real (Fase 6) ou
Fase 5 que envolva domínio com necessidade de descoberta
automatizada (saúde coletiva — PubMed; ciências sociais — SciELO;
políticas públicas — LexML/Câmara/Senado).

**Bateria de teste empírica como suite de regressão permanente**
(Sub-31.4 do `_changelog.md`): exemplares canonizados de testes da
skill (Teste 02, Teste 03 e subsequentes) viram suite de regressão
permanente dos scripts da infraestrutura. Operacionalização: Suíte
A (8 casos derivados do Teste 03 + um sintético de retratação) e
Suíte B (5 sub-casos derivados do Teste 03 via 2 fixtures), com
fixtures vivendo em `scripts/tests/teste03_doi_verify_cases.json`
e `scripts/tests/teste03_bib_consistency_fixtures/`. Critério de
expansão: cada Teste futuro com vetores não cobertos pela bateria
atual produz casos novos a serem incorporados às suítes existentes
ou a suítes novas, conforme a tipologia do vetor empírico.

## (iv) Módulos `bibliographic-styles/` específicos

**Objetivo.** `vancouver-numeric.md`, `vancouver-brazilian-conventions.md`,
`abnt-nbr-6023-2018.md`, `abnt-nbr-10520-2023.md`, `apa-7.md` — regras
específicas de cada estilo: ordem autoral, abreviação de periódico, uso de
*et al.*, hierarquia de metadados na lista de referências, casos especiais
(capítulo em coletânea, tese, legislação, relatório institucional, dados
de repositório oficial).

**Inputs.** `style-detection-heuristics.md` aponta para estes arquivos;
epistemic-tagging §6 Fase 3 especifica as substituições por estilo
(decisões arquiteturais já estão lá — o módulo implementa os detalhes de
formatação); SKILL.md regra de carregamento condicional; NBR 6023:2018 e
NBR 10520:2023 (documentos oficiais da ABNT, externos — consulta por
aquisição ou acesso institucional).

**Critério de pronto.** Cada arquivo tem seções canônicas: "Citação no
texto", "Lista de referências", "Casos especiais", "Divergências entre
normas antigas e atuais". Validação cruzada: cada convenção no
`style-detection` encontra correspondência no módulo do estilo descrito.
Data de consulta às normas registrada no próprio arquivo (sob carimbo de
confiança — decisão 4 do changelog).

**Risco conhecido.** Normas ABNT são pagas e se atualizam — não copiar a
norma no arquivo; codificar a regra operacionalizada + ponteiro para o
documento oficial. APA mudou de 6 para 7 em 2019; o módulo cobre APA 7
explicitamente no nome do arquivo, mas alertar no próprio corpo. Vancouver
tem variantes ICMJE/NLM/AMA ligeiramente diferentes; o módulo `vancouver-
brazilian-conventions.md` existe justamente para documentar as escolhas
que RSP/CSP/C&SC fazem dentro da família Vancouver.

## (v) Propagação de "modo (d) intra" ao checklist — RESOLVIDA

**Status.** Resolvida em A.1 (canonização da taxonomia v2 em decisão
18 do `_changelog.md`) e efetivada em A.4 (reescrita dos módulos
derivados). A pergunta original — "(d) intra vira subcategoria de (d)
ou modo autônomo (f)?" — é inaplicável sob a v2, que não opera com
letras (a)–(e). A conflação intra-autoral silenciosa passa a ser
classificada como **Dim. 2 conteúdo afirmado + Dim. 3 conceitual**
(distinção importante em relação a pastiche intra-autoral, que
combina elementos bibliográficos em vez de fases teóricas — ver
`_taxonomy-v2-design.md §8.2`).

**Arquivos onde a resolução foi aplicada** (commit de A.4):

- `hallucination-prevention-checklist.md` — §2 reescrita para a v2;
  §4.3 com classificação v2 da conflação; §6 matriz de mitigação
  reescrita com linhas por valor terminal, incluindo Dim. 2 conteúdo
  afirmado com bifurcação Dim. 3 conceitual/factual; §7 red flag
  (vi) atualizado.
- `author-disambiguation-universal.md` — §1 (por que a desambiguação
  importa) reescrita em vocabulário v2; §5 (caso especial — homônimos
  no mesmo campo) com mapeamento para Dim. 2 conteúdo afirmado; §6
  (desambiguação intra-autoral) com mapeamento explícito para
  Dim. 2 conteúdo afirmado + Dim. 3 conceitual e contraste com
  pastiche intra-autoral.
- `argumentative-review-template.md` — §2.2 e §7 par 2 atualizados.
- `epistemic-tagging-rules.md` — §3 proibições atualizadas.
- `SKILL.md` regra 4 e glossário "conflação intra-autoral silenciosa"
  (já atualizados em A.3).

## (vi) Ajuste do passo 6 do SKILL.md — colunas obrigatórias da matriz

**Objetivo.** Propagar ao SKILL.md passo 6 as três colunas estabelecidas
como obrigatórias pelo MVP mas não listadas ainda naquele ponto:
`data_ultima_verificacao`, `risco_verificacao`, `fonte_desambiguacao`.

**Inputs.** SKILL.md passo 6 atual (lista 10 colunas mínimas); checklist
§3 (introduz `data_ultima_verificacao`); checklist §5.2 (introduz
`risco_verificacao`); `author-disambiguation` §§3-4 (introduz
`fonte_desambiguacao`).

**Critério de pronto.** SKILL.md passo 6 lista as 13 colunas; templates
da pendência (ii) trazem as 13; checklist e `author-disambiguation` param
de apontar para colunas que o SKILL.md não menciona. Coerência entre os
cinco arquivos que mencionam colunas (SKILL.md, checklist, author-
disambiguation, templates, e eventualmente os scripts).

**Risco conhecido.** SKILL.md precisa ficar abaixo de 500 linhas (boa
prática de progressive disclosure). Três colunas novas + justificativa
curta podem empurrar para perto do limite. Se exceder, mover a
justificativa para o checklist e deixar só os nomes das colunas no
SKILL.md — seguindo o mesmo padrão de decisão 1 (modos no SKILL.md com
ponteiro para checklist §2).

**Sugestão adicional a avaliar na resolução desta pendência.** Avaliar
se adicionar coluna `verificacao_cascata` à matriz de síntese
(valores típicos `OK` / `SUSPEITA` / `FABRICADA`, aplicáveis a
revisões bibliográficas sobre cuja lista de referências internas a
verificação meta-bibliográfica cascateada foi executada) seria
benefício operacional. A sugestão emergiu durante a execução do
Bloco A da Fase A.7 (consequência da decisão 21, A3), e está
registrada em `hallucination-prevention-checklist.md §5.6` na forma
de "registro em campo existente da matriz"; a promoção a coluna
dedicada depende da análise conjunta com as demais decisões sobre
estrutura da matriz pendentes nesta entrada — em particular, do
custo-benefício de expandir o número de colunas obrigatórias e do
impacto sobre o limite de 500 linhas do SKILL.md referido acima.

**Relação com a Frente 3** (Fase 4 — Infraestrutura, subset prioritário,
fechada em 2026-04-25 pela decisão 31). As três colunas obrigatórias do
passo 6 (`data_ultima_verificacao`, `risco_verificacao`,
`fonte_desambiguacao`) não são tocadas pelos scripts produzidos na
Frente 3; o fechamento da §(iii) parcial não força propagação simultânea
ao SKILL.md. A integração (passo 6 do SKILL.md citando os scripts; ou
scripts populando colunas da matriz que alimenta o passo 6) é Frente 4+
candidata.

## (vii) Memórias ativas

**Objetivo.** Resolver memórias **de projeto a resolver** registradas
em `<memory>/MEMORY.md` antes de empilhar novas na Fase 2.

**Recorte explícito (sincronizado em 2026-04-25, decisão de fechamento
da Frente 2).** Esta lista cobre apenas memórias que pedem resolução
operacional — uma ação concreta (incorporar ao código, decidir
canonização, implementar script). Memórias da seguinte natureza
**não** entram aqui:

- *Memórias de feedback durável* (instruções permanentes sobre como
  trabalhar — `feedback_*`): vivem em `<memory>/MEMORY.md` enquanto
  forem aplicáveis e não pedem resolução, são instrução ativa.
- *Memórias de estado/distribuição* (registros de pacote de zip, de
  observação empírica pendente de teste — `a6_*`, `a7_*`, etc.):
  vivem em `<memory>/MEMORY.md` como rastro pontual e expiram
  conforme o estado evolui; também não pedem resolução nesta seção.

A lista a seguir não é exaustiva no sentido de cobrir tudo o que
existe em `<memory>/MEMORY.md` — é exaustiva apenas no recorte "de
projeto a resolver":

- `phase2_verbatim_format_revisit.md` — avaliar alternativas ao formato
  inline `[SOURCED: k | verbatim: "..."]` em parágrafos com muitas
  paráfrases (nota de rodapé? bloco ao fim do parágrafo? painel lateral?).
- `phase2_extract_grey_literature_protocol.md` — avaliar se §5.3 do
  checklist sai para `references/grey-literature-protocol.md` conforme
  múltiplos módulos de domínio passarem a referenciá-la.
- `project_doi_verify_retraction_check.md` — implementar o script com
  os seis estados de retorno e o fallback OpenAlex (usado na pendência
  (iii)).
- `phase2_changelog_decision_13_distinctive_triggers.md` — **resolvida
  parcialmente pela decisão 18 do `_changelog.md`** (numeração de
  decisões pulou para 19+ após canonização da v2; a memória deixa de
  reservar numeração e passa a registrar somente o princípio de
  gatilhos lexicais distintivos para inclusão no `_changelog.md`).
  Pendência residual: avaliar se o princípio merece entrada própria
  no changelog em rodada de Fase 2 ou se permanece como observação
  da memória.
- `project_sync_handoff_memory_list.md` — **resolvida em 2026-04-25**
  pela presente sincronização (decisão de fechamento da Frente 2).
  Memória pode ser removida do `<memory>/MEMORY.md` em rodada
  operacional subsequente.

**Inputs.** As memórias listadas contêm gatilho e critério de decisão
individuais. O arquivo `feedback_ask_before_memoryfying_corrections.md`
orienta o processo de decisão (perguntar antes de salvar novas
memórias enquanto as abertas não forem resolvidas).

**Critério de pronto.** Cada memória fica em estado resolvida, com
decisão registrada no `_changelog.md` (como decisão nova ou refinamento
de existente). Memórias incorporadas à skill podem ser removidas do
`MEMORY.md` após a decisão aparecer no changelog e/ou nos arquivos
operacionais. Inclusão de memória nova nesta lista é decisão
deliberada — apenas memórias de projeto que pedem resolução
operacional entram; memórias de feedback durável ou de estado/registro
não entram.

**Risco conhecido.** Memórias envelhecem silenciosamente. Revisitar
esta seção no início da Fase 2 antes de tomar decisões novas —
preferir resolver abertas a empilhar. Segundo risco: decisões
incorporadas aos arquivos mas não registradas no changelog criam
divergência entre o estado do código e o estado do rastro; toda
decisão incorporada deve aparecer no changelog antes do merge.
Terceiro risco: lista do recorte pode envelhecer se o critério "de
projeto a resolver" for aplicado inconsistentemente em revisões
futuras — manter, na inclusão de memória nova, justificativa explícita
de por que ela cabe (ou não) no recorte.

## (viii) Candidatura a Regra 8 dedicada à Dim. 2 estrutura de sustentação argumentativa

**Objetivo.** Decidir se a Dim. 2 estrutura de sustentação
argumentativa — erro na mobilização retórica da referência quando a
obra existe, os metadados conferem e o conteúdo citado é fiel — merece
regra inegociável própria no `SKILL.md` ou permanece coberta
transversalmente pela Regra 5 (Prosa argumentativa) + Passo 8 do fluxo
obrigatório (autorrevisão cética).

**Inputs.** `_taxonomy-v2-design.md` §4 (definição da categoria e
exemplos construídos); `SKILL.md` Regra 5 e Passo 8 (cobertura
transversal atual); observação registrada na auditoria de A.3 (ausência
de regra dedicada identificada no esboço das regras inegociáveis
reescritas contra a v2).

**Critério de pronto.** Decisão tomada entre dois caminhos abertos, com
registro no `_changelog.md` como decisão nova (numeração 19+):

- **(a)** A.7 mantém seu escopo atual — testar Dim. 3 e calibrar o
  limite "dois ou mais elementos" de `_taxonomy-v2-design.md` §8.1 —
  mas o parágrafo-semente é desenhado de modo a **também** produzir
  casos de Dim. 2 estrutura de sustentação argumentativa (economia de
  teste).
- **(b)** A.7 preserva o escopo atual sem expansão, e uma subfase A.8
  autônoma trata da calibração entre cobertura transversal e regra
  dedicada.

Escolha entre (a) e (b) é de cronograma, não arquitetural — adiar
até o momento de abrir A.7.

**Risco conhecido.** Regra dedicada exige critério operacional claro
para detectar descompasso entre tipo de fonte e uso argumentativo —
julgamento qualitativo cuja concordância interanotador pode ser baixa,
o que o princípio pragmático de proporcionalidade
(`_taxonomy-v2-design.md` §2) considera ao avaliar eixo candidato. Se o
critério operacional não for definível sem ambiguidade, a cobertura
transversal pela Regra 5 + Passo 8 pode ser a solução estável.

## (ix) Limpeza arquitetural do bloco "Pendências ativas" do CLAUDE.md

**Objetivo.** Eliminar a duplicação entre o bloco "Pendências ativas"
de `CLAUDE.md` (itens (i)–(vii) enumerados literalmente) e as seções
correspondentes deste arquivo `_phase2-handoff.md` (fonte da verdade
declarada no próprio bloco). A duplicação contraria a decisão 17 do
`_changelog.md` (apontamento-não-duplicação): o bloco do CLAUDE.md
deve substituir a enumeração literal por parágrafo curto apontando ao
`_phase2-handoff.md`.

**Inputs.** `CLAUDE.md` bloco "Pendências ativas" (sete itens
enumerados); `_phase2-handoff.md` seções (i)–(ix) (fonte da verdade);
decisão 17 do `_changelog.md`.

**Critério de pronto.** Bloco "Pendências ativas" em `CLAUDE.md`
substitui a enumeração por parágrafo curto remetendo ao handoff como
fonte da verdade, sem reproduzir a lista de itens.

**Risco conhecido.** Subfase estritamente de limpeza arquitetural do
CLAUDE.md, distinta de A.4 (reescrita dos módulos derivados em
`references/`). Tratar como subfase autônoma — numeração a definir —
para não misturar escopos nem atrasar A.4. Uma vez executada, o bullet
(v) literal "modo (d) intra" sai do CLAUDE.md; o conteúdo continua
rastreável no handoff §(v) até que A.4 refatore o §(v) em si contra a
taxonomia v2.

## (x) Vetor "cadeia probatória interna contaminada" — reabertura de decisão prévia

**Objetivo.** Decidir a canonização taxonômica do vetor em que uma
referência é existente verificável, com metadados corretos, mas cujas
afirmações se apoiam em referências internas fabricadas — cadeia
probatória da obra citada contaminada em elo interno. Pendência
registrada pela decisão 21 do `_changelog.md` (A.7 Bloco A, A3). Nome
provisório: "cadeia probatória interna contaminada".

**Histórico da decisão arquitetural.** Esta pendência **não é
consideração inicial de vetor novo — é reabertura de decisão prévia**.
A possibilidade de canonizar este tipo de erro em cascata foi
considerada por Sidney na construção original da v2, à luz da
literatura existente sobre cadeias probatórias contaminadas em revisões
de literatura, e foi decidida contra na ocasião. O motivo específico
de reabertura agora é a **evidência empírica direta** obtida no Teste
02 da Fase A.7, distinta de mera revisão de argumento prévio.

**Exemplar empírico.** SOARES et al. (2024) / ALMEIDA-GOMES (2022),
Teste 02 da Fase A.7, ground truth v1.2 §3.7. SOARES et al. é revisão
bibliográfica legítima (DOI `10.61164/rmnm.v12i2.3211` resolve;
metadados corretos). A referência interna "ALMEIDA, J., & GOMES, M.
(2022). O Impacto da Desigualdade Digital no Ensino Remoto Durante a
Pandemia. Revista Brasileira de Educação, 27(3), 101-115" foi
confirmada como fabricação em verificação ativa com três evidências
convergentes: (i) formato de numeração impossível na RBE (volume único
por ano desde 2018, fluxo contínuo, identificadores `e270001` etc.);
(ii) zero ocorrências do título na web fora do próprio artigo de
SOARES; (iii) iniciais genéricas ("Almeida, J.", "Gomes, M.") sem
correspondência no sumário real da RBE 2022.

**Inputs.** Ground truth v1.4 do Teste 02 §3.7 e §4.4 (formalização do
vetor; três evidências convergentes); `_taxonomy-v2-design.md` §4
(definição canônica de Dim. 2 conteúdo afirmado e de Dim. 2 estrutura
de sustentação, contra as quais o vetor precisa ser contrastado);
documento de deliberação em
`<pasta-de-referencias>/skill-development/research/fase-A7-deliberacao-bloco-A.md`
§5 (registro completo do diferimento, da intervenção metodológica de
Sidney e do protocolo de reabertura); `_changelog.md` decisão 21.

**Questão taxonômica aberta.** Duas possibilidades, a serem decididas
à luz do Teste 03:

- sub-variante de **Dim. 2 conteúdo afirmado**, com qualificador
  específico — distinção em relação à Dim. 2 conteúdo afirmado
  canônica (exemplar DANTAS) é que não há distorção entre o que o
  texto citante atribui à obra e o que a obra contém; a distorção é
  interna à cadeia probatória da obra citada;
- **Dim. 4 nova** — "integridade da cadeia probatória interna da obra
  citada" —, eixo adicional condicionado à obra ser existente
  verificável com metadados corretos, distinto das três dimensões
  atuais por operar sobre as referências *da* obra citada, não sobre
  a obra citada em si.

**Critério de pronto.** Decisão de canonização tomada com base no
protocolo de três passos abaixo, registrada como decisão nova no
`_changelog.md`, com consequências operacionais aplicadas a
`_taxonomy-v2-design.md` (se canonizada). Se não canonizada, a
heurística operacional de `hallucination-prevention-checklist.md` §5.6
permanece como cobertura suficiente, e o registro é fechado no
changelog como decisão de manutenção do estado atual.

**Protocolo de três passos para o Teste 03.**

1. **Replicação empírica do vetor em exemplares distintos.** O desenho
   do Teste 03 precisa produzir ao menos dois exemplares adicionais de
   "cadeia probatória interna contaminada" em revisões bibliográficas
   distintas de SOARES, para testar se o padrão se replica ou se o caso
   do Teste 02 foi artefato do parágrafo-semente. Critério de sucesso:
   ao menos um exemplar adicional confirmado por verificação ativa com
   evidências convergentes análogas às três do Teste 02.
2. **Recuperação e confronto dos argumentos originais contra
   canonização.** Sidney decidiu contra a canonização na construção
   original da v2, à luz de literatura sobre cadeias probatórias
   contaminadas. Recuperar esses argumentos em forma registrada antes
   do Teste 03, se estiverem em forma registrada (anotações de sessão,
   notas de pesquisa, manuscrito-fonte da v2). Caso contrário, marcar
   essa recuperação como pendência adicional ao handoff, a ser
   executada antes do Teste 03 começar.
3. **Decisão de canonização.** Canonizar apenas se a evidência nova
   do Teste 03 (passo 1) for suficiente para **superar** as razões
   originais (passo 2). Decisão por replicação empírica sem confronto
   explícito aos argumentos originais não fecha a pendência — fecha
   apenas a parte empírica dela.

**Risco conhecido.** Dois riscos principais. Primeiro: o Teste 03 pode
replicar empiricamente o vetor mas falhar em superar os argumentos
originais contra canonização — nesse caso, o resultado correto é
manter a cobertura via heurística operacional em `hallucination-
prevention-checklist.md` §5.6 e fechar o registro sem canonização.
Segundo: se os argumentos originais não estiverem em forma registrada,
o custo de recuperação por reconstrução pode ser alto; convém
marcar agora a recuperação como pendência explícita para não
comprometer o cronograma do Teste 03.

### Execução do passo 2 (2026-04-24)

Passo 2 do protocolo de três passos — recuperação e confronto dos
argumentos originais contra canonização — **executado e fechado**
em sessão Papel 1 (Claude navegador) em 2026-04-24, registrado em
decisão 29 do `_changelog.md`. Argumentos recuperados em três
fontes canônicas: `_taxonomy-v2-design.md` §2.2 (regra formal de
quatro critérios cumulativos para admissão de eixos candidatos);
`_taxonomy-v2-design.md` §11 (justificativa específica do descarte
da categoria Cascatas sistêmicas — restrição de unidade de análise
— e gate explícito de reentrada); `fase-A1-manuscrito-taxonomia-v2.md`
§3.5 (fundamentação ampliada). Consolidação em documento-registro
dedicado:
`<pasta-de-referencias>\skill-development\research\fase-A8-recuperacao-argumentos-cadeia-probatoria.md`.

O documento-registro fixa três elementos operacionais contra os
quais o passo 3 precisa confrontar a evidência empírica do Teste
03: (i) a regra formal de §2.2; (ii) a justificativa específica do
descarte em §11; (iii) o gate de reentrada em §11. Também precisa
a distinção entre "item-por-item estendido" e "dupla-referência-em-
relação", estabelecendo que depth-1 não é extensão natural da
unidade de análise da v2, mas introdução de unidade composta. Passo
3 permanece pendente da execução do Teste 03; a canonização é
sustentável apenas se a evidência nova superar cada um dos três
elementos.

## (xi) Heurística B2 "inconsistência temporal interna como sinal de confabulação" — descartada (A.7 Bloco B)

**Status.** **Descartada** pela decisão 24 do `_changelog.md` (A.7
Bloco B, Cluster I). Não incorporada ao `hallucination-prevention-
checklist.md`. A entrada, originalmente aberta em 2026-04-23 como
"tratamento no Cluster I do Bloco B" (três caminhos considerados:
descarte, resgate estreito, suspensão), fica resolvida aqui com
registro do motivo do descarte para reabertura eventual em rodadas
futuras.

**Heurística candidata.** "Inconsistência temporal interna no título,
resumo ou corpo de uma referência constitui sinal de confabulação."
Proposta pelo Claude.ai navegador no Teste 02 da Fase A.7, a partir da
observação sobre o recorte "2019-2021" no título de MAGALHÃES; ROCHA,
interpretado durante a execução do Papel 2 como sinal de confabulação.

**Motivo do descarte: contra-exemplo empírico direto da rodada que
propôs.** A reclassificação em v1.5 (decisão 23 do `_changelog.md`)
estabeleceu que MAGALHÃES; ROCHA é **existente verificável** e que a
inconsistência temporal é real no próprio artigo (página 2 do PDF:
*"Em 2019, com o advento da pandemia de Covid-19..."*, quando o
advento da pandemia foi em 2020), derivada da adoção do período
"2019-2021" do relatório IBGE SIS como recorte da análise. A
inconsistência é **imprecisão histórica do próprio artigo real** —
não sinal de confabulação. O caso falseia diretamente a heurística
que ele próprio propôs; se aplicada, a regra produziria o mesmo falso
positivo de pastiche que os dois ambientes do Papel 2 cometeram.

**Racional da decisão.** No Cluster I do Bloco B (deliberação em
sessão de Papel 1 via Sidney), ponderaram-se três caminhos:
(i) descarte; (ii) resgate estreito, reformulando B2 de "sinal de
confabulação" para "sinal de que a referência merece atenção
adicional"; (iii) suspensão, adiando a decisão até acumular mais
dados. O descarte foi aceito como caminho correto. Justificativa:
heurística que nasce com contra-exemplo direto dentro da própria
rodada que a propôs parte de lugar epistemicamente frágil demais para
ser incorporada como regra ativa; o resgate estreito tornaria B2
quase inoperacional ("merece atenção adicional" é cobertura ampla
demais para valer como heurística dedicada); a suspensão seria custo
sem benefício imediato. Objeção considerada: viés de sobrecorreção
sobre contra-exemplo único. Respondida: a heurística é descartada
**com critério explícito de reabertura** (abaixo), o que permite
reavaliação à luz de casos positivos em rodadas subsequentes sem
compromisso prematuro no checklist atual.

**Critério de reabertura.** B2, na forma original ou em variante,
pode ser reaberta se e somente se surgir em rodadas futuras **caso
positivo documentado** em que inconsistência temporal interna tenha
sido efetivamente sinal de confabulação — referência com
inconsistência temporal interna **e** confirmada como fabricação ou
pastiche por verificação ativa independente. Reabertura segue o
padrão dos "Critérios de reabertura" do Bloco A (entrada nova no
`_changelog.md` sucedendo a decisão 24; consequências operacionais
aplicadas ao checklist).

**Documentação do falseamento.** Documento-registro em
`fase-A7-reclassificacao-magalhaes-rocha.md` §5.4; avaliação do
Claude.ai navegador v1.5 §3.5 (reinterpretação operacional da
observação original); entrada 24 do `_changelog.md` (Bloco B).

## (xii) Verificação manual externa como etapa arquitetural formal em Testes 03+

**Objetivo.** Avaliar incorporação de janela explícita de **verificação
manual externa pelo decisor** como etapa arquitetural formal no
protocolo de Testes 03 e posteriores, posicionada entre a ground truth
construída pelo Papel 1 e a execução do Papel 2. Proposta arquitetural
registrada em §6 do `fase-A7-reclassificacao-magalhaes-rocha.md`; não
é decisão tomada, é candidatura a deliberação formal.

**Origem.** Dois casos empíricos convergentes na Fase A.7 em que a
reclassificação ocorreu **depois** do Papel 2, com impacto sobre as
avaliações: CARDOSO; BERTONI (reclassificado em v1.1 após leitura
direta do PDF no OJS da UESB por Sidney; ajustado novamente em v1.4
para ano canônico) e MAGALHÃES; ROCHA (reclassificado em v1.5 após
leitura direta do PDF no OJS Portal Espiral do CP2 por Sidney). Em
ambos, a verificação manual externa foi tratada como intervenção
ad hoc disparada por divergência observada durante ou após a
avaliação; em ambos, antecipá-la teria evitado reclassificações
post-hoc com propagação para múltiplos documentos.

**Inputs.** §6 do documento-registro da reclassificação;
`teste02_ground_truth_2026-04-22_v1.5.md` §§1.2 e 6 (convenção de
"ground truth como baseline revisável"); `fase-A7-deliberacao-bloco-A.md`
(protocolo de execução vigente para o Bloco A); estrutura atual de
Papéis 0–3 registrada na ground truth v1.5 §1 e no preâmbulo da
síntese comparativa.

**Critério de pronto.** Decisão arquitetural sobre protocolo de
Testes 03+ tomada e registrada como entrada nova no `_changelog.md`
ou em documento de processo próprio no `research/` da pasta de referências
(conforme convenção aplicável no momento). Dois caminhos abertos:

- **Incorporação.** Janela formal de verificação manual externa
  entre Papel 1 e Papel 2 vira etapa obrigatória do protocolo de
  Testes 03+, com critério explícito de acionamento (ex.: toda
  referência classificada como pastiche ou inexistente-fabricada
  pelo Papel 1 passa por verificação manual antes do Papel 2) e
  registro do resultado na ground truth pré-rodada. Consequência
  operacional: protocolos dos Testes 03+ documentados com a nova
  etapa; templates de ground truth (se houver) atualizados.
- **Não incorporação.** Mantém-se o padrão atual (verificação manual
  ad hoc sob gatilho), registrando no changelog as razões contra
  formalização (ex.: custo de tempo do decisor em rodadas maiores;
  risco de deslocar autoridade da busca automatizada para o
  julgamento humano antes da necessidade). Registrar convenção de
  escalonamento para casos ambíguos.

**Risco conhecido.** **Custo-benefício em rodadas maiores**. A
proposta foi empiricamente sustentada em dois casos na Fase A.7 com
corpus de sete referências; em rodadas com corpus mais amplo (20+
referências), o custo de verificação manual pré-rodada cresce
linearmente e pode inviabilizar a janela. Mitigação: se incorporada,
definir critério de acionamento **seletivo** (só referências em
zona de alta incerteza da ground truth, não todas), para manter
o custo compatível com cronogramas realistas. Segundo risco:
**captura da ground truth pelo decisor**. Se a verificação manual
for sistemática, a ground truth passa a depender do acesso do
decisor a fontes institucionais fora das bases automatizadas,
deslocando parte da autoridade do Papel 1 (construção) para o
decisor. Mitigação: documentar explicitamente o deslocamento como
decisão de processo, com registro da diferença entre a ground truth
construída pelo Papel 1 e a ground truth pós-verificação manual
do decisor — já convencionada informalmente em v1.1/v1.4/v1.5 do
Teste 02 via notas de versão, mas a formalizar.

## (xiii) Heurística B3 "autor com agenda adjacente amplifica risco pastiche" — descartada (A.7 Bloco B)

**Status.** **Descartada** pela decisão 24 do `_changelog.md` (A.7
Bloco B, Cluster I). Não incorporada ao `hallucination-prevention-
checklist.md`.

**Heurística candidata.** "A presença de autor com agenda de pesquisa
adjacente ao tema da referência eleva o risco de pastiche — o autor é
real, o tema do autor é adjacente, a plausibilidade cognitiva de uma
fabricação amparada nessa adjacência é alta, e o pesquisador tende a
duvidar menos." Proposta pelo Claude.ai navegador no Teste 02 da
Fase A.7, a partir da observação sobre MAGALHÃES; ROCHA (artigo
adjacente real em *Manguinhos* 2021 do mesmo primeiro autor).

**Motivo do descarte duplo.**

- **(i) Contradição lógica direta com B6 (§9.1 do checklist).** A
  §9.1 afirma que desalinhamento entre agenda histórica do autor e
  tema da referência **não constitui** evidência contra existência;
  B3, na forma proposta, afirma o oposto (adjacência de agenda
  amplifica risco pastiche, o que é argumento contra existência em
  presença de não-localização). As duas heurísticas não podem
  coexistir como regras ativas sem contradição interna da §9 — e B6
  foi a incorporada como §9.1 após deliberação no Cluster I.
- **(ii) Contra-exemplo empírico direto em MAGALHÃES; ROCHA após
  v1.5.** O caso que parecia sustentar B3 na rodada original (o
  artigo adjacente em *Manguinhos* foi lido pelos dois ambientes
  como reforço da hipótese de pastiche) virou, na v1.5, **o caso
  canônico do falso positivo** que B3 produziria. A referência é
  existente verificável; o mesmo pesquisador é co-autor, com Leila
  Silva da Rocha, da referência real na *Revista Encontros* do CP2.
  A adjacência de agenda é, nesse caso, indício do par autoral
  **real** — não evidência contra existência.

**Racional da decisão.** Os dois motivos são cumulativamente
suficientes para descarte — qualquer um deles isoladamente o
justificaria. Manter B3 como regra ativa exigiria revogar B6, o que
contrariaria a evidência empírica dupla (CARDOSO; BERTONI e
MAGALHÃES; ROCHA) que a sustenta. Manter B3 como heurística adjacente
(§8) também foi considerado e rejeitado: heurística adjacente que
contradiz regra ativa da §9 introduziria incoerência de orientação
ao revisor cético.

**Critério de reabertura.** B3, na forma original ou em variante,
pode ser reaberta se e somente se surgir em rodadas futuras **caso
positivo robusto** em que a adjacência de agenda do autor tenha sido
efetivamente sinal de pastiche em contexto distinto do Teste 02
(i.e., caso em que outras evidências independentes confirmem o
pastiche, e a adjacência de agenda tenha acrescentado poder
diagnóstico real). A reabertura precisa também **reconciliar** o novo
caso com a §9.1 — se os dois não puderem coexistir, a reabertura
exige deliberação explícita sobre qual das duas regras prevalece.
Reabertura segue o padrão dos "Critérios de reabertura" do Bloco A
(entrada nova no `_changelog.md` sucedendo a decisão 24; consequências
operacionais aplicadas ao checklist).

**Documentação do falseamento.** Documento-registro em
`fase-A7-reclassificacao-magalhaes-rocha.md` §5 (reinterpretação da
observação do artigo adjacente); avaliações do Papel 3 v1.5 (navegador
§3.5 e Desktop §3.5, reinterpretações convergentes); entrada 24 do
`_changelog.md` (Bloco B).

## (xiv) Classe "indeterminada" em Dim. 1 — reconhecimento taxonômico formal

**Objetivo.** Avaliar se a prática editorial de **suspensão do
veredito em Dim. 1** — operacionalizada em `hallucination-prevention-
checklist.md` §9.3 via heurística B5 (regra de desempate em
"indeterminada" diante de alcance limitado de busca ativa) — merece
reconhecimento taxonômico formal na v2 como **quarto valor canônico
de Dim. 1** (ao lado de existente verificável, pastiche e
inexistente-fabricada), ou deve permanecer como **prática editorial
adjacente** da skill sem compromisso taxonômico correspondente.

**Origem.** Gatilho empírico: a deliberação do Bloco B (decisão 24 do
`_changelog.md`) sobre B5 identificou que o estado atual da v2
(três valores canônicos em Dim. 1; `_taxonomy-v2-design.md` §3)
não prevê a situação operacional típica capturada por B5 —
não-localização da referência como unidade bibliográfica com pelo
menos duas das três evidências parciais presentes (par autoral real,
evento real, veículo real). A saída pragmática adotada no checklist
foi registrar a suspensão como prática editorial; a pergunta
taxonômica ficou aberta.

**Inputs.** `hallucination-prevention-checklist.md` §9.3 (redação da
heurística B5; critério "dois dos três"; nota sobre estatuto da
suspensão); `_taxonomy-v2-design.md` §3 (definição canônica dos três
valores de Dim. 1 na v2); §2.2 do mesmo arquivo (regra de decisão
para extensões da taxonomia — quatro critérios cumulativos: ganho
demonstrável, custo compatível, não redundância, orientação corretiva
distinta); §8.1 (casos limítrofes pastiche × inexistente-fabricada,
que contêm tensão análoga); exemplares empíricos CARDOSO; BERTONI e
MAGALHÃES; ROCHA (ground truth v1.5 do Teste 02).

**Questão taxonômica aberta.** Três configurações possíveis:

- **(a) Incorporação como quarto valor canônico.** Dim. 1 passa a ter
  quatro valores: existente verificável, pastiche, inexistente-
  fabricada, **indeterminada**. A §9.3 do checklist deixa de ser
  prática editorial e passa a ser protocolo de classificação.
  Critérios de §2.2 a examinar: ganho (a classe captura situação
  operacional frequente em fontes brasileiras, com evidência dupla
  no Teste 02); custo (custo de classificação incremental é baixo);
  não redundância (a indeterminada é empiricamente distinta de
  pastiche e de inexistente-fabricada, no sentido de que o
  veredicto é **ausência de fechamento**, não **presença de
  fabricação**); orientação corretiva (a ação orientada pela
  indeterminada é "consultar portal institucional e, se persistir,
  registrar suspensão", distinta das ações das outras três
  classes). Os quatro critérios parecem satisfeitos, mas a avaliação
  formal cabe à saída de deliberação arquitetural.
- **(b) Permanência como prática editorial adjacente.** A §9.3
  mantém-se como regra operacional do checklist sem reconhecimento
  taxonômico na v2. Vantagem: preserva a arquitetura dimensional
  enxuta da v2 (decisão 18 do `_changelog.md`) e evita proliferação
  taxonômica. Risco: divergência entre vocabulário operacional
  (checklist suspende em "indeterminada") e vocabulário taxonômico
  (v2 não tem "indeterminada") pode gerar ambiguidade em relatórios
  diagnósticos e em comparações interanotador.
- **(c) Incorporação como qualificador de Dim. 1, não como quarto
  valor.** Dim. 1 mantém os três valores canônicos, mas ganha
  qualificador explícito "[suspenso]" aplicável a cada valor quando
  a busca for inconclusiva. Configuração intermediária: preserva
  arquitetura enxuta e endereça o risco de divergência vocabular.

**Critério de pronto.** Decisão tomada em deliberação arquitetural
formal (sessão de Papel 1 análoga às do Bloco A), com registro como
entrada nova no `_changelog.md` sucedendo a decisão 24. Se a saída
for (a), consequências operacionais aplicadas ao
`_taxonomy-v2-design.md` §3 (inclusão do valor), §4 (ajuste de
aplicabilidade — Dim. 2 não aciona quando Dim. 1 = indeterminada),
§6 (atualização da árvore decisória), §8 (eventual casos limítrofes
novos entre indeterminada e pastiche) e à redação de §9.3 do
checklist (prática editorial ↔ protocolo taxonômico). Se for (b) ou
(c), consequências menores, documentadas na entrada do changelog.

**Risco conhecido.** **Proliferação taxonômica** vs. **ambiguidade
vocabular**. O risco central é optar por (a) e descobrir em rodadas
futuras que "indeterminada" absorve casos que eram pastiche ou
inexistente-fabricada limítrofes, tornando a classificação mais
indulgente e o papel diagnóstico da v2 menos afiado. Mitigação: se
(a) for aprovada, definir critério de distinção explícito entre
indeterminada e pastiche no §8.1 — indeterminada é fechamento
suspenso por alcance limitado; pastiche é fechamento afirmativo em
presença de combinação probabilística. Segundo risco: optar por (b)
e observar que a divergência entre checklist e taxonomia cria
ambiguidade recorrente em relatórios, exigindo reabertura da
questão com custo de retrabalho. Mitigação: se (b) for aprovada,
adicionar glossário operacional no `_taxonomy-v2-design.md`
registrando "indeterminada" como termo editorial da skill sem
compromisso taxonômico.

## (xv) Vigilância do tamanho do SKILL.md — avaliação de reorganização em blocos futuros

**Objetivo.** Monitorar o crescimento do `SKILL.md` em subfases
posteriores e avaliar, se o arquivo continuar crescendo, se a
**reorganização** — movimentação de material auxiliar para
`references/`, preservando regras ativas no corpo do SKILL.md — é
caminho mais saudável do que compressão de regras ativas ou do que
seguir acumulando conteúdo acima do limite aspiracional de 500 linhas
(boa prática de progressive disclosure). **Pendência de vigilância
arquitetural, não de execução imediata.**

**Origem.** Gatilho empírico: execução do Bloco C da Fase A.7
(decisões 25 e 26 do `_changelog.md`) levou o `SKILL.md` de 397 para
539 linhas, excedendo o limite em 39 linhas. A decisão de aceitar o
excedente foi consciente, registrada na decisão 26 — a seção D
(C2.1) é regra de modo operacional de leitura na inicialização, não
referência auxiliar, e sua movimentação para `references/` foi
avaliada e rejeitada pelo risco de reintroduzir o gap de gatilho que
a síntese comparativa §5.1 identificou como hipótese causal H2/H3
(leitura sob demanda não garante que o modo diagnóstico seja lido
quando necessário). Esta entrada formaliza a **disciplina de rastro**
sobre o excedente e a diretriz para blocos futuros.

**Inputs.** `SKILL.md` em seu estado atual (539 linhas, pós-Bloco C);
decisão 26 do `_changelog.md` (justificativa do excedente e
alternativa rejeitada); síntese comparativa do Teste 02 §5.1
(hipóteses causais sobre exteriorização do vocabulário v2);
decisão 8 do `_changelog.md` (princípio "detecção reduz fricção,
não impõe"); decisão 13 (glossário de termos operacionais no SKILL.md
como proteção contra órfãos).

**Critério de pronto.** Revisitar esta entrada ao fim de cada bloco
futuro que toque o `SKILL.md` e decidir entre três caminhos:

- **(a) Estabilidade.** O `SKILL.md` não cresceu significativamente
  desde o Bloco C; manter o estado, sem intervenção. Esta entrada
  permanece aberta como monitor passivo.
- **(b) Reorganização preventiva.** O `SKILL.md` cresceu o suficiente
  para justificar movimentação de **material auxiliar** (candidato
  primário: o glossário de termos operacionais, atualmente no corpo
  do SKILL.md por decisão 13; pode migrar para
  `references/glossary.md` com SKILL.md preservando apenas ponteiro
  + lista de termos). Regras ativas — Regras inegociáveis, D1–D3,
  Passo 0, fluxo obrigatório, módulos de referência, regras de
  comportamento — **permanecem** no corpo do SKILL.md.
- **(c) Revisão do limite.** O crescimento acumulado sugere que o
  limite de 500 linhas foi subdimensionado para o escopo real da
  skill pós-v2. Reavaliar o limite em deliberação arquitetural
  formal, com registro de novo limite no `CLAUDE.md` ou no
  `_master-guide.md`.

Decisão registrada como entrada nova no `_changelog.md` quando
qualquer dos três caminhos for acionado; até lá, esta entrada fica
aberta como vigilância.

**Risco conhecido.** Dois riscos simétricos. Primeiro, **compressão
indevida de regras ativas**: se a pressão pelo limite de 500 empurrar
para comprimir D1–D3, a Regra 6, o Passo 0 ou o fluxo obrigatório,
a skill perde precisão operacional — o custo da compressão recai em
situações em que a regra precisa estar explícita para ser aplicada.
Mitigação: priorizar caminho (b) sobre (c), e caminho (c) sobre
compressão. Segundo, **inflação silenciosa**: se blocos futuros
acrescentam conteúdo sem reavaliar o limite, o `SKILL.md` pode
crescer indefinidamente. Mitigação: esta entrada é revisitada ao fim
de cada bloco que toque o `SKILL.md`, forçando decisão explícita em
vez de deriva.

## (xvi) Hipóteses causais sobre divergência navegador × Desktop — triagem condicional

**Objetivo.** Registrar, para Fase 2, a pendência de triagem das
hipóteses causais sobre **exteriorização do vocabulário v2** (vetor 1
da síntese comparativa do Teste 02 §5 — H1, H2, H3), com critério
de fechamento condicional a decisão de Fase 2 sobre investimento em
rodadas dedicadas.

**Origem.** Síntese comparativa do Teste 02 §5, que identificou dois
vetores sistemáticos de divergência entre Claude.ai navegador e
Claude Desktop e propôs seis hipóteses causais (três por vetor),
explicitando que nenhuma é testável com N=1 por ambiente e que a
triagem requer rodadas adicionais.

**Hipóteses do vetor 1 (exteriorização do vocabulário v2).** Três
hipóteses sobre por que os dois ambientes divergem na estrutura da
resposta (formalização dimensional no Desktop × prosa contínua no
navegador), caracterizada pela síntese §5.3 como **custo de
auditabilidade, não erro de conteúdo**:

- **H1** — pressão estilística/conversacional do navegador penaliza
  formalização dimensional;
- **H2** — gatilho do `SKILL.md` e do `_taxonomy-v2-design.md`
  assimétrico entre ambientes (documentos lidos em profundidade
  diferente);
- **H3** — resposta inline vs. como artefato (estrutura dimensional
  prospera em artefato, dispersa em conversação).

**Inputs.** Síntese comparativa do Teste 02 §5 (formulação original
das seis hipóteses e estratégia de investigação); decisão 22 do
`_changelog.md` (refinamento operacional da Dim. 3); "Pré-condições
do Teste 03" deste handoff, objetivo (A4).

**Critério de pronto.** Fecha por qualquer uma de três vias, com
decisão registrada explicitamente:

- **(i) Rodadas dedicadas executadas.** Desenho experimental definido
  em Fase 2 (a síntese §5.3 estima 3 variantes de prompt × 2
  ambientes × N=3 = 18 rodadas como ponto de partida, revisável).
  Resultado registrado em relatório da rodada e, se relevante, em
  entrada nova do `_changelog.md`.
- **(ii) Arquivamento formal.** Fase 2 decide explicitamente não
  investir em rodadas dedicadas; pendência arquivada como "custo de
  auditabilidade aceito", com registro da decisão no `_changelog.md`
  e critério de reabertura (surgimento de evidência de que a
  divergência de exteriorização compromete substância, e não só
  auditabilidade).
- **(iii) Reaproveitamento oportunista.** Rodadas de Fase 2
  executadas por outra razão permitem isolar o efeito de H1–H3; a
  triagem fecha como resultado lateral, sem custo dedicado. Registro
  em relatório da rodada original.

**Vetor 4 (Dim. 3 conceitual × factual).** As hipóteses do vetor 4
foram endereçadas fora desta entrada: **H4** (ambiguidade
terminológica) e **H5** (gatilho fraco da subdistinção) foram
parcialmente endereçadas pela decisão 22 do `_changelog.md` (A.7
Bloco A, A4), que adicionou ao `_taxonomy-v2-design.md` §5 o
refinamento operacional da Dim. 3; **H6** (uso residual de memória
paramétrica) está registrada como observação no objetivo (A4) das
"Pré-condições do Teste 03" deste handoff, a ser triada com o
material empírico produzido pelo Teste 03.

**Risco conhecido.** **Sobre-especificação do desenho experimental.**
Registrar aqui o desenho das 18 rodadas em detalhe fixaria
prematuramente uma configuração que a Fase 2 pode precisar ajustar.
Mitigação: o desenho detalhado fica para o documento da rodada que
executar; esta entrada registra apenas as hipóteses e as três vias
de fechamento.

### Resolução (2026-04-24)

Pendência **resolvida via critério (ii) — arquivamento formal**,
registrado na decisão 28 do `_changelog.md` (A.8). O Passo 1 do
Caminho C (10 rodadas baseline, cinco por ambiente, classificação
humana cega inter-ambiente registrada em
`<pasta-de-referencias>\skill-development\test-reports\caminho-c-fase-A.8\registro-preenchido.xlsx`)
produziu zero rodadas "ausentes" nos dois ambientes — a hipótese
forte do vetor 1 ficou diretamente falseada, e a divergência observada
no Teste 02 foi artefato de N=1. Passo 2 do Caminho C não executado.
Critério de reabertura: **≥3 rodadas consecutivas "ausentes" em um
ambiente enquanto o outro mantém "pleno" ou "parcial" nas rodadas
correspondentes, com pelo menos N=5 por ambiente** — detalhes e
racional na decisão 28. Achado lateral sobre possível frouxidão do
gatilho dimensional (distribuição 2-3 / 3-2 entre "pleno" e "parcial")
registrado como pendência nova em §(xvii), independente desta
resolução.

## (xvii) Frouxidão potencial do gatilho de classificação dimensional sistemática na skill

**Objetivo.** Avaliar, em Fase 2, se o gatilho atual para aplicação
sistemática do vocabulário dimensional da taxonomia v2 em **modo
diagnóstico** (regras D1–D3 da decisão 26 do `_changelog.md`) é
suficientemente firme para produzir classificação **plena** como
regra, ou se permite com frequência rotulagem **parcial** (invocação
de uma ou duas dimensões sem cobrir o conjunto aplicável previsto pela
árvore decisória). Pendência sobre o gatilho interno da skill, não
sobre divergência entre ambientes.

**Origem.** Achado lateral do Passo 1 do Caminho C da Fase A.8
(decisão 28 do `_changelog.md`). Em 10 rodadas baseline — cinco por
ambiente, parágrafos-semente comparáveis ao Teste 02, classificação
humana cega inter-ambiente —, a distribuição entre "pleno" e "parcial"
ficou 2-3 no navegador e 3-2 no Desktop, com zero "ausentes". A
simetria geral entre ambientes removeu a hipótese de divergência
sistemática do vetor 1 da §(xvi); a proporção 50/50 pleno-parcial
**em ambos os ambientes**, porém, sugere que o problema — se houver —
está no gatilho interno da própria skill, não na diferença entre
plataformas de execução.

**Hipóteses sobre o mecanismo.** Três leituras possíveis, a triar com
material empírico dirigido:

- **(a)** O gatilho de D1–D3 no SKILL.md é ambíguo sobre cobertura
  exigida: a regra D1 diz "toda avaliação de referência deve
  exteriorizar o rótulo dimensional v2 explicitamente", com formato
  que prevê Dim. 1 sempre, Dim. 2 quando aplicável e Dim. 3 quando
  aplicável. A aplicação parcial observada pode indicar que "quando
  aplicável" é interpretado com latitude — i.e., a skill invoca Dim. 1
  ou Dim. 2 sozinha em casos onde a árvore decisória pede as três
  aplicáveis.
- **(b)** O corpus de exemplares canônicos em `_taxonomy-v2-design.md`
  §3–§5 e §8 é denso em combinações parciais (rotulagens que ilustram
  uma dimensão por vez), o que pode enviesar a aplicação para
  subconjuntos em vez do conjunto aplicável completo.
- **(c)** Classificação dimensional plena em diagnóstico de parágrafo-
  semente com múltiplas referências tem custo cognitivo não trivial —
  a skill pode estar economizando rotulagem em parte dos casos por
  efeito prático, não por falha de gatilho.

**Inputs.** `SKILL.md` seção "Regras de exteriorização dimensional em
modo diagnóstico" (D1–D3, redação atual); `_taxonomy-v2-design.md`
§3–§5 e §8 (exemplares e árvore decisória); decisão 26 do
`_changelog.md` (canonização das regras); planilha de registro do
Caminho C Passo 1 em
`<pasta-de-referencias>\skill-development\test-reports\caminho-c-fase-A.8\registro-preenchido.xlsx`
(rodadas individuais e categoria "parcial" anotada em cada rodada
aplicável); decisão 28 do `_changelog.md` (contexto empírico da
triagem).

**Critério de pronto.** Decisão tomada sobre o estatuto da observação:

- **(a) Refinamento do gatilho.** Redação de D1 reforçada para
  explicitar que "exteriorizar o rótulo dimensional" significa cobrir
  **todo** o conjunto aplicável pela árvore decisória (Dim. 1 sempre;
  Dim. 2 se Dim. 1 = existente verificável; Dim. 3 se Dim. 2 =
  conteúdo afirmado), não um subconjunto conveniente. Eventual
  revisão de exemplares canônicos para cobrir o conjunto aplicável
  completo quando a árvore o pede. Consequências operacionais em
  `SKILL.md` e, se necessário, em `_taxonomy-v2-design.md` §8.
- **(b) Permanência do estado atual.** A classificação "parcial"
  observada é adequada na maioria dos casos e o custo de forçar
  cobertura completa supera o ganho de auditabilidade. Registrar no
  changelog a decisão de não intervir, com critério de reabertura se
  observação futura mostrar que "parcial" está absorvendo casos onde
  a dimensão omitida alteraria a orientação corretiva.

**Risco conhecido.** **Viés retrospectivo sobre amostra pequena.**
A amostra de N=5 por ambiente é suficiente para triar a existência de
divergência inter-ambientes (vetor 1 da §(xvi) resolvida), mas é
limitada para caracterizar com precisão a distribuição interna pleno /
parcial. Mitigação: a pendência é de avaliação em Fase 2, não de
intervenção imediata; a decisão sobre (a) ou (b) pode depender de
observação adicional em rodadas de outras fases (Teste 03, Teste 04)
onde a classificação dimensional for incidental, sem custo dedicado de
rodadas experimentais específicas para esta pergunta.

## Pré-condições do Teste 03

Seção introduzida pelas decisões 21 e 22 do `_changelog.md` (A.7 Bloco
A, A3 e A4; observação de fechamento 7.1 do documento de deliberação),
expandida pela decisão 23 (A.7 Teste 02, reclassificação de
MAGALHÃES; ROCHA) para acomodar pendência adicional sobre Dim. 1
pastiche. Registra condições que o desenho do Teste 03 deve
satisfazer para fechar as pendências empíricas herdadas do Bloco A e
da reclassificação do Teste 02.

**Três objetivos empíricos simultâneos.** O Teste 03 precisa cumprir,
no mesmo desenho de material:

- **(A3)** Replicar o vetor "cadeia probatória interna contaminada"
  em exemplares distintos, conforme passo 1 do protocolo em §(x).
- **(A4)** Produzir exemplar genuíno de **Dim. 3 conceitual**, para
  fechar o refinamento da decisão 22 com ambos os lados exercidos
  empiricamente. O refinamento atual apoia-se em exemplar conceitual
  construído a partir da literatura (conflação Bourdieu/Foucault em
  torno de biopolítica), não observado em teste — baseline revisável
  à luz de empiria dirigida. Ao executar o Teste 03 sobre este
  objetivo, observar também se a classificação do Papel 2 é
  consistente com regra explícita (§5 do `_taxonomy-v2-design.md`
  refinado) ou compatível com aplicação por analogia interna
  (hipótese H6 da síntese comparativa §5.2 — uso residual de memória
  paramétrica). Esta observação fornece material para a triagem de
  H4–H6 registrada em §(xvi).
- **(Teste 02 v1.5)** Produzir exemplar genuíno de **Dim. 1 pastiche
  stricto sensu**. A reclassificação de MAGALHÃES; ROCHA (decisão 23)
  removeu a única referência que sustentava empiricamente a categoria
  pastiche no Teste 02, deixando a cobertura da Dim. 1 pastiche em
  vácuo empírico dentro da Fase A.7. A categoria é centralmente
  importante para a v2 (contribuição de McGowan et al. 2023
  incorporada como valor intermediário da Dim. 1, ver
  `_taxonomy-v2-design.md` §1 e §3); o desenho do Teste 03 deve
  incluir ao menos uma referência fabricada com estrutura de
  pastiche — elementos (autor, título, periódico, ano) de múltiplas
  obras reais combinados probabilisticamente, sem unidade
  bibliográfica subjacente —, preferivelmente intra-autoral para
  também exercitar §8.2 do `_taxonomy-v2-design.md`. Pendência
  paralela à de Dim. 3 conceitual registrada em ground truth v1.5
  §5.2 e reforçada aqui.

Os três objetivos **não são antagônicos**: um mesmo desenho de
material pode endereçar todos se a construção for deliberada. O
parágrafo-semente do Teste 03 pode, por exemplo, incluir uma revisão
bibliográfica com referências internas fabricadas (A3) cuja paráfrase
no texto citante também conflita posições teóricas de correntes
divergentes atribuídas a autores do corpus (A4 — Dim. 3 conceitual),
ao lado de uma referência adicional com estrutura de pastiche
intra-autoral (Teste 02 v1.5). A compatibilização precisa estar no
**desenho**, não emergir por acaso.

**Consequência operacional.** Ao abrir o Teste 03, consultar esta
seção antes de fechar o desenho do parágrafo-semente. Se o desenho
não endereçar todos os objetivos, registrar explicitamente no
relatório do Teste 03 qual pendência fica para teste subsequente e
por quê.

## Critérios de reabertura

Seção introduzida pelas decisões 20 e 21 do `_changelog.md` (A.7 Bloco
A, A2 e A3; observação de fechamento 7.2 do documento de deliberação).
Registra, para decisões de diferimento ou descarte parcial tomadas no
Bloco A, os critérios sob os quais a questão pode ser reaberta em
rodadas futuras. Redundância deliberada com os registros
correspondentes em `_taxonomy-v2-design.md` §8.6 e
`hallucination-prevention-checklist.md` §5.6 — dois pontos de entrada
garantem que o gate apareça tanto para quem toca a taxonomia quanto
para quem consulta o handoff no início de fase.

**A2 — "Inflação retórica de certeza" e "conclusão normativa passando
como síntese científica".** Canonização das duas variantes como valores
v2 da Dim. 2 estrutura de sustentação argumentativa pode ser reaberta
se e somente se forem satisfeitos, cumulativamente, os dois critérios
abaixo:

- **(i)** Detecção independente em ambiente distinto do Desktop, em
  testes futuros — critério empírico da decisão 19 (A.7 Bloco A, A1):
  dupla detecção em ambientes que não se comunicam, em temporização
  separada, sem acesso à ground truth.
- **(ii)** Atendimento à cláusula de fronteira externa à v2 registrada
  em `_taxonomy-v2-design.md` §8.6 — descompasso detectável entre o
  que o texto diz sobre as fontes e o que as fontes mostram. Crítica
  de estilo epistêmico ou de argumentação normativa genérica
  permanece fora do escopo da v2 mesmo se (i) for satisfeito
  independentemente.

Se os dois critérios forem satisfeitos, abrir decisão nova no
`_changelog.md` que sucede a decisão 20 e registra a canonização;
consequências operacionais aplicadas a `_taxonomy-v2-design.md` §8.6
(elevação das heurísticas editoriais a variantes dimensionais) e a
`hallucination-prevention-checklist.md` §8 (remoção ou realocação das
entradas correspondentes).

**A3 — "Cadeia probatória interna contaminada".** Canonização do vetor
como sub-variante de Dim. 2 conteúdo afirmado ou como Dim. 4 nova
pode ser reaberta quando o Teste 03 executar o protocolo de três
passos do §(x) deste handoff. Condição de sucesso: replicação empírica
do vetor em exemplares distintos **e** confronto explícito dos
argumentos originais contra canonização (recuperados em forma
registrada ou reconstruídos) superado pela evidência nova. Decisão
registrada como entrada nova no `_changelog.md` que sucede a decisão
21; consequências operacionais aplicadas a `_taxonomy-v2-design.md`
(§4 se sub-variante de Dim. 2; §3 ou §4 se Dim. 4 nova, com ajuste da
árvore decisória em §6).

### Resolução A3 (2026-04-25)

A pendência A3 foi **resolvida em 2026-04-25 pela decisão de
fechamento da Frente 2 do roadmap v3.4** (Teste 03 / Fase A.7.2).
Canonização do exemplar A3 do Teste 03 com particularidade explícita
"cadeia probatória interna contaminada com refs internas fabricadas
em **múltiplas revisões**" (Campos et al. 2021 com Oliveira 2017
interna; Tavares & Camurça 2004 com Santos 1998 interna), em
expansão do exemplar do Teste 02 (SOARES et al. / ALMEIDA-GOMES) que
operava em revisão única. As três pré-condições da decisão 29 foram
superadas em ambos os ambientes do Papel 2 (Claude.ai navegador
Incognito + Claude Desktop Incognito): regra formal de §2.2,
justificativa de descarte §11, gate de reentrada §11. Ver §8 do
ground truth v2.0 e a entrada agregada de fechamento da Frente 2 no
`_changelog.md` (subdecisão de canonização do exemplar A3). Caminho
do ground truth canônico:
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`.
A entrada A3 dos critérios de reabertura permanece preservada como
registro histórico do protocolo prévio.

## (xviii) Variante metodológica "incognito-duplo" para o Papel 2 — registrada como válida

**Status.** **Registrada como variante metodológica válida** pela
decisão de fechamento da Frente 2 do roadmap v3.4 (Teste 03 /
Fase A.7.2; ver `_changelog.md`). Operação documentada em §1 e §7.4
do ground truth v2.0 do Teste 03
(`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`).

**Definição da variante.** Operação dos dois ambientes do Papel 2 em
**modo Incognito** simultâneo — Claude.ai navegador Incognito +
Claude Desktop Incognito —, em vez do desenho original "Navegador
Incognito + Desktop com instalação por Settings". A diferença
observada entre os dois ambientes é atribuível a (i) cliente,
(ii) eventuais diferenças de pipeline de processamento de skills,
(iii) variabilidade estocástica — **não** a presença/ausência de
memória persistente.

**Razão para registro como válida.** A operação em incognito-duplo
no Teste 03 controlou variável que estava livre no desenho original,
sem comprometer cobertura empírica: 10 dos 11 vetores planejados
foram detectados em ambos os ambientes do Papel 2 (Oliveira 2017
interno; Santos 1998 interno; Magnani 2011 pastiche; Tavares &
Camurça 2004 metadados; Velho via apud; Machado 2021 paráfrase
substantiva; Silva & Lopes 2020 DOI colidido; Ferreira 2023
fabricação simples; Escudero 2022; Campos et al. 2021;
classificação A4 reclassificada como Dim. 2 sustentação). Único
falso negativo material compartilhado: camada 4 do A4 (atribuição
cruzada de "olhar de perto e de dentro" a Velho via apud) — vetor
endereçado pela Sub-4 da decisão de fechamento da Frente 2 (regra
nominal de verificação ativa em `epistemic-tagging-rules.md`).

**Recomendação para testes futuros (Frente 3 ou subsequentes).**
Decidir explicitamente, na fase de **desenho** do teste, qual
variante metodológica operar:

- **Incognito-duplo**: quando o objetivo é isolar diferenças entre
  clientes (navegador vs. desktop) sem confundir com diferenças de
  instalação de skill. Custo: nenhum exemplar de skill instalada
  via Settings opera no teste — se a operação da skill em modo
  instalado for o objeto, esta variante é inadequada.
- **Incognito + Settings**: quando o objetivo inclui comparação
  entre ambientes de operação (incognito vs. instalação completa),
  ou quando a operação da skill instalada por Settings é o objeto
  do teste. Custo: a variável "instalação" entra no desenho e pode
  confundir com diferenças puramente de cliente.

A escolha é de **desenho**, não de execução. Testes que comecem com
uma variante e mudem no meio do caminho perdem auditabilidade da
operação.

**Inputs.** Ground truth v2.0 do Teste 03 §1 (registro da variação
metodológica) e §7.4 (decisão candidata 4); síntese comparativa
Desktop × navegador do Teste 03; protocolo de Papéis 0–3
estabelecido na Fase A.7 (ground truth v1.5 do Teste 02 §1 e
preâmbulo da síntese comparativa).

**Critério de pronto.** Esta entrada permanece como registro
arquitetural durável do estatuto da variante. Não exige resolução
adicional; a recomendação para testes futuros é orientação
operacional permanente. Reabertura para revogação só se rodada
futura observar artefato sistemático introduzido pelo
incognito-duplo que comprometa a integridade do desenho — caso em
que entrada nova no `_changelog.md` deve registrar o motivo da
revogação.

## (xix) Revisão da ground truth v2.0 do Teste 03 à luz do achado empírico de Ferreira 2023 (Frente 3 / Fase 4)

**Origem.** Achado empírico produzido em 2026-04-25 durante a
execução da §5.2 da Frente 3 do roadmap v3.4 (decisão 31 do
`_changelog.md`): o `doi_verify.py` (Sub-31.1), rodado contra a
Suíte A da bateria de regressão, retornou `MISMATCH` para o caso
Ferreira 2023, divergindo do estado `NOT_FOUND` que a ground truth
v2.0 do Teste 03 §2.2 antecipava ("DOI não resolve em CrossRef nem
aparece em buscas"). A divergência é sustentada por verificação
ativa multi-base: o DOI `10.1590/2236-9996.2023-5707` resolve em
CrossRef e em OpenAlex para um artigo real distinto.

**Objetivo.** Deliberar sobre três pontos substantivos:

- **(i) emissão de ground truth v2.1 do Teste 03** com
  reclassificação de Ferreira 2023 de "fabricação simples" (atual
  classificação Dim. 1 inexistente-fabricada na ground truth v2.0
  §2.2) para "fabricação com identificador colidido" (subtipo
  formal canonizado em decisão 30 Sub-30.2);
- **(ii) atualização de §3.4 da ground truth v2.0** sobre
  cobertura Dim. 1, registrando base empírica dupla (Silva & Lopes
  2020 + Ferreira 2023 dentro do mesmo Teste 03) — atualmente §3.4
  registra apenas Silva & Lopes 2020 como exemplar de DOI colidido;
- **(iii) eventual ampliação da Sub-30.2** ou subdecisão
  arquitetural nova consolidando a base empírica dupla e refinando
  o limiar entre "fabricação simples" e "fabricação com
  identificador colidido" no `_taxonomy-v2-design.md` §8.7.

**Inputs.**

- Ground truth v2.0 do Teste 03 §2.2 (registro atual de Ferreira
  2023) e §3.4 (cobertura Dim. 1 com base empírica única) em
  `<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`.
- Decisão 30 Sub-30.2 do `_changelog.md` (subtipo "fabricação com
  identificador colidido" canonizado).
- `scripts/tests/teste03_doi_verify_cases.json` caso 5 — registro
  empírico canônico do achado: DOI `10.1590/2236-9996.2023-5707`
  resolve em CrossRef e OpenAlex para AFONSO, Claudia. "A
  dignidade humana impactada por ambientes criados através de
  ferramentas digitais", *Cadernos Metrópole* v.25 n.57 p.515-536,
  2023; composite score 52.2 (authors 27.8, title 42.0, journal
  100, year 100, pages 40); estado retornado pelo `doi_verify.py`:
  `MISMATCH`.
- `scripts/doi_verify.py` (Sub-31.1) rodado em §5.2 da execução da
  Frente 3 — procedência da observação.
- Decisão 31 Sub-31.1 do `_changelog.md` (registro do achado em
  ponteiro a esta pendência).
- Decisão 31 Sub-31.4 do `_changelog.md` (Ferreira 2023 como
  primeiro caso emergente do critério de expansão da bateria de
  teste).

**Critério de pronto.** Deliberação em sessão dedicada (Papel 1 +
Sidney) registrada como entrada nova no `_changelog.md`, com
decisão explícita sobre os três pontos do objetivo. Cascata
documental subsequente — emissão de ground truth v2.1 (se
decidida), atualização de §3.4 (se decidida), ampliação da
Sub-30.2 ou subdecisão nova (se decidida) — entra como
consequência operacional da entrada nova, não como pré-requisito
de fechamento desta pendência.

**Risco conhecido.** Cascata de mudanças em múltiplos documentos
do Teste 03 (`05-ground-truth-v2.0-final.md` ao menos em §2.2 e
§3.4; potencial revisão de
`04-sintese-comparativa-desktop-navegador.md` sobre cobertura
Dim. 1 nos dois ambientes do Papel 2) e potencial ampliação da
Sub-30.2. Não fazer incidentalmente. Frente dedicada (provavelmente
Frente 4 ou subsequente) é o lugar — a decisão 31 não toca a
ground truth canonizada nem a Sub-30.2; preserva separação entre
frente de implementação (Frente 3) e frente de calibração
taxonômica.

**Reflexividade adicional.** Este achado é caso reflexivo no
sentido forte — o `doi_verify.py`, hard gate canonizado pela
Sub-31.1, apanhou divergência que a verificação manual da ground
truth v2.0 (canonizada em 2026-04-25) não viu. O princípio
metodológico da decisão 18 ("aplicação integral dos marcadores
antes da classificação final") foi honrado em direção contrária ao
habitual: o agente automatizado supera a verificação manual quando
aquele opera sob hard gate e este opera sob baseline humana com
janela de busca limitada. Reforça o princípio de "ground truth como
baseline revisável, não oráculo" registrado na decisão 23.
