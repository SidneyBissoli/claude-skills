# Taxonomia de erros bibliográficos — desenho operacional (v2)

**Versão**: v2 (tridimensional hierárquica condicional).
**Data**: 2026-04-20.
**Manuscrito-fonte**:
`<pasta-de-referencias>/skill-development/research/fase-A1-manuscrito-taxonomia-v2.md`.
**Estado**: substitui a taxonomia v1 de cinco modos (a)–(e). Arquivos
operacionais da skill foram refatorados contra esta v2 nas fases
A.2, A.3 e A.4 do roadmap; vocabulário v1 preservado deliberadamente
em `_changelog.md` decisões 1 e 18 (registro histórico e tabela de
remapeamento) e em §9 deste arquivo (reclassificação dos oito casos
do teste 01). Ver `_changelog.md` para estado corrente.

## 0. Como usar este documento

Este arquivo define a taxonomia contra a qual erros em referências
bibliográficas são classificados durante a geração e a revisão de
revisões de literatura assistidas. É consultado **uma vez no início da
sessão**, junto com `hallucination-prevention-checklist.md`, e
revisitado seletivamente durante verificação ativa, autorrevisão
cética (passo 8 do fluxo obrigatório do `SKILL.md`) e
composição de parecer diagnóstico.

Consulta seletiva, não integral:

- §1 para filiação teórica (a declarar ao pesquisador quando relevante).
- §2 para o princípio de desenho e a regra de decisão para extensões.
- §3–§5 para as três dimensões, na ordem em que são aplicadas.
- §6 para a árvore decisória.
- §7 para o protocolo de verificação — a seção que transforma a
  taxonomia em ação. Em modo diagnóstico, a exteriorização do
  vocabulário v2 no output do parecer segue D1–D3 da seção "Regras
  de exteriorização dimensional em modo diagnóstico" do `SKILL.md`.
- §8 para casos limítrofes, regras de desempate, variantes nomeadas
  de Dim. 2 sustentação (§8.6) e subtipos formais de Dim. 1 (§8.7).
- §9 para consulta rápida da reclassificação dos oito casos do teste
  01.
- §10 e §11 para limitações e eixos descartados.

**Nota sobre vocabulário residual.** Arquivos operacionais da skill
foram refatorados contra esta v2 (ver `_changelog.md` para estado).
Onde surgir referência ao vocabulário v1 — como registro histórico em
`_changelog.md` decisões 1 e 18, §9 deste arquivo, ou material externo
pré-refatoração — o mapeamento mínimo é: (a) erros menores → Dim. 1
existente verificável + Dim. 2 metadados; (b) fabricação total →
Dim. 1 inexistente/fabricada *ou* pastiche, conforme §8.1;
(c) conteúdo distorcido → Dim. 2 conteúdo afirmado, com Dim. 3
aplicada; (d) conflação teórica v1 bifurca na v2 conforme a natureza
do erro — se o erro é **conceitual** (conceito, enquadramento ou
tradição atribuído incorretamente a fonte existente), classifica-se
como Dim. 2 conteúdo afirmado + Dim. 3 conceitual; se o erro é
**bibliográfico** (elementos de obras distintas do mesmo autor
combinados em ficha sem unidade), classifica-se como Dim. 1 pastiche
intra-autoral, conforme §8.2; (e) drift temporal → vetor ortogonal,
não coberto pela v2 (defesa permanece em
`hallucination-prevention-checklist.md` §3, carimbo de confiança).

## 1. Filiação teórica

A estrutura genérica de uma taxonomia com eixo descritivo de objeto
cruzado com eixo ortogonal é herança direta da tradição bibliométrica
biomédica — Doms (1989), De Lacey, Record e Wade (1985), Fenton et al.
(2000), Lukić et al. (2004). A categoria **pastiche** é contribuição
nominal e conceitual de McGowan et al. (2023), incorporada aqui como
valor intermediário da Dimensão 1. A subdistinção entre **pastiche
puro** e **pastiche intra-autoral** (§8.2) é contribuição específica
deste projeto, introduzida para orientar correção diferenciada: no
intra-autoral, costuma haver obra real recuperável pelo autor mais
tema mais janela temporal, e a correção pode substituir o pastiche
por essa obra real; no puro, a correção exige substituição integral.
A proposta específica da v2 — seleção de três dimensões, regra de
articulação hierárquica condicional, princípio pragmático de desenho —
foi esboçada por Claude (Anthropic) no contexto do projeto
`literature-review-academic-ptbr`. As decisões de escopo — inclusão da
dimensão Existência em resposta ao fenômeno pós-LLM, inclusão da
dimensão Natureza para orientar verificação diferenciada em erros de
conteúdo, exclusão de Grau, Consequência argumentativa e Cascatas
sistêmicas, adoção da ABNT, manutenção enxuta em três dimensões —
foram tomadas por Sidney Bissoli, designer do projeto. Desenvolvimento
completo no manuscrito-fonte.

## 2. Princípio de desenho

### 2.1 Proporcionalidade pragmática

Eixo só entra na taxonomia se o ganho de informação excede o custo de
classificação. A economia da v2 vem de duas escolhas estruturais
combinadas: reduzir o número de eixos (três, não cinco ou sete) e
aplicar os eixos de forma hierárquica condicional. A classificação
completa das três dimensões é aplicada apenas ao subconjunto
analiticamente mais rico — erros em conteúdo atribuído a referências
que existem —, enquanto casos mais simples terminam em uma ou duas
dimensões. Isso preserva granularidade fina onde o ganho justifica o
custo, sem impor custo uniforme.

### 2.2 Regra de decisão para extensões futuras

Eixo candidato a entrar na taxonomia precisa atender, cumulativamente,
aos quatro critérios a seguir:

- **(a) Ganho demonstrável**: dados empíricos indicam redução de erro
  ou aumento de acerto atribuível ao eixo.
- **(b) Custo compatível**: classificação do eixo cabe no tempo
  disponível por referência, sem comprometer cobertura.
- **(c) Não redundância**: o eixo distingue casos que as dimensões já
  presentes colapsam.
- **(d) Orientação corretiva distinta**: o eixo produz ação diferente,
  não apenas rótulo descritivo diferente.

Os três eixos listados em §11 foram examinados e falharam em ao menos
um desses critérios. A Dimensão 3 (Natureza) passou nos quatro.

## 3. Dimensão 1 — Existência

**Aplica-se sempre, a toda referência.** Avalia se a referência tem
correspondente real no mundo bibliográfico. Três valores.

### Existente verificável

A referência corresponde a obra real e única, recuperável por
identificador estável (DOI, PMID, ISBN) ou — na ausência destes —
pela combinação de autor, ano, título e periódico/editora via busca
em bases bibliográficas. Pequenos erros de metadados **não**
desqualificam a referência como existente; a questão é se o referente
pode ser localizado.

Exemplos do teste 01:

