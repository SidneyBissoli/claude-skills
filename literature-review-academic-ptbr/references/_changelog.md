# Changelog arquitetural — Fase 1 do MVP

Decisões que emergiram durante a construção dos seis arquivos da skill
`literature-review-academic-ptbr`. Ordem por consequência, da mais
estrutural (afeta todo o pipeline) para a mais localizada (afeta a
interface de uma seção). Cada entrada: o que foi decidido e por que
foi decidido assim.

## Decisões

**1. Cinco modos de falha (a-e) com formas curtas canônicas.** `(a) erros menores`,
`(b) fabricação total`, `(c) conteúdo distorcido`, `(d) conflação teórica`,
`(e) drift temporal` — os quatro primeiros bibliográficos, o quinto temporal.
Definidos em checklist §2; replicados em SKILL.md regra 3 com ponteiro.
Razão: modo (e) é ortogonal, vetor pelo qual qualquer outro pode ressurgir
tardiamente.

**2. Paráfrase com verbatim lado a lado (SKILL.md regra 7).** Toda paráfrase
de obra específica carrega trecho verbatim de até 25 palavras + página, no
mesmo bracket da tag epistêmica, no rascunho de trabalho. Razão: única
defesa prática contra modo (c) — permite conferência humana em segundos.

**3. Leitura humana estratificada como única camada que fecha (c).** Matriz
de mitigação (checklist §6) marca `✓ (única)`; §5.2 estabelece amostragem
por risco: 100% obras-chave e seções de alto risco, ≥20% no resto.
Razão: reconhecer a fronteira estrutural da automação evita a ilusão de
que mais script resolve.

**4. Carimbo de confiança como camada temporal autônoma.** Em vez de
rearranjar a matriz bibliográfica, modo (e) recebeu defesa dedicada; opera
por reverificação pré-submissão, não por detecção em tempo de geração.
Razão: drift temporal é ortogonal aos vetores bibliográficos e precisa de
camada própria.

**5. Multi-fonte `[SOURCED: k1, k2]` só após SOURCED individual.** Regra
dura em epistemic-tagging §1: cada chave agregada deve ter aparição
individual com verbatim em outro ponto. Razão: multi-fonte sem verificação
individual recria conflação ou atalho.

**6. `[GENERAL KNOWLEDGE]` exclui especificidade nacional.** Teste cumulativo:
(a) afirmação apareceria em manual introdutório **internacional** sem citação;
(b) não depende de especificidade nacional. SUS, DATASUS, legislação BR
exigem `[SOURCED]`. Razão: manuais brasileiros específicos codificam
convenções locais que não integram o saber internacional compartilhado.

**7. Override do pesquisador vence heurística de estilo.** style-detection §7:
declaração explícita, instruções vigentes do periódico, ou preferências
compatíveis com variantes sobrescrevem o registry. Razão: autoridade sobre
estilo bibliográfico é do autor e do periódico, não da skill.

**8. Detecção reduz fricção, não impõe.** Corolário de (7) promovido a
princípio de design: heurística evita pergunta quando a resposta é óbvia;
nunca decide por cima do pesquisador. Razão: skill que sobrescreve decisões
vira atrito, não utilidade.

**9. "Parar é melhor que atribuir" na desambiguação.** author-disambiguation §5:
quando cinco critérios (ORCID → afiliação → área → coautores → histórico) e
fallbacks não resolvem homônimos, parar e pedir confirmação humana.
Razão: custo de parar é uma mensagem; custo de atribuir errado é modo (c)
não-detectável.

**10. Conflação intra-autoral silenciosa como subcategoria de (d).**
author-disambiguation §6: citar `(Saffioti, 1969; 2004)` em paráfrase de
convergência sem marcar distância teórica é conflação ainda com autor único.
Exemplos canônicos: Saffioti, Connell, Foucault, Butler, Bourdieu.
Razão: os mecanismos de conflação entre autores valem para fases teóricas
do mesmo autor.

**11. Dois regimes + caso especial para literatura cinzenta.** checklist §5.3:
(1) com identificador persistente (handle, ISBN + páginas, ISSN + volume +
páginas) — identificador é âncora, URL descartável; (2) só com URL — URL +
carimbo, SHA256 para casos críticos. Dados de repositório oficial têm
protocolo próprio. Razão: estratégia de defesa depende de onde a obra vive.

**12. Registro discursivo e nome de campo separados.** "Carimbo de confiança"
em prosa (metáfora pedagógica); `data_ultima_verificacao` em estrutura de
dados (buscável, literal). Razão: prosa aceita metáfora; estrutura de dados
pede literalidade para grep e scripts.

**13. Glossário de termos operacionais no SKILL.md.** Adicionado após teste
em Claude Desktop revelar que termos como "carimbo de confiança" estavam
órfãos — definidos apenas em arquivos de `references/`, não no corpo do
SKILL.md. 12 entradas alfabéticas inseridas entre "Regras inegociáveis" e
"Fluxo obrigatório"; header do fluxo ajustado para "Fluxo obrigatório
(instância do padrão generate-critique-refine)". Razão: SKILL.md deve ser
autocontido em vocabulário para o caso de sessão sob pressão pular o
passo 1 do fluxo obrigatório (ler o checklist inteiro).

**14. Zip de distribuição com listagem explícita, não wildcard.** A
regeneração do `.zip` da skill usa lista nomeada dos artefatos a empacotar
(`SKILL.md`, `references/`), nunca `Compress-Archive *`. Razão: wildcard
puxa silenciosamente arquivos transitórios (backup do editor, artefatos do
empacotador, estados intermediários dentro de `.git/`) para dentro da
skill instalada, e esse drift é invisível até a skill rodar em produção
com conteúdo estranho no pacote. Consequência operacional: todo comando
`Compress-Archive` lista explicitamente os paths de entrada; auditoria do
conteúdo do zip (`Expand-Archive` em pasta temporária + `Get-ChildItem
-Recurse`) precede cada upload, com verificação explícita de que
`SKILL.md` está na raiz do zip e não dentro de pasta envolvente.

