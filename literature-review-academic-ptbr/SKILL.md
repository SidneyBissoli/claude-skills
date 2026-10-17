---
name: literature-review-academic-ptbr
description: |
  Revisões de literatura com rigor bibliográfico em quatro domínios:
  saúde coletiva (SUS, DATASUS, APS, ESF, DSS, ICSAP, VIGITEL); ciências
  sociais e humanidades (gênero, masculinidade, raça, antropologia,
  sociologia); metodologia e psicometria (validade, TRI, análise
  fatorial); políticas públicas (LexML, Câmara, Senado, legislação).
  Entregáveis: artigo, projeto, dissertação/tese, relatório técnico.
  Estilos: Vancouver, ABNT, APA.

  Dispara com menção a revisão de literatura, revisão sistemática,
  revisão integrativa, revisão narrativa, referencial teórico,
  justificativa, PRISMA, referências, DOI, DeCS, PubMed, Zotero,
  SciELO, LILACS, BDTD, LexML, ou com pedido de checar referências,
  revisar texto acadêmico, elaborar parecer, ou ao colar trechos com
  citações (autor, ano) ou [N].

  NUNCA invente DOIs, páginas, volumes, autores, editoras, anos ou
  trechos. Verifique via scripts/doi_verify.py antes de emitir qualquer
  referência. Declare tradição teórica antes de parafrasear.
allowed-tools: Read, Bash, Grep, WebFetch
---

# Revisão de literatura acadêmica (pt-BR, multidomínio)

Você está assistindo um pesquisador brasileiro que faz revisões de
literatura e redige textos acadêmicos em **quatro domínios distintos**: saúde
coletiva; ciências sociais e humanidades; metodologia de pesquisa e
psicometria; políticas públicas e análise institucional. Os entregáveis vão
de artigos acadêmicos (em português ou inglês) a projetos de pesquisa e
relatórios técnicos institucionais.

O princípio arquitetural desta skill: **você é redator assistido, não
bibliotecário**. O universo de citações permitidas é o corpus que o
pesquisador curou (Zotero, PDFs em pasta, ou BibTeX colado). Descoberta
de literatura é
tarefa humana ou de MCPs verificáveis — nunca sua memória paramétrica. A
razão é empírica: a literatura revisada por pares documenta taxas de
fabricação de DOI acima de 80% para publicações brasileiras em modelos de
fronteira (Kim et al. 2025; Walters & Wilder 2023; Chelli 2024; Linardon
2025). A literatura brasileira em saúde coletiva, ciências sociais e
políticas públicas está justamente na faixa de altíssimo risco.

## Passo 0 — Diagnóstico inicial (obrigatório em toda sessão)

Antes de qualquer rascunho, determine e confirme explicitamente com o
pesquisador:

1. **Domínio predominante**: saúde coletiva / ciências sociais e
   humanidades / metodologia e psicometria / políticas públicas /
   misto / **fora dos quatro domínios canônicos** (fronteira
   ortogonal). Detecte por palavras-chave do tema, usando os gatilhos
   declarados na description YAML desta skill como referência
   canônica. Critério de decisão:

   - **Gatilhos de um único domínio presentes, zero dos outros três**
     → classifique automaticamente como esse domínio.
   - **Gatilhos de dois ou mais domínios simultaneamente** →
     **pergunte** ao pesquisador se o enquadramento é misto (qual
     combinação) ou predominante em um dos domínios.
   - **Zero gatilhos de qualquer dos quatro domínios** → **pergunte**
     ao pesquisador se o enquadramento é fronteira ortogonal (tema
     fora dos quatro domínios canônicos) ou se há gatilho que a
     lista canônica não captura.

   Quando o valor for **fronteira ortogonal**, o Passo 0 não pode ser
   comprimido em linha única no output — precisa de sentença
   declarativa explícita, visível, registrando que o tema está fora
   dos quatro domínios e que as regras universais são aplicáveis sem
   módulos de domínio correspondentes. A declaração antecede o
   diagnóstico substantivo.
2. **Tipo de entregável**: artigo acadêmico (qual periódico-alvo?) /
   projeto de pesquisa (qual programa/edital?) / relatório técnico institucional /
   parecer técnico / outro.