- Abd-Alrazaq et al. 2020 — DOI resolve; metadados conferem
  integralmente.
- Fitzpatrick, Darcy e Vierhile 2017 — obra real; erro localizado
  depois em metadado da ficha (ver §4).
- WHO 2021 — documento real; erros em informações secundárias de
  editora/coleção.

### Pastiche

A referência é plausível em aparência, mas nenhum conjunto único de
metadados completos corresponde a obra real. Os elementos — autor(es),
fragmentos de título, periódico, ano — derivam de múltiplas obras
reais combinadas probabilisticamente, sem unidade bibliográfica
subjacente. Cinco marcadores operacionais (McGowan et al. 2023):
(a) autor(es) reais e ativos no tema; (b) periódico real e
tematicamente pertinente; (c) título plausível; (d) combinação
específica não recuperável; (e) elementos individuais rastreáveis a
obras distintas.

Exemplos do teste 01:

- Provoost et al. 2021 — pastiche intra-autoral: obra real de 2017 do
  mesmo autor com ano, volume, número e DOI transplantados de Xu et
  al. 2021.
- Topol 2020 — pastiche intra-autoral: título do livro *Deep Medicine*
  de 2019 combinado com DOI do artigo "High-performance medicine" de
  2019, mesmo autor.

Distinção pastiche puro × intra-autoral em §8.2.

### Inexistente/fabricada

A referência não corresponde a obra alguma e não apresenta estrutura
de pastiche. Autores podem ser inventados, periódicos podem ser
inventados, ou a combinação é inteiramente arbitrária. Quando há
identificador, ele é não resolvível ou aponta para obra completamente
não relacionada, e buscas por autor + título + periódico não retornam
obra localizável.

Exemplos do teste 01:

- Bickmore, Trinh e Asadi 2021 — DOI pertence a Selvanathan e Jetten
  2020; artigo sobre agentes conversacionais em saúde mental não
  localizado em busca ativa.
- Lim et al. 2022 — DOI pertence a Maurits et al. 2022 sobre EHRs;
  artigo declarado não existe.
- Mathur et al. 2023 — DOI 404; periódico declarado inexistente com
  esse nome exato.

## 4. Dimensão 2 — Objeto do erro

**Aplica-se apenas quando Dimensão 1 = existente verificável.**
Pastiche e inexistente/fabricada esvaziam a pergunta sobre localização
do erro: no pastiche, o erro é de unidade ontológica; na fabricação,
não há objeto sobre o qual erro localizado seria definido.

Três valores. Os exemplos para **conteúdo afirmado** e para
**estrutura de sustentação argumentativa** abaixo são **construídos**,
não empíricos do teste 01 — o perfil de erros do parágrafo-teste
concentrou-se em Existência e Metadados e não produziu casos que
acionem essas duas categorias. A cobertura empírica delas depende do
teste 02, em planejamento.

### Metadados bibliográficos

Erro em elementos da ficha: autoria (nome trocado, omissão de coautor,
ordem errada), ano, título (palavra trocada, subtítulo omitido,
tradução imprecisa), periódico, volume, fascículo, páginas, DOI,
edição, editora, local, tradutor, organizador. O conteúdo afirmado no
texto citante pode ser fiel à obra; apenas a ficha está comprometida.

Exemplos do teste 01:

- Fitzpatrick et al. 2017 — terceira autora é Vierhile, não Viera;
  subtítulo ": A Randomized Controlled Trial" omitido.
- WHO 2021 — divergências menores em editora/coleção.

### Conteúdo afirmado

Erro nas proposições atribuídas à fonte. A obra existe, os metadados
podem estar corretos, mas o texto citante lhe atribui afirmação que a
obra não contém ou que contém em sentido diverso — inversão de
polaridade, supergeneralização, descontextualização, simplificação
distorcida, conflação com posição de outro autor.

Exemplos construídos:

- Paráfrase afirma que a fonte X demonstrou "redução de 40% em
  sintomas depressivos"; o abstract reporta redução de 40% em
  *ansiedade*, não em depressão (supergeneralização com troca de
  desfecho).
- Paráfrase atribui a Connell o conceito de "masculinidade tóxica"; a
  autora propõe "masculinidade hegemônica", conceito teoricamente
  distinto — ver §5.

### Estrutura de sustentação argumentativa

Erro no modo de mobilização retórica. A obra existe, os metadados
conferem, o conteúdo citado é fiel, mas a função argumentativa da
referência no texto é inadequada.

Exemplos construídos:

- Fonte conceitual (ensaio teórico) invocada para sustentar afirmação
  empírica específica sobre prevalência.
- Revisão crítica invocada afirmativamente, sem registrar que a
  revisão é justamente a que desafia a afirmação (cf. LETRUD;
  HERNES, 2019).
- Resultado preliminar (N pequeno, estudo-piloto) invocado como
  evidência definitiva.
- Estudo em amostra específica (p. ex., universitários de um único
  campus) invocado como evidência populacional geral.

Para variantes formalmente nomeadas desta dimensão — com regra de
desempate, cláusula de fronteira externa à v2 e exemplares canônicos
detalhados — ver §8.6.

## 5. Dimensão 3 — Natureza do erro

**Aplica-se apenas quando Dimensão 2 = conteúdo afirmado.** Erros em
metadados ou em estrutura de sustentação não acionam essa distinção.

A Dim. 3 orienta **tipo de verificação e de ação corretiva**, não
descrição cosmética. Dois valores.

**Pergunta operacional — eixo de distinção.** A distorção é sobre o
que a obra **diz/argumenta** (posições, conceitos, arcabouços teóricos
atribuídos) ou sobre o que a obra **mediu/observou/descreveu**
(metodologia, escopo, população, tipo de achado)? Se é sobre o que a
obra diz → **conceitual**. Se é sobre o que a obra mediu ou observou
→ **factual**.

### Conceitual

O que foi distorcido é atribuição teórica, conceito, enquadramento ou
invocação de tradição. A fonte propõe (ou é reconhecida por propor) o
conceito X, a doutrina Y, o enquadramento Z; o texto citante
atribui-lhe conceito X', doutrina Y', enquadramento Z' — correlatos
mas teoricamente distintos, com implicações analíticas divergentes.

- Verificação: **releitura interpretativa** da fonte e comparação
  conceitual fina; consultar, quando houver, módulo apropriado de
  `references/domain-*/theoretical-currents-*.md`.
- Ação corretiva: reformulação teórica da paráfrase ou substituição da
  referência por fonte que efetivamente sustente a atribuição feita.