**15. Instalação no Claude Desktop via upload de zip, não via symlink.**
O `SKILL.md` chega ao Claude Desktop pelo mesmo caminho do Claude.ai web:
regenerar o zip (decisão 14) e fazer upload via *Settings → Capabilities →
Skills*. Symlink de `~\.claude\skills\` para o repositório em
`<pasta-de-skills>\` — tentativa inicial da Fase 1 registrada no
roadmap v1 — foi abandonado como estratégia de instalação. Razão: upload
de zip é o caminho oficialmente documentado pela Anthropic; Claude Desktop
não lê confiavelmente do symlink em Windows — observação empírica da
Fase 1 em que edições no repositório não se propagavam ao ambiente apesar
do symlink válido no sistema de arquivos. Symlink também requer privilégio
de administrador e cria assimetria com o Claude.ai web (um ambiente via
referência viva, outro via snapshot), assimetria que mascara o próprio
ato de propagação e convida drift silencioso entre o código e a skill
instalada em cada ambiente. Consequência operacional: toda edição no
repositório exige regenerar o zip e re-uploadar nos dois ambientes
separadamente — a convenção "não há sincronização automática" do
`CLAUDE.md` materializa essa escolha.

**16. Distinção entre decisões arquiteturais (changelog) e convenções
operacionais (CLAUDE.md).** Changelog registra decisões nossas sobre a
skill — regras, formatos, escopos, procedimentos. Observações empíricas
sobre comportamento de plataformas (Claude Desktop, Claude.ai web, Claude
Code) vão para CLAUDE.md seção "Convenções operacionais". Razão: misturar
as duas categorias no changelog erode o propósito do changelog como rastro
de decisões deliberadas. Consequência operacional: ao identificar
convenção operacional nova, adicionar a CLAUDE.md; ao tomar decisão
arquitetural nova, adicionar ao changelog.

**17. Documentação aponta para fonte da verdade, não duplica estado.**
CLAUDE.md e outros arquivos de orientação não replicam dados (contagens,
datas, numeração) que vivem em arquivos-fonte (`_changelog.md`,
`_phase2-handoff.md`, `git log`). Razão: duplicação de estado cria
defasamento silencioso — a cópia envelhece toda vez que o original muda, e
a correção vira fricção recorrente. Consequência operacional: ao escrever
ou revisar documentação, substituir estados específicos por apontamentos
("ver changelog", "consultar git log", "listado em handoff") e manter
apenas descrições estáveis ("decisões arquiteturais em ordem de
consequência").

**18. Refatoração canônica da taxonomia para v2 (tridimensional
hierárquica condicional).** A taxonomia v1 de cinco modos (a)–(e) é
substituída por taxonomia v2 com três dimensões aplicadas
condicionalmente: Dim. 1 Existência (sempre; valores: existente
verificável / pastiche / inexistente-fabricada); Dim. 2 Objeto (se
Dim. 1 = existente verificável; valores: metadados / conteúdo
afirmado / estrutura de sustentação argumentativa); Dim. 3 Natureza
(se Dim. 2 = conteúdo afirmado; valores: conceitual / factual).
Desenho operacional em `_taxonomy-v2-design.md`; fundamentação em
`<pasta-de-referencias>/skill-development/research/fase-A1-manuscrito-taxonomia-v2.md`.

Filiação em camadas: estrutura bidimensional genérica herdada da
tradição bibliométrica biomédica (Doms 1989; De Lacey, Record e Wade
1985; Fenton et al. 2000; Lukić et al. 2004); categoria pastiche de
McGowan et al. (2023); subdistinção pastiche puro × intra-autoral como
contribuição do projeto (ausente em McGowan); arquitetura v2 — seleção
dos três eixos, regra de articulação hierárquica condicional,
princípio pragmático de proporcionalidade — esboçada por Claude
(Anthropic) no contexto do projeto; decisões de escopo por Sidney
Bissoli.

Razão: o teste 01 (Fase 3.1) expôs defeitos estruturais da v1 — casos
híbridos sem lugar (Provoost, Topol), intensidade binária sem
categoria intermediária, modo (e) órfão no fluxo. A v2 reflete o
mecanismo gerativo comum das falhas pós-LLM (composição probabilística
de elementos de obras reais, capturada pela categoria pastiche) e
orienta verificação diferenciada em erros de conteúdo (Dim. 3).

Preservação do rastro histórico. As decisões 2, 3, 4 e 10 permanecem
válidas retrospectivamente sob o vocabulário da época; nenhuma é
reescrita ou invalidada. Tradução para termos v2:

| Decisão v1 | Vocabulário v1 | Equivalente em v2 |
|---|---|---|
| 2 | anti-modo-(c) | Dim. 2 conteúdo afirmado |
| 3 | fecha (c) | Dim. 2 conteúdo afirmado |
| 4 | modo (e) | vetor ortogonal fora da v2; defesa em `hallucination-prevention-checklist.md` §3 (carimbo de confiança) |
| 10 | subcategoria de (d) | Dim. 2 conteúdo afirmado + Dim. 3 conceitual *ou* Dim. 1 pastiche intra-autoral, conforme natureza do erro |

Princípio metodológico emergente. O protocolo de verificação da v2
(`_taxonomy-v2-design.md` §7) aplica-se tanto a revisões de literatura
assistidas quanto aos próprios casos usados como exemplo em documentos
operacionais ou acadêmicos que os invocam. Constatação de DOI
incorreto é condição **necessária mas não suficiente** para
classificar caso como inexistente/fabricada; os cinco marcadores de
pastiche (`_taxonomy-v2-design.md` §3, subseção "Pastiche") devem ser
aplicados integralmente antes da classificação final. Esse princípio
emergiu na A.1.5, reabertura parcial da A.1 por auditoria que detectou
aplicação incompleta dos marcadores aos casos 2 (Bickmore) e 4 (Lim)
do teste 01.

Consequência operacional — arquivos a refatorar em fases subsequentes:
- **A.2**: `_master-guide.md`.
- **A.3**: `SKILL.md` (frontmatter, regra 1 "Zero fabricação",
  glossário, "Módulos de referência — quando carregar o quê" com
  `_taxonomy-v2-design.md` adicionado ao bloco "sempre carregar") e
  `CLAUDE.md` (raiz do projeto).
- **A.4**: `hallucination-prevention-checklist.md`,
  `epistemic-tagging-rules.md`, `argumentative-review-template.md`,
  `author-disambiguation-universal.md`.
- Varredura posterior do `_taxonomy-v2-design.md` para remover
  referências transitórias ("até a fase A.3") quando A.3 concluir.

**19. Canonização da variante "agregação para fabricação de convergência
empírica" em Dim. 2 estrutura de sustentação argumentativa (A.7 Bloco A,
A1).** No `_taxonomy-v2-design.md` §8.4, a variante canônica existente
(conflação teórica fabricada entre autores de correntes divergentes)
recebe companhia de uma segunda variante nomeada. O critério de
distinção é o eixo "posições atribuídas × evidências agregadas": na
variante canônica, cada autor é representado dizendo o que não disse;
na variante nova, cada autor é citado corretamente, mas o conjunto das
fontes não sustenta empiricamente a afirmação de convergência que o
parágrafo citante faz. Sinais de acionamento em dois vetores —
linguístico (marcadores de convergência/consenso) e estrutural
(heterogeneidade do mosaico de fontes incompatível com a especificidade
da afirmação). Cláusula de fronteira obrigatória: variantes de Dim. 2
estrutura de sustentação argumentativa só são acionadas quando há
descompasso detectável entre o que o texto diz sobre as fontes e o
que as fontes mostram; observações sobre adequação retórica, seleção
editorial do corpus ou qualidade da conclusão normativa ficam fora
da v2.

Motivação. Gatilho empírico do Teste 02 da Fase A.7: detecção
substantiva por dois ambientes executores independentes (Claude.ai
navegador e Claude Desktop), em ângulos distintos, sem acesso à ground
truth — critério clássico de validade de conteúdo. Exemplar
auto-contido na ground truth §4.2 (sete referências × tipo de fonte ×
escopo × validade inferencial), com descompasso visível entre
afirmação de âmbito nacional sobre Ensino Médio público e o perfil do
mosaico de sustentação.

Justificativa condensada. Dupla detecção independente por ângulos
distintos; exemplar auto-contido; distinção genuína frente ao caso
paradigmático (compartilham o eixo dimensional, não se sobrepõem em
conteúdo); implicação operacional acionável via dois vetores
verificáveis. Objeção considerada: custo de fronteira — variante nova
empurra §8.4 para perto da crítica argumentativa genérica, risco de
§8.4 virar catálogo de queixas editoriais disfarçadas de dimensões
taxonômicas. Respondida com a cláusula de fronteira obrigatória, que
preserva o escopo da skill como instrumento de detecção de alucinação
e distorção bibliográfica.

Consequências operacionais. Arquivo tocado: `_taxonomy-v2-design.md`
§8.4 (sub-seção nomeada da variante; definição operacional; sinais de
acionamento; exemplar canônico extraído do Teste 02; regra de
desempate frente à variante canônica; cláusula de fronteira externa
à v2).

Referência cruzada. Documento de deliberação formal em
`<pasta-de-referencias>/skill-development/research/fase-A7-deliberacao-bloco-A.md`
§3.

**20. Registro de "inflação retórica de certeza" e "conclusão normativa
passando como síntese científica" como heurísticas editoriais adjacentes
à v2 (A.7 Bloco A, A2).** As duas variantes propostas pelo Claude
Desktop no Teste 02 da Fase A.7 não são canonizadas no
`_taxonomy-v2-design.md`. Entram no
`hallucination-prevention-checklist.md` com status declarado de
"orientação crítica adjacente à skill, fora do sistema dimensional v2",
em seção dedicada às heurísticas editoriais adjacentes. Parágrafo
explícito imediatamente abaixo da cláusula de fronteira da §8.4 define
o gate de reabertura: canonização futura dessas variantes só com
detecção independente em ambiente distinto (critério empírico da A1)
**e** atendimento à cláusula de fronteira.

Motivação. Gatilho: propostas do próprio Desktop no Teste 02 em ângulo
distinto dos diagnósticos principais. Evidência empírica única, em
ambiente único — sem convergência independente análoga à que
fundamentou a A1. O próprio proponente admite que "Conclusão normativa"
pode "configurar variante adicional de Dim. 2 estrutura, ou ser tratado
fora da v2 como crítica editorial".

Justificativa condensada. Consistência do critério de canonização
entre A1 e A2: detecção isolada não satisfaz a barra de admissão da
A1; relaxá-la aqui criaria inconsistência de critério na mesma saída
arquitetural. As duas variantes cruzam a cláusula de fronteira da A1
(uma é crítica de estilo epistêmico; a outra, crítica de argumentação
normativa); reincluí-las contradiria a decisão recém-tomada. Objeção
considerada: conservadorismo excessivo, dado que o Desktop é o
ambiente mais rigoroso bibliograficamente da rodada. Respondida com
a inconsistência de critério como custo maior que conservadorismo
pontual; o registro no checklist preserva o valor operacional das
heurísticas sem comprometer a arquitetura dimensional.

Consequências operacionais. Arquivos tocados:
`hallucination-prevention-checklist.md` (seção nova de heurísticas
editoriais adjacentes à v2, com duas entradas);
`_taxonomy-v2-design.md` §8.4 (parágrafo sobre o gate de reabertura
abaixo da cláusula de fronteira); `_phase2-handoff.md` (entrada em
"Critérios de reabertura" para A2).

Referência cruzada. Documento de deliberação formal em
`<pasta-de-referencias>/skill-development/research/fase-A7-deliberacao-bloco-A.md`
§4.

**21. Diferimento da canonização do vetor "cadeia probatória interna
contaminada" (A.7 Bloco A, A3) — reabertura de decisão arquitetural
prévia.** O vetor dimensional formalizado na ground truth v1.2 §4.4
do Teste 02 — referência existente verificável com metadados corretos,
cujas afirmações se apoiam em referências internas fabricadas — não é
canonizado na v2 nesta rodada. Registrado como pendência arquitetural
em `_phase2-handoff.md` §(x), com compromisso de teste dirigido no
Teste 03 e protocolo em três passos. A implicação operacional imediata
é capturada pela heurística "verificação meta-bibliográfica cascateada",
regra ativa no `hallucination-prevention-checklist.md` §5.6.

**Nota explícita.** Esta decisão é **reabertura de decisão
arquitetural prévia**, não consideração inicial do vetor. A
possibilidade de canonizar este tipo de erro em cascata foi considerada
na construção original da v2, à luz da literatura existente sobre
cadeias probatórias contaminadas em revisões de literatura, e foi
decidida contra por Sidney na ocasião. O motivo específico de
reabertura é evidência empírica direta nova obtida no Teste 02
(SOARES et al. / ALMEIDA-GOMES, três evidências convergentes de
fabricação documentadas em ground truth v1.2 §3.7), distinta de mera
revisão de argumento prévio.

Motivação. Achado empírico do Desktop no Teste 02 em SOARES et al.,
confirmado em verificação ativa de v1.2 com três evidências
convergentes: formato de numeração impossível na Revista Brasileira
de Educação; zero ocorrências do título na web; iniciais genéricas
sem identificação.

Justificativa condensada. Vetor empiricamente genuíno, mas o
enquadramento taxonômico correto não está fechado — a ground truth
sugere como sub-variante de Dim. 2 conteúdo afirmado e reconhece
explicitamente a possibilidade alternativa de Dim. 4 nova ("integridade
da cadeia probatória interna"). Canonizar com enquadramento
precipitado arrisca distorcer a arquitetura da v2; custo assimétrico
favorece o diferimento (decisão de enquadramento é custosa de
desfazer; adição incremental é barata quando o enquadramento estiver
claro). Implicação operacional imediata capturável via checklist sem
depender da canonização. Objeção considerada: a evidência empírica já
está completa — por que diferir? Respondida com a distinção entre a
existência do vetor (sólida) e o enquadramento taxonômico (em aberto);
canonizar sem fechar é pior do que diferir para fechar com informação
melhor. A intervenção metodológica de Sidney na sessão alterou o
estado epistêmico da pendência de "consideração inicial de vetor novo"
para "reabertura de decisão arquitetural prévia", com exigência
adicional de recuperação e confronto dos argumentos originais contra
canonização no Teste 03.

Consequências operacionais. Arquivos tocados:
`_phase2-handoff.md` §(x) (pendência com histórico de reabertura e
protocolo de três passos); `hallucination-prevention-checklist.md`
§5.6 (heurística ativa de verificação meta-bibliográfica cascateada);
`_phase2-handoff.md` "Pré-condições do Teste 03" e "Critérios de
reabertura".

Referência cruzada. Documento de deliberação formal em
`<pasta-de-referencias>/skill-development/research/fase-A7-deliberacao-bloco-A.md`
§5.

**22. Refinamento da subdistinção Dim. 3 conceitual × factual
(A.7 Bloco A, A4).** A subdistinção entre os dois valores da
Dimensão 3 no `_taxonomy-v2-design.md` §5 recebe quatro elementos
operacionais: (i) pergunta operacional em uma linha como eixo de
distinção — "a distorção é sobre o que a obra diz/argumenta ou sobre
o que a obra mediu/observou/descreveu?"; (ii) exemplares canônicos
contrastados lado a lado (factual: DANTAS et al. 2024, Teste 02;
conceitual: conflação Bourdieu/Foucault em torno do conceito de
biopolítica); (iii) regra de desempate para coocorrência — quando a
distorção atinge simultaneamente posição teórica e metodologia/escopo,
**ambos** os valores de Dim. 3 são acionados em paralelo, sem escolha
entre eles; (iv) heurística anti-padrão: distorção sobre metodologia,
escopo, população ou tipo de achado empírico é factual, mesmo quando
a obra é teórica ou qualitativa e a distorção é sofisticada.

Motivação. Gatilho empírico: fragilidade operacional observada no
Desktop no único caso de acionamento de Dim. 3 na rodada do Teste 02
(DANTAS et al. 2024, ground truth §3.3). O ambiente reconhecido como
o mais rigoroso e mais sistemático dimensionalmente dos dois
classificou como "conceitual" onde a regra v2 e a ground truth
classificam como "factual" — evidência direta de insuficiência
operacional da regra, não de falha do executor.

Justificativa condensada. Erro do Desktop como evidência direta de
fragilidade da regra atual (ambiente mais rigoroso falhando no único
caso disponível é sinal forte sobre a regra); a distinção é menos
intuitiva do que parece, com gravitação previsível para o valor que
soa mais sofisticado ("conceitual") em casos limítrofes; exemplar
canônico já pronto em DANTAS, com contraste empírico claro entre
atribuição e realidade da obra; custo de não refinar alto e silencioso
(Dim. 3 frágil vira ruído em toda rodada futura). Objeções
consideradas: viés retrospectivo, já que a heurística anti-padrão foi
construída sobre o caso DANTAS e o explica perfeitamente — mitigada
declarando o refinamento como baseline revisável à luz do Teste 03 e
rodadas posteriores; prematuridade, dado que Dim. 3 conceitual ainda
não foi acionada empiricamente — respondida com o argumento de que a
alternativa é fragilidade documentada sem ação versus refinamento
parcial com ajuste posterior, sendo a segunda a forma normal de
calibração taxonômica iterativa.

Consequências operacionais. Arquivo tocado: `_taxonomy-v2-design.md`
§5 (pergunta operacional; exemplares contrastados; regra de desempate
para coocorrência; heurística anti-padrão). Dependência com A3
registrada em `_phase2-handoff.md` "Pré-condições do Teste 03"
(Teste 03 precisa produzir exemplar genuíno de Dim. 3 conceitual para
fechar o refinamento com ambos os lados exercidos empiricamente).

Referência cruzada. Documento de deliberação formal em
`<pasta-de-referencias>/skill-development/research/fase-A7-deliberacao-bloco-A.md`
§6.

**23. Ratificação empírica da decisão arquitetural "ground truth como
baseline revisável, não oráculo" (A.7 Teste 02, reclassificação de
MAGALHÃES; ROCHA).** Em 2026-04-22, a classificação canônica da
ground truth v1.0–v1.4 do Teste 02 para MAGALHÃES; ROCHA (pastiche,
com alternativa inexistente-fabricada) foi revogada por verificação
manual externa executada pelo decisor arquitetural (Sidney): o PDF
integral do artigo foi localizado no OJS institucional do Colégio
Pedro II (`portalespiral.cp2.g12.br`), endereço não alcançado pelas
buscas automatizadas em CrossRef/OpenAlex/web anteriores à ground
truth v1.4. A referência é **existente verificável**, de autoria
Rocha; Magalhães (ordem invertida em relação à grafia do
parágrafo-semente), em *Revista Encontros* v. 20 n. 38 (2022), Colégio
Pedro II, sem DOI. Classificação v1.5: Dim. 1 existente verificável;
Dim. 2 duplo acionamento (metadados — ordem de autoria invertida;
conteúdo afirmado — distorção de escopo e tipo de estudo); Dim. 3
factual. A revisão foi aplicada aos quatro documentos do Teste 02
(ground truth; síntese comparativa; duas avaliações do Papel 3),
preservados em v1.4 por convenção archival e atualizados como v1.5
paralelamente.

Esta entrada **não é abertura de decisão arquitetural nova** —
é **ratificação empírica** da decisão original registrada no §1.2 da
ground truth ("princípio de ground truth não-oráculo", herdada da Fase
A.1.5). A cláusula original previa revisão por verificação externa em
magnitude pequena (refinamentos incrementais de metadados e de
enquadramento, exemplificados pelo ciclo CARDOSO; BERTONI em v1.1 a
v1.4). O caso MAGALHÃES; ROCHA validou a cláusula em magnitude maior:
reclassificação de Dim. 1 inteira (pastiche → existente verificável),
com acionamento subsequente de Dim. 2 duplo e Dim. 3 factual. O
mecanismo de revisão incremental por notas de versão absorveu
reclassificação drástica sem contradição interna.

Motivação. Durante a execução do Bloco B da Fase A.7 (incorporação de
heurísticas ao `hallucination-prevention-checklist.md`, em curso em
sessão de Papel 1), a deliberação sobre a heurística B5 (regra de
desempate pastiche × existente-verificável diante de alcance limitado
de busca ativa) aproximou a regra proposta da classificação canônica
da ground truth, produzindo divergência de critério. Sidney resolveu
a pendência por via empírica, executando a verificação manual que a
ground truth v1.4 declarava não ter sido feita. Gatilho empírico, não
gatilho teórico.

Justificativa condensada. A convergência entre dois ambientes do
Papel 2 (Claude.ai navegador e Claude Desktop) em falso positivo de
pastiche para MAGALHÃES; ROCHA, pela mesma rota de fechamento
prematuro sem alcance a OJS institucional, replica o padrão já
documentado em CARDOSO; BERTONI (v1.1/v1.4) e consolida **base empírica
dupla** para a recomendação de maior prioridade operacional da síntese
comparativa (regra R1 de prospecção em portais institucionais). Além
disso, MAGALHÃES; ROCHA adiciona segundo exemplar canônico de Dim. 3
factual ao lado de DANTAS, reforçando o refinamento da decisão 22
(A.7 Bloco A, A4). Objeção considerada: registrar a reclassificação
como decisão arquitetural nova em vez de ratificação empírica de
decisão prévia. Respondida: a cláusula de revisão era pré-existente;
o caso novo a exerce, não a altera. Registrá-la como decisão nova
inflaria o changelog com operação que a arquitetura já previa como
rotina.

Consequências operacionais. Arquivos tocados (fora do repositório da
skill, em `<pasta-de-referencias>\skill-development\test-reports\teste-02-fase-A.7.1\`):
`teste02_ground_truth_2026-04-22_v1.5.md`,
`sintese_comparativa_navegador_vs_desktop_2026-04-22_v1.5.md`,
`avaliacao_claude_navegador_2026-04-22_v1.5.md`,
`avaliacao_claude_desktop_2026-04-22_v1.5.md`. Versões v1.0–v1.4
preservadas por convenção archival (cada versão do Teste 02 coexiste
como arquivo próprio). Implicações para o Bloco B em curso registradas
no documento-registro da reclassificação (§5: B4, B5, B7 reforçadas
por base empírica; B2 "inconsistência temporal interna como sinal de
confabulação" falseada por contra-exemplo direto da própria rodada) —
a incorporação concreta dessas implicações ao
`hallucination-prevention-checklist.md` acontece quando o Bloco B
concluir em sessão de Papel 1.

Pendências derivadas (a registrar em `_phase2-handoff.md` em sessão
subsequente, quando o escopo for reaberto): Dim. 1 pastiche stricto
sensu deixa de estar acionada no Teste 02 após v1.5 (pendência nova,
paralela à de Dim. 3 conceitual, para teste dirigido em rodada
subsequente); tratamento de B2 no Cluster I do Bloco B; verificação
manual pelo decisor como etapa arquitetural formal em Testes 03 e
posteriores (observação arquitetural do §6 do documento-registro).

Referência cruzada. Documento-registro formal em
`<pasta-de-referencias>\skill-development\research\fase-A7-reclassificacao-magalhaes-rocha.md`.

**24. Bloco B — nove heurísticas candidatas deliberadas
(A.7 Fase B).** Seis heurísticas incorporadas ao
`hallucination-prevention-checklist.md`; duas descartadas com
registro de falseamento no `_phase2-handoff.md`; três já haviam sido
absorvidas pelo Bloco A sem ação adicional. Unidade semântica do
Bloco B registrada em entrada única, análoga à decisão 18 (v2
canonizada em ciclo agregado). O desenho de nove candidatas e os
Clusters que as agrupam são produto da deliberação em sessão Papel 1
(Claude navegador) via Sidney, posterior ao Bloco A e anterior à
incorporação concreta pelo Claude Code.

**Incorporadas (seis heurísticas, regras ativas).**

- **B6 (§9.1 do checklist) — desalinhamento agenda-tema não é
  evidência contra existência.** Bloqueio preventivo contra uso de
  adjacência de agenda como argumento auxiliar de classificação em
  pastiche ou inexistente-fabricada. Exemplares empíricos: CARDOSO;
  BERTONI (anais de IC da UESB) e MAGALHÃES; ROCHA (co-autoria
  orientadora–orientanda em ProfEPT). Três configurações regulares de
  desalinhamento legítimo documentadas (co-autoria com orientando;
  incursão temática em períodos de interesse coletivo; docência em
  programas interdisciplinares).
- **B4 (§9.2) — prospecção obrigatória em portais institucionais.**
  Gatilho pelos termos "Anais", "Seminário", "Congresso" etc.;
  exceção para periódicos em fluxo regular com DOI; princípio lógico
  subjacente (não-localização em bases agregadoras ≠ não-existência,
  pela sub-representação estrutural de literatura cinzenta e
  semi-cinzenta brasileira). Dois exemplares empíricos convergentes
  (CARDOSO; BERTONI e MAGALHÃES; ROCHA).
- **B5 (§9.3) — regra de desempate em "indeterminada" diante de
  alcance limitado.** Suspensão do veredito em Dim. 1 quando a busca
  ativa não localiza a referência e pelo menos duas das três
  evidências estão presentes (par autoral real, evento real, veículo
  real). Operacionalização como prática editorial da skill, não como
  quarto valor canônico da v2 (pendência arquitetural derivada
  registrada em `_phase2-handoff.md §(xiv)`). Aplica-se **depois** de
  B4 executada.
- **B7 (§9.4) — ano do volume vs. data OJS vs. ano do evento.**
  Heurística bidirecional sobre publicações institucionais
  brasileiras: direção A (falso positivo em Dim. 2 metadados se data
  OJS é tratada como "erro de ano"; exemplar BOF; MORAES v. 7/2022 com
  OJS 2023-01-02); direção B (subdimensionamento se ano do evento
  entra no lugar do ano dos anais; exemplar inferido CARDOSO; BERTONI
  evento 2025 / anais 2026).
- **B9 (§5.7) — declaração explícita de não-verificação para corpus
  recomendado.** Regra pós-geração para marcação de sugestões
  bibliográficas fora do corpus sob análise; formulação canônica
  sugerida; articulação distinta com B1 (B1 cobre referências
  **dentro** do corpus; B9 cobre **fora**). Lugar em §5 em vez de §4
  decidido durante a execução: paralelismo com §5.3 (literatura
  cinzenta) e §5.5 (declaração de uso de IA), ambas sobre regras de
  marcação no output.
- **B1 (§9.5) — DOI de repositórios abertos sem revisão por pares
  exige verificação da indexação do veículo.** Gatilho por prefixo
  (Zenodo, Figshare, OSF); princípio (resolução do DOI confirma
  depósito, não status editorial); verificação adicional via
  SciELO/LILACS/DOAJ/Qualis CAPES; escalonamento do
  `risco_verificacao` se o veículo não for indexado. Exemplar canônico
  de funcionamento normal: FUZZO et al. (2024), *RevistaFT* com DOI
  Zenodo (veículo indexado, passa pelo fluxo normal).

**Descartadas com registro de falseamento (duas heurísticas).**

- **B2 — "inconsistência temporal interna como sinal de
  confabulação".** Descartada. Contra-exemplo empírico direto na
  rodada que a propôs (MAGALHÃES; ROCHA v1.5): inconsistência
  temporal real no artigo, mas referência existente verificável. Se
  aplicada, produziria o mesmo falso positivo de pastiche que os
  dois ambientes cometeram. Registro em `_phase2-handoff.md §(xi)`
  (convertida de pendência aberta — criada em 2026-04-23 durante a
  propagação de pendências derivadas da reclassificação — para
  descarte resolvido), com critério de reabertura explícito.
- **B3 — "autor com agenda adjacente amplifica risco pastiche".**
  Descartada por dois motivos cumulativos: contradição lógica direta
  com B6 (§9.1) aprovada; contra-exemplo empírico em MAGALHÃES; ROCHA
  v1.5. Registro em `_phase2-handoff.md §(xiii)` novo, com critério
  de reabertura que exige reconciliação explícita com §9.1 em caso
  futuro.

**Já incorporadas pelo Bloco A, sem ação adicional nesta entrada.**
B8 (verificação meta-bibliográfica cascateada) foi canonizada pelo
Bloco A como §5.6 do checklist (decisão 21, A3). B10 (inflação
retórica de certeza) e B11 (conclusão normativa passando como síntese
científica) foram registradas como heurísticas editoriais adjacentes
no §8.1 e §8.2 (decisão 20, A2).

Motivação. Gatilho empírico agregado: o Teste 02 da Fase A.7
produziu fragilidades compartilhadas documentadas em dois exemplares
(CARDOSO; BERTONI e MAGALHÃES; ROCHA) pela mesma rota — fechamento
prematuro da busca sem prospecção de OJS institucional —, com perda
de erros reais em Dim. 1, Dim. 2 metadados e Dim. 2 conteúdo afirmado
por ambiente. A reclassificação de MAGALHÃES; ROCHA (decisão 23) não
apenas validou o padrão como também falseou duas heurísticas
candidatas que emergiram na própria rodada — situação epistemicamente
rica que permitiu canonizar o que sobreviveu e descartar o que foi
falseado em uma só deliberação.

Justificativa condensada. Seis heurísticas com base empírica dupla
ou mecanismo bibliográfico claro (fundamento normativo ABNT em B7;
arquitetura do escudo epistêmico da skill em B9; assimetria de prova
em B5; sub-representação estrutural de literatura cinzenta brasileira
em B4) passam ao checklist. Duas heurísticas falseadas pela própria
rodada vão para o handoff com critério de reabertura, não para o
checklist — o princípio "heurística que nasce com contra-exemplo
dentro da rodada que a propôs parte de lugar epistemicamente frágil"
(primeiro estabelecido no Bloco A na A3 sobre cadeia probatória
interna) opera aqui com força dupla em B2 e B3. Três heurísticas já
absorvidas pelo Bloco A são registradas como tal, sem duplicação.
Objeções consideradas: (i) risco de proliferação de heurísticas na
§9 — respondida com agrupamento em seção dedicada à busca e
prospecção em fontes brasileiras, ordem interna por função
operacional, e com a cláusula de fronteira do §8.6 da taxonomia
impedindo deriva para crítica genérica; (ii) risco de B5
operacionalizar quarto valor de Dim. 1 sem compromisso taxonômico —
respondida com a pendência §(xiv) explícita para reconhecimento
formal posterior; (iii) risco de contradição interna entre B3 e B6
se ambas fossem aceitas — respondida com descarte explícito de B3.

Consequências operacionais. Arquivos tocados na skill:
`hallucination-prevention-checklist.md` (§9 nova com cinco
subseções — §9.1 a §9.5; §5.7 nova; §0 atualizada para descrever
§9); `_phase2-handoff.md` (§(xi) convertida de pendência aberta para
descarte resolvido; §(xiii) nova para B3; §(xiv) nova para classe
indeterminada em Dim. 1).

Referência cruzada. Síntese de execução arquivada em
`<pasta-de-referencias>\skill-development\research\fase-A7-sintese-execucao-bloco-B.md`.
Diferente do Bloco A, o Bloco B não produziu documento-registro de
deliberação separado — a deliberação das nove heurísticas foi
conduzida em sessão Papel 1 e consolidada inline no prompt de
execução enviado ao Claude Code; o arquivo de síntese arquivado
funciona como registro único do Bloco B (rastro deliberativo via
conteúdo do prompt citado + rastro executivo via seções de
implementação).

**25. Declaração de fronteira ortogonal no Passo 0 (A.7 Bloco C,
C1).** A skill passa a declarar explicitamente, no Passo 0 item 1,
quando o tema do material está fora dos quatro domínios canônicos
(saúde coletiva; ciências sociais e humanidades; metodologia e
psicometria; políticas públicas). A detecção opera por heurística
composta sobre os gatilhos declarados na description YAML da skill:
gatilhos de um único domínio presentes com zero dos outros três
acionam classificação automática; gatilhos de dois ou mais domínios
simultaneamente, ou zero gatilhos de qualquer dos quatro domínios,
escalam para pergunta ao pesquisador. O valor possível "fronteira
ortogonal" entra ao lado dos cinco já existentes (quatro domínios
canônicos e misto) como sexto valor do campo. Quando o valor for
fronteira ortogonal, o Passo 0 não pode ser comprimido em linha única
— exige sentença declarativa visível antes do diagnóstico substantivo.
A seção "Módulos de domínio na versão atual" do SKILL.md recebe
parágrafo adicional articulando o caso fronteira ortogonal com a
regra de §5.7 do `hallucination-prevention-checklist.md` (declaração
explícita de não-verificação para corpus recomendado), já que
fronteira ortogonal é a situação em que sugestões bibliográficas
complementares estão mais longe do escudo de verificação ativa.

Motivação. Gatilho empírico do Teste 02 da Fase A.7: ausência
compartilhada de meta-comentário sobre escopo nos dois ambientes do
Papel 2, com correlação observada (N=1 por ambiente) entre ausência
de declaração e sugestões de corpus fora do escudo de verificação
ativa. Fragilidade compartilhada documentada na síntese comparativa
§4.3 e §6.2; recomendação operacional em §7.5 e §9 ponto 6. O Teste
02 cobriu tema educacional, ortogonal aos quatro domínios canônicos
— cenário típico em que a skill pode ser acionada sem que o
pesquisador esteja consciente da fronteira.

Justificativa condensada. Extensão de princípio já presente na seção
"Módulos de domínio na versão atual" (instrução de informar quando
módulo não está implementado), agora integrada ao próprio diagnóstico
do Passo 0 em vez de diluída em seção posterior. A heurística
composta (três ramos) mitiga risco de declaração mecânica — a
classificação automática só dispara quando os gatilhos são
inequívocos; nos casos ambíguos a skill pergunta, preservando o
princípio "detecção reduz fricção, não impõe" da decisão 8.

Limitação declarada. Base empírica unilateral: sem caso em que a
declaração tenha atrapalhado; N=1 por ambiente no Teste 02. A
intervenção é aceita como extensão de princípio pré-existente, não
como inferência estatística sobre frequência de fronteira ortogonal
em corpus futuro.

Consequências operacionais. Arquivos tocados: SKILL.md Passo 0 item 1
(reescrito); SKILL.md seção "Módulos de domínio na versão atual"
(parágrafo adicional); `_phase2-handoff.md §(i)` (sentença nova no
campo "Risco conhecido" registrando mitigação parcial por C1 sem
substituir a implementação dos módulos).

Referência cruzada. Prompt de execução
`prompt-claude-code-bloco-C-2026-04-23.md` em
`<pasta-de-referencias>\Skill\Prompts\`; base empírica em
`sintese_comparativa_navegador_vs_desktop_2026-04-22_v1.5.md` §4.3,
§6.2, §7.5 e §9 ponto 6.

**26. Exteriorização dimensional em modo diagnóstico (A.7 Bloco C,
C2).** A skill passa a exteriorizar o vocabulário dimensional da
taxonomia v2 obrigatoriamente em **modo diagnóstico** — pedido de
parecer, checagem de referências, revisão de texto alheio, análise
de trechos com citações colados pelo pesquisador. **Modo redação**
(fluxo obrigatório de 11 passos) não é afetado; a defesa lá permanece
Regra 6 + matriz de síntese + hard gates, não rotulagem dimensional.
Três sub-regras canonizadas em seção nova do SKILL.md ("Regras de
exteriorização dimensional em modo diagnóstico"):

- **D1 (rotulagem obrigatória).** Toda avaliação de referência deve
  exteriorizar o rótulo dimensional v2 explicitamente. Formato:
  Dim. 1 sempre aplicável; Dim. 2 quando Dim. 1 = existente
  verificável; Dim. 3 quando Dim. 2 = conteúdo afirmado; notação `+`
  de §8.4 para erros em múltiplas dimensões; variantes nomeadas de
  §8.6 quando aplicáveis ao parágrafo citante. Substância e rótulo
  operam juntos: nenhum dos dois isoladamente cumpre D1.
- **D2 (cláusula de incerteza — suspensão).** Linguagem canônica
  "Dim. X suspensa por [justificativa]". Três situações típicas:
  Dim. 1 suspensa por §9.3 do checklist (busca inconclusiva com
  evidências parciais); Dim. 2 suspensa por limite de verificação
  (leitura humana da fonte primária não executada); Dim. 3 suspensa
  por ambiguidade de registro (possível duplo acionamento conceitual
  + factual sem elementos para decidir). Suspensão não é recurso
  default — acionada apenas quando a base é explicitamente
  insuficiente e a suspensão é registrável.
- **D3 (escopo).** Alcança valores terminais de Dim. 1, 2, 3 e
  variantes nomeadas de §8.6. Não alcança heurísticas editoriais
  adjacentes à v2 (§8 do checklist), heurísticas ativas de busca
  (§9 do checklist) nem marcações epistêmicas da Regra 6 (modo
  redação).

Motivação. Gatilho empírico do Teste 02 da Fase A.7: divergência
sistemática entre Claude.ai navegador (substância correta, rótulos
ausentes) e Claude Desktop (rotulagem sistemática) em oito vetores
distintos, documentada em síntese comparativa §4.1. Em fluxo real de
auditoria, a auditabilidade depende do rótulo; análise substantiva
sem rótulo não cumpre a função instrumental da v2.

Linguagem da suspensão. Adotada formulação α: "Dim. X suspensa por
[justificativa]", explicitando o estatuto não-canônico da suspensão
como prática editorial da skill, sem antecipar decisão de
`_phase2-handoff.md §(xiv)` sobre reconhecimento taxonômico formal
de "indeterminada" como quarto valor canônico da Dim. 1. A §(xiv)
permanece aberta, a ser deliberada em sessão própria.

Objeção considerada. Síntese comparativa §4.4 sinaliza que rotulagem
errada pode ser pior que omissão (caso DANTAS no Desktop — Dim. 3
rotulado como "conceitual" onde a regra manda "factual"). Resposta:
C2 e o refinamento A4 da Dim. 3 (decisão 22) são complementares — A4
ataca a **precisão do valor**; C2 ataca a **presença do rótulo**. O
risco de rótulo forçado em contexto de baixo sinal é mitigado
explicitamente pela cláusula de incerteza D2.

Limitação declarada. Base empírica unilateral (N=1 por ambiente;
hipóteses causais H1–H3 da síntese §5.1 não triagadas). Intervenção
aceita como heurística operacional de auditabilidade, não como
inferência estatística sobre a causa da divergência entre ambientes.

Consequências operacionais. Arquivo principal tocado: SKILL.md
(seção nova "Regras de exteriorização dimensional em modo
diagnóstico" com D1–D3, inserida entre a Regra 7 e "Termos
operacionais (glossário mínimo)"). Ajuste colateral:
`_taxonomy-v2-design.md §0` ganha uma frase apontando para D1–D3 no
modo diagnóstico (extensão da cláusula existente sobre "composição
de parecer diagnóstico"). Nenhuma outra intervenção arquitetural;
`hallucination-prevention-checklist.md` não é tocado nesta decisão.

Tamanho do SKILL.md pós-C2: 539 linhas (antes do Bloco C: 397;
acréscimo de 142 — 110 da seção D em C2.1, 18 da reescrita do Passo
0 em C1.1, 13 do parágrafo em "Módulos de domínio" em C1.2). Limite
aspiracional de 500 linhas (boa prática de progressive disclosure)
excedido em 39 linhas. Decisão consciente, não silenciada: a seção D
é **regra de modo operacional de leitura na inicialização**, não
referência auxiliar, e pertence ao corpo do SKILL.md para ser lida
junto com as Regras inegociáveis no disparo da skill. Alternativa
avaliada e rejeitada: mover D1–D3 para `references/diagnostic-mode-
rules.md` com ponteiro no SKILL.md reduziria o arquivo para ~450
linhas, mas reintroduziria o gap de gatilho que a síntese comparativa
§5.1 identificou como hipótese causal H2/H3 da divergência de
exteriorização entre ambientes — leitura sob demanda não garante que
o modo diagnóstico seja lido quando necessário. Vigilância do
crescimento do SKILL.md em blocos futuros e avaliação de
reorganização (via movimentação de material auxiliar como o
glossário, não de regras ativas) registradas em
`_phase2-handoff.md §(xv)`.

Referência cruzada. Prompt de execução
`prompt-claude-code-bloco-C-2026-04-23.md` em
`<pasta-de-referencias>\Skill\Prompts\`; base empírica em
`sintese_comparativa_navegador_vs_desktop_2026-04-22_v1.5.md` §4.1 e
§4.4.

**27. Bloco D da Fase A.7 — registro de hipóteses causais do Teste 02
no handoff (A.7 Bloco D).** Último bloco substantivo da Fase A.7. A
síntese comparativa do Teste 02 §5 (v1.5) identificou dois vetores
sistemáticos de divergência entre Claude.ai navegador e Claude
Desktop — vetor 1 (exteriorização do vocabulário v2) e vetor 4
(classificação Dim. 3 conceitual × factual) — e propôs seis hipóteses
causais (três por vetor), explicitando que nenhuma é testável com
N=1 por ambiente. O Bloco D registra §(xvi) no `_phase2-handoff.md`
cobrindo o vetor 1 (H1, H2, H3) com três vias de fechamento: rodadas
dedicadas executadas; arquivamento formal com critério de reabertura;
reaproveitamento oportunista. O vetor 4 fica endereçado fora de
§(xvi): H4 e H5 pela decisão 22 (refinamento operacional da Dim. 3);
H6 como observação no objetivo (A4) das "Pré-condições do Teste 03",
com referência cruzada bilateral para §(xvi).

Motivação. Gatilho arquitetural: a síntese comparativa do Teste 02
§5 formalizou as seis hipóteses causais sobre divergências
sistemáticas entre ambientes e declarou que a triagem requer rodadas
adicionais. Sem registro formal no handoff, as hipóteses ficariam
presas à síntese como material arquivado, sem gancho arquitetural
para recuperação em Fase 2. O Bloco D delibera sobre o lugar desse
registro.

Justificativa condensada. (i) §(xvi) preserva a unidade do registro
"seis hipóteses da síntese §5" em um ponto de entrada arquitetural,
respeitando a decisão 17 (apontamento-não-duplicação) ao não
reescrever material já coberto pelo changelog. (ii) H6 vai para
"Pré-condições" (A4) porque é ali que será testada — leitor da seção
encontra imediatamente o que observar. (iii) Articulação bilateral
(A4 aponta para §(xvi); §(xvi) aponta para A4) replica o padrão dos
"Critérios de reabertura" (redundância deliberada em dois pontos de
entrada). (iv) Nível de detalhe intermediário (hipóteses listadas,
sem desenho experimental fixado) respeita a função do handoff como
rastreador de pendências, não documento de planejamento experimental.

Decisão sobre o protocolo de verificação pós-hoc. Deliberado e **não
registrado** como pendência dedicada. O rastro nas versões v1.1–v1.5
dos documentos do Teste 02 é suficiente; o eixo "verificação manual
externa pelo decisor" já está coberto por §(xii) (em momento distinto
do protocolo). Registro aqui para rastro da deliberação.

Consequências operacionais. Arquivos tocados: `_phase2-handoff.md`
§(xvi) nova (inserção entre §(xv) e "Pré-condições do Teste 03");
`_phase2-handoff.md` "Pré-condições do Teste 03" objetivo (A4)
atualizado com observação sobre H6 e referência cruzada a §(xvi).
Nenhuma alteração em outros arquivos da skill.

Fase A.7 — estado após o Bloco D. Todos os quatro blocos substantivos
concluídos (A, B, C, D). Próximo passo arquitetural: Teste 03 e/ou
abertura da Fase 2.

Referência cruzada. Síntese comparativa do Teste 02 §5 em
`<pasta-de-referencias>\skill-development\test-reports\teste-02-fase-A.7.1\sintese_comparativa_navegador_vs_desktop_2026-04-22_v1.5.md`.

**28. Arquivamento formal da pendência §(xvi) do `_phase2-handoff.md` via
critério (ii) — divergência de exteriorização v2 não reproduzida em
Passo 1 do Caminho C (A.8).** O vetor 1 da síntese comparativa do Teste
02 §5 (exteriorização do vocabulário v2; hipóteses H1, H2, H3), que
registrava divergência observada entre Claude.ai navegador e Claude
Desktop com N=1 por ambiente, é formalmente arquivado pela via (ii) da
pendência §(xvi) — arquivamento com critério de reabertura, sem
execução do Passo 2 do Caminho C. A §(xvi) permanece no handoff como
registro histórico, marcada como resolvida, com referência cruzada
bilateral a esta decisão.

Motivação. Gatilho empírico: execução do Passo 1 do Caminho C na Fase
A.8 — 10 rodadas baseline (cinco por ambiente, parágrafos-semente
comparáveis ao Teste 02, classificação humana cega inter-ambiente
registrada em
`<pasta-de-referencias>\skill-development\test-reports\caminho-c-fase-A.8\registro-preenchido.xlsx`)
— produziu dados diretamente incompatíveis com a hipótese forte do
Teste 02. A matriz de frequências (aba `resumo`) é
`pleno 2 / parcial 3 / ausente 0`
no navegador e `pleno 3 / parcial 2 / ausente 0` no Desktop, com três
achados convergentes: (i) zero rodadas "ausentes" em qualquer ambiente
— a hipótese de que o navegador não exterioriza o vocabulário v2 está
falseada em observação direta; (ii) diferença de um caso em cinco na
categoria "pleno" entre ambientes, compatível com variação por acaso
com N=5 por grupo; (iii) padrão geral convergente, com maioria em
pleno/parcial e zero em ausente nos dois ambientes.

Justificativa condensada. A divergência observada no Teste 02 foi
**artefato de N=1**, não padrão sistemático — o que a §5.3 da síntese
comparativa já antecipava como risco explícito ao declarar que as seis
hipóteses não eram testáveis com N=1 por ambiente. O desenho do
Caminho C Passo 1 — rodadas baseline comparáveis, classificação cega
inter-ambiente — é a forma mínima suficiente para triar a existência
da divergência sem necessidade de variação de prompt; os três achados
convergem com a conclusão de que o fenômeno não existe como padrão.
Executar o Passo 2 (18 rodadas com variação de prompt para isolar H1,
H2, H3) seria investimento em triagem de hipóteses causais de um
efeito que o Passo 1 mostrou não existir. A via (ii) da §(xvi) — não
investir em rodadas dedicadas, arquivar como "custo de auditabilidade
aceito" — foi precisamente desenhada para este cenário e é acionada
aqui por evidência direta, não por decisão de prioridade de Fase 2.

Critério de reabertura. A pendência §(xvi) pode ser reaberta se, em
qualquer rodada futura (Teste 03, Teste 04, etc.), for observada
divergência sistemática de exteriorização entre ambientes. Divergência
sistemática significa, operacionalmente: **≥3 rodadas consecutivas em
um ambiente classificadas como "ausente"** enquanto o outro ambiente
mantém "pleno" ou "parcial" nas rodadas correspondentes, com **pelo
menos N=5 rodadas por ambiente** observadas no desenho. O critério
articula-se com o padrão dos "Critérios de reabertura" do Bloco A
(redundância bilateral entre entrada do changelog e registro na §(xvi)
resolvida).

Objeção considerada. Conservadorismo estatístico: N=5 por ambiente é
amostra pequena; o Passo 2 ampliaria para N=3 por célula em desenho
3×2, totalizando N=9 por ambiente. Respondida: o Passo 1 já triagem
a questão primária (existe divergência sistemática de exteriorização?)
com zero "ausentes" nos dois ambientes — a hipótese forte do vetor 1
está falseada em dado direto, não apenas não sustentada em dado
ambíguo. Ampliar N para triar hipóteses causais (H1, H2, H3) de um
fenômeno que o dado primário mostra não ocorrer seria refinamento
desenhado sobre base empírica ausente. A resposta correta é arquivar
com critério de reabertura que reativa a investigação se o dado futuro
mostrar o fenômeno, não antecipar investigação de hipóteses causais na
ausência do fenômeno.

Pendência derivada para Fase 2. Achado lateral do Passo 1 do Caminho
C, independente da decisão de arquivamento: a distribuição entre
"pleno" e "parcial" nos dois ambientes (2-3 / 3-2 em cinco rodadas
cada) sugere que o **gatilho para classificação dimensional sistemática
na skill pode ser frouxo** — casos classificados como "parcial"
indicam aplicação incompleta ou irregular do vocabulário v2 mesmo em
rodadas onde ele é invocado. A pendência é sobre a skill (frouxidão
potencial do gatilho de D1–D3 da decisão 26 no modo diagnóstico), não
sobre divergência entre ambientes, e é registrada como §(xvii) nova do
`_phase2-handoff.md`. A decisão de arquivar §(xvi) não depende da
resolução desta nova pendência; são questões distintas que o mesmo
material empírico permitiu separar.

Consequências operacionais. Arquivos tocados: `_phase2-handoff.md`
§(xvi) (marcada como resolvida via critério (ii), com subcabeçalho
"Resolução (2026-04-24)" remetendo a esta decisão; texto original
preservado); `_phase2-handoff.md` §(xvii) nova (pendência derivada
sobre frouxidão do gatilho dimensional). Nenhuma alteração em
`SKILL.md` ou nos módulos funcionais da skill — a decisão é
arquitetural/documental. Artefato empírico local, fora do controle
de versão do repositório da skill (pasta de referências externa ao worktree):
`<pasta-de-referencias>\skill-development\test-reports\caminho-c-fase-A.8\registro-preenchido.xlsx`.

Referência cruzada. `_phase2-handoff.md §(xvi)` resolução;
`_phase2-handoff.md §(xvii)` pendência derivada; planilha de registro
do Caminho C Passo 1 (aba `resumo` e rodadas individuais) em
`<pasta-de-referencias>\skill-development\test-reports\caminho-c-fase-A.8\registro-preenchido.xlsx`.

**29. Execução formal do passo 2 do protocolo de §(x) — recuperação
dos argumentos originais contra canonização do vetor "cadeia
probatória interna contaminada" (A.8, pós-arquivamento de §(xvi)).**
O passo 2 do protocolo de três passos registrado em
`_phase2-handoff.md §(x)` — recuperação em forma registrada e
confronto explícito dos argumentos originais que levaram à decisão
contra canonização do vetor na Fase A.1 — é formalmente executado
e fechado. Os argumentos foram recuperados em três pontos canônicos
dos documentos-fonte da v2 (`_taxonomy-v2-design.md` §2.2 e §11;
`fase-A1-manuscrito-taxonomia-v2.md` §3.5) e consolidados em
documento-registro dedicado
(`<pasta-de-referencias>\skill-development\research\fase-A8-recuperacao-argumentos-cadeia-probatoria.md`).
O passo 3 do protocolo (confronto entre evidência empírica do Teste
03 e os argumentos originais) permanece pendente da execução do
Teste 03.

Motivação. Gatilho procedimental: o protocolo de §(x) exige
recuperação e confronto dos argumentos originais como pré-requisito
do passo 3; a decisão 21 advertiu explicitamente que "se os
argumentos originais não estiverem em forma registrada, o custo de
recuperação por reconstrução pode ser alto". A busca em documentos
canônicos e em conversas arquivadas da Fase A.1 confirmou que os
argumentos estão registrados em três fontes distintas — regra
formal de quatro critérios cumulativos em `_taxonomy-v2-design.md`
§2.2; justificativa específica do descarte da categoria Cascatas
sistêmicas e gate de reentrada em `_taxonomy-v2-design.md` §11;
fundamentação ampliada em `fase-A1-manuscrito-taxonomia-v2.md`
§3.5. Recuperação foi possível sem reconstrução argumentativa.

Categoria. Esta entrada é **execução formal de protocolo prévio**,
não decisão arquitetural substantiva nova — análoga em estatuto à
decisão 23, que foi rotulada como ratificação empírica de princípio
prévio. A entrada registra que o passo 2 foi cumprido e especifica
o baseline contra o qual o passo 3 será executado no Teste 03.

Justificativa condensada. O documento-registro consolida três
elementos operacionais contra os quais o passo 3 precisa confrontar
a evidência empírica do Teste 03: (i) regra de §2.2 do
`_taxonomy-v2-design.md` com quatro critérios cumulativos para
admissão de eixos candidatos (ganho demonstrável; custo compatível;
não redundância; orientação corretiva distinta); (ii) justificativa
específica do descarte de Cascatas sistêmicas em §11 — restrição de
unidade de análise, v2 opera item por item enquanto cascatas exigem
rede; (iii) gate explícito de reentrada registrado em §11 —
canonização de Cascatas "reentra quando a skill incorporar camada
de análise de co-citação em corpora de revisões; tal camada opera
acima da v2, não como substituta". O documento também precisa a
distinção entre "item-por-item estendido" e "dupla-referência-em-
relação", estabelecendo que depth-1 (inspeção do interior de uma
referência citante) não é extensão natural da unidade de análise
atômica da v2, mas introdução de unidade composta — categoria que
estruturalmente pertence à família Cascatas, ainda que em
profundidade 1. Consequência operacional para o passo 3: a
evidência empírica do Teste 03 precisa superar cada um dos três
elementos, não apenas o primeiro, para sustentar canonização.

Consequências operacionais. Arquivo tocado: `_phase2-handoff.md
§(x)` (subcabeçalho novo "Execução do passo 2 (2026-04-24)"
remetendo à presente decisão e ao documento-registro; texto
original da §(x) preservado, com nota análoga em estilo à
"Resolução (2026-04-24)" de §(xvi)). Nenhuma alteração em
`SKILL.md`, `_taxonomy-v2-design.md`, `hallucination-prevention-checklist.md`
ou demais módulos funcionais da skill — esta é execução de
protocolo, não refatoração. Sem regeneração de zip de distribuição.
Artefato fora do controle de versão do repositório da skill
(pasta de referências externa ao worktree):
`<pasta-de-referencias>\skill-development\research\fase-A8-recuperacao-argumentos-cadeia-probatoria.md`.

Referência cruzada. `_phase2-handoff.md §(x)` (pendência arquitetural,
histórico de reabertura e protocolo de três passos); `_changelog.md`
decisão 21 (diferimento original, A.7 Bloco A, A3);
`_taxonomy-v2-design.md` §2.2 (regra de decisão para extensões) e
§11 (eixo Cascatas sistêmicas descartado, com gate de reentrada);
`fase-A1-manuscrito-taxonomia-v2.md` §3.5 (eixos alternativos
considerados e descartados); `hallucination-prevention-checklist.md`
§5.6 (heurística operacional "verificação meta-bibliográfica
cascateada", cobertura operacional ativa do vetor).

**30. Fechamento da Frente 2 do roadmap v3.4 (Teste 03 / Fase A.7.2).**
Entrada agregada que registra o fechamento da Frente 2 do roadmap
v3.4, executado em 2026-04-25 com Papel 1b (Gemini), Papel 2 em
incognito-duplo (Claude.ai navegador Incognito + Claude Desktop
Incognito) e Papel 3 (síntese comparativa). Seis subdecisões
substantivas registradas, com separação explícita entre **decisões
arquiteturais** que alteram a taxonomia ou estrutura da skill
(30.2, 30.3, 30.4), **decisão de pesquisa** sobre canonização do
exemplar empírico (30.1), e **observações operacionais** sobre
plataforma e casos de estudo (30.5, 30.6). A canonização do
exemplar A3 é decisão de pesquisa, não arquitetural — registra a
absorção de evidência empírica sob o vetor já coberto pela
heurística meta-bibliográfica cascateada (decisão 21 + §5.6 do
checklist), sem reestruturação da taxonomia.

Data: 2026-04-25.
Escopo: arquitetural + canonização + atualizações de skill.
Referência canônica: ground truth v2.0 do Teste 03 fixado em
2026-04-25, em
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`.

