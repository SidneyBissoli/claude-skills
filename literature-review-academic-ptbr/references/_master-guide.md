# Guia estratégico: Claude para revisões de literatura multidomínio

**Versão**: reescrita para a taxonomia v2.
**Data**: 2026-04-20.
**Relação com a taxonomia**: este guia organiza a base estratégica e
empírica da skill sob a taxonomia v2 (três dimensões hierárquicas
condicionais). Desenho operacional em `_taxonomy-v2-design.md`;
fundamentação acadêmica em
`<pasta-de-referencias>/skill-development/research/fase-A1-manuscrito-taxonomia-v2.md`.
Regras inegociáveis e fluxo obrigatório vivem em `SKILL.md`; este
guia aponta para esses artefatos quando relevante e não duplica seu
conteúdo.

## 0. Como usar este documento

Este arquivo é a base **estratégica e empírica** da skill: por que o
pipeline existe, que evidência o sustenta, qual é a arquitetura de
MCPs disponíveis em abril de 2026, e como o workflow se integra às
normas acadêmicas e institucionais brasileiras. Não é regra
operacional.

Consultado uma vez ao início do trabalho de instalação ou revisão
arquitetural da skill — não a cada sessão. Revisitado quando emergem
decisões estratégicas (escolha de plataforma, escolha de MCP,
interpretação de norma, empacotamento de entregáveis).

Consulta seletiva, não integral:

- §1 para padrões de prompt validados na literatura peer-reviewed.
- §2 para taxas empíricas de fabricação, catálogo de bases de
  verificação e vinculação ao protocolo v2.
- §3 para quando extended thinking / think tool ajuda ou não.
- §4 para catálogo de MCPs e pontes de verificação por domínio.
- §5 para arquitetura de skills e estrutura da skill atual.
- §6 para escolha entre Claude.ai, Desktop, Code, Cowork.
- §7 para normas acadêmicas, institucionais e de divulgação de IA.
- §8 para workflow end-to-end e as três intervenções de maior retorno.
- §9 para limitações reconhecidas.
- §10 para conclusão.

Para regras operacionais ativas durante a geração, consultar:
`SKILL.md` (regras inegociáveis, fluxo obrigatório, glossário);
`_taxonomy-v2-design.md` (taxonomia de três dimensões, árvore
decisória, protocolo de verificação em seis passos, casos
limítrofes); `hallucination-prevention-checklist.md` (checklists pré,
durante e pós-geração); `epistemic-tagging-rules.md` (marcação
epistêmica); `author-disambiguation-universal.md` (desambiguação de
sobrenomes comuns).

## 1. Engenharia de prompt para revisões de literatura

A combinação mais eficaz é **tratar Claude como redator assistido,
nunca como bibliotecário** — ancorar cada citação em um corpus
verificado (Zotero + MCP + Citations API), impor um workflow em
cadeia (matriz de síntese → rascunho → autorrevisão cética →
verificação automatizada contra a taxonomia v2) e empacotar tudo na
skill `literature-review-academic-ptbr`, com módulos por domínio. Essa
arquitetura ataca as três dimensões de erro bibliográfico definidas em
`_taxonomy-v2-design.md` — Existência, Objeto do erro, Natureza do
erro — e funciona tanto para artigo acadêmico quanto para relatório
técnico, em Vancouver, ABNT, APA ou estilo específico do
periódico-alvo.

A hierarquia oficial da Anthropic
(docs.claude.com/en/docs/build-with-claude/prompt-engineering) ordena
técnicas por efetividade: **clareza → multishot → chain-of-thought →
tags XML → role prompting → prefilling → chaining → long-context →
extended thinking**. Para revisões acadêmicas em qualquer domínio,
cinco padrões se destacam.

**Primeiro, sempre permita que Claude diga "não sei".** O próprio
tutorial da Anthropic (github.com/anthropics/courses, notebook
*Avoiding Hallucinations*) recomenda a instrução explícita "responda
apenas se tiver certeza; caso contrário, escreva `[SEM FONTE]`".

**Segundo, restrinja o universo de citações permitidas** com a regra
"cite apenas obras presentes em `<provided_sources>`; você está
proibido de gerar DOIs, páginas, volumes, ou dados bibliográficos que
não apareçam literalmente no material fornecido".

**Terceiro, use a Citations API**
(claude.com/news/introducing-citations-api) — na documentação oficial,
a fintech **Endex** reportou queda de alucinações de fonte de 10%
para 0% ao migrar de prompts para a API de Citações, com aumento de
20% em referências por resposta; **Thomson Reuters/CoCounsel**
relatou facilidade qualitativa para citar e vincular fontes
primárias, minimizando risco de alucinação. É a alavanca técnica
mais poderosa contra fabricação quando o corpus é curado.

