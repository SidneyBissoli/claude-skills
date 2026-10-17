# Checklist de prevenção de alucinação bibliográfica

## 0. Como usar este documento

Este checklist é lido **uma vez** no início da sessão, no passo 1 do
fluxo obrigatório definido no SKILL.md — não a cada parágrafo, para
economia de contexto. As regras passam a valer durante toda a sessão.

Como aplicar cada seção:

- §1 calibra postura (por que cada camada de defesa existe).
- §2 apresenta a taxonomia v2 em três dimensões hierárquicas
  condicionais (definição canônica em `_taxonomy-v2-design.md`).
- §3 é checklist de pré-geração, verificado antes do primeiro parágrafo.
- §4 é checklist durante a geração, verificado a cada parágrafo
  concluído.
- §5 é checklist pós-geração, verificado antes da submissão.
- §6 sintetiza em tabela qual camada apanha qual valor terminal da
  taxonomia v2.
- §7 lista red flags operacionais que disparam abort-and-verify
  imediato.
- §8 registra heurísticas editoriais adjacentes à v2 — padrões
  detectáveis no texto, fora do sistema dimensional, aplicáveis como
  observações complementares ao revisor cético.
- §9 registra heurísticas **ativas** de busca e prospecção em fontes
  brasileiras — regras aplicáveis durante a verificação de Dim. 1 e
  de Dim. 2 metadados, centralmente nas cinco situações canonizadas
  no Teste 02 da Fase A.7 (desalinhamento agenda-tema; prospecção de
  portais institucionais; regra de desempate em "indeterminada"; ano
  do volume vs. data OJS; DOI de repositórios abertos).

## 1. Calibragem de risco — por que este pipeline existe

Taxas de fabricação de referências em literatura revisada por pares,
ordem aproximada:

- GPT-3.5 em revisão de literatura: ~55% de referências fabricadas
  (Walters & Wilder 2023, *Scientific Reports*).
- GPT-4 na mesma tarefa: ~18%.
- GPT-4o em saúde mental: ~19,9% fabricadas; outras ~45,4% com erros
  entre as referências reais (Linardon 2025, *JMIR Mental Health*).
- Gemini Advanced: ~76,7%.
- Bard em revisão sistemática: ~91,4% (Chelli 2024).
- Claude-3-haiku em publicações de países de menor renda: >80% de DOIs
  fabricados (Kim et al. 2025, *Publications*).

Literatura brasileira em saúde coletiva, ciências sociais, políticas
públicas — áreas com indexação internacional desigual — cai justamente
na faixa de altíssimo risco medido. Publicações pós-2020 pioram a taxa
em todos os modelos testados.

RAG é antídoto parcial, não completo. Wallat et al. 2024
(arXiv:2412.18004) documentam até 57% de citações "pós-racionalizadas"
mesmo com recuperação ativa — o modelo gera a resposta a partir da
memória paramétrica e, depois, faz shallow-matching com uma citação
plausível. Conclusão operacional: verificação por script mais leitura
humana é obrigatória, não opcional, mesmo quando o corpus é fornecido.

McGowan et al. 2023 (*Psychiatry Research*) documentaram ainda que
LLMs produzem sistematicamente objetos bibliográficos plausíveis em
aparência mas sem unidade subjacente — elementos reais combinados
probabilisticamente. Essa categoria, denominada **pastiche**, é
incorporada como valor intermediário da Dimensão Existência na v2
(§2 abaixo).

## 2. A taxonomia v2 — três dimensões hierárquicas condicionais

A taxonomia canônica da skill é a v2, definida em detalhe em
`_taxonomy-v2-design.md`. Apresentação sintética aqui para que este
checklist seja autossuficiente; o desenho operacional, a árvore
decisória, o protocolo de verificação em seis passos
(`_taxonomy-v2-design.md §7`) e os casos limítrofes ficam no
documento-fonte.

**Dimensão 1 — Existência** (aplica-se sempre). Avalia se a
referência corresponde a obra real recuperável. Três valores:

- **Existente verificável** — obra real, única, recuperável por DOI,
  PMID, ISBN ou por busca em bases bibliográficas por autor + título
  + periódico.
- **Pastiche** — elementos (autor, título, periódico, ano) de
  múltiplas obras reais combinados sem unidade bibliográfica
  subjacente. Categoria derivada de McGowan et al. 2023; distinção
  entre pastiche puro e intra-autoral em `_taxonomy-v2-design.md §8.2`.
- **Inexistente-fabricada** — nenhuma obra real subjacente; elementos
  combinados arbitrariamente ou inventados.

**Dimensão 2 — Objeto do erro** (aplica-se quando Dim. 1 = existente
verificável). Avalia onde reside o erro. Três valores:

- **Metadados bibliográficos** — erro em elementos da ficha (autor,
  ano, título, periódico, volume, páginas, DOI, edição).
- **Conteúdo afirmado** — erro nas proposições atribuídas à fonte
  (paráfrase distorce o que a obra diz).
- **Estrutura de sustentação argumentativa** — erro na mobilização
  retórica da fonte (fonte do tipo errado para a afirmação; estatuto
  epistêmico atribuído pelo texto incompatível com o estatuto efetivo
  da fonte).

**Dimensão 3 — Natureza do erro** (aplica-se quando Dim. 2 = conteúdo
afirmado). Avalia em que registro o conteúdo foi distorcido. Dois
valores:

- **Conceitual** — atribuição teórica, conceito, enquadramento ou
  invocação de tradição distorcida. Verificação exige releitura
  interpretativa da fonte.
- **Factual** — dado empírico específico distorcido (taxa, valor,
  data, amostra). Verificação exige confronto numérico ou documental.

**Vetor ortogonal — drift temporal.** A fonte se deteriora após a
citação (retratação de artigo com DOI; republicação silenciosa de
relatório institucional sob mesma URL; mudança de status de
tramitação em LexML/Câmara/Senado; atualização retroativa de
microdado em DATASUS/IBGE/RAIS). Não é erro no momento da geração; é
deterioração posterior. Fora do escopo da v2 (que opera em tempo da
geração); defesa autônoma pelo **carimbo de confiança** (§3) e
reverificação pré-submissão. Uma referência válida hoje e retratada
amanhã torna-se inexistente-fabricada superveniente — não porque a
geração errou, mas porque o mundo mudou.

### Detectabilidade e custo por valor terminal

- **Dim. 1 (existência)** e **Dim. 2 metadados** — detectáveis por
  script (`doi_verify.py`, `bib_consistency.py`). Custo típico:
  10-30 min de retrabalho por referência errada encontrada na
  revisão de prova; retratação potencial se uma inexistente-fabricada
  não é detectada.
- **Dim. 2 conteúdo afirmado** — invisível a script; só leitura
  humana da fonte primária detecta. Custo típico: questionamento
  ético na banca ou em pareceres.
  - **Dim. 3 conceitual** exige releitura interpretativa (protocolo
    em `_taxonomy-v2-design.md §7.5.1`).
  - **Dim. 3 factual** exige confronto numérico/documental (protocolo
    em `_taxonomy-v2-design.md §7.5.2`).
- **Dim. 2 estrutura de sustentação argumentativa** — invisível a
  script; exige leitura contextual do parágrafo citante contra o
  estatuto epistêmico da fonte. Cobertura transversal parcial pela
  regra 5 (prosa argumentativa) do `SKILL.md` e pelo Passo 8 do fluxo
  obrigatório (autorrevisão cética); candidatura a regra dedicada
  registrada em `_phase2-handoff.md §(viii)`.