- Exemplar canônico — conflação Bourdieu/Foucault sobre poder,
  Direção 1 (atribuir a Bourdieu posição foucaultiana). Texto citante
  atribui a Bourdieu enquadramento foucaultiano — por exemplo,
  paráfrase do tipo *"Bourdieu mostra que o poder opera através da
  produção de corpos dóceis e de dispositivos de governamentalidade"*.
  A atribuição é incongruente: Bourdieu teoriza poder via **campo,
  *habitus* e capital** (estruturas relacionais objetivas e
  disposições incorporadas), não via dispositivos disciplinares nem
  via biopolítica. O mecanismo da conflação é adoção do vocabulário
  foucaultiano como *lingua franca* em teoria social brasileira e
  extensão indevida ao sociólogo "equivalente" — instância direta do
  padrão descrito na heurística anti-padrão da subseção de refinamento
  operacional abaixo (gravitação para o valor conceitual mais
  prestigiado). Direção inversa (atribuir a Foucault posição
  bourdieusiana) é possível, porém de frequência empírica menor.
  Outros exemplares: citar Connell para sustentar "masculinidade
  tóxica" quando a autora propõe "masculinidade hegemônica"; citar
  Bardin para sustentar procedimento de análise temática reflexiva
  (Braun e Clarke).

### Factual

O que foi distorcido é dado empírico específico — taxa, valor
numérico, data, amostra, achado concreto. A fonte reporta número ou
fato verificável; o texto citante lhe atribui número ou fato distinto.

- Verificação: **confronto numérico ou documental** contra tabela do
  artigo, figura, seção de resultados; abstract como recurso rápido,
  mas não suficiente em casos críticos.
- Ação corretiva: substituição do dado ou reformulação da afirmação
  para refletir o valor real.
- Exemplar canônico — DANTAS et al. (2024), Teste 02 da Fase A.7.
  O artigo é reflexão teórica qualitativa sobre impactos da pandemia
  de covid-19 na educação, baseado em impressões de familiares e
  professores e em entrevistas/análise de TCCs de pós e graduação,
  cobrindo Educação Básica ao Ensino Superior no Distrito Federal. O
  parágrafo-semente do Teste 02 atribui ao artigo achados empíricos
  sobre "lacunas em competências fundamentais como leitura e
  matemática" entre estudantes do Ensino Médio público brasileiro em
  âmbito nacional. A distorção é sobre **o que a obra mediu/observou**:
  a obra não mede competências, não avalia aprendizagem empiricamente,
  não trata de Ensino Médio público em âmbito nacional. Classificação:
  Dim. 3 factual. Outros exemplares: paráfrase afirma que o inquérito
  X reporta prevalência de 22% para o desfecho Y, quando o dado
  publicado é 27%; paráfrase afirma que a amostra do estudo-alvo foi
  3.000 participantes, quando a amostra real foi 300.

### Subdistinção conceitual × factual — refinamento operacional

Refinamento introduzido pela decisão 22 do `_changelog.md`
(A.7 Bloco A, A4). Gatilho empírico: fragilidade da regra original
observada no Teste 02, em que o único caso de acionamento de Dim. 3
(DANTAS et al. 2024) foi classificado como "conceitual" por ambiente
reconhecido como rigoroso, onde a regra v2 manda "factual" — evidência
de insuficiência operacional da regra, não de falha do executor. O
refinamento tem quatro elementos, aplicáveis a cada caso de Dim. 3.

- **Pergunta operacional.** Declarada acima, no cabeçalho desta seção:
  a distorção é sobre o que a obra *diz/argumenta* ou sobre o que a
  obra *mediu/observou/descreveu*? Resposta → valor da Dim. 3.
- **Exemplares contrastados lado a lado.**
  - Factual: DANTAS et al. (2024), Teste 02 — obra reflexiva
    qualitativa; distorção sobre o que a obra mediu/observou.
  - Conceitual: conflação Bourdieu/Foucault sobre poder, Direção 1
    (atribuir a Bourdieu posição foucaultiana) — obra teórica;
    distorção sobre a posição que a obra sustenta.
- **Regra de desempate para coocorrência.** Quando a distorção atinge
  simultaneamente posição teórica *e* metodologia/escopo, **ambos**
  os valores da Dim. 3 são acionados. Não há escolha entre — registra-
  se Dim. 3 conceitual e Dim. 3 factual em paralelo, como duplo
  acionamento. Esta regra instancia, para a Dim. 3 em §5, o padrão
  de dupla classificação desenvolvido em §8.5.
- **Heurística anti-padrão.** Distorção sobre metodologia, escopo,
  população ou tipo de achado empírico é **factual**, mesmo quando a
  obra é teórica ou qualitativa e a distorção é sofisticada. O caráter
  conceitual da obra não transfere automaticamente para o valor da
  Dim. 3. A heurística protege contra a gravitação cognitiva
  previsível para o valor que soa mais sofisticado ("conceitual") em
  casos limítrofes — erro observado empiricamente em DANTAS.

Baseline revisável. Este refinamento foi construído com base em um
único caso empírico de acionamento de Dim. 3; o exemplar conceitual é
clássico da literatura, não empírico do teste. O Teste 03 está
encarregado de produzir exemplar genuíno de Dim. 3 conceitual — ver
`_phase2-handoff.md` "Pré-condições do Teste 03".

## 6. Regra de articulação e fluxo decisório

A estrutura é hierárquica condicional. A Dim. 1 aplica-se sempre. A
Dim. 2 aplica-se apenas quando Dim. 1 = existente verificável. A
Dim. 3 aplica-se apenas quando Dim. 2 = conteúdo afirmado. Termine a
classificação no primeiro ramo que produzir veredito suficiente para a
ação corretiva.

```
Para cada referência da revisão:

  ┌── Dim. 1 — a obra existe e é verificável? ──┐
  │                                              │
  SIM                                            NÃO
  │                                              │
  │                                              ├── elementos combinam
  │                                              │   obras reais sem
  │                                              │   unidade?
  │                                              │
  │                                              ├── SIM → PASTICHE (fim)
  │                                              │
  │                                              └── NÃO → INEXISTENTE/
  │                                                         FABRICADA (fim)
  │
  └── EXISTENTE VERIFICÁVEL → Dim. 2 — onde está o erro?
       │
       ├── nos elementos da ficha? → METADADOS (fim)
       │
       ├── no modo de mobilização retórica?
       │     → ESTRUTURA DE SUSTENTAÇÃO (fim)
       │
       └── nas proposições atribuídas? → CONTEÚDO AFIRMADO →
             Dim. 3 — que tipo de conteúdo foi distorcido?
             │
             ├── atribuição teórica/conceito/enquadramento?
             │     → CONCEITUAL (fim)
             │
             └── dado empírico/taxa/valor/data?
                   → FACTUAL (fim)
```

A árvore representa o caso simples, em que cada ramo termina em um
valor único. Para casos com erros em mais de uma dimensão na mesma
referência — por exemplo, existente verificável com erro em metadados
*e* em conteúdo afirmado —, aplicar §8.4 após a classificação primária
para registrar a classificação secundária com a notação `+`.

## 7. Protocolo de verificação