**Subdecisão 30.1 — Canonização do exemplar A3 do Teste 03 (decisão
de pesquisa, não arquitetural).** O exemplar A3 do Teste 03 é
canonizado, com particularidade explícita registrada: vetor "cadeia
probatória interna contaminada com refs internas fabricadas em
**múltiplas revisões**" (Campos et al. 2021 com Oliveira 2017
interna; Tavares & Camurça 2004 com Santos 1998 interna), em
expansão do exemplar do Teste 02 (SOARES et al. / ALMEIDA-GOMES) que
operava em revisão única. As três pré-condições do passo 2 da
decisão 29 são superadas em ambos os ambientes do Papel 2:
acionamento explícito de §(xii) com prioridade alta/máxima sobre
Oliveira 2017 e Santos 1998 (regra formal §2.2); articulação por
que paráfrase via revisão é insustentável sem auditar cadeia interna
(justificativa de descarte §11); recomendação concreta de
reabilitação ou descarte em ambos os papéis 3 (gate de reentrada
§11). A canonização é decisão de pesquisa porque absorve evidência
empírica sob vetor já coberto operacionalmente — não modifica a
taxonomia v2 nem cria categoria nova; o vetor permanece como
heurística operacional ativa em §5.6 do
`hallucination-prevention-checklist.md`. Resolução da pendência
§(x) do `_phase2-handoff.md` aplicada como subcabeçalho "Resolução
A3 (2026-04-25)" análogo em estilo às resoluções anteriores.