- **Vetor drift temporal** — não se detecta no momento da geração;
  reverificação pré-submissão com carimbo de confiança é a única
  defesa.

À medida que se vai de Dim. 1 para Dim. 2 conteúdo afirmado e Dim. 2
estrutura de sustentação, o custo aumenta e a detectabilidade por
script diminui — priorizar tempo humano nas camadas de Dim. 2
quando o prazo aperta.

## 3. Checklist pré-geração (antes de qualquer parágrafo)

- [ ] Passo 0 completo: domínio, tipo de entregável, estilo, corpus
      confirmados com o pesquisador.
- [ ] BibTeX validado por `scripts/doi_verify.py` (zero DOI 404; zero
      estado `RETRACTED` sem decisão tomada).
- [ ] Matriz de síntese preenchida, inclusive coluna `corrente_teorica`
      e coluna `risco_verificacao`.
- [ ] Módulos `references/domain-*/` e
      `references/bibliographic-styles/<x>` correspondentes carregados.
      Se o módulo de domínio apropriado não existir no diretório,
      sinalizar ao pesquisador e aplicar somente as regras universais.
- [ ] Carimbo de confiança registrado para cada fonte — coluna
      `data_ultima_verificacao` na matriz. Crítico para literatura
      cinzenta (IPEA, CEPAL, BM), legislação (atos podem ser revogados,
      consolidados, emendados), preprints (podem ter sido publicados
      com mudanças) e URLs em geral (link rot). Para DOI/PMID o
      identificador é persistente, mas metadados e status de retratação
      não: registrar o carimbo mesmo assim, especialmente para
      referências-chave. `doi_verify.py` devolve status de retratação
      na consulta CrossRef; o carimbo é o registro de quando se confiou
      naquela fonte. Protege contra o vetor ortogonal drift temporal
      (§2).

## 4. Checklist durante a geração

### 4.1 Regras de escrita — autoconferência ativa

A cada parágrafo concluído:

- [ ] Toda afirmação factual tem marcação epistêmica
      (`[SOURCED:<chave>]`, `[INFERRED]`, `[UNCERTAIN]`;
      `[GENERAL KNOWLEDGE]` apenas para conhecimento genuinamente
      compartilhado, proibido para estatísticas, datas, nomes próprios
      ou paráfrases de obras identificáveis).
- [ ] Toda paráfrase de obra específica traz verbatim lateral (até 25
      palavras) mais página, no rascunho de trabalho.
- [ ] Toda citação corresponde a chave BibTeX presente no corpus
      fornecido.
- [ ] Lacunas do corpus declaradas como *"não coberta pelas
      referências fornecidas"*, nunca supridas por inferência.
- [ ] Autor não aparece como sujeito gramatical da frase principal
      (preferir *"a evidência indica… (A, B)"* a *"A mostra que…"*).

### 4.2 Intrusão da memória paramétrica — diagnóstico e protocolo

A regra "cite apenas o que está no corpus" é violada silenciosamente
quando a memória paramétrica do modelo injeta uma lembrança plausível.
A prosa resultante é fluida e a citação parece competente. O problema
só emerge na verificação final ou no parecer.

#### Cinco sinais de intrusão

**(i)** Prosa fluida sem chamadas a ferramentas. Claude escreve
parágrafos inteiros sem consultar o BibTeX carregado, o PDF na pasta,
o MCP do Zotero ou a matriz de síntese. Se a prosa deriva do corpus,
é de se esperar que o modelo esteja lendo algo — a ausência de leitura
é sinal.

**(ii)** Citação de obra sem chave no corpus, ou chave inventada sem
rastreabilidade ao Zotero/BibTeX fornecido. A referência citada não
aparece no `.bib` carregado nem nas entradas do Zotero consultadas
nesta sessão; ou a chave aparece plausível mas não tem origem no
corpus fornecido — Claude pode ter fabricado uma chave para obra
que "lembra" da memória paramétrica. Chave plausível é sinal, não
prova de legitimidade.

**(iii)** Formato de citação divergente do estilo acordado no Passo 0.
Se o estilo-alvo é ABNT autor-data e aparece "(Author et al., 2019)",
ou se é Vancouver numérico e aparece "(Souza, 2020, p. 45)", é
autocompletion paramétrica: o modelo reproduziu o formato mais
frequente da obra na memória de treino, não o estilo do corpus.

**(iv)** Datas ou estatísticas específicas sem tag `[SOURCED]`. *"A
prevalência foi de 12,3% em 2019"*, *"em 1978 Alma-Ata estabeleceu…"*,
*"o coeficiente de Gini passou de X para Y"* sem marcação epistêmica —
esses tipos de afirmação são proibidos como `[GENERAL KNOWLEDGE]` e
exigem fonte.

**(v)** Paráfrase detalhada de obra sem PDF nem verbatim no corpus.
Quando há paráfrase com alto grau de detalhe e nenhum verbatim lateral,
a probabilidade de intrusão é alta — a paráfrase não teria de onde
derivar.

#### Protocolo de interrupção

Ao detectar qualquer um dos cinco sinais (em autorrevisão de Claude ou
em leitura do pesquisador):

1. Parar imediatamente a geração do parágrafo corrente.
2. Sinalizar explicitamente a suspeita ao pesquisador, apontando qual
   sinal foi observado e qual afirmação/citação o disparou.