Ordem operacional ao classificar uma referência. Cada passo responde a
uma pergunta específica e alimenta a decisão de dimensão
correspondente. Seguir a ordem — inversões aumentam custo sem ganho.

### 7.1 Consulta por identificador estável

Se a referência traz DOI, PMID ou ISBN: consultar Crossref (DOI),
PubMed (PMID) ou catálogo da editora (ISBN). Três resultados
possíveis:

- Resolve, e metadados retornados conferem com os declarados →
  candidata a existente verificável; seguir para §7.4.
- Resolve, mas metadados retornados são de obra diferente da declarada
  (autor, título, periódico divergem) → candidata a pastiche ou
  inexistente/fabricada; seguir para §7.2 com busca ativa para
  esclarecer.
- Não resolve (404, identificador inválido) → candidata a
  inexistente/fabricada ou pastiche; seguir para §7.2.

### 7.2 Busca ativa por autor + título + periódico

Se o identificador falha ou inexiste: buscar em PubMed, Google
Scholar, SciELO, LILACS, BDTD, LexML ou base apropriada ao domínio,
usando combinação autor + fragmento de título + periódico/editora +
ano. Dois resultados:

- Obra localizada com combinação única e coerente de autor, título,
  periódico e ano → existente verificável (mesmo que o identificador
  declarado tenha falhado); seguir para §7.4.
- Obra não localizada com combinação única → Dim. 1 = pastiche ou
  inexistente/fabricada; seguir para §7.3.

### 7.3 Pastiche × inexistente/fabricada

Aplicar o diagnóstico do §8.1 para decidir entre os dois valores. Se
pastiche, a classificação termina em Dim. 1; se
inexistente/fabricada, idem. Dim. 2 e Dim. 3 não são acionadas.

### 7.4 Conferência de metadados campo a campo

Quando Dim. 1 = existente verificável: comparar elemento por elemento
da ficha declarada contra os metadados canônicos retornados por
Crossref/PubMed/editora. Conferir autoria (nome completo, grafia,
ordem, coautores), ano, título (incluindo subtítulo), periódico (nome
oficial, abreviação quando aplicável), volume, fascículo, páginas,
DOI, edição, editora, local.

- Se há divergência em qualquer campo → Dim. 2 = metadados. Registrar
  o campo divergente e o valor canônico.
- Se todos os campos conferem → prosseguir para §7.5.

### 7.5 Verificação de conteúdo afirmado

Quando a paráfrase na revisão atribui à fonte afirmação específica
(não mera atribuição canônica de conceito ao autor que o cunhou): ler
abstract ou, para casos críticos, a seção relevante do texto completo.
Comparar a paráfrase contra o que a fonte efetivamente diz.

- Se a paráfrase é fiel → Dim. 2 ≠ conteúdo afirmado; prosseguir para
  §7.6.
- Se a paráfrase distorce a fonte → Dim. 2 = conteúdo afirmado;
  acionar §7.5.1 ou §7.5.2.

#### 7.5.1 Erro conceitual — releitura interpretativa

Gatilho: a distorção é de atribuição teórica, conceito, enquadramento
ou invocação de tradição. Procedimento:

- Ler a seção da fonte em que o conceito é definido.
- Comparar a definição da fonte com a atribuição feita pelo texto
  citante.
- Consultar `references/domain-*/theoretical-currents-*.md` quando o
  módulo de domínio existir, para determinar se o conceito atribuído
  pertence a corrente distinta.
- Veredito: Dim. 3 = conceitual.

#### 7.5.2 Erro factual — confronto numérico/documental

Gatilho: a distorção é de dado empírico específico (taxa, valor, data,
amostra, achado). Procedimento:

- Localizar na fonte o valor canônico (tabela, figura, seção de
  resultados).
- Comparar com o valor declarado pelo texto citante.
- Em casos de números com intervalo de confiança ou variação
  metodológica, confrontar a paráfrase com a formulação da própria
  fonte.
- Veredito: Dim. 3 = factual.

### 7.6 Avaliação de estrutura de sustentação

Quando metadados e conteúdo conferem: avaliar se a função
argumentativa da referência no texto é adequada. Perguntar — a fonte é
do tipo certo para sustentar esta afirmação? O estatuto epistêmico que
o texto lhe atribui (definitivo, preliminar, geral, local) coincide
com o estatuto efetivo da fonte? Essa avaliação exige leitura
contextual — do parágrafo citante e da fonte — e é a mais cara do
protocolo.

- Se há descompasso entre tipo de fonte e uso argumentativo → Dim. 2 =
  estrutura de sustentação.
- Se não há descompasso → referência classificada como existente
  verificável sem erro; encerrar.

### Regra de parada

Se §7.1 confirma identificador e §7.4 confirma metadados, e o texto
citante não faz paráfrase de conteúdo específico (apenas atribuição
canônica de conceito ao autor que o cunhou, sem paráfrase de
passagem) nem invocação argumentativa suspeita, a referência termina
em "existente verificável, sem erro". Não forçar classificação em
§7.5 ou §7.6 quando não há objeto a verificar.

## 8. Casos limítrofes

### 8.1 Pastiche × inexistente/fabricada em ambiguidade

Gatilho: obra não localizada em §7.2, e ao menos um elemento (autor,
título, periódico) aparenta ser real.

Regra: se **dois ou mais** dos elementos declarados rastreiam, em
busca independente, a obras reais do(s) mesmo(s) autor(es) ou ao
corpus do mesmo periódico — e os elementos restantes são plausíveis
mas não formam unidade com os primeiros — classificar como pastiche.
Caso contrário, classificar como inexistente/fabricada.

Heurística prática:

- Crossref/PubMed retorna obra do mesmo autor no mesmo tema, próxima
  em data à declarada, com metadados parcialmente coincidentes →
  pastiche.
- Nenhum elemento rastreia a obra real, ou apenas o nome do autor é
  real sem tema próximo → inexistente/fabricada.

Nota sobre o limite binário. A regra "dois ou mais elementos" é
simplificação operacional deliberada. Casos em que apenas um elemento
rastreia a obra real com força muito desigual — por exemplo, autor
super-ativo no tema exato, mas periódico, ano e DOI sem coincidência —
ficam, sob essa regra, classificados como inexistente/fabricada,
ainda que fenomenologicamente próximos de pastiche. A calibração do
limite contra dados empíricos diversos é trabalho de A.7.

### 8.2 Pastiche puro × pastiche intra-autoral

Ambos classificam como Dim. 1 = pastiche. Assinaturas diagnósticas
distintas, úteis para orientar a correção.

- **Pastiche puro**: elementos de obras de autores diferentes
  combinados. Hipótese gerativa: autor real A + título real de obra de
  B (outro autor) + periódico real de C. Obra real subjacente pelo
  autor declarado não existe.