**Subdecisão 30.2 — Subtipo formal "Dim. 1 fabricação com
identificador colidido" (arquitetural).** Novo subtipo formal de
Dim. 1 incorporado ao `_taxonomy-v2-design.md` §8 (subseção §8.7
nova). Definição: referência fabricada cujo DOI, ISSN, ISBN ou outro
identificador estável **resolve para artigo, livro ou periódico real
distinto**, gerando ilusão de existência verificável quando o
identificador é consultado isoladamente. Distingue-se de pastiche
stricto sensu (que combina autor real com título/periódico fabricados
em padrão lexical canônico, sem identificador resolvível) e de
fabricação simples (identificadores não-resolvíveis ou ausentes) por
ter identificador resolvível mas para entidade distinta da
referência citada. Detecção depende de §(xii) com confronto de
metadados completos (autor, título, periódico, volume, número,
páginas, ano) — a ação corretiva não pode parar na resolução do
DOI. Exemplar canônico: **Silva & Lopes (2020)** no Teste 03 — DOI
10.1590/s0102-6992-202035020008 resolve em CrossRef para artigo
real distinto (SILVA, R. A. da. "Para além do Estado: Marx, Lenin
e a crítica da estatalidade", *Sociedade e Estado* v.35 n.2
p.553-579, 2020). A canonização opera o critério (d) de §2.2
(orientação corretiva distinta) — o subtipo orienta operação de
verificação distinta dos demais subtipos Dim. 1.