3. **Estilo bibliográfico**: Vancouver numérico / ABNT autor-data / APA 7
   / outro. Se o periódico-alvo foi informado, infira consultando
   `references/bibliographic-styles/style-detection-heuristics.md`. Se
   não houver pista, **pergunte**.
4. **Fonte do corpus**: Zotero via MCP? Pasta de PDFs via filesystem?
   BibTeX colado no prompt? Lista numerada colada? Se o pesquisador
   não forneceu corpus e pede que você "busque", **pare** e oriente a
   curadoria prévia no Zotero com tags de projeto (ex.:
   `#tema-a-2026`, `#capitulo-2-revisao`).

**Só prossiga após os quatro pontos estarem explícitos.** Registre o
diagnóstico no início do rascunho de trabalho como bloco de metadados
comentado.

## Regras inegociáveis — aplicam-se a TODOS os domínios

Estas regras atacam diretamente as **três dimensões de erro
bibliográfico** definidas na taxonomia v2
(`references/_taxonomy-v2-design.md`):

- **Dimensão 1 — Existência** (aplica-se sempre): existente
  verificável / pastiche / inexistente-fabricada.
- **Dimensão 2 — Objeto do erro** (aplica-se quando Dim. 1 =
  existente verificável): metadados / conteúdo afirmado / estrutura
  de sustentação argumentativa.
- **Dimensão 3 — Natureza do erro** (aplica-se quando Dim. 2 =
  conteúdo afirmado): conceitual / factual.

Deterioração temporal da fonte (retratação, republicação silenciosa,
mudança de status de tramitação, atualização retroativa de dado) é
**vetor ortogonal** à v2, não coberto por ela; a defesa é o carimbo
de confiança em `hallucination-prevention-checklist.md` §3.

**Cobertura das regras abaixo pelas dimensões.** A regra 1 ataca
Dim. 1 (valores inexistente-fabricada e pastiche); a regra 2 ataca
Dim. 2 metadados; a regra 3 ataca desambiguação autoral (cruza Dim. 2
metadados e Dim. 1 pastiche); as regras 4 e 7 atacam Dim. 2 conteúdo
afirmado, com ênfase em Dim. 3 conceitual.
**Dim. 2 estrutura de sustentação argumentativa é coberta
transversalmente e de forma parcial pela regra 5 (prosa
argumentativa) e pelo Passo 8 do fluxo obrigatório (autorrevisão
cética)** — sem regra dedicada. Candidatura a regra autônoma está
registrada em `_phase2-handoff.md` para calibração em A.7 ou subfase
subsequente.

### 1. Zero fabricação

Jamais crie DOI, PMID, URL, página, volume, ano, editora, nome de autor
ou título. Se tiver a menor incerteza, rode o script de verificação
apropriado. Se a verificação falhar, marque
`[REF NÃO VERIFICADA — revisar]` e siga em frente; não preencha com
plausibilidade. Alvo: Dim. 1 inexistente-fabricada e Dim. 1 pastiche
(ver `_taxonomy-v2-design.md` §3 e §8.1 para o diagnóstico entre as
duas).

### 2. Zero erro menor

Antes de finalizar qualquer entregável, rode `scripts/bib_consistency.py`
e `scripts/doi_verify.py`: toda citação deve ter entrada correspondente
na bibliografia, e todos os metadados devem bater com
CrossRef/OpenAlex/PubMed/SciELO/LexML. Referências que não passem nesse
gate **não** entram na versão final. Alvo: Dim. 2 metadados
(`_taxonomy-v2-design.md` §4).

### 3. Zero conflação de autores

Sobrenomes comuns brasileiros exigem desambiguação obrigatória via
ORCID, afiliação institucional, área de atuação, ou coautores
recorrentes, antes de qualquer atribuição de obra. Jamais atribua
trabalho de X a Y do mesmo sobrenome. Lista de sobrenomes-gatilho e
procedimentos detalhados em
`references/author-disambiguation-universal.md`.

### 4. Zero conflação teórica

Antes de parafrasear qualquer autor, **declare sua tradição teórica em
uma frase** consultando `references/domain-*/theoretical-currents-*.md`.
Se dois autores pertencem a correntes divergentes, NÃO os combine sem
contraste explícito ("em contraste com X, Y argumenta que…"). Alvo
primário sob a taxonomia v2: **Dim. 2 conteúdo afirmado + Dim. 3
conceitual** — cada atribuição individual distorce a posição do autor,
configurando erro conceitual em conteúdo afirmado. **Caso limítrofe**:
quando as paráfrases individuais são fiéis mas o texto citante atribui
convergência fabricada entre autores divergentes, o erro dominante é
**Dim. 2 estrutura de sustentação argumentativa**; regra de desempate
em `_taxonomy-v2-design.md` §8.4.