- **Pastiche intra-autoral**: elementos de múltiplas obras do **mesmo
  autor** combinados. Exemplos do teste 01:
  - Provoost et al. 2021 — autor e tema da obra real de 2017 do mesmo
    autor, mas ano, volume, número e DOI transplantados de Xu et al.
    2021 (artigo de outro autor, mesmo periódico).
  - Topol 2020 — título do livro *Deep Medicine* (Basic Books, 2019)
    combinado com DOI do artigo "High-performance medicine"
    (*Nature Medicine*, 2019); mesmo autor, duas obras distintas.

Consequência prática: no intra-autoral, costuma haver obra real
recuperável pelo autor + tema + janela temporal, e a correção pode
substituir o pastiche por essa obra real. No puro, a correção exige
substituição integral — procurar fonte apropriada desde o começo.

### 8.3 Referências sem DOI e sem PMID

Aplica-se a livros, capítulos em coletâneas, literatura cinzenta,
documentos institucionais (WHO, IPEA, CEPAL, BM, ministérios),
legislação, teses e dissertações, anais de congresso sem ISSN. Seguir
`hallucination-prevention-checklist.md` §5.3 para a distinção entre
Regime 1 (identificador persistente: ISBN, handle BDTD, tombamento
LexML, ISSN + volume + páginas) e Regime 2 (só URL institucional ou de
evento).

Adaptação do protocolo:

- §7.1 substituído por consulta ao identificador do Regime 1
  apropriado (ISBN no catálogo da editora; handle na BDTD; tombamento
  no LexML); ou, no Regime 2, acesso à URL institucional declarada
  com registro do carimbo de confiança.
- §7.2 permanece: busca ativa por autor + título + editora/instituição
  + ano.
- §7.3 a §7.6 procedem normalmente, tratando as informações do
  Regime 1/2 como metadados canônicos de comparação.

Dados de repositórios oficiais (IBGE, DATASUS, VIGITEL, Ipeadata,
Banco Central, TSE, INEP, RAIS) têm convenção própria — seguir
`hallucination-prevention-checklist.md` §5.3, "Caso especial — dados
de repositórios oficiais".

### 8.4 Erros múltiplos em dimensões diferentes

Quando uma mesma referência apresenta mais de um erro em dimensões
distintas:

- **Classificação primária** = erro mais severo, conforme ordem
  canônica: Dim. 1 inexistente/fabricada > Dim. 1 pastiche > Dim. 2
  conteúdo afirmado > Dim. 2 metadados > Dim. 2 estrutura de
  sustentação.
- **Classificação secundária** = erro(s) adicional(is), registrado(s)
  com notação `+`.

Dim. 3 não entra na ordem canônica porque é condicional a Dim. 2 =
conteúdo afirmado. Quando Dim. 2 é conteúdo afirmado, Dim. 3 é sempre
aplicada; quando Dim. 2 é metadados ou estrutura de sustentação,
Dim. 3 é n/a. Por isso Dim. 3 não concorre com outros valores na
ordem de severidade.

Exemplos:

- Existente verificável, com erro em conteúdo afirmado conceitual *e*
  em metadados → `conteúdo afirmado (conceitual) + metadados`.
- Existente verificável, com erro em estrutura de sustentação *e* em
  metadados → `metadados + estrutura de sustentação` (metadados vem
  primeiro pela ordem canônica, apesar da menor expressividade
  analítica — é onde age a correção imediata).

Observação. A ordem canônica é regra geral de desempate. Em casos
específicos em que a severidade prática contraria a ordem — p. ex.,
erro de metadado trivial combinado com distorção grave em estrutura de
sustentação — registrar a justificativa junto à classificação; a ordem
canônica permanece referência default, não absoluta.

### 8.5 Conteúdo afirmado com registros misturados

Gatilho: a paráfrase invoca simultaneamente uma atribuição conceitual
*e* um dado factual da mesma fonte, e a verificação detecta distorção
em ao menos um dos dois registros.

Regra:

- Se **ambos** os registros estão distorcidos → **exceção ao padrão
  de rótulo único**: aplicar Dim. 3 em dupla classificação,
  `conceitual + factual`, registrando separadamente o que foi
  distorcido em cada registro. A ação corretiva é dupla: releitura
  interpretativa para o conceitual, confronto numérico/documental
  para o factual.
- Se **apenas um** registro está distorcido → classificar pelo
  registro efetivamente errado; o outro não contamina a classificação.

A dupla classificação é exceção, não padrão. Casos típicos terminam
em um único valor da Dim. 3.

### 8.6 Variantes nomeadas de Dim. 2 estrutura de sustentação argumentativa

A Dim. 2 estrutura de sustentação argumentativa é definida
genericamente em §4, com quatro exemplos construídos. Esta subseção
codifica variantes nomeadas do fenômeno, com sinais de acionamento e
exemplares canônicos detalhados, quando a empiria acumulada nos testes
permite distingui-las. A inclusão de variante nova obedece à regra
de decisão de §2.2 mais o critério empírico consolidado na
Fase A.7: detecção independente em ao menos dois ambientes distintos
sem acesso à ground truth. A cláusula de fronteira ao final desta
subseção delimita o escopo, e o parágrafo sobre o gate de reabertura
explicita as condições para canonização de variantes adicionais.

#### Conflação teórica fabricada entre autores de correntes divergentes (caso canônico)

Variante canônica. O parágrafo citante agrega autores de correntes
teoricamente divergentes em paráfrase de convergência, sem marcador de
contraste, atribuindo a cada autor posição que ele não sustenta no
corpus próprio. Cada autor é representado dizendo o que não disse; a
convergência retórica é fabricada por sobreposição de posições.

- Eixo: vício sobre **posições atribuídas** (o que as fontes *dizem*).
- Sinais de acionamento: paráfrase conjunta de dois ou mais autores
  no mesmo parágrafo sem marcador explícito de contraste; ausência de
  diferenciação teórica prévia (p. ex., autores de pares-gatilho
  canônicos listados no SKILL.md regra 4 aparecendo como uma voz só).
- Ação corretiva: desagregar as paráfrases, declarar a posição de
  cada autor a partir do seu próprio corpus, reformular com marcador
  de contraste quando a agregação retórica for mantida.
- Exemplar canônico: Bourdieu e Foucault sobre poder. Conflação
  fabricada típica: paráfrase agregativa do tipo "Bourdieu e Foucault
  mostram que o poder opera através de mecanismos não-coercivos,
  produzindo subjetividade conforme", que oculta a divergência
  ontológica entre estrutural-relacional (Bourdieu) e
  estratégico-produtivo (Foucault) sob formulação genérica sobre
  "poder não-coercivo". Bourdieu teoriza poder via **campo, habitus
  e capital** — estruturas relacionais objetivas e disposições
  incorporadas. Foucault teoriza poder via **dispositivos,
  governamentalidade, biopolítica** — produção estratégica de
  subjetividade e de corpos governáveis. O par é também exemplar
  canônico da Dim. 3 conceitual em §5, em instância operacional
  distinta: lá a conflação incide sobre referência individual
  (atribuir a um autor posição do outro — Direção 1 canonizada:
  atribuir a Bourdieu posição foucaultiana); aqui a conflação incide
  sobre a estrutura argumentativa do parágrafo (os dois autores
  apresentados como convergentes sem marcador de contraste). Paralelo
  pedagógico deliberado; mecanismos operacionais separados.