**Subdecisão 30.3 — Subvariante "convergência fabricada entre
autores de correntes vizinhas / aplainamento de heterogeneidade
interna" (arquitetural).** Nova subvariante de Dim. 2 estrutura de
sustentação argumentativa incorporada ao `_taxonomy-v2-design.md`
§8.6, ao lado das duas variantes pré-existentes (conflação teórica
fabricada entre autores de correntes divergentes — caso canônico;
agregação para fabricação de convergência empírica — variante A.7).
Definição: tratamento de autores que partilham vinculação
institucional, diálogo acadêmico ou apresentação conjunta na
bibliografia, **mas operam em chaves teóricas distintas**, como se
fossem interlocutores naturais de tradição unificada — produzindo
aplainamento de heterogeneidade interna. Distinta da conflação
Dim. 3 stricto sensu (que opera entre tradições divergentes —
Bourdieu × Foucault, Connell × Butler, Bardin × Minayo); aqui a
vizinhança é real e o vício está na supressão das divisões
internas. Exemplar canônico: **par Magnani × Velho** (A4 do
Teste 03), em que vizinhança institucional (antropologia urbana
brasileira) e diálogo acadêmico são reais, mas a complementaridade
metodológica declarada no parágrafo-semente é fabricada. Detecção
via Regra 5 do `SKILL.md` (marcador de contraste obrigatório).
Reclassifica o fenômeno A4 do Teste 03 de Dim. 3 conceitual stricto
sensu (expectativa do ground truth v1.0) para Dim. 2 estrutura de
sustentação. Regra de desempate de §8.6 ampliada para três
variantes em vez de duas.