3. Aguardar decisão humana. Três opções:
   1. adicionar a obra ao Zotero/corpus e reiniciar o parágrafo com
      base no material agora disponível;
   2. reescrever o parágrafo sem a afirmação intrusa (*"não coberta
      pelas referências fornecidas"*);
   3. aceitar a afirmação com tag `[UNCERTAIN]` e plano de verificação
      posterior.
4. **Não tentar corrigir sozinho.** No workflow padrão, quando o modelo
   substitui uma citação suspeita sem intervenção humana, a
   substituição vem da mesma fonte paramétrica que produziu a suspeita
   original. O resultado superficial parece resolver o problema, mas a
   intrusão apenas muda de forma.

### 4.3 Contraste teórico obrigatório — regra do marcador

Antes de parafrasear dois ou mais autores no mesmo parágrafo,
determinar se compartilham posição ou pertencem a correntes distintas.

- Autores de mesma corrente → paráfrase conjunta legítima, sem
  marcador obrigatório.
- Autores de correntes distintas → paráfrase conjunta só com marcador
  explícito de contraste (*"em contraste com…"*, *"convergindo
  parcialmente com…"*, *"em tensão com…"*, *"posição alternativa
  em…"*).
- Autores de correntes distintas agregados em paráfrase de convergência
  sem marcador → conflação. Classificação v2: **Dim. 2 conteúdo
  afirmado + Dim. 3 conceitual** (ver `_taxonomy-v2-design.md §5`).

Pares-gatilho canônicos estão listados na regra 4 do SKILL.md. Detalhes
por domínio (quando o respectivo módulo existir) em
`references/domain-*/theoretical-currents-*.md`. Na ausência do módulo
de domínio, declarar explicitamente a posição de cada autor antes de
qualquer agregação — sem suporte textual, não se improvisa taxonomia
teórica.

## 5. Checklist pós-geração (hard gate antes da submissão)

### 5.1 Verificação automatizada — hard gate obrigatório

Nenhum entregável sai sem que os três scripts abaixo passem:

- [ ] `scripts/doi_verify.py` — cada DOI/PMID retorna `VERIFIED`,
      `VERIFIED_WITH_CORRECTION`, `RETRACTED`, `EXPRESSION_OF_CONCERN`,
      `METADATA_MISMATCH` ou `NOT_FOUND`. Estado `RETRACTED` bloqueia
      submissão até decisão explícita (remover ou citar com nota de
      retratação). `NOT_FOUND` bloqueia até reverificação manual; se
      persistir, marcar `[REF NÃO VERIFICADA — revisar]` e não
      publicar.
- [ ] `scripts/bib_consistency.py` — zero citação órfã (chave na prosa
      sem entrada na bibliografia) e zero entrada sem citação no corpo
      (salvo decisão editorial explícita).
- [ ] `scripts/style_formatter.py` — formato bibliográfico conforme
      estilo acordado no Passo 0 (Vancouver/ABNT/APA).

Reverificação antes da submissão final: para revisões em
desenvolvimento longo (tese, artigo em review por meses, relatórios
técnicos atualizados), rerodar `doi_verify.py` antes da submissão
definitiva e atualizar o carimbo de confiança de cada referência —
retratações e erratas emergem ao longo do tempo, e a verificação
inicial não cobre.

### 5.2 Verificação humana amostral — única defesa contra Dim. 2 conteúdo afirmado

Script não apanha Dim. 2 conteúdo afirmado (nem conceitual nem
factual) nem Dim. 2 estrutura de sustentação; verbatim lateral ajuda
mas não substitui conferência da paráfrase contra o PDF. Como o tempo
humano é escasso, a amostragem é estratificada por risco.

**100% — paráfrases de obras-chave.** Obra-chave é aquela cuja tese
central é citada (não apenas um dado tangencial); ou obra de autor que
aparece múltiplas vezes ao longo do texto; ou obra que fundamenta
diretamente uma afirmação, recomendação ou posicionamento do
entregável.

**100% — paráfrases em seções que sustentam a pergunta de pesquisa ou
a justificativa.** Custo de distorção máximo: introdução, justificativa,
pergunta de pesquisa, framework teórico, conclusão quando faz
afirmações substantivas. Em relatórios técnicos, incluir a seção de
recomendações — uma recomendação apoiada em paráfrase distorcida é o
pior desfecho possível do entregável.

**≥20% em amostra aleatória nas demais seções.** Contextualização,
pano de fundo histórico, revisão tangencial, discussões secundárias.
Seleção por script ou planilha, não "por conveniência" (a tentação
humana é conferir as mais fáceis, justamente as menos informativas
sobre problemas).

Operacionalização:

- Coluna `risco_verificacao` na matriz de síntese: `alto` | `baixo`.
  `alto` cobre obras-chave e paráfrases em seções de alto risco
  argumentativo; `baixo`, o resto.
- Registrar resultado por paráfrase conferida: `FIEL` | `DISTORÇÃO
  LEVE` | `DISTORÇÃO GRAVE` | `INVENÇÃO`. Os dois últimos bloqueiam
  submissão até reescrita e nova conferência.

### 5.3 Fontes sem DOI e literatura cinzenta

**Regime 1 — fonte com identificador persistente.** Exemplos: DOI,
handle BDTD (teses), tombamento LexML (legislação), PMID, ISBN
(livros); ISBN mais páginas (capítulos em coletâneas); ISSN mais volume
mais páginas (anais indexados, como SBPC ou congressos com publicação
formal); handle ou DOI do paper quando o congresso atribui (cada vez
mais comum). Anais sem ISSN — frequentes em Anpocs, Abrapso, ABA,
ANPEPP — caem no Regime 2.

O identificador é a âncora; URL é descartável. Registrar o carimbo de
confiança (data de última verificação) — protege contra retratação ou
erratas em DOI, mudança de metadados em handle, reedição em coletânea
com ISBN.

**Regime 2 — fonte só com URL institucional ou de evento.** Exemplos:
IPEA, CEPAL, Banco Mundial, OCDE, Planalto, ministérios, notas técnicas
avulsas, anais de congressos BR sem indexação (Anpocs, Abrapso, ABA,
ANPEPP quando publicados só como coletânea no site do evento).

Registrar URL exata consultada mais carimbo de confiança. Para casos
críticos (relatório que fundamenta recomendação central do entregável;
nota técnica objeto de disputa interpretativa; paper de congresso que
pode sumir quando o site do evento é desligado): baixar PDF local e
registrar SHA256 do arquivo — única defesa contra republicação
silenciosa da mesma URL com conteúdo alterado, ou contra
desaparecimento do link.

Exceção parcial: Câmara (`dadosabertos.camara.leg.br`) e Senado
(`www12.senado.leg.br/dados-abertos`) mantêm links permanentes por
proposição, discurso, sessão e ata.
- Estável (link permanente suficiente): texto do discurso, texto da
  proposição na versão consultada, data da sessão, autor, URL.
- Variável (envelhece rápido; carimbo de confiança deve ser próximo à
  data de publicação do entregável): status de tramitação
  (aprovada/arquivada/pendente), emendas subsequentes, situação atual.
- Implicação prática: citar um discurso ou versão específica de
  proposição → confiar no link permanente. Citar status de tramitação
  ("o PL X está em análise na CCJ") → a afirmação tem prazo de validade
  curto; reverificar imediatamente antes da submissão.

**Caso especial — dados de repositórios oficiais.** Extração de dados
ou indicadores de repositórios oficiais (IBGE, DATASUS, VIGITEL,
Ipeadata, Banco Central, TSE, INEP, RAIS, ANEEL, CAGED) não é citação
de documento — é snapshot de uma base que atualiza silenciosamente. A
convenção dos dois regimes anteriores não cobre esse caso; usa-se
protocolo próprio.

Convenção mínima obrigatória:

- fonte (nome do sistema: "DATASUS/SIM", "IBGE/PNAD Contínua",
  "VIGITEL", "Ipeadata/IPCA");
- ano de referência dos dados (o ano a que os dados se referem, não o
  ano da consulta);
- data de extração — crítico: mesma consulta em datas diferentes pode
  retornar valores distintos, por correção retrospectiva ou atualização
  do painel. É o carimbo de confiança desse caso;
- URL estável da consulta (link permanente quando o sistema oferece;
  caso contrário, URL do painel mais descrição do filtro aplicado,
  suficiente para replicação);
- versão do microdado quando houver (PNS v1 vs. v2 corrigida; SIM/DO
  consolidado vs. preliminar; RAIS com reclassificação retroativa de
  CNAE).

Exemplos canônicos:

> "Taxa de mortalidade infantil, Brasil, 2020. Fonte: DATASUS/SIM,
> microdados consolidados v2 (dados atualizados pelo MS em 2023).
> Extração em 12 mar 2026 via tabnet.datasus.gov.br/…"

> "Proporção de adultos com hipertensão autorreferida, capitais, 2019.
> Fonte: VIGITEL 2019, Ministério da Saúde. Extração em 05 abr 2026
> via vigitel.saude.gov.br/…"

Reverificar sempre que o entregável se aproximar da submissão: bases
oficiais aplicam correções retrospectivas sem aviso, e o número citado
pode ter mudado. Em relatórios técnicos com dados que sustentam
recomendação, a reverificação deve constar explicitamente na seção de
metodologia ou em nota de rodapé da tabela/gráfico.

### 5.4 Revisor cético — protocolo de três passos

O workflow generate-critique-refine (Cao et al. 2025;
Kallmes et al. 2025) só funciona se o passo de crítica for explícito e
separado do passo de reescrita. Sem separação, Claude corrige no mesmo
turno em que detecta, e o pesquisador perde visibilidade sobre o
diagnóstico.

**Passo 1 — Assumir explicitamente o papel.** Claude anuncia
literalmente a mudança de modo: *"Vou agora atuar como parecerista
cético do [periódico-alvo]"*. Role prompting consta na hierarquia de
engenharia de prompt da Anthropic como técnica padrão. A postura é
**hostil, não colaborativa**: o revisor está do lado do editor, não do
autor.

**Passo 2 — Relatório estruturado, sem reescrita.** Claude gera
relatório com categorias fixas, nesta ordem:

- **Fabricações suspeitas**: cada citação marcada como `VERIFICADA` /
  `NÃO VERIFICADA` / `PROVAVELMENTE FABRICADA`, com justificativa
  (chave no corpus? metadados batem? DOI existe?).
- **Conflações teóricas**: parágrafos onde autores de correntes
  divergentes aparecem em paráfrase de convergência sem marcador de
  contraste. Citar parágrafo e autores envolvidos.
- **Fio argumentativo**: parágrafos sem tópico-frase clara; seções sem
  frase-síntese final; citações em série sem tensão argumentativa.
- **Adequação ao estilo**: divergências em relação ao estilo
  bibliográfico acordado (Vancouver/ABNT/APA); formatação de citação;
  posicionamento do DOI; hierarquia de títulos.
- **Paráfrase vs. verbatim**: conferência amostral de paráfrases contra
  os verbatim laterais; sinalizar paráfrases que extrapolam o trecho
  citado.
- **Marcação epistêmica**: afirmações sem `[SOURCED]` que deveriam ter;
  `[GENERAL KNOWLEDGE]` em estatística/data/nome próprio.

O relatório termina com um veredicto: "pronto para submissão" /
"revisão menor" / "revisão maior" / "refazer a partir da matriz".

**Passo 3 — Reescrita apenas após aprovação do relatório.** Claude
**não** reescreve o texto junto com o relatório. Aguarda o pesquisador
revisar o diagnóstico, aceitar/rejeitar/ajustar pontos, e só então
emite o plano de reescrita. Três razões:

- O relatório pode estar errado: pode marcar como "fabricação provável"
  uma citação que o pesquisador consegue validar por outros caminhos,
  ou deixar passar conflação sutil. Aprovação humana filtra esses erros
  antes que virem reescrita.
- Reescrita a partir de diagnóstico errado é mais trabalhosa de desfazer
  do que diagnóstico errado sozinho.
- Manter os dois turnos separados preserva rastro auditável — "que
  problemas foram detectados" e "o que foi feito a respeito" ficam em
  registros distintos, úteis para a declaração de uso de IA
  (especialmente sob Portaria CNPq 2.664/2026, que exige documentação
  de etapas).

### 5.5 Declaração de uso de IA — escolha do template

Antes de submeter, inserir a declaração apropriada, conforme
`assets/ai_disclosure_templates_ptbr.md`:

- Template A — uso mínimo (revisão linguística de parágrafos
  previamente escritos pelo autor).
- Template B — uso substantivo (organização preliminar da matriz a
  partir de extrações humanas; rascunho inicial de parágrafos a partir
  de referências curadas; revisão linguística).
- Template C — revista com teto de participação de IA (Ciência & Saúde
  Coletiva limita a 20%); usar B mais declaração de estimativa.
- Template D — relatório técnico institucional (uso interno com
  responsabilidade integral da equipe técnica).

A Portaria CNPq 2.664/2026, art. 9, exige declaração em qualquer etapa
apoiada por IA. O rastro auditável do revisor cético (§5.4 Passo 2),
os logs de verificação (§5.1) e a matriz de síntese com carimbo de
confiança (§3) constituem a documentação operacional que sustenta a
declaração. Conservar esses artefatos junto com o entregável final.

### 5.6 Verificação meta-bibliográfica cascateada

Regra ativa, introduzida pela decisão 21 do `_changelog.md` (A.7 Bloco
A, A3). Em referências que são **revisões bibliográficas** (narrativa,
integrativa, sistemática, *scoping review*, revisão crítica) citadas
no corpo do entregável, a inspeção da lista de referências internas
da revisão passa a ser etapa adicional de verificação, **mesmo quando
os metadados da revisão citada são corretos e a paráfrase do
entregável é fiel à revisão**.

Motivação. Uma referência pode ser existente verificável, metadados
corretos, conteúdo citado fiel — e ainda assim sustentar suas
afirmações em referências internas fabricadas. A cadeia probatória
da obra citada está contaminada em elo interno. A camada de
verificação anterior (Dim. 1, Dim. 2 metadados, Dim. 2 conteúdo
afirmado do texto citante contra a revisão) passa pela revisão sem
detectar o defeito.

Procedimento mínimo:

- [ ] Identificar as revisões bibliográficas no corpus — por gênero
      declarado (título, resumo) ou por inspeção do método.
- [ ] Para cada revisão citada em posição de sustentação argumentativa
      no entregável (não apenas menção tangencial): abrir a lista de
      referências internas e inspecionar amostra aleatória de ao menos
      cinco entradas, com prioridade para: autores com iniciais
      genéricas ("Silva, J.", "Almeida, M.") sem prenomes distintivos;
      periódicos nacionais com padrão de numeração conhecido em que
      o formato declarado destoa; entradas que sustentam afirmações
      centrais da revisão.
- [ ] Conferir cada referência interna inspecionada contra CrossRef,
      PubMed, Google Scholar, SciELO, LILACS, BDTD ou base apropriada,
      pelo mesmo protocolo de §7.1–§7.2 do `_taxonomy-v2-design.md`.
- [ ] Registrar o resultado da inspeção em campo existente da matriz
      de síntese (coluna de observações, nota associada à revisão, ou
      mecanismo equivalente) — o objetivo é garantir que a verificação
      foi feita e é rastreável, não fixar o mecanismo estrutural de
      registro. Em caso de achados `SUSPEITA` ou `FABRICADA`, escalar o
      `risco_verificacao` da revisão para `alto` e disparar leitura
      humana estratificada da paráfrase (§5.2). A avaliação de promover
      este registro a coluna dedicada da matriz está registrada como
      sugestão em `_phase2-handoff.md §(vi)`.

Exemplar de acionamento — SOARES et al. (2024), Teste 02 da Fase A.7.
A referência é revisão bibliográfica legítima sobre impactos da
pandemia no ensino-aprendizagem na rede básica, com metadados corretos
e paráfrase fiel no parágrafo-semente. Inspeção da lista de
referências internas revelou, entre outras entradas suspeitas, a
referência "ALMEIDA, J., & GOMES, M. (2022). O Impacto da Desigualdade
Digital no Ensino Remoto Durante a Pandemia. Revista Brasileira de
Educação, 27(3), 101-115", confirmada como fabricação em verificação
ativa com três evidências convergentes: formato de numeração
impossível na *Revista Brasileira de Educação* (volume único por ano
desde 2018, fluxo contínuo, identificadores `e270001` etc. — não
existe "v. 27, n. 3" em 2022); zero ocorrências do título na web
fora do próprio artigo de SOARES; iniciais genéricas ("Almeida, J.",
"Gomes, M.") sem correspondência no sumário real da RBE 2022.

Referência cruzada. A pendência arquitetural sobre canonização do
vetor correspondente ("cadeia probatória interna contaminada") está
registrada em `_phase2-handoff.md` §(x), com compromisso de teste
dirigido no Teste 03. A regra operacional deste §5.6 **não depende**
da canonização taxonômica para funcionar — é heurística ativa desde
já, aplicável em todo entregável que cite revisão bibliográfica em
posição de sustentação argumentativa.

### 5.7 Declaração explícita de não-verificação para corpus recomendado

Regra ativa, introduzida pela decisão 24 do `_changelog.md` (A.7 Bloco
B). Quando a skill, em qualquer etapa do entregável, sugerir literatura
adicional **fora do corpus sob análise** — bibliografia complementar,
leituras para aprofundamento, obras sugeridas em seção de "próximos
passos", referências colaterais citadas em resposta a perguntas
específicas do pesquisador —, a sugestão **deve vir acompanhada de
declaração explícita** de que as referências recomendadas não passaram
pelo protocolo de verificação ativa aplicado ao corpus sob análise. A
declaração deve ser textualmente visível (nota, parágrafo de abertura
da seção de sugestões, rodapé), não presumida como contexto.

Formulação canônica sugerida:

> "As referências listadas abaixo são sugestões complementares ao
> corpus fornecido e não passaram pelo protocolo de verificação ativa
> (DOI, indexação, conferência de metadados) aplicado às referências
> do corpus sob análise. Recomenda-se verificação independente antes
> de incorporação ao entregável."

Princípio. A arquitetura da skill opera com distinção estrita entre
corpus verificado e material fora desse escudo. Sugestões
bibliográficas são geradas fora do pipeline de verificação e estão
sujeitas a taxas de fabricação análogas às documentadas em §1 para
literatura não-curada. **Contaminação de contexto** — leitor assumindo
sobre sugestões o mesmo nível de confiança que tem sobre o corpus
verificado — é risco operacional real, que a declaração explícita
endereça.

Exemplar de acionamento. No Teste 02 da Fase A.7, ambos os ambientes
executores produziram seções de "corpus recomendado" com sugestões de
literatura adicional (Betthäuser et al. 2023 no navegador; Lichand et
al. 2022, Senkevics & Bof 2022, entre outros, no Desktop), **sem
declaração explícita de não-verificação**. Fragilidade compartilhada
documentada na síntese comparativa do Teste 02 §4.3 e §6.2.

Articulação com heurísticas adjacentes. §5.7 trata de referências
**fora** do corpus sob análise (sugestões bibliográficas
complementares). §9.5 trata de referências **dentro** do corpus
(DOI de repositórios abertos, verificação ativa com escalonamento
interno). Regimes distintos, complementares no pipeline.

## 6. Matriz de mitigação diferencial

Cada valor terminal da taxonomia v2 é apanhado (ou não) pelas camadas
empilhadas do pipeline. Leia por linha para ver a defesa de cada valor;
leia por coluna para ver a função de cada camada.

A tabela assume pipeline completo com todas as camadas ativas. Se
alguma camada for removida — corpus colado sem Zotero, entrega sem
tempo para revisor cético, matriz de síntese omitida em revisão
curta — a carga de detecção se redistribui para as camadas
restantes, na maior parte das vezes para leitura humana, que é a
camada mais custosa em tempo. Remover camada é escolha legítima sob
prazo, mas deve ser consciente. Use a tabela como instrumento de
decisão, não como descrição estática.

Linhas por valor terminal efetivamente detectável; condicionalidade
da v2 é expressa pela nomenclatura das linhas ("Dim. 2 metadados"
pressupõe Dim. 1 = existente verificável; "Dim. 3 conceitual"
pressupõe Dim. 2 = conteúdo afirmado). Vetor ortogonal (drift
temporal) em linha própria.

| Valor terminal                                 | Zotero SOT | Matriz + `corrente_teorica` | Verbatim lateral | `doi_verify.py` | `bib_consistency.py` | Leitura humana estratificada | Revisor cético | Carimbo de confiança |
|------------------------------------------------|:----------:|:---------------------------:|:----------------:|:---------------:|:--------------------:|:----------------------------:|:--------------:|:--------------------:|
| Dim. 1 pastiche                                | ✓¹         | ✗                           | parcial²         | parcial³        | parcial              | ✓                            | parcial⁴       | ✗                    |
| Dim. 1 inexistente-fabricada                   | ✓¹         | ✗                           | ✓                | ✓               | parcial              | ✓                            | ✓              | ✗                    |
| Dim. 2 metadados                               | parcial⁵   | ✗                           | ✗                | ✓               | ✓                    | parcial                      | parcial        | ✗                    |
| Dim. 2 conteúdo afirmado / Dim. 3 conceitual   | ✗          | ✓                           | parcial⁶         | ✗               | ✗                    | **✓ (terminal)**             | ✓              | ✗                    |
| Dim. 2 conteúdo afirmado / Dim. 3 factual      | ✗          | ✗                           | ✓                | ✗               | ✗                    | **✓ (terminal)**             | parcial⁷       | ✗                    |
| Dim. 2 estrutura de sustentação argumentativa  | ✗          | ✗                           | parcial⁸         | ✗               | ✗                    | parcial                      | parcial        | ✗                    |
| Vetor ortogonal — drift temporal               | ✗          | ✗                           | ✗                | parcial⁹        | ✗                    | parcial                      | ✗              | **✓ (única)**        |

¹ Zotero SOT impede pastiche e inexistente-fabricada na escrita: obra
não existente no corpus curado não tem entrada coerente; o modelo não
tem como redigir a partir dela.
² Verbatim lateral detecta pastiche apenas quando o pesquisador tenta
conferir o trecho e descobre que a combinação de autor + obra não
recupera a passagem — sinal indireto.
³ `doi_verify.py` apanha pastiche quando o DOI resolve para obra
diferente da declarada (CrossRef retorna metadados discrepantes); não
apanha pastiche em que os elementos formam combinação plausível sem
DOI ou com DOI correto mas autor/título de outra obra.
⁴ Revisor cético cobre pastiche com DOI inválido (entra em
PROVAVELMENTE FABRICADA); pastiche com DOI válido mas metadados
combinados de obras distintas exige busca ativa
(`_taxonomy-v2-design.md §7.2`) que a autorrevisão pode ou não
executar.
⁵ Zotero SOT garante metadados corretos para obras já no corpus;
cópia de metadados de fonte externa (colagem manual de PDF, importação
de site do periódico) pode introduzir erro que o Zotero não previne.
⁶ Verbatim lateral ajuda a identificar distorção conceitual grosseira,
mas fidelidade conceitual fina exige releitura interpretativa
(`_taxonomy-v2-design.md §7.5.1`).
⁷ Revisor cético detecta factual apenas se o dado estiver na memória
de trabalho da sessão ou no PDF acessível — raro em workflow padrão.
⁸ Verbatim da fonte mostra o que ela diz; uso argumentativo inadequado
exige leitura contextual do parágrafo citante, não coberta por
verbatim isolado.
⁹ `doi_verify.py` apanha retratação em DOIs via campos `update-to` /
`update-nature` do CrossRef, mas não apanha republicação silenciosa de
documento sem DOI, mudança de status de tramitação em
LexML/Câmara/Senado, nem atualização retroativa de microdado em
DATASUS/IBGE/RAIS.

Cinco leituras críticas:

1. **Leitura humana estratificada é a camada terminal contra Dim. 2
   conteúdo afirmado** (conceitual e factual). Revisor cético é defesa
   intermediária, com cobertura parcial em factual dependente de dado
   em memória de trabalho. Script algum apanha distorção em
   obra-autor reais; a fronteira é estrutural, não tecnológica.
2. **Scripts (`doi_verify.py`, `bib_consistency.py`) são fortes em
   Dim. 1 e Dim. 2 metadados, cegos para Dim. 2 conteúdo afirmado e
   Dim. 2 estrutura de sustentação.** Essa é a fronteira estrutural
   do que a automação pode fazer.
3. **Dim. 2 conteúdo afirmado com Dim. 3 conceitual — incluindo
   casos de conflação entre correntes teóricas divergentes —
   previne-se estruturalmente, não se detecta posteriormente.** A
   coluna `corrente_teorica` na matriz de síntese obriga a
   diferenciação antes da prosa. Quando a conflação entra na prosa,
   a remediação passa obrigatoriamente por leitura humana e por
   revisor cético.
4. **Dim. 2 estrutura de sustentação argumentativa não tem camada
   dedicada;** cobertura transversal parcial via regra 5 do SKILL.md
   (prosa argumentativa) e autorrevisão cética no fluxo obrigatório.
   Candidatura a regra dedicada registrada em `_phase2-handoff.md
   §(viii)`.
5. **Vetor ortogonal — drift temporal — cobre-se exclusivamente por
   carimbo de confiança com reverificação pré-submissão.** Fora do
   escopo da v2, dentro do escopo operacional da skill.

## 7. Red flags — padrões que disparam abort-and-verify imediato

Os padrões abaixo são sinais operacionais de que algo provavelmente
está errado — não prova, mas gatilho suficiente para interromper a
geração ou a leitura e verificar antes de prosseguir.

**(i)** DOI com padrão suspeito (sufixo curto demais, prefixo
inconsistente com o periódico alegado, sequência repetida entre DOIs
supostamente distintos).

**(ii)** Citação sem chave BibTeX correspondente no corpus fornecido —
a chave foi produzida, não recuperada.

**(iii)** Paráfrase de autor cuja obra citada está ausente do corpus
(embora outras obras do mesmo autor possam estar presentes — a intrusão
se aproveita da plausibilidade do sobrenome).

**(iv)** Autor com sobrenome comum (Silva, Souza, Santos, Oliveira,
Costa etc.) sem ORCID, afiliação institucional ou coautor na matriz
que permita desambiguação.

**(v)** Citação em série sem tensão argumentativa: *"A, B, C e D
mostram que…"* em vez de agrupamento por posição no debate com
contraste explícito.

**(vi)** Paráfrase que agrega correntes teóricas divergentes sem
marcador de contraste — sinal de Dim. 2 conteúdo afirmado + Dim. 3
conceitual (`_taxonomy-v2-design.md §5`).

**(vii)** Uso de `[GENERAL KNOWLEDGE]` para estatística específica,
data específica, nome próprio ou paráfrase de obra identificável.

**(viii)** Mudança abrupta de registro entre parágrafos — um parágrafo
em prosa argumentativa ancorada em evidência, o seguinte em prosa
genérica e ornamental. Sinal de que a geração alternou entre paráfrase
do corpus e preenchimento retórico produzido de memória. O parágrafo
ornamental precisa ser tratado como suspeito até conferência.

**(ix)** Frase que soa boa demais para ser paráfrase — formulação
polida em excesso, paralelismo sintático perfeito, simetria elegante,
aforismo. Paráfrase autêntica de fonte científica raramente é
esteticamente lisa; texto acadêmico carrega as rugosidades do argumento
que o gerou. Formulação polida demais é, com frequência, reformulação
de memória apresentada como paráfrase. Red flag linguístico mais
difícil de aplicar com precisão, mas genuíno — quando o pesquisador se
pegar admirando a beleza da frase, desconfiar.

**(x)** Citação "pós-racionalizada": chave de citação anexada ao final
de frase visivelmente escrita antes, sem verbatim lateral, sem gancho
específico para o trecho citado. Wallat et al. 2024 documentam até
57% de pós-racionalização mesmo com RAG — quando presente, tende a
aparecer junto com vários outros red flags desta lista.

Meta-observação: o item (ix) advoga contra prosa polida mas é, ele
mesmo, formulado com polidez — é argumento sobre paráfrase, não
paráfrase. A regra que decorre: não suavizar prosa correta para
parecer que passou pelo crivo estético; o teste é a proveniência, não
a estética. Texto rugoso ancorado em fonte é preferível a texto
elegante sem ancoragem.

## 8. Heurísticas editoriais adjacentes à v2

Seção de padrões detectáveis no texto que o pesquisador pode querer
endereçar em revisão final, mas que **não integram o sistema
dimensional v2**. Distinguem-se das red flags de §7 por dois
critérios: não disparam abort-and-verify imediato (são orientação de
revisão editorial, não gatilho de interrupção); e estão explicitamente
fora do escopo taxonômico da skill, por cruzarem a cláusula de
fronteira da Dim. 2 estrutura de sustentação argumentativa
(`_taxonomy-v2-design.md` §8.6) — a v2 é instrumento de detecção de
alucinação e distorção bibliográfica, não de crítica retórica ou
argumentativa genérica.

Estatuto operacional. Heurísticas adjacentes podem ser aplicadas
pelo revisor cético (§5.4) como observações complementares ao
relatório estruturado, sem peso de veredicto dimensional. Seu
registro aqui preserva o valor editorial do padrão sem comprometer a
arquitetura taxonômica da v2. Entradas adicionais podem ser
acrescentadas no futuro; canonização de qualquer delas como variante
v2 só ocorre se atender ao gate de reabertura descrito em
`_taxonomy-v2-design.md` §8.6.

### 8.1 Inflação retórica de certeza

Descrição. Uso de marcadores linguísticos de alta certeza — "consenso
acadêmico", "a literatura converge", "evidências inequívocas",
"está estabelecido que" — sem que a **forma de evidência** mobilizada
(revisão sistemática, meta-análise, estudo controlado de grande
escala) justifique o grau de certeza invocado. A prosa veicula grau de
confiança superior ao que o tipo de fonte sustenta.

Acionamento. Paráfrases apoiadas em revisões narrativas, reflexões
qualitativas, estudos de caso ou pesquisas exploratórias redigidas
com marcadores de consenso acadêmico. A detecção exige leitura
contextual do parágrafo citante contra o gênero bibliográfico das
fontes agregadas.

Ação editorial sugerida. Rebaixar o registro retórico ao nível de
certeza que o tipo de fonte sustenta ("estudos exploratórios sugerem",
"análises qualitativas indicam", "evidência preliminar aponta") ou
substituir fontes para cobrir a afirmação no grau de certeza
pretendido.

Status declarado. Orientação crítica adjacente à skill, **fora do
sistema dimensional v2**. Cruza a cláusula de fronteira de
`_taxonomy-v2-design.md` §8.6 (é crítica de estilo epistêmico, não
descompasso detectável entre o que o texto diz sobre as fontes e o
que as fontes mostram). Registrada como heurística editorial após
proposta do Desktop no Teste 02 da Fase A.7, sem convergência
independente em ambiente distinto — ver `_changelog.md` decisão 20.

### 8.2 Conclusão normativa passando como síntese científica

Descrição. Uso da estrutura retórica de revisão de literatura para
veicular conclusão normativa — "exige políticas públicas robustas",
"é imperativo que", "demanda ação urgente" —, operando como *slippage*
deôntico-descritivo: a conclusão prescritiva aparece como se fosse
implicação direta da síntese das evidências, sem demarcação explícita
da passagem entre descrever o que as fontes mostram e recomendar o
que se deve fazer a partir daí.

Acionamento. Parágrafos de síntese ou fechamento de seção em que o
verbo principal migra de descritivo ("a literatura indica que X") para
prescritivo ("é preciso Y") sem marcador de transição
(recomendação, posicionamento do autor, implicação prescritiva
declarada). Mais frequente em conclusões e em seções de implicações
em relatórios técnicos e revisões com escopo aplicado.

Ação editorial sugerida. Demarcar explicitamente a passagem do plano
descritivo para o prescritivo — por marcador textual
("a partir dessas evidências, argumentamos que…", "implicação
prescritiva: …") ou por separação estrutural (parágrafo de síntese
descritiva seguido de parágrafo de recomendação declarada). Alternativa:
manter apenas o plano descritivo na seção de revisão e deslocar a
conclusão normativa para seção própria (Recomendações, Discussão,
Implicações).

Status declarado. Orientação crítica adjacente à skill, **fora do
sistema dimensional v2**. Cruza a cláusula de fronteira de
`_taxonomy-v2-design.md` §8.6 (é crítica de argumentação normativa, não
descompasso entre o que o texto diz sobre as fontes e o que as fontes
mostram). Registrada como heurística editorial após proposta do
Desktop no Teste 02 da Fase A.7, sem convergência independente em
ambiente distinto — ver `_changelog.md` decisão 20.

## 9. Heurísticas de busca e prospecção em fontes brasileiras

Seção introduzida pela decisão 24 do `_changelog.md` (A.7 Bloco B),
incorporando cinco heurísticas cujo gatilho empírico consolidou-se no
Teste 02 da Fase A.7 — notadamente nos casos CARDOSO; BERTONI e
MAGALHÃES; ROCHA, ambos falsos positivos convergentes de pastiche em
dois ambientes executores por fechamento prematuro da busca sem
prospecção de portais institucionais brasileiros. Diferente da §8 (que
agrupa heurísticas editoriais adjacentes à v2), esta §9 reúne **regras
ativas**, aplicáveis durante a verificação de Dim. 1 (Existência) e de
Dim. 2 metadados. Ordem interna por função operacional: §9.1 bloqueia
argumento errôneo antes das demais; §9.2 manda prospectar o portal
institucional; §9.3 regra o desempate quando a prospecção é
inconclusiva; §9.4 trata do campo "ano" uma vez alcançado o OJS; §9.5
trata de DOI de repositórios abertos.

### 9.1 Desalinhamento agenda-tema não é evidência contra existência

Regra. Desalinhamento entre agenda histórica de pesquisa dos autores
(linha de publicação identificável em Lattes, ORCID, perfis acadêmicos
ou produção anterior) e o tema declarado da referência em causa
**não constitui evidência contra existência**. Não pode figurar,
isolado ou em composição com não-localização em bases, como base para
classificação em pastiche ou inexistente-fabricada.

Fundamentos. A agenda de um autor acadêmico não é propriedade fixa nem
transitiva para todo trabalho em que a pessoa aparece. Três
configurações regulares produzem desalinhamento legítimo:

- **Co-autoria com orientando.** O tema é predominantemente do
  orientando; o orientador supervisiona a elaboração metodológica sem
  necessariamente partilhar da mesma agenda substantiva.
- **Incursão temática em períodos de interesse coletivo.** Pandemias,
  crises ambientais, transformações políticas mobilizam pesquisadores
  de áreas adjacentes a publicar sobre o interesse coletivo, fora da
  agenda principal.
- **Docência em programas interdisciplinares ou em rede.** Programas
  que reúnem pesquisadores de áreas distintas em torno de objeto comum
  (ProfEPT, PPGEH, programas multicêntricos de saúde pública) produzem
  publicações cujo tema diverge da agenda original.

Caso canônico — anais de iniciação científica. Em anais de IC, o tema
é escolhido pelo bolsista com autonomia relativa; o orientador figura
como supervisor acadêmico, não como co-proponente do tema. O
desalinhamento entre agenda histórica do orientador e tema do trabalho
de IC é padrão regular, não anômalo.

Exemplares empíricos no Teste 02 da Fase A.7:

- **CARDOSO; BERTONI** — anais do Seminário de Iniciação Científica
  da UESB. Agenda histórica das orientadoras em áreas distintas do
  impacto da pandemia na aprendizagem. Ambos os ambientes do Papel 2
  usaram a incongruência de agenda como argumento auxiliar para
  classificação errada de pastiche. Referência é existente verificável
  (ground truth v1.5).
- **MAGALHÃES; ROCHA** — *Revista Encontros* (Colégio Pedro II),
  co-autoria orientadora–orientanda em ProfEPT. Agenda histórica de
  Rodrigo César Magalhães em história das políticas de saúde,
  evidenciada por publicação adjacente em *Manguinhos* 2021. Ambos os
  ambientes inferiram incongruência de agenda, sustentando
  classificação errada de pastiche. Referência é existente verificável
  (ground truth v1.5; ver decisão 23 do `_changelog.md`).

Precisão operacional. A regra proíbe o uso de desalinhamento de agenda
como argumento **contra existência**. Não proíbe o uso de agenda como
informação diagnóstica em geral: confirmação de existência via
Lattes/ORCID permanece legítima; composição improvável de autor +
veículo + tema pode continuar informando suspeita de pastiche quando
combinada com outros sinais e desde que a etapa de prospecção
institucional de §9.2 tenha sido executada.

### 9.2 Prospecção obrigatória em portais institucionais

Gatilho. Quando o campo de veículo/tipo de publicação da referência
mencionar explicitamente "Anais", "Seminário", "Congresso", "Encontro",
"Jornada", "Simpósio", "Colóquio", "Conferência", "Fórum", "Reunião
Anual" ou equivalentes, a verificação **deve** incluir prospecção do
portal institucional da universidade, entidade organizadora, sociedade
científica ou órgão público responsável pelo evento. Formas típicas de
portal institucional incluem, sem esgotar: OJS dedicado a anais do
evento, repositório institucional (DSpace), página do evento no site
da entidade, portal de publicações da sociedade científica.

Exceção ao gatilho. O gatilho não incide quando "Anais" ou termo
equivalente figura como nome de periódico em fluxo regular com DOI
CrossRef/SciELO (ex.: *Anais da Academia Brasileira de Ciências*,
*Anais Brasileiros de Dermatologia*). Nesses casos, a referência é
periódico comum e segue fluxo normal de verificação.

Princípio lógico subjacente. Não-localização em CrossRef, OpenAlex ou
buscadores gerais **não equivale** a não-existência. A produção
acadêmica brasileira em literatura cinzenta e semi-cinzenta (anais de
eventos universitários, publicações de fundações estaduais,
dissertações em repositórios institucionais) está estruturalmente
sub-representada nessas bases. Concluir pastiche ou inexistente-
fabricada a partir de amostra enviesada é erro lógico antes de ser
erro bibliográfico.

Exemplares canônicos no Teste 02 da Fase A.7:

- **CARDOSO; BERTONI** — OJS do Seminário de Iniciação Científica e
  Tecnológica da UESB (`anais2.uesb.br/index.php/semicit`). Dois
  ambientes classificaram como pastiche por não-localização em
  CrossRef/OpenAlex/web, sem prospectar o OJS institucional.
- **MAGALHÃES; ROCHA** — OJS Portal Espiral do Colégio Pedro II
  (`portalespiral.cp2.g12.br`). Dois ambientes classificaram como
  pastiche sem prospectar o OJS institucional; a referência é
  existente verificável (ver decisão 23 do `_changelog.md`).

Articulação com heurísticas adjacentes. Uma vez alcançado o portal
institucional, aplicar §9.4 (distinção ano do volume vs. data OJS)
para leitura correta do campo "ano".

### 9.3 Regra de desempate em "indeterminada" diante de alcance limitado

Regra. Durante a verificação de Dim. 1 (Existência), quando a busca
ativa não localiza a referência como unidade bibliográfica e,
simultaneamente, pelo menos **duas das três** evidências abaixo estão
presentes:

- par autoral real (autores identificáveis em perfis Lattes, ORCID,
  repositórios institucionais, redes acadêmicas);
- evento real (seminário, congresso, encontro efetivamente realizado
  pela entidade mencionada, com data e edição compatíveis);
- veículo real (periódico existente com numeração plausível, OJS
  ativo; ou série editorial institucional com volumes localizáveis).

A classificação em Dim. 1 **deve suspender o veredito**, registrando
"classificação suspensa — bases consultadas e evidências parciais
documentadas" com registro explícito das bases verificadas (mínimo:
CrossRef, OpenAlex, OJS institucional quando aplicável por §9.2,
buscador geral). A classificação **não fecha** em pastiche nem em
inexistente-fabricada nessas condições.

Critério de "não fechamento como unidade bibliográfica". Fechamento
significa acesso à obra ou a metadados completos na página canônica do
portal institucional (OJS, repositório, anais). Confirmação isolada de
componentes separados (só autores, só evento, só veículo) não
constitui fechamento.

Estatuto da suspensão. A taxonomia v2 prevê três valores canônicos em
Dim. 1 (existente verificável, pastiche, inexistente-fabricada). A
suspensão operada por esta heurística é **prática editorial da skill**:
registra-se suspensão motivada do julgamento enquanto a busca não
conclui, sem comprometer compromisso taxonômico com uma quarta classe.
A avaliação sobre se a suspensão merece reconhecimento taxonômico
formal está registrada como pendência em `_phase2-handoff.md §(xiv)`.

Princípio lógico subjacente. Não-localização em amostra de bases não
equivale a não-existência. A produção acadêmica brasileira em
literatura cinzenta e semi-cinzenta está estruturalmente sub-
representada em bases agregadoras internacionais; alcance limitado de
busca é a regra, não a exceção. A prova de inexistência é mais
exigente do que a prova de existência.

Exemplares canônicos no Teste 02 da Fase A.7:

- **CARDOSO; BERTONI** — par autoral real + evento real (XXIX
  Seminário de Iniciação Científica e Tecnológica da UESB). Dois dos
  três gatilhos acionam. Referência é existente verificável (ground
  truth v1.5).
- **MAGALHÃES; ROCHA** — par autoral real + veículo real (*Revista
  Encontros*, CP2, numeração bianual consistente). Dois dos três
  gatilhos acionam. Referência é existente verificável (ground truth
  v1.5).

Articulação com heurísticas adjacentes. A regra se aplica **depois**
de §9.2 (prospecção obrigatória em portais institucionais). Se, após
§9.2 executada, a referência ainda não fechar como unidade
bibliográfica, suspensão do veredito é o tratamento correto — não
pastiche por não-localização ampliada.

### 9.4 Ano do volume vs. data OJS vs. ano do evento

Fundamento normativo. Pela ABNT NBR 6023:2018, o campo "ano" da
referência recebe o **ano do volume / ano de publicação da obra**, não
a data de publicação efetiva do OJS, nem o ano do evento em que o
trabalho foi apresentado. Em estilos APA e Vancouver a regra é
análoga, com convenções de apresentação diferentes.

Fenômeno editorial frequente no Brasil. Em publicações institucionais
brasileiras — INEP, IPEA, FGV, FIOCRUZ, fundações estaduais de
pesquisa, LexML, anais de eventos universitários em OJS — é prática
comum o volume ser datado de um ano (ou o evento ocorrer em um ano) e
a publicação efetiva no OJS se dar em janeiro do ano seguinte. As três
datas coexistem no OJS e precisam ser distinguidas antes de avaliar o
campo "ano" da referência.

Risco na direção A — falso positivo em Dim. 2 metadados. Tratar a data
OJS como "erro de ano" da referência quando o volume é designado com
ano anterior produz falso positivo: identifica fato editorial real mas
aplica enquadramento errado. Exemplar canônico: BOF; MORAES (2022),
*Cadernos de Estudos e Pesquisas em Políticas Educacionais* (INEP),
volume "v. 7 (2022)" com publicação OJS "02-01-2023" (Teste 02 da
Fase A.7; falso positivo do Claude.ai navegador).

Risco na direção B — subdimensionamento. Não alcançar o OJS
institucional e, ao fechar a referência em outra classificação
(tipicamente pastiche em Dim. 1), perder erro real em que o ano do
evento foi registrado no lugar do ano de publicação dos anais.
Exemplar complementar: CARDOSO; BERTONI, anais do Seminário de
Iniciação Científica e Tecnológica da UESB — evento em 2025, anais
publicados em 2026 (ABNT canônico = 2026); ChatGPT registrou 2025;
ambos os ambientes do Papel 2 fecharam prematuramente em pastiche sem
prospecção no OJS da UESB. O mecanismo pelo qual 2025 entrou na
referência (confusão entre ano do evento e ano dos anais) é inferido,
não documentado.

Operacionalização. **Antes de registrar erro de ano em Dim. 2
metadados ou fechar uma referência a publicação institucional em
pastiche/inexistente-fabricada**, consultar o OJS institucional (não
apenas CrossRef, OpenAlex ou buscadores gerais) e identificar, na
página canônica do OJS, qual das três datas é o ano do volume /
publicação. Este é o ano ABNT. A comparação com o campo "ano" da
referência do texto citante tem que ser feita contra esse ano, não
contra a data OJS nem contra o ano do evento.

### 9.5 DOI de repositórios abertos sem revisão por pares

Gatilho. Referências com DOI cujo prefixo identifica repositório aberto
sem revisão por pares — notadamente Zenodo (`10.5281/zenodo.`),
Figshare, OSF (`10.17605/OSF.IO/`) e repositórios institucionais
genéricos. Esses repositórios emitem DOI para qualquer depósito
(artigo, dataset, apresentação, preprint, versão auto-arquivada) sem
filtro editorial.

Princípio. Resolução do DOI confirma apenas que o **depósito** existe.
Não informa sobre o **status editorial** do conteúdo hospedado. Dois
trabalhos com DOI Zenodo podem ter trajetórias editoriais totalmente
distintas: um pode ser artigo em periódico legítimo que usa Zenodo
como hospedagem; outro pode ser auto-depósito individual sem revisão
por pares.

Verificação adicional requerida. Quando o DOI é de repositório aberto,
verificar a indexação do veículo hospedado em base reconhecida (SciELO,
LILACS, DOAJ, Qualis CAPES, ou plataforma específica do domínio). Se o
veículo é periódico indexado, a referência passa pelo fluxo normal. Se
não é, a referência deve ser tratada como **material não-revisado por
pares**, com implicações correspondentes:

- escalar `risco_verificacao` da matriz para `alto`;
- disparar leitura humana estratificada da paráfrase (§5.2);
- registrar estatuto editorial na coluna de observações da matriz.

Exemplar de acionamento. FUZZO et al. (2024), *RevistaFT* 28(135), DOI
`10.5281/zenodo.11664323`. Verificação positiva: *RevistaFT* tem ISSN
1678-0817 e é periódico legítimo que usa Zenodo como plataforma de
hospedagem. Teste 02 da Fase A.7 — caso em que a heurística passa sem
acionar alarme, exemplar de funcionamento normal.

Articulação com heurísticas adjacentes. §9.5 trata de referências
**dentro** do corpus sob análise (verificação ativa). §5.7 (declaração
de não-verificação para corpus recomendado) trata de referências **fora**
do corpus (sugestões bibliográficas complementares). Regimes distintos.