#### Agregação para fabricação de convergência empírica (variante nova, A.7)

Variante estrutural descrita originalmente na ground truth do
Teste 02 da Fase A.7, canonizada pela decisão 19 do `_changelog.md`
(A.7 Bloco A, A1). O parágrafo citante constrói narrativa de
convergência acadêmica por empilhamento de fontes heterogêneas em
tipo, escopo e poder inferencial, quando o conjunto das fontes não
sustenta empiricamente a afirmação específica veiculada. Cada autor é
citado corretamente; o consenso é que é fabricado.

- Eixo: vício sobre **evidências agregadas** (o que as fontes
  *medem/observam*).
- Sinais de acionamento em dois vetores:
  - *Linguístico*: marcadores de convergência/consenso no parágrafo
    citante ("a literatura converge para…", "evidências apontam…",
    "em síntese, o consenso acadêmico sugere que…").
  - *Estrutural*: heterogeneidade do mosaico de fontes incompatível
    com a especificidade da afirmação veiculada — mistura de pesquisa
    empírica nacional com estudo de caso local, revisão narrativa
    genérica, reflexão teórica qualitativa, iniciação científica,
    pastiche.
- Ação corretiva: desmontar a narrativa de convergência; caracterizar
  cada fonte pelo seu poder inferencial efetivo; rebaixar o nível da
  afirmação ao que o conjunto das fontes sustenta, ou substituir
  fontes para cobrir a afirmação pretendida.

Exemplar canônico. Parágrafo-semente do Teste 02 da Fase A.7: a
afirmação sintética do texto citante é empírica, nacional, sobre
estudantes do Ensino Médio público brasileiro; o mosaico das sete
referências agregadas é heterogêneo de modo incompatível com essa
especificidade.

| Ref. | Tipo de fonte | Escopo | Validade inferencial |
|---|---|---|---|
| BOF; MORAES | Pesquisa empírica institucional (INEP) | Saeb nacional 3ª EM | Alta, para aprendizagem no EM |
| CARDOSO; BERTONI | Trabalho de iniciação científica | Indeterminado | Baixa (iniciação científica, 9 páginas) |
| DANTAS et al. | Reflexão teórica qualitativa | Educação Básica ao Ensino Superior, DF | Baixa para claim de leitura/matemática no EM |
| FUZZO et al. | Estudo de caso | 1º ano EM, escola única em Lábrea-AM | Muito local; nacional não |
| MAGALHÃES; ROCHA | Indeterminada | — | — |
| MELO | Análise de conteúdo documental | Educação pública brasileira, genérico | Baixa-média |
| SOARES et al. | Revisão narrativa | Rede básica, genérico | Média |

Apenas uma das sete fontes (BOF; MORAES) tem poder inferencial
nacional compatível com a afirmação do parágrafo. As demais são locais,
genéricas, reflexivas ou de gênero bibliográfico incompatível. A
"convergência" é construída pela agregação retórica, não pela
evidência agregada.

#### Convergência fabricada entre autores de correntes vizinhas / aplainamento de heterogeneidade interna a uma tradição (variante nova, Frente 2 / Teste 03)

Variante estrutural canonizada pela decisão de fechamento da Frente 2
do roadmap v3.4 (Teste 03 / Fase A.7.2; ver `_changelog.md`). O
parágrafo citante trata autores que partilham vinculação institucional,
diálogo acadêmico ou apresentação conjunta na bibliografia comentada
brasileira, **mas operam em chaves teóricas distintas**, como se fossem
interlocutores naturais de uma tradição unificada — produzindo
aplainamento de heterogeneidade interna a uma tradição. A vizinhança
acadêmica é real; a complementaridade metodológica declarada não é.

- Eixo: vício sobre **estrutura de sustentação argumentativa** quando
  a vizinhança acadêmica entre autores é genuína, mas a
  complementaridade metodológica declarada é fabricada. Distinto da
  conflação Dim. 3 stricto sensu, que opera entre **tradições
  divergentes** (Bourdieu × Foucault, Connell × Butler, Bardin ×
  Minayo) — aqui a vizinhança é real e o vício está na supressão das
  divisões internas.
- Mecanismos típicos:
  - *Atribuição genérica unificadora*: bloco unitário sob rótulo
    abrangente ("tradição canônica de X", "vertente brasileira de Y")
    que oculta cisões teórico-metodológicas internas.
  - *Convergência declarada sem marcador de contraste*: ausência das
    locuções obrigatórias da Regra 5 do `SKILL.md` ("em contraste",
    "convergindo com", "essa visão é desafiada por") quando autores
    de correntes vizinhas são apresentados conjuntamente.
  - *Equivalência metodológica sem reconhecimento de divisão de
    trabalho*: tratamento de categorias-âncora distintas como
    exercícios análogos ou complementares, sem registrar a separação
    entre os corpora teóricos próprios.
- Detecção: aplica-se a Regra 5 do `SKILL.md` (marcador de contraste
  obrigatório); ausência do marcador é o sinal primário. Quando o
  conceito-âncora canônico de um autor é mobilizado via apud para
  outro autor da mesma vizinhança, acionar adicionalmente a regra
  "verificação ativa de conceitos-âncora canônicos mobilizados via
  apud" do `epistemic-tagging-rules.md`.
- Ação corretiva: declarar separadamente a tradição teórica de cada
  autor (consultando `references/domain-*/theoretical-currents-*.md`
  quando o módulo de domínio existir); marcar as categorias-âncora
  próprias de cada um; reformular com marcador de contraste explícito
  quando a apresentação conjunta for mantida; corrigir atribuições
  cruzadas via apud.

Exemplar canônico. **Par Magnani × Velho** (A4 do Teste 03 da
Fase A.7.2). Magnani (NAU-USP, etnografia estrutural-espacial;
categorias-âncora **pedaço, mancha, trajeto, circuito, pórtico**) e
Velho (PPGAS-Museu Nacional/UFRJ, antropologia
fenomenológico-individualista; categorias-âncora **trajetória,
projeto, campo de possibilidades**, "olhar de perto e de dentro" como
método). Vizinhança institucional (antropologia urbana brasileira) e
diálogo acadêmico reais; complementaridade metodológica declarada no
parágrafo-semente é fabricada. O parágrafo cita autores corretamente
mas suprime a separação entre os dois corpora teóricos.

#### Regra de desempate entre as três variantes

Pergunta primária: **o vício está no que as fontes *dizem*, no que as
fontes *medem/observam*, ou na supressão de divisões teóricas dentro
de uma vizinhança real?**