**Subdecisão 30.4 — Regra nominal "verificação ativa de
conceitos-âncora canônicos mobilizados via apud" (arquitetural).**
Regra nominal incorporada ao `epistemic-tagging-rules.md` §8 (nova
seção). Cobre vetor de risco identificado como **falso negativo
material da camada 4 do A4 no Teste 03** — atribuição cruzada de
"olhar de perto e de dentro" (conceito magnaniano) a Velho via
Tavares & Camurça apud. Vetor não detectado por nenhum dos dois
ambientes do Papel 2; o Desktop chegou a propagar o erro. Regra:
sempre que conceito-âncora canônico aparecer mobilizado via apud
em material auditado, acionar §(xii) com prioridade alta para
verificação da atribuição autoral em fonte primária, ainda que a
citação apud esteja corretamente estruturada e a fonte secundária
seja existente verificável. Catálogo inicial inclui Magnani
(pedaço, mancha, trajeto, circuito, pórtico, "olhar de perto e de
dentro") e Velho (campo de possibilidades, projeto, trajetória,
metamorfose, "observando o familiar", antropologia interpretativa);
expansível conforme casos forem detectados em testes futuros.
Acopla-se à subvariante 30.3 quando o conceito-âncora é mobilizado
via apud para autor da mesma vizinhança acadêmica.