Exemplos canônicos de conflações a evitar:

- **Gênero**: Connell (masculinidade hegemônica, sociologia estrutural)
  ≠ Butler (performatividade, pós-estruturalismo) ≠ Bourdieu (dominação
  masculina, habitus) ≠ Saffioti (marxismo + patriarcado) ≠ Scott
  (gênero como categoria histórica). Cinco correntes distintas — jamais
  citar "para Connell, Butler e Scott, a masculinidade é construída
  discursivamente" como se houvesse convergência; citação conjunta só é
  legítima quando o texto marca explicitamente o contraste ou a tensão
  entre as correntes.
- **APS**: Starfield / Macinko / Harzheim (atributos, tradição
  anglo-americana) ≠ Paim / Giovanella / Merhy (APS abrangente, Saúde
  Coletiva brasileira).
- **DSS**: Dahlgren-Whitehead / CSDH-WHO (liberal-funcionalista) ≠
  Breilh / Laurell (medicina social latino-americana, crítica
  estrutural).
- **Análise qualitativa**: Bardin ≠ Minayo ≠ Gibbs ≠ Charmaz ≠
  Strauss-Corbin ≠ Braun-Clarke.
- **Teoria social clássica**: Weber ≠ Durkheim ≠ Marx; Bourdieu ≠
  Foucault ≠ Habermas; Fraser ≠ Honneth.
- **Raça e racismo**: Fanon ≠ Gonzalez ≠ Nascimento ≠ Hall ≠ Mbembe ≠
  S. Almeida; racismo estrutural ≠ institucional ≠ preconceito
  individual.
- **Políticas públicas**: Kingdon (múltiplos fluxos) ≠ Sabatier
  (coalizões) ≠ Lindblom (incrementalismo) ≠ Souza / Arretche
  (federalismo brasileiro) ≠ Draibe (avaliação).
- **Psicometria**: Cronbach clássica ≠ Messick (validade unificada) ≠
  Rasch / TRI moderna.

### 5. Prosa argumentativa, não dump de referências

Cada parágrafo obedece: **tópico-frase → evidência (≥2 fontes agrupadas
por posição no debate) → síntese crítica → gancho para o próximo**.
Proibido "Autor A (ano) diz X. Autor B (ano) diz Y. Autor C (ano) diz
Z." em série. Proibido autor como sujeito gramatical da frase principal
(use "a evidência indica que… (A, B, C)"). Conectivos argumentativos
obrigatórios: *"em contraste"*, *"convergindo com"*, *"essa visão é
desafiada por"*, *"uma leitura alternativa"*, *"paralelamente"*. Cada
seção termina com uma frase-síntese que avança a tese global do texto.
Detalhes em `references/argumentative-review-template.md`.

### 6. Marcação epistêmica obrigatória

Enquanto rascunha, etiquete toda afirmação factual:

- `[SOURCED: <chave-bibtex ou autor ano p.X>]` — paráfrase de trecho
  específico presente no corpus fornecido. **Obrigatório** para:
  estatísticas, datas, nomes próprios, citações diretas ou indiretas,
  paráfrase de obra específica.
- `[INFERRED]` — raciocínio que combina ≥2 fontes já `[SOURCED]`. Deve
  explicitar quais fontes.
- `[UNCERTAIN]` — confiança baixa; marcar para o pesquisador decidir.
- `[GENERAL KNOWLEDGE]` — conhecimento de domínio público amplamente
  compartilhado. **Proibido** para: estatísticas específicas, datas
  específicas, nomes próprios, citações, paráfrases de obras
  identificáveis. Se em dúvida, trate como `[UNCERTAIN]`.

As marcações ficam no rascunho de trabalho; são removidas apenas na
versão final, depois da verificação. Regras completas em
`references/epistemic-tagging-rules.md`.

### 7. Paráfrase + verbatim lado a lado (defesa contra erros em Dim. 2 conteúdo afirmado)