- Posições teóricas atribuídas divergem do que as fontes efetivamente
  sustentam no corpus próprio, e os autores vêm de **tradições
  divergentes** → **conflação teórica fabricada** (variante canônica).
- Cada fonte é citada corretamente, mas o conjunto agregado não
  sustenta empiricamente a afirmação de convergência que o parágrafo
  veicula → **agregação para fabricação de convergência empírica**
  (variante A.7).
- Cada autor é citado corretamente, a vizinhança institucional ou
  acadêmica entre eles é real, mas a complementaridade metodológica
  declarada suprime as divisões internas da tradição → **convergência
  fabricada entre autores de correntes vizinhas / aplainamento de
  heterogeneidade interna** (variante Frente 2).

Coocorrência das variantes no mesmo parágrafo é possível em princípio.
Registrar as classificações em paralelo, sem escolha entre. Em
particular, distinguir conflação Dim. 3 stricto sensu (tradições
divergentes) de aplainamento Dim. 2 sustentação (correntes vizinhas)
é decisão sobre o **eixo da divergência** — divergência teórica
profunda aciona Dim. 3; vizinhança real com supressão de cisões
internas aciona Dim. 2 sustentação.

#### Cláusula de fronteira externa à v2

Variantes de Dim. 2 estrutura de sustentação argumentativa são
acionadas **apenas** quando há descompasso detectável entre o que o
texto diz sobre as fontes e o que as fontes mostram. Observações
sobre adequação retórica, seleção editorial do corpus ou qualidade
da conclusão normativa ficam **fora** da v2 — são crítica editorial
ou argumentativa genérica, não dimensão taxonômica. O escopo da
skill é detecção de alucinação e distorção bibliográfica; variantes
que cruzam essa fronteira não entram em §8.6 mesmo quando
empiricamente sustentadas.

#### Gate para canonização futura de variantes adicionais

Variantes adicionais previamente descartadas (ver `_changelog.md`,
entrada correspondente à decisão A2 da Fase A.7, no caso concreto de
"inflação retórica de certeza" e "conclusão normativa passando como
síntese científica", registradas como heurísticas editoriais adjacentes
em `hallucination-prevention-checklist.md`) só podem ser canonizadas
futuramente se atenderem a esta cláusula de fronteira **e**
apresentarem detecção independente em ambiente distinto, conforme
critério empírico da decisão A1 da Fase A.7. A cláusula de fronteira
não é fechamento permanente; é critério de admissão. Reabertura exige
os dois requisitos simultaneamente, e a decisão é registrada como
entrada nova no `_changelog.md`.

### 8.7 Subtipos formais de Dim. 1 — fabricação com identificador colidido