**Subdecisão 30.5 — Variante metodológica "incognito-duplo"
registrada como válida (observação operacional).** A operação dos
dois ambientes do Papel 2 em modo Incognito simultâneo (Claude.ai
navegador Incognito + Claude Desktop Incognito) é variante
metodológica válida, registrada em `_phase2-handoff.md` §(xviii).
A diferença observada entre os dois ambientes é atribuível a (i)
cliente, (ii) eventuais diferenças de pipeline de processamento de
skills, (iii) variabilidade estocástica — **não** a presença/
ausência de memória persistente. Validação empírica: cobertura não
comprometida no Teste 03 (10 de 11 vetores planejados detectados em
ambos os ambientes do Papel 2). Recomendação para testes futuros
(Frente 3 ou subsequentes): decidir explicitamente, na fase de
**desenho** do teste, se incognito-duplo (objetivo: isolar
diferenças entre clientes sem confundir com instalação) ou
incognito + Settings (objetivo: comparar instalação completa) é a
variante a operar. A escolha é de desenho, não de execução. Esta
subdecisão é observação operacional sobre plataforma — análoga em
estatuto às convenções operacionais sobre Claude Desktop e
Filesystem MCP do `CLAUDE.md` —, não decisão arquitetural sobre a
taxonomia.

**Subdecisão 30.6 — Caso reflexivo "skill manifestando o risco que
cataloga (§4.2)" registrado em CLAUDE.md (observação operacional).**
Manifestação concreta no Teste 03: o Claude Desktop Incognito, ao
detectar pastiche stricto sensu de Magnani (2011) corretamente,
identificou a obra-fonte real do pastiche (Magnani 2005 — "Os
circuitos dos jovens urbanos") mas atribuiu erradamente o veículo
da obra-fonte: afirmou que a obra foi publicada em *Horizontes
Antropológicos*, quando o veículo correto é ***Tempo Social*** v.17
n.2, 2005. Mecanismo: intrusão da memória paramétrica do agente
subjacente operando sob a skill, exatamente o vetor contra o qual
§4.2 do `hallucination-prevention-checklist.md` alerta. A memória
paramétrica acertou no diagnóstico (reconheceu o pastiche e
identificou a obra-fonte) mas errou no detalhe de metadado
(veículo). Significado: a skill, operando sobre material que testa
a própria skill, manifestou o vetor de risco que ela cataloga —
caso reflexivo no sentido forte. Lição operacional: verificação
ativa deve sempre exceder a memória paramétrica do agente; §(xii) é
o protocolo de fechamento desse vetor, não detalhe opcional. A
Subdecisão 30.4 endereça vetores cognatos. Esta subdecisão é
observação operacional sobre comportamento da plataforma, não
decisão arquitetural sobre a taxonomia — segue a convenção de
decisão 16 (separação entre decisão arquitetural e convenção
operacional).

Consequências operacionais. Arquivos tocados:
`_taxonomy-v2-design.md` §0 (mapa de consulta seletiva), §8.6
(três variantes em vez de duas, com nova subvariante; regra de
desempate ampliada), §8.7 nova (subtipo "fabricação com
identificador colidido"); `epistemic-tagging-rules.md` §0 (mapa
estendido) e §8 nova (regra nominal de verificação via apud com
catálogo inicial expansível); `_phase2-handoff.md` §(vii)
(sincronização do recorte de memórias ativas; resolução da memória
`project_sync_handoff_memory_list.md`), §(x) (resolução A3 com
canonização do exemplar do Teste 03), §(xviii) nova (registro do
incognito-duplo como variante metodológica válida); `CLAUDE.md`
(seção nova "Casos reflexivos sobre a operação da skill" com o
caso §4.2 reflexivo); roadmap v3 (versão 3.6, fechamento da Fase
A.9 / Frente 2; Frente 3 = Fase 4 marcada como aguardando
abertura). Organização da pasta de test-reports: nova pasta
`teste-03-fase-A.7.2/` na pasta de referências com cinco arquivos prefixados
numericamente (`01-` a `05-`) refletindo a ordem lógica do teste;
nenhum arquivo `.md` solto em `test-reports/`. Sem regeneração de
zip de distribuição — `SKILL.md` não foi tocado nesta entrada.

Referência cruzada. Ground truth v2.0 do Teste 03 §7 (cinco
decisões candidatas) e §8 (veredito sobre canonização do A3) em
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`;
síntese comparativa Desktop × navegador em
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\04-sintese-comparativa-desktop-navegador.md`;
roadmap v3 versão 3.6 §A.9 (bloco "Subdecisões da Fase A.9"
correspondente).

**31. Fechamento da Frente 3 do roadmap v3.4 (Fase 4 —
Infraestrutura completa, subset prioritário).** Entrada agregada
que registra o fechamento da Frente 3 do roadmap v3.4, executado
em 2026-04-25 com Claude Code (execução), Claude navegador
(auditoria via Sidney) e Sidney (decisor final). Cinco subdecisões
substantivas registradas, com separação explícita entre
**componentes operacionais** (31.1, 31.2, 31.3), **decisão
arquitetural** (31.4) e **decisão de escopo** com critério de
reabertura (31.5). A canonização opera dentro do escopo herdado da
pendência §(iii) do `_phase2-handoff.md` (scripts Python como hard
gate) e do princípio metodológico da decisão 18 (exemplares
acadêmicos da skill servindo também como testes operacionais).

Data: 2026-04-25.
Escopo: implementação + canonização + atualizações de skill.
Referência canônica: plano canônico em
`<pasta-de-referencias>\skill-development\research\fase-4-deliberacao-frente-3.md`.

**Subdecisão 31.1 — `doi_verify.py` canonizado (componente
operacional).** `scripts/doi_verify.py` implementado como hard
gate de verificação de DOI. Recebe DOI(s) como argumento e retorna
um dos seis estados:

- **`OK`** — DOI resolve em CrossRef e metadados (autores, ano,
  título, periódico, volume, número, páginas) batem com referência
  fornecida acima do threshold de fuzzy matching definido pelo
  script.
- **`MISMATCH`** — DOI resolve mas metadados divergem (subtipo da
  Sub-30.2 — fabricação com identificador colidido).
- **`NOT_FOUND`** — DOI não resolve em CrossRef nem em fallback
  OpenAlex.
- **`NO_DOI`** — referência fornecida sem DOI; estado documentado
  conforme decisão 4 do `_changelog.md` (declaração explícita de
  limitação no output, não pular silenciosamente).
- **`RETRACTED`** — DOI resolve mas a publicação está marcada como
  retratada (CrossRef `update-nature` / `relation` /
  `crossmark-restriction`; fallback OpenAlex `is_retracted`).
  Verificação cross-source: ambas as fontes são consultadas mesmo
  quando CrossRef resolve, porque CrossRef pode silenciar retração
  que OpenAlex flagra (caso forte: Wakefield 1998 — CrossRef
  prefixa o título com "RETRACTED:" mas não expõe campo
  estruturado consultado pelo script; OpenAlex `is_retracted=true`
  pegou).
- **`ERROR`** — falha de rede, timeout ou erro de API.

Threshold de fuzzy matching: `COMPOSITE_OK_THRESHOLD = 75/100`,
com pesos `authors 0.30 / title 0.40 / journal 0.15 / year 0.10 /
pages 0.05` (renormalizado quando `pages` ausente em metadados
esperados). Calibrado contra Silva & Lopes 2020 da Sub-30.2 — DOI
`10.1590/s0102-6992-202035020008` resolve em CrossRef para artigo
real distinto (SILVA, R. A. da. "Para além do Estado: Marx, Lenin
e a crítica da estatalidade", *Sociedade e Estado* v.35 n.2
p.553-579, 2020); composite score observado 54.6, abaixo de 75 →
`MISMATCH`. Casos legítimos pontuam 94.6–99.4 → `OK`.
Justificativa empírica completa documentada na docstring do
módulo.

Cobertura empírica: Suíte A da bateria de teste — sete casos do
corpus visível do Teste 03 + um caso sintético de retratação
(Wakefield et al. 1998, DOI `10.1016/S0140-6736(97)11096-0`).
8 de 8 casos passam após reclassificação empiricamente
fundamentada de Ferreira 2023 (registro do achado lateral em
§(xix) do `_phase2-handoff.md`).

CLI: aceita `.bib`, `.json` de fixtures ou `--doi` único como
entrada; retorna relatório em `.json` ou `.md`. Docstring com
exemplos. User-Agent CrossRef com e-mail de contato conforme
convenção da API (lido da variável de ambiente `CROSSREF_MAILTO`). Paralelismo via
`concurrent.futures.ThreadPoolExecutor(max_workers=16)` (analogia
ao padrão `--transfers 16` do rclone) — escolha documentada na
docstring do módulo.

Cita: decisão 4 (carimbo de confiança / `data_ultima_verificacao`);
decisão 30 Sub-30.2 (subtipo "fabricação com identificador
colidido") e Sub-30.4 (regra nominal de verificação ativa);
§(iii) e §(xii) do handoff; memória
`project_doi_verify_retraction_check.md` (estados de retorno e
fallback OpenAlex).

**Subdecisão 31.2 — `bib_consistency.py` canonizado (componente
operacional).** `scripts/bib_consistency.py` implementado como
hard gate de verificação de consistência citação ↔ entrada
bibliográfica. Recebe `.bib` + texto fonte (`.md` ou `.docx`) e
retorna um dos quatro estados por elemento auditado:

- **`OK`** — citação no texto tem entrada correspondente no `.bib`
  e vice-versa.
- **`ORPHAN_CITATION`** — citação aparece no texto mas não há
  entrada correspondente no `.bib` (alvo direto da Sub-30.1 —
  refs internas fabricadas dentro de paráfrases).
- **`UNCITED_REFERENCE`** — entrada no `.bib` não é referenciada
  em nenhuma citação do texto.
- **`APUD_ONLY`** — citação aparece exclusivamente via apud sem
  entrada primária correspondente (alvo do vetor §(xii) e da
  Regra 2 ABNT NBR 10520). **Decisão de granularidade tomada**:
  `APUD_ONLY` mantido como categoria distinta (não subsumido em
  `ORPHAN_CITATION`). Justificativa em três pontos da docstring:
  ação corretiva diferente (apud orphan exige reincorporação da
  obra primária via NBR 10520, não verificação ativa de
  existência); cobertura arquitetural existente nominal (§(xii) e
  Sub-30.4); custo de complexidade marginal compensado pelo ganho
  de auditabilidade.

Estratégia de matching bidirecional via canonical keys
(surname[s] + year), independente de convenção de entry ID —
robusta a `.bib` gerados por Better BibTeX, Zotero, ou qualquer
outro gerenciador.

Cobertura empírica: Suíte B da bateria de teste — quatro casos do
Teste 03 + um caso sintético `UNCITED_REFERENCE` (Bourdieu 1979,
em variante `referencias-com-nao-citada.bib`). 21 de 21
verificações passam através dos 5 sub-casos. Casos fortes:
Oliveira 2017 e Santos 1998 internas (`ORPHAN_CITATION`).

Biblioteca de parsing escolhida: `bibtexparser >= 1.4, < 2`. A
série 2.x permanecia em alpha/beta em 2026-04 com mudanças de API
entre point releases (notavelmente reescrita do writer e modelo
Library/Block/Failed-Block); a série 1.4.x é estável e
battle-tested para a superfície usada (entry parsing, acesso a
campos). Justificativa documentada em `scripts/requirements.in` e
na docstring do módulo.

CLI: aceita `.bib` + texto fonte como entrada e retorna relatório
em `.json` ou `.md`. Bidirecionalidade da verificação documentada
na docstring.

Cita: decisão 30 Sub-30.1 (canonização do exemplar A3 — refs
internas fabricadas em múltiplas revisões) e Sub-30.4 (regra
nominal de verificação ativa via apud); §5.6 do
`hallucination-prevention-checklist.md` (heurística
meta-bibliográfica cascateada); §(iii) e §(xii) do handoff.

**Subdecisão 31.3 — Zotero MCP integrado (componente
operacional).** Zotero MCP (`zotero-mcp-server` v0.3.0, instalado
via `pipx`) configurado no Claude Desktop em modo **API local**
(variável de ambiente `ZOTERO_LOCAL=true`, sem credenciais
persistidas no `claude_desktop_config.json`). Better BibTeX
(instalado na Fase 0.3) permanece como fonte canônica de `.bib` —
citation key `auth.lower + year + title.lower.select(1,1).lower`.

**Decisão arquitetural lateral**: a opção pela API local é
canônica para a skill enquanto o uso for em máquina única. Web API
(`zotero-mcp setup --no-local --api-key K --library-id L`) fica
adiada para frente futura, com critério de reabertura: cenário de
operação multi-máquina, Zotero remoto, ou demanda explícita de uso
sem Zotero rodando localmente.

**Particularidade operacional**: a edição efetiva da entrada
`zotero` em `claude_desktop_config.json` foi via inserção manual
(Claude navegador escreveu em pasta acessível ao seu sandbox;
Sidney copiou para `%APPDATA%\Claude\` via PowerShell), não via
`zotero-mcp setup`. O setup automatizado v0.3.0 falhou
silenciosamente em persistir a edição — causa raiz não
diagnosticada conclusivamente; o relato do Claude Code foi
baseado em exit code e output do subprocesso, não em inspeção do
arquivo (sandbox do filesystem MCP do Claude Code não alcança
`%APPDATA%\Claude\`). O caso é registrado como reflexivo no
`CLAUDE.md` "Casos reflexivos sobre a operação da skill" —
"Claude Code reportando edição fora do sandbox sem inspeção do
arquivo (Frente 3 / Fase 4)" — e motivou a convenção operacional
nova "Sandbox do Claude Code para edições de configuração de
sistema" registrada em paralelo no `CLAUDE.md`. O estado canônico
final do `mcpServers` está documentado em
`scripts/SETUP-ZOTERO-MCP.md`.

Convenção UTF-8 sem BOM do `claude_desktop_config.json` preservada
(verificada antes e depois da edição); convenção crítica herdada
da decisão de Filesystem MCP da Fase 2. Padrão da entrada
`zotero` diverge do `cmd /c npx` do Filesystem MCP — usa caminho
absoluto do executável `.exe` instalado por pipx em
`%USERPROFILE%\.local\bin\zotero-mcp.exe`, com `\\` escapados
em JSON, mais variável de ambiente `ZOTERO_LOCAL=true`.

Teste funcional de fechamento: prompt "quantos itens tenho no
Zotero?" no Claude Desktop retornou a contagem real de itens da
biblioteca, confirmando o ciclo end-to-end. Filesystem MCP segue
funcional após a edição.

Configuração de busca semântica adiada via flag
`--skip-semantic-search`, aderente ao princípio just-in-time.
Ativação tardia documentada em `scripts/SETUP-ZOTERO-MCP.md`
(`zotero-mcp setup --semantic-config-only` + `zotero-mcp
update-db`); reabertura prevista para Fase 5 (módulo de domínio
prioritário) ou demanda real.

Cita: Fase 0.3 do roadmap (Zotero 7 instalado, Better BibTeX
configurado); Fase 2 do roadmap (Filesystem MCP — UTF-8 sem BOM
como convenção operacional crítica); seção "Convenções
operacionais" e "Casos reflexivos sobre a operação da skill" do
`CLAUDE.md` (sandbox do Claude Code para edições de configuração
de sistema; caso reflexivo da Frente 3).

**Subdecisão 31.4 — Bateria de teste empírica derivada do Teste
03 como suite de regressão permanente (decisão arquitetural).**
Princípio canonizado: **exemplares canonizados de testes da skill
(Teste 02, Teste 03 e subsequentes) viram suite de regressão
permanente dos scripts da infraestrutura**. Aplicação direta do
princípio metodológico da decisão 18 (exemplares acadêmicos
servindo também como testes operacionais — aplicação integral dos
marcadores antes da classificação final).

Operacionalização imediata: Suíte A (`doi_verify.py`, 8 casos) e
Suíte B (`bib_consistency.py`, 5 sub-casos via 2 fixtures)
derivadas do Teste 03; fixtures vivem em
`scripts/tests/teste03_doi_verify_cases.json` e
`scripts/tests/teste03_bib_consistency_fixtures/`. Cada exemplar
canonizado em decisão 30 Sub-30.1 (Oliveira 2017 e Santos 1998
internas → `ORPHAN_CITATION`) e Sub-30.2 (Silva & Lopes 2020 →
`MISMATCH`) é caso de regressão direta.

**Critério de expansão**: cada Teste futuro com vetores não
cobertos pela bateria atual produz casos novos a serem
incorporados às suítes existentes ou a suítes novas, conforme a
tipologia do vetor empírico. A própria Frente 3 já produziu o
primeiro caso adicional emergente: o achado de Ferreira 2023 como
segundo exemplar de DOI colidido (registrado em §(xix) do
handoff; deliberação para incorporação à Sub-30.2 ou expansão do
exemplar canônico fica adiada para frente dedicada).

Distinção em relação à Sub-30.5 (incognito-duplo) e Sub-30.6
(caso reflexivo do Teste 03): aquelas são observações
operacionais sobre plataforma; esta é decisão arquitetural sobre
**estrutura de manutenção** — como a skill incorpora aprendizado
empírico em sua infraestrutura, não achado pontual sobre cliente
ou comportamento de agente.

Cita: decisão 18 (princípio metodológico emergente); decisão 30
Sub-30.1 e Sub-30.2 (exemplares fonte das Suítes A e B); §(iii)
do handoff.

**Subdecisão 31.5 — Adiamento explícito de componentes
não-prioritários (decisão de escopo).** Adiados de forma
explícita, com critério de reabertura registrado:

- **`style_formatter.py`** — depende de §(iv) do handoff
  (`bibliographic-styles/` específicos: Vancouver, ABNT 6023/10520,
  APA 7); criar antes dos módulos de estilo é programar contra
  superfície indefinida.
- **`openalex_search.py` standalone** — utilitário de descoberta;
  OpenAlex entra como fallback interno do `doi_verify.py`
  (verificação de existência + `is_retracted`), suficiente para o
  estado atual; standalone fica para frente futura quando demanda
  de descoberta autônoma surgir.
- **PubMed MCP, Crossref MCP** — utilitários de descoberta; HTTP
  direto via `requests` no `doi_verify.py` é suficiente para o
  hard gate; MCPs entram quando demanda de descoberta interativa
  via Claude Desktop emergir.
- **Demais utilitários de descoberta** (`zotero_extract`,
  `scielo_search`, `lexml_search`, `camara_senado_search`) — fora
  do hard gate; entrada por demanda dirigida.

Justificativa: hierarquia hard gate vs. utilitário (§(iii) do
handoff); `style_formatter` depende de §(iv); descobertas
dependem de demanda real (just-in-time da Fase 5 — módulo de
domínio prioritário; ou Fase 6 — primeiro projeto real).

**Critério de reabertura**: demanda de projeto real (Fase 6) ou
Fase 5 que envolva domínio com necessidade de descoberta
automatizada (saúde coletiva — PubMed; ciências sociais —
SciELO; políticas públicas — LexML/Câmara/Senado).

Cita: §(iii) do handoff (hard gate vs. utilitário); §(iv) do
handoff (módulos de estilo); roadmap v3.6/v3.7 Fases 4.2 e 5
(just-in-time).

## Pendências para Fase 2 — detalhes em `_phase2-handoff.md`

Módulos de domínio; templates de matriz; scripts de verificação; módulos de
estilo; propagação de (d) intra; coluna `data_ultima_verificacao` no
SKILL.md; memórias ativas.