**Quarto, aplique regras de fidelidade autoral em tags XML** para
bloquear a conflação de correntes teóricas divergentes — erro em
conteúdo afirmado com natureza conceitual, na taxonomia v2. A
literatura chama isso de *citation faithfulness vs. correctness*:
Wallat et al. 2024 (arXiv:2412.18004, "Correctness is not Faithfulness
in RAG Attributions") documentou que **até 57% das citações LLM são
"pós-racionalizadas"** — o modelo gera a resposta a partir da
memória paramétrica e depois faz *shallow-matching* com uma citação,
produzindo conteúdo que parece correto mas não deriva da fonte
citada. O bloco de regras deve exigir: (i) antes de usar um autor,
declare sua tradição teórica em uma frase; (ii) cite literalmente o
trecho de até 25 palavras com número de página; (iii) só então
parafraseie; (iv) jamais combine paráfrases de dois autores na mesma
frase sem verificar que concordam; (v) se uma agregação for incerta,
emita `[CONCORDÂNCIA NÃO VERIFICADA — revisar]`. A regra é
domínio-agnóstica: vale para distinguir Starfield de Paim em APS,
Connell de Bourdieu de Butler em gênero, Bardin de Gibbs em análise
de conteúdo, ou Weber de Durkheim de Marx em teoria social. Pares
canônicos consolidados em `SKILL.md` (seção de regras inegociáveis) e
nos módulos `references/domain-*/theoretical-currents-*.md` quando
existirem.

**Quinto, force prosa argumentativa, não dump de referências**, via
*writing requirements* explícitos: cada parágrafo abre com uma
*topic sentence* que avança a tese; autores são agrupados por posição
no debate (não listados serialmente); citações vão ao final da
afirmação, nunca como sujeito gramatical; conectivos argumentativos
obrigatórios ("em contraste", "convergindo com", "essa visão é
desafiada por"); cada seção termina com uma frase-síntese. Detalhes
em `references/argumentative-review-template.md`.

O workflow em cadeia é indispensável. A página oficial
*chain-prompts* da Anthropic lista explicitamente "Pesquisa: extrair
citações → resumir achados → sintetizar em revisão" como caso
canônico. A evidência empírica é sólida: o pipeline **otto-SR** (Cao
et al., medRxiv 2025, DOI: 10.1101/2025.06.13.25329541) reproduziu um
volume equivalente a uma edição de revisões Cochrane (n=12) em dois
dias, com sensibilidade de 96,7% na triagem e 93,1% na extração; a
plataforma **AutoLit/Nested Knowledge** (Kallmes et al. 2025,
*Cochrane Evidence Synthesis and Methods*, DOI: 10.1002/cesm.70059)
validou o mesmo loop *human-in-the-loop* sobre revisões sistemáticas,
reportando 82–97% de *recall* em triagem por revisor e ganhos de
tempo de 50% (triagem de abstracts) e 70–80% (extração qualitativa);
o **Elicit** atingiu 81,4% de acurácia em extração vs. 86,7% humanos
(Hilkenmeier et al. 2025, *Social Science Computer Review*,
DOI: 10.1177/08944393251404052, diferença não estatisticamente
significativa). Embora a maior parte dessa evidência empírica venha
de biomedicina e ciências sociais, o padrão **generate-critique-refine**
é domínio-agnóstico — vale para revisão narrativa em ciências
sociais, meta-síntese qualitativa, revisão de literatura cinzenta em
políticas públicas, ou mapeamento de escopo.

Na prática, o workflow se traduz em: Prompt 1 gera matriz de síntese
com tags teóricas explícitas; Prompt 2 escreve prosa a partir
*apenas* da matriz; Prompt 3 roda revisão cética ("você é Professor
Crítico, revisor hostil do periódico-alvo: marque cada citação como
VERIFICADA/NÃO VERIFICADA/PROVAVELMENTE FABRICADA; sinalize
conflações teóricas; sinalize parágrafos sem fio argumentativo");
Prompt 4 reescreve a partir do relatório do revisor. É o padrão
*generate-critique-refine* oficial da Anthropic, implementado como
fluxo obrigatório em `SKILL.md`.

## 2. Detecção de alucinação e pipeline de verificação

Para calibração, as **taxas de fabricação de referências medidas em
estudos revisados por pares** são brutais: GPT-3.5 em revisão de
literatura, 55% (Walters & Wilder 2023, *Scientific Reports*,
DOI: 10.1038/s41598-023-41032-5); GPT-4, 18%; Gemini Advanced, 76,7%;
Bard em revisão sistemática, 91,4% (Chelli 2024, *Journal of Medical
Internet Research*, DOI: 10.2196/53164); Claude-3-haiku, **>80% de
fabricação de DOI para publicações de países de menor renda** (Kim,
Kipchumba e Min, 2025, *Publications* 13(4),
DOI: 10.3390/publications13040049), com taxas que se agravam para
publicações pós-2020 em todas as regiões segundo o mesmo estudo.

Um estudo mais granular em saúde mental (Linardon et al. 2025,
*JMIR Mental Health*, DOI: 10.2196/80371) analisou 176 citações
produzidas pelo GPT-4o em seis revisões e encontrou 19,9%
fabricadas; entre as reais, 45,4% apresentavam erros
bibliográficos — cerca de **dois terços do total** entre fabricação
e imprecisão. O mesmo estudo documenta variação sistemática por
especificidade do tópico: transtornos menos visíveis, como
transtorno dismórfico corporal (29%) e transtorno de compulsão
alimentar periódica (28%), apresentam taxas de fabricação bem
superiores às de transtornos de alta visibilidade como depressão
maior (6%). A implicação operacional é direta: tópicos com literatura
mais rarefeita — exatamente o perfil de muitas revisões em saúde
coletiva, ciências sociais e políticas públicas no Brasil — estão na
faixa alta de risco, independentemente do modelo escolhido.

**Verificação pós-geração é mandatória, não opcional, em qualquer
domínio.**

### Como a taxonomia v2 organiza a resposta técnica

A taxonomia v2 classifica erros em referências bibliográficas em
três dimensões hierárquicas condicionais, cada uma definida em
`_taxonomy-v2-design.md`:

- **Dimensão 1 — Existência** (aplica-se sempre): existente
  verificável / pastiche / inexistente-fabricada.
- **Dimensão 2 — Objeto do erro** (aplica-se se Dim. 1 = existente
  verificável): metadados / conteúdo afirmado / estrutura de
  sustentação argumentativa.
- **Dimensão 3 — Natureza do erro** (aplica-se se Dim. 2 = conteúdo
  afirmado): conceitual / factual.

Árvore decisória e casos limítrofes em `_taxonomy-v2-design.md` §6 e
§8. O **protocolo de verificação em seis passos** que transforma
essa classificação em ação está em `_taxonomy-v2-design.md` §7.

### Base empírica da categoria pastiche

A categoria pastiche tem base empírica independente: McGowan et al.
2023 (*Psychiatry Research*, DOI: 10.1016/j.psychres.2023.115334)
documentou que ChatGPT e Bard, em buscas de literatura em
psiquiatria, produzem sistematicamente objetos bibliográficos
plausíveis em aparência que, ao exame, se revelam combinações
probabilísticas de elementos de obras reais sem unidade subjacente
— autores reais, periódicos reais, títulos plausíveis, mas a
combinação específica não recupera obra alguma. McGowan é **fonte
empírica** do fenômeno pós-LLM e **fonte nominal e conceitual** da
categoria **pastiche**, hoje incorporada como valor intermediário da
Dimensão Existência (ver `_taxonomy-v2-design.md` §3, subseção
"Pastiche").

### Catálogo de bases de verificação

Para cada citação gerada, consultar:

- **CrossRef REST API** (`api.crossref.org/works/{DOI}`) — cobre
  ~160M obras, todas as áreas, retorna 404 para DOIs fabricados.
  Método usado por Kim et al. 2025.
- **OpenAlex** (`api.openalex.org/works`) — >270M obras, todas as
  áreas, inclui SciELO, autor-ORCID-afiliação.
- **PubMed E-utilities** — biomedicina, enfermagem, psicologia
  clínica (indexa também RSP, CSP, C&SC, *Revista Brasileira de
  Psiquiatria*, *Psicologia: Reflexão e Crítica*).
- **SciELO ArticleMeta API** (`articlemeta.scielo.org/api/v1`) e
  **OAI-PMH** (`scielo.br/oai/scielo-oai.php`) — cobre saúde,
  ciências sociais, humanidades, educação no Brasil.
- **BVS/iAHx** (`pesquisa.bvsalud.org/portal/?format=json`) —
  literatura latino-americana em saúde.
- **Unpaywall** — verifica DOI e devolve URL de texto completo OA.
- **BDTD (Biblioteca Digital Brasileira de Teses e Dissertações)** —
  `bdtd.ibict.br` via OAI-PMH; essencial para teses e dissertações
  brasileiras.
- **LA Referencia** (OAI-PMH em `lareferencia.info`) — agregador de
  repositórios institucionais latino-americanos.
- **LexML** (`lexml.gov.br`) — legislação federal, estadual,
  municipal, jurisprudência.
- **Portal de Dados Abertos da Câmara e Senado** — metadados de
  proposições, emendas, discursos, projetos de lei.

Essas bases são os instrumentos do protocolo de verificação. A
**associação entre base e passo** é: Crossref e PubMed cobrem
`_taxonomy-v2-design.md` §7.1 (consulta por identificador estável);
Crossref, PubMed, OpenAlex, **SciELO e LILACS/BVS** cobrem §7.2
(busca ativa por autor + título + periódico) — a inclusão das bases
lusófonas é crítica para literatura brasileira indexada
regionalmente; `scripts/bib_consistency.py` e `scripts/doi_verify.py`
executam §7.1 e §7.4 como hard gate pré-submissão.

### Princípio metodológico emergente (decisão 18 do changelog)

O protocolo de verificação da v2 aplica-se tanto a revisões de
literatura assistidas quanto aos **próprios casos usados como exemplo
em documentos operacionais ou acadêmicos que os invocam**. A
constatação de DOI incorreto é condição **necessária mas não
suficiente** para classificar um caso como Dim. 1 inexistente/fabricada:
os cinco marcadores de pastiche (`_taxonomy-v2-design.md` §3,
"Pastiche") devem ser aplicados integralmente antes da classificação
final. O princípio emergiu em auditoria interna à Fase A.1, que
detectou aplicação incompleta dos marcadores em exemplo-teste; ver
decisão 18 em `_changelog.md`.

### Marcação epistêmica como camada adicional

Complemento poderoso é a marcação epistêmica no próprio prompt:
obrigar Claude a etiquetar toda afirmação factual como
`[SOURCED:<cite>]`, `[INFERRED]`, `[GENERAL KNOWLEDGE]` ou
`[UNCERTAIN]`, com proibição expressa de `[GENERAL KNOWLEDGE]` para
estatísticas, datas, nomes próprios, citações e paráfrases de obras
identificáveis. Regras completas em `epistemic-tagging-rules.md`.
Farquhar et al. 2024 (*Nature* 630, DOI: 10.1038/s41586-024-07421-0,
"Detecting hallucinations in large language models using semantic
entropy") valida o princípio subjacente: entropia no nível de
significado detecta confabulações sem *ground-truth* — a versão
puramente prompt-baseada é pedir três respostas independentes e
sinalizar qualquer afirmação que varie entre elas.

### Os limites da verificação automatizada

Script de verificação apanha erros de Dim. 1 (existência) e Dim. 2
metadados. **Não apanha** erros de Dim. 2 conteúdo afirmado —
independentemente de Dim. 3 ser conceitual ou factual, a verificação
exige leitura humana da fonte primária contra a paráfrase, com
protocolo diferenciado para cada natureza (releitura interpretativa
para conceitual; confronto numérico/documental para factual — ver
`_taxonomy-v2-design.md` §5 e §7.5). Também não apanha erros de
Dim. 2 estrutura de sustentação argumentativa, que exige leitura
contextual. **RAG é antídoto parcial, não completo**: Wallat et al.
2024 documenta 57% de pós-racionalização mesmo *com* RAG — o modelo
gera a resposta a partir da memória paramétrica e faz
*shallow-matching* com uma citação após o fato. A regra da
**paráfrase com verbatim lateral**, registrada em `SKILL.md`, é a
defesa operacional: permite conferência humana em segundos, em vez
de horas.

## 3. Extended thinking, ultrathink e o think tool

Extended thinking (docs.claude.com/en/docs/build-with-claude/extended-thinking)
é um *scratchpad* interno alocado antes da resposta visível,
disponível de Sonnet 3.7 em diante. Na API clássica:
`thinking={"type":"enabled","budget_tokens":10000}` (mínimo 1.024;
acima de ~32k, retornos decrescentes; temperatura obrigatoriamente
1). Em Opus/Sonnet 4.6, o `budget_tokens` manual foi substituído por
**adaptive thinking** (`thinking={"type":"adaptive"}` +
`output_config={"effort":"high"}`), com *interleaved thinking*
automático entre chamadas de ferramenta — crítico para que Claude
reflita após cada resultado do CrossRef, SciELO, ou LexML.

**Ultrathink** é convenção **exclusiva do Claude Code CLI**, não
recurso universal. O preprocessador do Claude Code mapeia
palavras-chave em orçamentos de pensamento: `think` ≈ 4.000 tokens;
`think hard`/`megathink` ≈ 10.000; `think harder`/`ultrathink` ≈
31.999 (máximo). Digitar "ultrathink" em Claude.ai web ou na API
bruta não tem efeito algum. No Claude.ai web e Desktop, ativa-se
extended thinking via toggle "Extended thinking" embaixo da caixa de
mensagem; no Code via `/effort max` ou pelos gatilhos de palavra.

Quando extended thinking ajuda para revisão de literatura: síntese
transversal de muitos documentos, avaliação crítica argumentativa,
detecção de contradições entre autores (conforme Dim. 2 conteúdo
afirmado, `_taxonomy-v2-design.md` §4) e cálculos de meta-análise.
O ganho no GPQA Diamond para Sonnet 3.7 foi de 68,0% → 84,8%
(+16,8 pontos) com extended thinking. **Quando *não* ajuda**: Zhao,
Hooi e Ng (arXiv:2509.06861, 2025, "Test-Time Scaling in Reasoning
Models Is Not Effective for Knowledge-Intensive Tasks Yet")
avaliaram modelos de raciocínio em benchmarks intensivos em
conhecimento e reportaram que **aumentar computação em tempo de
teste não melhora consistentemente a acurácia**, e, ao contrário,
pode induzir viés de confirmação com alucinações confiantes.
Tradução operacional: extended thinking é **necessário mas não
suficiente** para o problema de fabricação; sempre pareie com RAG
e verificação automática.

O **think tool** (anthropic.com/engineering/claude-think-tool) é
conceito distinto e complementar: ferramenta no-op que Claude chama
para pausar e planejar após resultados de outras ferramentas. Em
τ-bench, domínio *airline*, Claude 3.7 com o think tool combinado a
prompt otimizado atingiu 0,570 em pass¹ contra 0,370 do baseline —
**melhoria relativa de 54%** (Anthropic, 20 mar 2025). Munir Claude
do think tool permite que, após cada resposta do CrossRef, PubMed,
SciELO ou LexML, Claude avalie qualidade da correspondência e decida
se re-busca — exatamente o que falta quando um *match* ambíguo é
aceito e a escrita prossegue.

## 4. MCPs e ferramentas acadêmicas gratuitas — catálogo multidomínio

Até abril de 2026, a Anthropic consolidou um diretório de ≈280
connectors em `claude.com/connectors`. Mapeando por domínio:

### Núcleo universal (toda revisão se beneficia)

- **Zotero + 54yyyu/zotero-mcp** como *source-of-truth* curada
  manualmente. Instalação no Windows: Zotero 7 com API local
  (`localhost:23119`) + plugin Better BibTeX + `pipx install
  zotero-mcp-server && zotero-mcp setup`. Permite busca, leitura de
  metadados e anotações, exportação BibTeX. Servidor alternativo:
  **cookjohn/zotero-mcp** (plugin Zotero, mais rápido).
- **OpenAlex MCP** (`cyanheads/openalex-mcp-server`) — índice amplo
  multidisciplinar, filtros por país
  (`authorships.countries:BR`), OA, ano, *concepts*. Única solução
  escalável para reviews com escopo Brasil.
- **Consensus MCP** (`mcp.consensus.app/mcp`) — OAuth; tier gratuito
  limita a 3 resultados por chamada; 200M+ artigos via
  OpenAlex/Semantic Scholar. Indexa DOIs em qualquer área, mas
  recuperação em português é fraca.

### Saúde pública / biomedicina / psicologia clínica

- **PubMed MCP** — servidor comunitário
  `masa061580/enhanced-pubmed-mcp-server` é o mais simples no
  Windows:
  `{"pubmed":{"command":"npx","args":["-y","enhanced-pubmed-mcp-server"]}}`
  em `%APPDATA%\Claude\claude_desktop_config.json`. Cobre MEDLINE
  inteiro, inclui periódicos brasileiros indexados (RSP, CSP, C&SC,
  *Rev Bras Epidemiol*, *Psicologia: Reflexão e Crítica*,
  *Psicologia USP*).
- **SciELO / BVS** — *nenhum MCP público existe em abril de 2026*.
  Alternativas viáveis: (i) ArticleMeta API
  (`articlemeta.scielo.org/api/v1`) via wrapper Python `pip install
  articlemeta`; (ii) OAI-PMH SciELO; (iii) parâmetro `format=json`
  do iAHx BVS; (iv) Filesystem MCP apontando para pasta alimentada
  por script Python agendado. **Oportunidade**: vibe-coding um MCP
  SciELO/BVS mínimo seria o primeiro MCP público BR-focado e
  contribuição relevante.

### Ciências sociais e humanidades

- **OpenAlex** (já no núcleo) cobre sociologia, antropologia,
  psicologia social, estudos de gênero via *concepts*.
- **SciELO Social Sciences and Humanities**
  (`socialsciences.scielo.org`) — mesma API ArticleMeta com filtro
  por coleções de ciências sociais; cobre Mana, Dados, RBCS, Cad.
  Pagu, Estudos Feministas, Horizontes Antropológicos.
- **JSTOR** — sem MCP público; acesso institucional via Portal de
  Periódicos CAPES/CAFe. Para metadados sem acesso institucional:
  OpenAlex costuma indexar os DOIs JSTOR.
- **SocArXiv / PsyArXiv** — via OpenAlex ou diretamente em
  `osf.io/preprints`.
- **PhilPapers** — API JSON em `philpapers.org/s/X`; sem MCP, mas
  `web_fetch` resolve para consultas pontuais em filosofia (útil
  para marcos teóricos: Foucault, Butler, Fraser, Honneth,
  Habermas).
- **Anpocs, Abrapso, ABA, ANPEPP** — repositórios de anais; acesso
  via `web_fetch` ou Filesystem MCP.
- **Google Scholar** — apenas scraping, que viola ToS e bloqueia IP;
  evitar. OpenAlex + Consensus + SciELO cobrem a maior parte
  legalmente.

### Metodologia de pesquisa e psicometria

- **OpenAlex** (*concepts* de metodologia, psicometria,
  estatística).
- **APA PsycNet / PsycINFO** — sem MCP; acesso institucional via
  CAPES.
- **Biblioteca do IBGE** — PNS, PNAD, VIGITEL como fonte primária;
  manuais em `ibge.gov.br/estatisticas` via `web_fetch`.
- **Cochrane Methodology Register**, **Campbell Collaboration** —
  via OpenAlex ou `web_fetch`.
- **Manuais canônicos** (Cronbach, Messick, Bandalos, DeVellis,
  Kline, Furr, Hair et al., Pasquali, Urbina) — devem estar no
  Zotero como referências permanentes.

### Políticas públicas, legislação, análise institucional

- **LexML** — não existe como MCP público; acesso via `web_fetch` em
  `lexml.gov.br` ou API REST. Cobre legislação federal/estadual/
  municipal, jurisprudência, doutrina. **Segunda oportunidade** para
  vibe-coding de MCP próprio.
- **Portal de Dados Abertos da Câmara**
  (`dadosabertos.camara.leg.br`) e **Senado**
  (`www12.senado.leg.br/dados-abertos`) — APIs REST bem
  documentadas. Um MCP cliente dessas duas APIs cobriria boa parte
  do trabalho em análise institucional.
- **Planalto** (`planalto.gov.br`) — legislação consolidada;
  `web_fetch`.
- **RAP, RSP-ENAP, Opinião Pública, DADOS, RBCS** — via SciELO e
  OpenAlex.
- **IPEA, IBGE, Banco Mundial, OCDE, CEPAL** — relatórios técnicos;
  Filesystem MCP com PDFs ou `web_fetch`.

### Suporte universal

- **Filesystem MCP** — essencial para ler PDFs, anotações, matrizes.
- **arxiv-mcp-server** (blazickjp) — preprints metodológicos.
- **paper-search-mcp** (openags) — agregador multi-fonte OA-first.

### Considerações práticas

Cada servidor injeta ~500–1.500 tokens no system prompt; com 6–8
servidores ativos, gasta-se 4–8k tokens em definições. A Anthropic
lançou **Tool Search / Programmatic Tool Calling** no final de 2025
exatamente para carregar definições sob demanda (disponível em
Claude Code); em Claude Desktop, desativar connectors não usados por
sessão. Logs no Windows em `%APPDATA%\Claude\logs\mcp-server-*.log`.

**Zotero como source-of-truth** é o padrão validado pela comunidade
em 2026 e vale para qualquer domínio. Fluxo operacional: o
pesquisador curata tudo manualmente (PubMed/SciELO/OpenAlex/LexML →
conector de navegador → Zotero, com tags por projeto); inicia cada
sessão com instrução "ancore toda afirmação em itens da biblioteca
via zotero-mcp; não cite fontes fora da biblioteca; se faltar algo,
sugira uma busca e pare"; encadeia `zotero_search` → (se lacuna)
PubMed/OpenAlex/Consensus/SciELO/LexML → Claude rascunha nota → o
pesquisador importa via conector → volta ao passo 1.

## 5. Claude Skills — arquitetura e tutorial

A Anthropic anunciou **Agent Skills em 16 de outubro de 2025**. Uma
Skill é uma pasta com `SKILL.md` (frontmatter YAML + corpo
Markdown), mais opcionalmente `references/`, `scripts/` e
`assets/`. O mecanismo-chave é **progressive disclosure**: Claude
carrega apenas o nome e a descrição de cada skill instalada no
início da sessão (custo ≈dezenas de tokens por skill); quando o
pedido do usuário casa com a descrição, Claude lê o corpo completo;
só então puxa arquivos de `references/` e executa `scripts/` (cujo
corpo nunca entra em contexto — só o stdout). Isso permite dezenas
de skills instaladas sem inchar o contexto. **O campo `description`
no frontmatter é o que aciona a skill — escrever uma descrição
"empurrada" com palavras-chave distintivas é a intervenção de maior
retorno**, porque Claude tende a sub-ativar skills.

Distinções críticas. **vs. System prompts**: estes se aplicam sempre
e inflam toda conversa; skills são condicionais. **vs. Projects**:
Projects dão uma base de conhecimento estática em um workspace;
skills são *know-how procedural portátil* reusável entre projetos,
Claude Code e API. **vs. MCP**: MCP expõe ferramentas/fontes de
dados; skills são o *playbook* que ensina Claude *como* usá-las
corretamente.

O **repositório oficial** é `github.com/anthropics/skills`.
Marketplaces: `mcpmarket.com/tools/skills`, `aitmpl.com/skills`,
`playbooks.com/skills`. Skills acadêmicas já públicas mais
relevantes: **Claude Scholar**, **ZoteroSynth**, **Zotero Research
Agent**, **ZoFiles**, **claude-zotero-skills**, **Thesis Writing
Assistant**, **Valyu skill**. Nenhuma cobre ABNT brasileiro,
Vancouver brasileiro, desambiguação de correntes teóricas em
múltiplos domínios, nem as particularidades de relatórios técnicos
legislativos — a lacuna que a skill `literature-review-academic-ptbr`
preenche.

Plataformas: Claude.ai (todos os planos) via *Customize → Skills*
com .zip; Claude Desktop lê de `~/.claude/skills/`; Claude Code é o
habitat nativo; API via ferramenta *code-execution*.
**Portabilidade**: SKILL.md é padrão aberto — mas skills
customizadas *não* sincronizam automaticamente entre superfícies;
skill enviada ao Claude.ai precisa ser reinstalada no Code. Skills
não estão cobertas por ZDR.

**Construir a skill em seis passos**: (1) frontmatter com
`description` cheia de palavras-chave distintivas; (2) SKILL.md
abaixo de 500 linhas, detalhe em `references/`; (3) arquivos de
referência por domínio; (4) scripts determinísticos; (5) templates
em `assets/`; (6) testar disparo (deve disparar em 5 fraseados
alternativos; não deve disparar em 3 prompts não relacionados).

### Estrutura da skill `literature-review-academic-ptbr`

A estrutura canônica vive no próprio repositório da skill e
evolui com o projeto; a leitura autoritativa está em `SKILL.md`
(frontmatter + seção "Módulos de referência — quando carregar o
quê"). Esqueleto atual em alto nível:

```
literature-review-academic-ptbr/
├── SKILL.md
├── CLAUDE.md
├── references/
│   # Meta (estratégia, decisões, taxonomia)
│   # obs.: _taxonomy-v2-design.md também entra no bloco "sempre
│   # carregar" — reescrita do SKILL.md em A.3 consolidará
│   ├── _master-guide.md               # este arquivo
│   ├── _taxonomy-v2-design.md         # taxonomia canônica v2
│   ├── _changelog.md
│   ├── _phase2-handoff.md
│   # Universais (sempre carregados)
│   ├── hallucination-prevention-checklist.md
│   ├── argumentative-review-template.md
│   ├── epistemic-tagging-rules.md
│   ├── author-disambiguation-universal.md
│   ├── bibliographic-styles/
│   │   ├── vancouver-numeric.md
│   │   ├── vancouver-brazilian-conventions.md
│   │   ├── abnt-nbr-6023-2018.md
│   │   ├── abnt-nbr-10520-2023.md
│   │   ├── apa-7.md
│   │   └── style-detection-heuristics.md
│   # Por domínio (carregados conforme detecção)
│   ├── domain-public-health/
│   ├── domain-social-sciences/
│   ├── domain-methodology-psychometry/
│   └── domain-public-policy/
├── scripts/
│   ├── doi_verify.py
│   ├── bib_consistency.py
│   ├── style_formatter.py
│   ├── zotero_extract.py
│   └── (pubmed/scielo/openalex/lexml/camara_senado search wrappers)
└── assets/
    ├── synthesis_matrix_*.xlsx   (genérico + uma variante por domínio)
    ├── review_outline_*.docx
    └── ai_disclosure_templates_ptbr.md
```

Módulos de `references/domain-*/` e `bibliographic-styles/` podem
existir parcialmente em uma versão da skill; quando ausentes, o
`SKILL.md` instrui a sinalizar a ausência e prosseguir com as
regras universais.

## 6. Escolha de plataforma — análise comparativa

| Dimensão | Claude.ai + Projects | Claude Desktop + MCPs | Claude Code | Claude Cowork |
|---|---|---|---|---|
| Janela de contexto | 200K Sonnet / 1M Opus 4.6 no Max+; Projects faz auto-RAG | Mesmas janelas; sem auto-RAG | Mesmas + `--add-dir` + auto-compactação | Idem Desktop + paralelismo |
| MCP/connectors | Apenas remotos | **MCP local + remoto** | MCP + hooks + ferramentas custom | MCP + filesystem |
| I/O PDF/.docx/.bib | Lê PDF; escreve .docx via skill; sem FS local | Lê/escreve via filesystem MCP | **Nativo no FS local** | **Nativo**; .xlsx/.docx/.pptx reais |
| Persistência | **Project + custom instructions** | Por chat | CLAUDE.md + memória entre sessões | Workspace + tarefas agendadas |
| Suporte a Skills | ✓ (.zip) | ✓ | ✓ nativo, `/slash`, subagentes | ✓ |
| Extended thinking | ✓ toggle | ✓ | ✓ `ultrathink` | ✓ |
| Reprodutibilidade | Histórico de chat | Idem | **Git log + transcripts (melhor)** | **Fraca** |
| Fricção para não-dev | **Menor** | Média | **Maior** | Baixa |

**Recomendação priorizada.** Use **Claude.ai Projects (Max) como
ferramenta primária** para redação diária, com a skill
`literature-review-academic-ptbr` instalada e um Project por grande
tema, carregando PDFs e custom instructions em português. Use
**Claude Code como ferramenta secundária** para autoria e
versionamento da skill e dos scripts
(`~/.claude/skills/literature-review-academic-ptbr/` em git). Use
**Claude Desktop em terceiro lugar** para busca semântica ancorada
em Zotero via `zotero-mcp` + `pubmed-mcp` + `openalex-mcp` + MCPs
custom de SciELO/LexML quando houver. **Evitar Cowork** para
trabalho regulado — não usar para dissertação ou manuscrito
submetido.

## 7. Normas: acadêmicas, institucionais e de divulgação de IA

### Estilos bibliográficos

- **Vancouver numérico** (ICMJE/NLM): saúde pública e biomedicina
  (RSP, CSP, C&SC, RBE, revistas internacionais). Citações [1],
  [2,3]; lista numerada por ordem de aparição.
- **ABNT NBR 10520:2023** (citações) e **NBR 6023:2018**
  (referências): ciências sociais brasileiras, humanidades, direito,
  educação, administração pública, maior parte das pós-graduações
  brasileiras. Autor-data: (Connell, 2005, p. 832); lista
  alfabética.
- **APA 7**: psicologia, psicometria, educação internacional,
  administração, algumas revistas brasileiras interdisciplinares.
  Autor-data: (Connell, 2005).

A skill tem `style_formatter.py` que converte entre os três a partir
de um `.bib` verificado.

### Convenções por tipo de entregável

**Artigo acadêmico — saúde coletiva.** RSP: 3.500 palavras, 30
refs, Vancouver, resumo estruturado ≤300 palavras, exige "caráter
descritivo-discursivo" com crítica teórico-metodológica em revisões
narrativas. CSP: revisão crítica até 8.000 palavras, 3-5 descritores
DeCS, ORCID obrigatório, revisões sistemáticas com protocolo
PROSPERO. C&SC: até 45.000 caracteres, IA limitada a 20% com
declaração.

**Artigo acadêmico — ciências sociais.** *Dados*, *RBCS*, *Mana*,
*Cad. Pagu*, *Estudos Feministas*, *Horizontes Antropológicos*,
*Sociologias*: ABNT, 8.000–12.000 palavras, exigência forte de
diálogo teórico, posicionamento autoral, crítica à literatura.
*Psicologia: Reflexão e Crítica*, *Psicologia USP*, *Estudos de
Psicologia*: APA/Vancouver/ABNT conforme a revista, ≤8.000
palavras.

**Artigo acadêmico — políticas públicas / administração.** *RAP*,
*RSP-ENAP*, *Opinião Pública*, *RAC*: ABNT, 6.000–10.000 palavras,
exigência de framework analítico explícito (teoria do programa,
cadeia causal, stakeholders, neoinstitucionalismo, policy transfer).

**Projeto de pesquisa.** Estrutura clássica (Minayo; Gil; Severino):
objeto → justificativa → problema → objetivos → referencial teórico
→ metodologia → cronograma → referências. Revisão é
**indutivo-expositiva**: ampla, mapeia estado da arte, identifica
lacunas, posiciona teoricamente.

**Relatório técnico institucional (p. ex., de casa legislativa).** Formato
institucional: sumário executivo → contextualização → metodologia
→ análise → recomendações → referências. Público
parlamentar/assessor/jornalista — linguagem direta, gráficos
sintéticos, recomendações acionáveis. Citações ABNT, lista enxuta
(10–30 itens) priorizando fontes institucionais (IPEA, IBGE, Banco
Mundial, CEPAL), legislação (LexML), dados primários (Câmara,
Senado), literatura acadêmica-chave. Revisão de literatura aqui é
**instrumental**: sustenta o diagnóstico e fundamenta recomendações.

### Quadro normativo de IA em abril de 2026

Três eixos: sem autoria de IA; divulgação obrigatória;
responsabilidade integral humana.

- **ICMJE** (jan 2024): IA não é autor; divulgar em Agradecimentos
  (escrita) ou Métodos (análise); revisores/editores não podem
  subir manuscritos para IA.
- **COPE** (DOI 10.24318/cCVRZBms): espelha ICMJE.
- **WAME** (Zielinski et al. 2023): documentar prompt, data, versão.
- **SciELO** (*Guia de uso de ferramentas e recursos de IA*,
  set/2023): permite IA para paráfrase/legibilidade tipo Grammarly;
  proíbe geração substantiva sem divulgação.
- **ABEC Brasil**: alinhada a COPE/ICMJE/SciELO.
- **Portaria CNPq nº 2.664/2026** (6 mar 2026, verificada via
  `gov.br/cnpq`): institui a Política de Integridade na Atividade
  Científica; escopo geral (aplica-se a servidores, proponentes,
  beneficiários e usuários dos sistemas do CNPq). Exige declaração
  de uso de IA generativa em qualquer etapa; proíbe submeter
  conteúdo de IA como humano; proíbe IA em pareceres; atribui
  responsabilidade integral ao autor humano, inclusive por
  eventual plágio ou imprecisão gerada pela ferramenta; sanções
  incluem suspensão de bolsas.
- Por periódico: C&SC 20%; CSP permite com declaração; RSP segue
  ICMJE; *Cad. Pagu* e *Estudos Feministas* adotaram políticas
  restritivas; *Dados* e *RBCS* seguem COPE.
- **Relatórios institucionais (p. ex., de órgãos públicos)**: não há norma
  pública específica em abril de 2026, mas boa prática é declarar
  uso interno para transparência institucional.

### Templates de declaração de IA

Vivem em `assets/ai_disclosure_templates_ptbr.md` (A — uso mínimo;
B — uso substantivo; C — teto de 20% para C&SC; D — relatório
institucional). Apontamento, não duplicação: o conteúdo integral
dos templates não é reproduzido aqui.

## 8. Workflow end-to-end e três intervenções de maior retorno

O pipeline de oito fases mantém IA sempre a jusante de material
verificado.

**Fase 1 — Busca.** Formular a pergunta (PICO/PICo/PCC em saúde e
metodologia; SPIDER para qualitativa; PEO/SPICE para políticas;
pergunta livre orientada por teoria em ciências sociais); traduzir
conceitos (DeCS/MeSH em saúde; tesauros disciplinares em ciências
sociais; vocabulário LexML em legislação); buscas paralelas conforme
domínio (saúde: PubMed, LILACS, SciELO, Embase, WoS, Scopus, CAPES;
ciências sociais: SciELO SSH, Scopus, WoS, JSTOR, SocArXiv, BDTD,
repositórios institucionais, anais Anpocs/Abrapso; metodologia:
PsycINFO, OpenAlex, Scopus, arXiv métodos; políticas: LexML,
Planalto, Câmara/Senado, IPEA, IBGE, CEPAL, Banco Mundial, BDTD,
SciELO); registrar data, base, string, hits.

**Fase 2 — Triagem.** Importar tudo ao Zotero (dedupe); exportar a
Rayyan para triagem com cegamento (útil mesmo em revisão narrativa
para disciplinar escolhas); leitura de cada abstract; "maybes" vão
para texto completo.

**Fase 3 — Texto completo.** SciELO, PMC, SocArXiv, SSRN abertos;
CAPES/CAFe; Unpaywall; e-mail direto ao autor; armazenar PDFs no
Zotero com metadados verificados.

**Fase 4 — Extração.** Matriz apropriada ao domínio (template na
skill), sempre com coluna `corrente_teorica` taggeada; regra
mestra: IA só recebe matriz verificada, nunca "encontre estudos".

**Fase 5 — Redação.** Prompt-esqueleto: "Atue como coautor. Use
EXCLUSIVAMENTE as referências em [BibTeX] e achados em [matriz].
NÃO acrescente referências ou citações fora do fornecido. [Estilo
de citação alvo]. Distinga [lista de contrastes teóricos relevantes
ao tema]. Lacunas: escreva 'não coberta pelas referências
fornecidas' em vez de inferir." Rascunho modular com extended
thinking adaptativo `effort: high`; nunca autocomplete de citação —
colar chave BibTeX e formatar via Better BibTeX.

**Fase 6 — Verificação.** Aplicar o **protocolo de seis passos** de
`_taxonomy-v2-design.md §7`: (1) consulta por identificador
estável; (2) busca ativa por autor + título + periódico se o
identificador falhar; (3) decisão pastiche × inexistente-fabricada
(§8.1 do mesmo documento); (4) conferência de metadados campo a
campo; (5) verificação de conteúdo afirmado (abstract ou texto
completo); (6) avaliação de estrutura de sustentação
argumentativa. Scripts cruzam cada referência com CrossRef/PubMed/
OpenAlex/SciELO/LexML; verbatim lateral permite conferência de
paráfrase; checagem teórica específica para conflações do domínio;
plágio/IA via Turnitin ou Plagius quando exigido.

**Fase 7 — Polimento.** Auditoria do estilo bibliográfico (Zotero
CSL do periódico-alvo); leitura em voz alta; auditoria de *topic
sentences*; simulação de revisor (colega humano ou Claude
pós-verificação); checklist de submissão (word count, resumo,
descritores, ORCID, ética quando aplicável, conflito de interesse,
declaração IA).

**Fase 8 — Divulgação.** Template apropriado ao contexto (A/B/C/D
em `assets/ai_disclosure_templates_ptbr.md`).

### Três intervenções de maior retorno (válidas em qualquer domínio)

1. **Inverter o fluxo de referências.** Zotero como *source-of-truth*
   + zotero-mcp + Citations API, de modo que Claude escreva apenas a
   partir do corpus curado. Fecha Dim. 1 inexistente/fabricada e
   grande parte de Dim. 1 pastiche.
2. **Verificação automatizada obrigatória** via scripts
   CrossRef/PubMed/OpenAlex/SciELO/LexML como *hard gate* antes de
   qualquer submissão. Captura resíduos de Dim. 1 e erros de Dim. 2
   metadados, e é exigência implícita da Portaria CNPq
   nº 2.664/2026.
3. **Workflow em cadeia com matriz-antes-de-prosa + regras explícitas
   de fidelidade autoral + paráfrase com verbatim lateral +
   autorrevisão cética**, empacotados na skill com módulos por
   domínio. Ataca Dim. 2 conteúdo afirmado (tanto Dim. 3 conceitual
   quanto factual) e Dim. 2 estrutura de sustentação argumentativa:
   a matriz obriga tagueamento de corrente teórica por linha, a
   prosa é derivada da matriz taggeada, e o verbatim lateral permite
   conferência humana da paráfrase. A regra do verbatim é
   particularmente crítica em ciências sociais, onde o conteúdo
   conceitual é mais plástico e a conflação entre correntes teóricas
   divergentes é mais fácil.

As três são multiplicativas, não aditivas. Extended thinking e o
*think tool* são complementos úteis para qualidade argumentativa,
mas não reduzem fabricação factual por si só.

## 9. Limitações reconhecidas

- Nenhum modelo de fronteira em abril de 2026 é seguro para geração
  não supervisionada de referências. A resposta é arquitetural (ver
  §8), não de "prompt melhor".
- Nenhum MCP público cobre SciELO/LILACS/BVS, LexML ou Câmara/Senado
  nativamente — construir essas pontes é a maior lacuna de
  infraestrutura para pesquisa brasileira multidomínio.
- Portabilidade de Skills entre superfícies Claude ainda exige
  reinstalação manual.
- Cowork não é auditável para cargas regulatórias.
- A Citations API controla fabricação quando o corpus é provido,
  mas **não resolve descoberta** — descoberta deve ser humana + MCP,
  nunca LLM-livre.
- A verificação automatizada detecta Dim. 1 inexistente/fabricada e
  Dim. 2 metadados, mas **não detecta** Dim. 2 conteúdo afirmado
  nem Dim. 2 estrutura de sustentação argumentativa — isso continua
  exigindo leitura humana da fonte primária (ver também as
  limitações próprias da taxonomia em `_taxonomy-v2-design.md` §10:
  cascatas sistêmicas fora de escopo, verificabilidade dependente
  de indexação, unidade de análise item por item, ausência de
  validação empírica formal da v2).
- Skills só funcionam se Claude as ativa: `description` com
  palavras-chave distintivas é a prática atual, mas o modelo
  sub-ativa skills; testar explicitamente o disparo e iterar a
  descrição.

## 10. Conclusão

Os erros bibliográficos descritos pela taxonomia v2 não são
problemas de "prompt melhor" — são problemas estruturais que se
resolvem reconfigurando quem é dono do universo de citações. Claude
deixa de ser bibliotecário e passa a ser redator assistido. A
biblioteca Zotero curada manualmente é o universo permitido, e isso
vale tanto para uma revisão em saúde coletiva quanto para uma sobre
gênero, psicometria ou políticas públicas. MCPs expõem Zotero,
PubMed, OpenAlex, SciELO, LexML, Câmara e Senado como ferramentas
verificáveis; a skill `literature-review-academic-ptbr` codifica o
playbook em torno da taxonomia v2 (desenho operacional em
`_taxonomy-v2-design.md`), com módulos por domínio; scripts rodam
como *hard gate*; as normas ICMJE e Portaria CNPq nº 2.664/2026 têm
templates de declaração já prontos (A/B/C/D) para cada contexto. A
arquitetura inverte a pergunta de "como fazer Claude acertar?" para
"como impedir Claude de errar?" — essa inversão, respaldada por
evidência peer-reviewed de fabricação em 20–80%, é o que diferencia
um pipeline pesquisável de um gerador de plausibilidade textual.