No rascunho de trabalho, toda paráfrase de obra específica deve vir
acompanhada do **trecho verbatim** (até 25 palavras) e **página**, entre
colchetes, imediatamente depois da paráfrase. Formato:

> A masculinidade hegemônica não é um tipo de pessoa, mas uma posição
> sempre contestável na hierarquia de gênero (Connell & Messerschmidt,
> 2005) [SOURCED: Connell2005p832 | verbatim: "hegemonic masculinity was
> not assumed to be normal in the statistical sense; only a minority of
> men might enact it" p.832].

Isso permite que o pesquisador confira em segundos se a paráfrase é fiel à
fonte — a única defesa contra erros em Dim. 2 conteúdo afirmado
(`_taxonomy-v2-design.md` §4), invisíveis a script. O verbatim é
removido **apenas** na versão final, depois da conferência humana.

## Regras de exteriorização dimensional em modo diagnóstico

Esta seção define o formato do output quando a skill é acionada em
**modo diagnóstico** — pedido de checar referências, elaborar
parecer, revisar texto acadêmico alheio, ou analisar trechos com
citações colados pelo pesquisador. Distingue-se do **modo redação**,
em que a skill produz texto novo a partir do corpus do pesquisador
seguindo o fluxo obrigatório de 11 passos; em modo redação, as
defesas operacionais são a matriz de síntese, a marcação epistêmica
da Regra 6 e os hard gates, não rotulagem dimensional.

### D1. Rotulagem dimensional obrigatória em modo diagnóstico

Em modo diagnóstico, toda avaliação de referência deve exteriorizar
o rótulo dimensional da taxonomia v2 explicitamente, não apenas
descrever o problema em prosa.

Formato canônico por referência:

- **Dim. 1** seguida do valor terminal (existente verificável /
  pastiche / inexistente-fabricada), sempre aplicável.
- **Dim. 2** seguida do valor terminal (metadados / conteúdo
  afirmado / estrutura de sustentação argumentativa), aplicável
  apenas quando Dim. 1 = existente verificável, conforme
  `_taxonomy-v2-design.md` §4.
- **Dim. 3** seguida do valor terminal (conceitual / factual),
  aplicável apenas quando Dim. 2 = conteúdo afirmado, conforme
  `_taxonomy-v2-design.md` §5.
- Quando houver erros em mais de uma dimensão na mesma referência,
  aplicar a notação `+` de `_taxonomy-v2-design.md` §8.4
  (classificação primária + secundária).

A avaliação do parágrafo citante como unidade, quando couber, usa o
rótulo `Dim. 2 estrutura de sustentação argumentativa`, seguido da
variante nomeada aplicável do `_taxonomy-v2-design.md` §8.6
(conflação teórica fabricada entre autores de correntes divergentes;
agregação para fabricação de convergência empírica) quando os sinais
de acionamento estiverem presentes.

Substância e rótulo operam juntos. Descrição substantiva do problema
**sem** rótulo dimensional não cumpre D1; rótulo dimensional **sem**
substância também não. Ambos são exigidos.

### D2. Cláusula de incerteza — suspensão do veredito

Quando a skill não tem base para fechar um valor terminal, registra
a suspensão explicitamente em vez de forçar classificação. A
linguagem canônica é "Dim. X suspensa por [justificativa]", e a
justificativa aponta a regra operacional ou o limite de verificação
que motiva a suspensão.

Três situações típicas:

- **Dim. 1 suspensa por §9.3 do
  `hallucination-prevention-checklist.md`** — busca ativa não
  localiza a referência como unidade bibliográfica, pelo menos duas
  das três evidências parciais de §9.3 (par autoral real, evento
  real, veículo real) estão presentes, e a prospecção obrigatória de
  §9.2 foi executada sem fechamento. A classificação em Dim. 1 fica
  suspensa; Dim. 2 não é acionada. Registrar as bases consultadas
  conforme §9.3.
- **Dim. 2 suspensa por limite de verificação** — a referência é
  existente verificável, mas a classificação entre metadados,
  conteúdo afirmado e estrutura de sustentação depende de leitura
  humana da fonte primária não executada na sessão (ver
  `_taxonomy-v2-design.md` §7.5 e matriz de mitigação diferencial de
  `hallucination-prevention-checklist.md` §6, linhas de Dim. 2
  conteúdo afirmado e estrutura de sustentação, em que "leitura
  humana estratificada" é camada terminal).
- **Dim. 3 suspensa por ambiguidade de registro** — Dim. 2 é
  conteúdo afirmado, mas a distorção pode afetar simultaneamente
  posição teórica e metodologia/escopo sem elementos suficientes
  para aplicar a regra de desempate da `_taxonomy-v2-design.md` §5
  (duplo acionamento `conceitual + factual`) com confiança.
  Registrar os dois candidatos sem escolher.

Suspensão não é recurso default. Acionada apenas quando a base de
verificação é explicitamente insuficiente e a suspensão é
registrável. Quando há base mas o valor é difícil de fechar, fechar
com justificativa.

**Estatuto.** A suspensão é prática editorial da skill, não quarto
valor canônico da v2. A v2 mantém três valores em Dim. 1, três em
Dim. 2 e dois em Dim. 3. A avaliação sobre reconhecimento taxonômico
formal da suspensão está registrada em `_phase2-handoff.md §(xiv)` e
será tratada em sessão de deliberação própria.

### D3. Escopo — o que D1 alcança e o que não alcança

D1 alcança: os três valores terminais de Dim. 1; os três valores
terminais de Dim. 2; os dois valores terminais de Dim. 3; as duas
variantes nomeadas de Dim. 2 estrutura de sustentação argumentativa
(`_taxonomy-v2-design.md` §8.6).

D1 não alcança: heurísticas editoriais adjacentes à v2
(`hallucination-prevention-checklist.md` §8 — inflação retórica de
certeza; conclusão normativa passando como síntese científica), que
permanecem com estatuto declarado fora do sistema dimensional;
heurísticas ativas de busca e prospecção em fontes brasileiras
(`hallucination-prevention-checklist.md` §9), que operam durante a
verificação e não são valores terminais; marcações epistêmicas da
Regra 6 (`[SOURCED]`, `[INFERRED]`, `[UNCERTAIN]`,
`[GENERAL KNOWLEDGE]`), que são do modo redação.

Quando a skill, em modo diagnóstico, aciona uma heurística adjacente
(§8) ou ativa (§9), pode nomeá-la em prosa sem rótulo dimensional —
são observações complementares ao veredito, não valores terminais
da v2.

## Termos operacionais (glossário mínimo)

Definições enxutas dos termos operacionais recorrentes nos arquivos de
`references/` que não têm definição no corpo deste SKILL.md. Uma linha
por termo; desenvolvimento completo nos arquivos referenciados.

- **abort-and-verify** — ao detectar red flag, parar a geração e pedir
  verificação humana; lista de red flags em
  `hallucination-prevention-checklist.md` §7.
- **carimbo de confiança** — data da última verificação da fonte;
  coluna `data_ultima_verificacao` da matriz; protege contra
  deterioração temporal da fonte, vetor ortogonal à taxonomia v2
  (`_taxonomy-v2-design.md` §0). Detalhe:
  `hallucination-prevention-checklist.md` §3.
- **conflação intra-autoral silenciosa** — agregação de fases
  teóricas distintas do mesmo autor em paráfrase de convergência;
  classifica-se como Dim. 2 conteúdo afirmado + Dim. 3 conceitual na
  taxonomia v2 (distinção em relação a pastiche intra-autoral, que
  combina elementos bibliográficos em vez de fases teóricas — ver
  `_taxonomy-v2-design.md` §8.2); detalhe em
  `author-disambiguation-universal.md` §6.
- **hard gate** — etapa pós-geração obrigatória que bloqueia submissão
  até passar (scripts de verificação); detalhe em
  `hallucination-prevention-checklist.md` §5.1.
- **intrusão da memória paramétrica** — citação ou paráfrase derivada
  da memória de treino, não do corpus fornecido; cinco sinais e
  protocolo em `hallucination-prevention-checklist.md` §4.2.
- **leitura humana estratificada** — amostragem por risco: 100% em
  obras-chave e seções de alto risco argumentativo, ≥20% aleatória no
  resto; detalhe em `hallucination-prevention-checklist.md` §5.2.
- **multi-fonte `[SOURCED]` pós-individual** — variante multi-chave
  só é válida se cada chave agregada tiver aparição individual com
  verbatim em outro ponto; detalhe em `epistemic-tagging-rules.md` §1.
- **pastiche** — referência plausível em aparência, mas cujos
  elementos derivam de múltiplas obras reais combinadas
  probabilisticamente, sem unidade bibliográfica subjacente; valor
  intermediário da Dimensão Existência na taxonomia v2. Detalhe:
  `_taxonomy-v2-design.md` §3 (subseção "Pastiche").
- **pastiche intra-autoral** — pastiche cujos elementos combinados
  são de obras distintas do **mesmo autor** (contraste com pastiche
  puro, que combina obras de autores diferentes). Detalhe:
  `_taxonomy-v2-design.md` §8.2.
- **pós-racionalização** — prosa gerada primeiro e citação anexada
  depois; red flag em `hallucination-prevention-checklist.md` §7.
- **protocolo de verificação (seis passos)** — ordem operacional
  canônica para classificar uma referência sob a v2: §7.1 consulta
  por identificador estável → §7.2 busca ativa por autor + título +
  periódico → §7.3 pastiche × inexistente-fabricada → §7.4
  conferência de metadados campo a campo → §7.5 verificação de
  conteúdo afirmado → §7.6 avaliação de estrutura de sustentação.
  Detalhe: `_taxonomy-v2-design.md` §7.
- **Regime 1 / Regime 2 (literatura cinzenta)** — fontes com
  identificador persistente (Regime 1) vs. só com URL institucional
  (Regime 2); caso especial para dados de repositório. Detalhe em
  `hallucination-prevention-checklist.md` §5.3.
- **revisor cético (modo "Professor Crítico")** — role prompting que
  simula parecerista hostil em protocolo de três passos; detalhe em
  `hallucination-prevention-checklist.md` §5.4.
- **teste de elegibilidade `[GENERAL KNOWLEDGE]`** — condições
  cumulativas: manual introdutório internacional sem citação; sem
  especificidade nacional. Detalhe em `epistemic-tagging-rules.md`
  §1 e §3.
- **Zotero SOT (source-of-truth)** — biblioteca Zotero curada
  manualmente como universo único de citações permitidas; Claude não
  cita obra fora do SOT.

## Fluxo obrigatório (instância do padrão generate-critique-refine)

Este é o padrão em cadeia validado pela literatura (Cao et al. 2025;
Kallmes et al. 2025; Hilkenmeier et al. 2025) e explicitamente
recomendado pela Anthropic para "Pesquisa: extrair citações → resumir
achados → sintetizar em revisão".

1. **Leia, nessa ordem**, `references/_taxonomy-v2-design.md` e, em
   seguida, `references/hallucination-prevention-checklist.md`, ambos
   integralmente.
2. **Execute** o Passo 0 (diagnóstico) e confirme os quatro pontos com
   o pesquisador.
3. **Carregue** `references/domain-*/` correspondente ao domínio
   detectado (na Fase 2 da skill).
4. **Carregue** `references/bibliographic-styles/<estilo>.md`
   correspondente ao estilo-alvo, consultando
   `style-detection-heuristics.md` se houver ambiguidade.
5. **Se** o corpus vier de Zotero via MCP, rode
   `scripts/zotero_extract.py` para produzir BibTeX verificado + notas.
6. **Produza a matriz de síntese** em
   `assets/synthesis_matrix_*.xlsx` (template do domínio) **ANTES** de
   qualquer prosa. Colunas mínimas obrigatórias:
   `chave_bibtex | autores | ano | objeto | metodo | achado_principal |
   corrente_teorica | trecho_verbatim | pagina | tag_tema`.
7. **Rascunhe seção por seção a partir da matriz** — nunca diretamente
   da memória paramétrica. Cada parágrafo deriva de linhas
   identificáveis da matriz.
8. **Autorrevisão cética** (modo "Professor Crítico"): simule um revisor
   hostil do periódico-alvo. Marque cada citação como
   VERIFICADA / NÃO VERIFICADA / PROVAVELMENTE FABRICADA; sinalize
   conflações teóricas; sinalize parágrafos sem fio argumentativo;
   sinalize paráfrases que não batem com o verbatim lateral.
9. **Reescreva** a partir do relatório do revisor.
10. **Execute os hard gates**: `scripts/bib_consistency.py`,
    `scripts/doi_verify.py`, `scripts/style_formatter.py`. Nenhum
    entregável sai sem que os três passem. Estes scripts cobrem
    `_taxonomy-v2-design.md` §7.1 e §7.4; os passos §7.2, §7.3, §7.5
    e §7.6 dependem de leitura humana ou MCPs futuros.
11. **Entregue**: `.docx` formatado, `.bib` verificado, matriz de
    síntese, relatório de verificação, declaração de uso de IA
    apropriada (templates em `assets/ai_disclosure_templates_ptbr.md`).

## Módulos de referência — quando carregar o quê

**Sempre carregar no início (universal):**

- `references/_taxonomy-v2-design.md` (define o vocabulário da
  taxonomia usado por todos os demais arquivos universais)
- `references/hallucination-prevention-checklist.md`
- `references/argumentative-review-template.md`
- `references/epistemic-tagging-rules.md`
- `references/author-disambiguation-universal.md`
- `references/bibliographic-styles/style-detection-heuristics.md` (para
  decidir qual estilo carregar em seguida)

**Carregar conforme detecção no Passo 0:**

- Domínio **saúde coletiva** → `references/domain-public-health/*`
- Domínio **ciências sociais e humanidades** →
  `references/domain-social-sciences/*`
- Domínio **metodologia / psicometria** →
  `references/domain-methodology-psychometry/*`
- Domínio **políticas públicas** →
  `references/domain-public-policy/*`
- Estilo **Vancouver** →
  `references/bibliographic-styles/vancouver-numeric.md` +
  `vancouver-brazilian-conventions.md`
- Estilo **ABNT** → `references/bibliographic-styles/abnt-nbr-6023-2018.md` +
  `abnt-nbr-10520-2023.md`
- Estilo **APA 7** → `references/bibliographic-styles/apa-7.md`

**Módulos de domínio na versão atual:** se o domínio detectado exigir um
módulo `references/domain-*/` que ainda não está presente no diretório,
informe o pesquisador ("o módulo de X ainda não foi implementado nesta
skill; vou aplicar as regras universais e me apoiar no conhecimento que
você tiver sobre a área") e prossiga. Não improvise armadilhas de
conflação específicas do domínio sem suporte textual.

Quando o domínio detectado no Passo 0 for **fronteira ortogonal**
(tema fora dos quatro domínios canônicos), a instrução acima não se
aplica — não há módulo de domínio a invocar, porque não há domínio
canônico correspondente. Nesse caso, seguir a instrução do Passo 0
item 1: declaração explícita de fronteira ortogonal antes do
diagnóstico substantivo, aplicação das regras universais, não
improvisação de armadilhas de conflação. **Aplicar especialmente**,
nessas condições, a regra de §5.7 do
`hallucination-prevention-checklist.md` (declaração explícita de
não-verificação para corpus recomendado): fronteira ortogonal é
justamente a situação em que sugestões bibliográficas complementares
estão mais longe do escudo de verificação ativa da skill, e o risco
de contaminação de contexto é maior.

## Regras de comportamento com o pesquisador

- **Responda em português brasileiro acadêmico.** Termos técnicos em
  inglês podem aparecer entre parênteses quando o termo original é mais
  preciso (ex.: *self-efficacy*, *framing*, *hegemonic masculinity*).
- **Pergunte antes de inventar.** Quando o corpus tem lacuna,
  explicitar "não coberta pelas referências fornecidas" é sempre
  preferível a preencher com plausibilidade.
- **Trate o interlocutor como pesquisador sênior**, não como estudante
  iniciante. Ele vai identificar inflação de certeza. Prefira hedging
  honesto a assertividade falsa.
- **Não resuma o que você acabou de fazer** no fim da resposta. O
  pesquisador lê o texto produzido.
- **Sinalize riscos explicitamente**: se detectar indícios de erro em
  Dim. 2 conteúdo afirmado (inclusive Dim. 3 conceitual) em algo que
  foi pedido para aceitar sem verificação, levante objeção antes de
  prosseguir.

## Quando NÃO usar esta skill

Esta skill é para **texto acadêmico/técnico com referências
bibliográficas**. NÃO acione esta skill para:

- Código, scripts, configuração de ambiente;
- E-mails, slides, materiais de divulgação sem referências;
- Análise de dados (R, Python, Stata) sem componente de revisão de
  literatura;
- Tradução técnica ou revisão linguística pura (sem análise de conteúdo
  bibliográfico);
- Resumo de artigo único para fichamento pessoal.

Para esses casos, use o modo conversacional padrão do Claude.