A Dim. 1 inexistente/fabricada admite subtipos formais que orientam
prioridade diferencial em §(xii) e exigem operações de verificação
distintas. Esta subseção codifica o subtipo "fabricação com
identificador colidido" canonizado pela decisão de fechamento da
Frente 2 do roadmap v3.4 (Teste 03 / Fase A.7.2; ver `_changelog.md`).
Outros subtipos potenciais ("pastiche stricto sensu", "fabricação
simples") permanecem na queue de refinamento da skill em §9 do
ground truth v2.0 do Teste 03 — endereçáveis em rodadas futuras.

#### Fabricação com identificador colidido

Definição. Referência fabricada cujo DOI, ISSN, ISBN ou outro
identificador estável **resolve para artigo, livro ou periódico real
distinto**, gerando ilusão de existência verificável quando o
identificador é consultado isoladamente.

Vetor de risco. Satisfaz o teste superficial "DOI existe" mas falha no
teste rigoroso "metadados do DOI batem com a referência citada". É
distinto dos demais subtipos Dim. 1:

- **Pastiche stricto sensu** combina autor real com título e/ou
  periódico fabricados em padrão lexical canônico do autor, sem
  identificador resolvível ou com identificador transplantado de obra
  do próprio autor (intra-autoral) ou de outro autor (puro). Ver §8.2.
- **Fabricação simples** tem identificadores não-resolvíveis ou
  ausentes; não há entidade bibliográfica real correspondente ao
  identificador declarado.
- **Fabricação com identificador colidido** tem identificador
  resolvível, mas para entidade distinta da referência citada — a
  "colisão" é entre o identificador declarado e a referência declarada,
  não entre dois autores ou duas obras.

Detecção. Depende de §(xii) — verificação ativa em
CrossRef/SciELO/OJS com confronto de metadados completos: autor,
título, periódico, volume, número, páginas, ano. A ação corretiva
não pode parar na resolução do DOI; precisa comparar os metadados
retornados com os declarados em todos os campos.

Exemplar canônico. **Silva & Lopes (2020)** no Teste 03 da Fase A.7.2.
Referência declarada: "Silva & Lopes (2020), *Sociedade e Estado*
v.35 n.2 p.521-545, DOI 10.1590/s0102-6992-202035020008". O DOI
resolve em CrossRef para artigo real distinto: **SILVA, R. A. da.
"Para além do Estado: Marx, Lenin e a crítica da estatalidade",
*Sociedade e Estado* v.35 n.2 p.553-579, 2020**. Mesmo periódico,
mesmo volume, mesmo número, mesmo ano; autor único distinto da dupla
declarada; título e páginas distintos. Caso clássico de colisão de
identificador: o DOI sintético segue o padrão estrutural do
periódico mas não corresponde à referência declarada.

Ação corretiva. Quando o identificador colide, registrar a referência
como fabricada e oferecer, se cabível ao texto citante, a obra real
para a qual o identificador resolve — desde que essa obra seja
relevante ao tema. Quando a obra real não atende ao tema citante,
buscar fonte verificada apropriada e substituir integralmente.

#### Princípio expansível

A canonização de "fabricação com identificador colidido" é a primeira
operação de subtipos formais de Dim. 1 na v2. Outros subtipos
candidatos — em particular a separação formal entre "pastiche stricto
sensu" e "fabricação simples", hoje inferida da §8.2 e do contraste
implícito com pastiche — permanecem na queue da skill (§9.2 do ground
truth v2.0 do Teste 03). A admissão de novos subtipos segue a regra de
§2.2 (quatro critérios cumulativos) acrescida do critério empírico
consolidado na Fase A.7: detecção em rodada de teste com material novo
distinto da rodada que originou o candidato.

## 9. Reclassificação rápida dos oito casos do teste 01

Consulta rápida. Análise desenvolvida no manuscrito-fonte, seção 3.7.

| Nº | Referência declarada | Verificação | Dim. 1 | Dim. 2 | Dim. 3 | Ação corretiva |
|---|---|---|---|---|---|---|
| 1 | Abd-Alrazaq et al. 2020 | DOI resolve; metadados conferem | existente verificável | — | — | nenhuma (sem erro) |
| 2 | Bickmore, Trinh e Asadi 2021 | DOI pertence a Selvanathan e Jetten 2020; os três autores declarados são coautores reais de Bickmore et al., *JMIR* 20(9):e11510, 2018, em tema adjacente (segurança de assistentes conversacionais para informação médica) | pastiche | n/a | n/a | substituir pela obra real (Bickmore et al., *JMIR* 20(9):e11510, 2018) se o tema do texto citante admitir; ou substituir por fonte verificada alinhada ao tema específico declarado |
| 3 | Fitzpatrick, Darcy e Viera 2017 | Obra real; autora é Vierhile; subtítulo omitido | existente verificável | metadados | n/a | corrigir autoria e subtítulo na ficha |
| 4 | Lim et al. 2022 | DOI pertence a Maurits et al. 2022; obra real com autor, ano e periódico declarados coincidentes — Lim SM et al., *Behavior Therapy* 53(2):334–347, 2022, sobre chatbot-delivered psychotherapy para depressão e ansiedade | pastiche | n/a | n/a | substituir pela obra real (Lim et al., *Behavior Therapy* 53(2):334–347, 2022) |
| 5 | Mathur et al. 2023 | DOI 404; periódico declarado "Nature Digital Medicine" não existe com esse nome exato (real seria *npj Digital Medicine*); busca ativa em PubMed, arXiv, Google Scholar e Semantic Scholar não localiza obra de Mathur como primeiro autor sobre LLMs e risco suicida em 2022–2024 | inexistente/fabricada | n/a | n/a | substituir por fonte verificada sobre risco suicida e LLMs |
| 6 | Provoost et al. 2021 | Autor e tema da obra real de 2017; ano/volume/número/DOI de Xu et al. 2021 | pastiche (intra-autoral) | n/a | n/a | substituir pela obra real: Provoost et al. 2017, *JMIR* 19(5), e151 |
| 7 | Topol 2020 | Título do livro *Deep Medicine* (2019) + DOI do artigo "High-performance medicine" (2019); mesmo autor, duas obras distintas | pastiche (intra-autoral) | n/a | n/a | desfazer o pastiche: escolher entre livro ou artigo e corrigir a ficha |
| 8 | WHO 2021 | Documento existe; divergências em editora/coleção | existente verificável | metadados | n/a | corrigir editora/coleção |

**Nota.** A Dimensão 3 (Natureza) não foi acionada em nenhum dos oito
casos, porque nenhum apresenta erro em conteúdo afirmado. A
distribuição é: quatro pastiches (Provoost, Topol, Bickmore, Lim), um
inexistente/fabricada (Mathur), dois existentes verificáveis com erro
em metadados (Fitzpatrick, WHO), um existente verificável sem erro
(Abd-Alrazaq). Observação informativa sobre o perfil de erros do
ChatGPT gratuito, nessa versão e nesse tema: concentração forte em
**pastiche** — a categoria específica pós-LLM introduzida por McGowan
et al. (2023) e adotada pela v2 como valor intermediário da Dimensão
Existência —, com fabricação integral respondendo por apenas um caso.
O teste 02, em planejamento, está sendo desenhado para incluir
parágrafo cujos erros sejam mais concentrados em conteúdo afirmado,
justamente para produzir exemplos que acionem a Dim. 3.

## 10. Limitações reconhecidas

- **Cascatas sistêmicas fora de escopo.** A v2 opera item por item;
  fenômenos como *citation transmutation* (Greenberg 2009),
  *affirmative citation bias* (Letrud e Hernes 2019), *academic urban
  legends* (Rekdal 2014) exigem unidade de análise superior — redes
  de co-citação. Camada sobre a v2 é trabalho futuro.
- **Verificabilidade dependente de indexação.** A Dim. 1 pressupõe
  acesso a Crossref, PubMed, Google Scholar, SciELO, LILACS, BDTD,
  LexML. Em domínios de cobertura parcial — literatura brasileira em
  ciências humanas, publicações em editoras locais não registradas em
  Crossref — classificações de "inexistente" podem ser artefato de
  cobertura. Classificador prudente registra incerteza quando ausência
  de cobertura é plausível.
- **Unidade de análise item por item.** A classificação é da
  referência, não do parágrafo nem do argumento. Uma revisão pode ter
  todas as referências classificadas como existentes verificáveis sem
  erro e ainda assim ser veículo de distorção coletiva por viés de
  seleção.
- **Ausência de validação empírica formal.** A reclassificação dos
  oito casos do teste 01 é ilustração, não validação. Concordância
  interanotador, sensibilidade a modelos diferentes de LLM, utilidade
  operacional nos contextos preventivo e diagnóstico — tudo isso
  depende de testes subsequentes.
- **Dimensão Natureza não acionada no caso-teste aplicado.** A
  cobertura empírica da Dim. 3 depende do teste 02. Até lá, os
  exemplos dados em §4 (conteúdo afirmado) e §5 são construídos, não
  observados.
- **Taxonomia desenhada para revisão de literatura.** Transferência
  para outros gêneros (artigo empírico original, editorial, parecer
  técnico) pode exigir adaptação das categorias, sobretudo em Dim. 2 =
  estrutura de sustentação, cuja noção de função argumentativa é
  específica ao gênero.

## 11. Extensões futuras

Três eixos examinados no desenho da v2 e descartados. Permanecem
candidatos documentados à reentrada, cada um com critério específico,
alinhado a §2.2.

- **Grau (pontual × estruturado).** Herdeiro de De Lacey/Fenton/Lukić.
  Descartado porque não altera ação corretiva na v2 atual (erro de
  DOI *major* ou *minor* demanda a mesma correção). Reentra se dados
  empíricos de aplicação mostrarem que Grau separa fluxos corretivos
  distintos em contextos reais — p. ex., decisões editoriais de
  retratação versus correção, ou priorização de verificação humana
  sob restrição de tempo.
- **Consequência argumentativa (SciCite —
  background/method/result).** Descartado porque a consequência
  argumentativa de uma citação fabricada é analiticamente independente
  do fato de ela ser fabricada, e a ação corretiva é idêntica nos três
  valores. Reentra se a skill integrar ferramentas NLP dedicadas à
  classificação de função de citação e a informação resultante puder
  alimentar o fluxo (p. ex., priorização de verificação por função).
- **Cascatas sistêmicas.** Descartado por restrição de unidade de
  análise — exigem rede, não item. Reentra quando a skill incorporar
  camada de análise de co-citação em corpora de revisões; tal camada
  opera **acima** da v2, não como substituta.

**Natureza não figura aqui.** A Dim. 3 (conceitual × factual) é parte
integrante da v2 e foi incorporada após análise comparativa entre o
ganho marginal de cada eixo candidato e o critério (d) de §2.2 —
Natureza produz orientação corretiva operacionalmente distinta
(releitura interpretativa × confronto numérico), enquanto Grau,
Consequência e Cascatas produzem predominantemente rótulo descritivo.
