# Desambiguação universal de autores

## 0. Quando consultar este documento

Este arquivo é consultado em três momentos:

1. **Pré-geração** (§3 do checklist): ao validar o BibTeX, qualquer
   entrada cujo primeiro autor tenha sobrenome na lista §2 exige
   desambiguação antes de qualquer prosa.
2. **Durante T2** (template argumentativo, agregação de autores em
   evidência): ao parafrasear ou agregar autores com sobrenomes
   comuns, confirmar identidade pela protocolo §3.
3. **Na construção da matriz de síntese**: a coluna `autores` deve
   identificar a pessoa (via ORCID ou outro identificador), não
   apenas o sobrenome.

A regra 3 do SKILL.md ("zero conflação de autores") aponta para este
arquivo como procedimento operacional.

## 1. Por que a desambiguação importa

Desambiguação incorreta aciona três valores terminais distintos da
taxonomia v2 (ver §2 do checklist e `_taxonomy-v2-design.md`), por
caminhos diferentes dos vetores bibliográficos tradicionais:

- **Dim. 1 pastiche por colisão**: confundir dois autores reais com
  mesmo sobrenome produz ficha cujos elementos vêm de obras
  distintas — autor A declarado + título/DOI de obra de autor B.
  Verificação automática (CrossRef/OpenAlex) encontra a obra, mas
  em autor diferente; o script passa se não cruzar o campo autor
  com o que o texto declara.
- **Dim. 2 conteúdo afirmado por atribuição lateral**: tese de
  Silva-sociólogo atribuída a Silva-epidemiologista; a obra é real,
  o conteúdo é real, mas o autor atribuído é outro. Invisível a
  script; caso típico de Dim. 3 conceitual quando a tese atribuída
  é teórica.
- **Dim. 2 conteúdo afirmado + Dim. 3 conceitual (conflação lateral)**:
  quando os dois homônimos pertencem a correntes distintas, misturar
  suas posições na mesma paráfrase é conflação — sem marcador de
  contraste, porque o texto acredita estar citando uma pessoa só.

O problema não é só bibliográfico; é substantivo. Corrigir o nome
do autor não repara a atribuição errada de conteúdo ou a conflação
teórica que a colisão produziu.

## 2. Sobrenomes-gatilho brasileiros

Lista de partida. Extensível por simples adição à seção
correspondente quando novo caso de colisão aparecer na prática. A
regra: qualquer BibTeX cujo primeiro autor esteja nesta lista passa
obrigatoriamente por §3.

### Alta frequência — colisão muito provável

Silva, Santos, Souza (ou Sousa), Oliveira, Ferreira, Pereira, Lima,
Costa, Almeida, Rodrigues, Gomes, Ribeiro, Martins, Carvalho, Alves,
Lopes.

### Frequência média — colisão provável em bases maiores (OpenAlex, Lattes)

Moreira, Mendes, Dias, Rocha, Nunes, Machado, Freitas, Teixeira,
Barbosa, Araújo, Castro, Cardoso, Reis, Nascimento, Correia,
Monteiro, Pinheiro, Batista.

### Sobrenomes compostos de alta frequência

Combinações muito comuns que **não** funcionam como desambiguador
natural apesar da aparência: Silva Santos, Silva Oliveira, Souza
Silva, Souza Santos, Santos Silva, Oliveira Silva. Tratar como
alta frequência mesmo quando o segundo sobrenome aparenta ser
distintivo — o conjunto se repete frequentemente o bastante para
que a colisão ocorra.

### Nota sobre convenção de publicação

Nome brasileiro típico tem formato "Nome (Meio) Sobrenome1
Sobrenome2". A convenção de qual sobrenome aparece na citação **não
é padronizada na prática**: o mesmo autor pode publicar como
"Silva, J.", "Santos Silva, J." ou "J. Silva Santos" em momentos
distintos. Isso é vetor adicional de colisão — dois registros do
mesmo autor podem parecer dois autores distintos, e dois autores
distintos podem parecer o mesmo por coincidência de grafia. Ambos
os erros são capturados pelo protocolo §3.

### Extensão da lista

Ao encontrar nova colisão em uso real, acrescentar o sobrenome à
categoria correspondente com nota curta sobre o contexto. O arquivo
é de crescimento incremental; a lista não precisa ser exaustiva
desde o início.

## 3. Protocolo ordenado de desambiguação

Aplicar em ordem. Parar no primeiro critério conclusivo e registrar
no metadado do BibTeX/Zotero qual critério decidiu — serve de âncora
para sessões futuras.

### Critério 1 — ORCID (ouro-padrão)

Identificador numérico único por pessoa (formato
`0000-0000-0000-0000`), atribuído pelo próprio pesquisador em
orcid.org. Quando presente nos metadados do artigo (CrossRef,
OpenAlex trazem quando registrado) e no BibTeX, resolve
univocamente.

Verificar:
- Campo ORCID no BibTeX ou no Zotero
- Metadados do artigo em CrossRef
  (`api.crossref.org/works/{DOI}`), OpenAlex, ou no próprio PDF
- Consulta direta a orcid.org para confirmar a obra ↔ pessoa

Cobertura: crescente na literatura BR a partir de 2020; quase
ausente antes de 2015. Ver §4 para fallbacks.

### Critério 2 — Afiliação no momento da publicação

Metadados do artigo trazem afiliação declarada. Confrontar com o
CV Lattes (lattes.cnpq.br) — plataforma nacional com cobertura
quase total da produção acadêmica BR.

Verificar:
- Afiliação no metadado do artigo em CrossRef/OpenAlex/Scielo
- Lattes do autor: formação, afiliação histórica, área CAPES
- ResearchGate, Academia.edu quando Lattes inacessível

Afiliação isolada pode enganar (autor pode ter passado por vários
lugares); combinar com critério 3 ou 4 quando a decisão depende
só dessa pista.

### Critério 3 — Área de atuação dominante

Cruzar CV Lattes (área CAPES declarada) ou OpenAlex concepts para
identificar a área de atuação primária do pesquisador.

Aplicação:
- Quando um dos candidatos é claramente de outra área
  (Silva-epidemiologista vs. Silva-antropólogo), resolve.
- Quando os candidatos são da mesma área, este critério não
  decide; ir para 4 ou 5.

### Critério 4 — Coautores recorrentes

Rede de coautoria é assinatura forte e estável. OpenAlex,
Scopus Author ID e Lattes permitem visualizar coautores frequentes.

Aplicação:
- "Silva J" que coautoria com X, Y, Z repetidamente versus
  "Silva J" que coautoria com A, B, C é pessoa diferente.
- Útil especialmente quando dois homônimos estão na mesma área
  (critério 3 falha) e não têm ORCID (critério 1 falha).

### Critério 5 — Histórico temporal

Primeira publicação, continuidade da produção, ano de doutoramento.

Aplicação:
- Se "Silva J" publica continuamente desde 1985 e há outro
  "Silva J" que só aparece a partir de 2010, são provavelmente
  dois.
- Cruzar com Lattes (ano de defesa de doutorado, início de
  vínculo institucional).
- Este critério raramente decide sozinho; funciona como
  confirmador.

### Registro da decisão

Depois de aplicar o protocolo, registrar no campo de notas do
BibTeX ou Zotero: qual critério decidiu, qual identificador
ancorou (ORCID quando houver), data da decisão (carimbo de
confiança — mesma lógica da coluna `data_ultima_verificacao` na
matriz). Futuras citações do mesmo autor usam a ancoragem já
feita; o trabalho não se repete.

## 4. Fallbacks quando ORCID não está disponível

Cenários em que ORCID é raro:
- Literatura brasileira pré-2015 em geral.
- Humanidades e algumas áreas das ciências sociais BR (adoção
  institucional mais lenta).
- Autores aposentados ou falecidos sem registro póstumo.
- Autores fora da academia institucional tradicional
  (pesquisadores autônomos, think tanks, consultores).

Substitutos em ordem decrescente de confiabilidade:

1. **Lattes** (lattes.cnpq.br) — para autores brasileiros vivos
   ou falecidos recentemente; cobertura quase total da produção
   nacional. Menos confiável para autores estrangeiros com
   colaboração pontual no Brasil.
2. **Scopus Author ID** — cobertura internacional razoável;
   gerado por desambiguação algorítmica e pode conter
   falsos-positivos quando o autor tem poucas publicações.
3. **OpenAlex Author ID** — cobertura ampla (integra ORCID +
   Microsoft Academic + heurística interna); mais falsos-positivos
   que Scopus, mas útil como primeira aproximação.
4. **Perfil Google Scholar** — útil quando o autor mantém o perfil
   atualizado; não é um identificador estruturado.
5. **Verificação manual** — cruzar título e ano do artigo em bases
   bibliográficas (SciELO, JSTOR, BVS, PubMed) para confirmar que
   a obra atribuída é de fato da pessoa supostamente citada.

Registrar na matriz de síntese qual fallback foi usado
(`fonte_desambiguacao: lattes | scopus | openalex | verificação manual`).
Nenhum fallback é tão confiável quanto ORCID; o registro protege
contra erro silencioso quando a ambiguidade for revisitada.

## 5. Caso especial — homônimos no mesmo campo

Cenário: dois ou mais pesquisadores com mesmo nome publicando em
área compatível. Exemplo hipotético: duas "Silva M. J." em saúde
coletiva, ambas publicando sobre APS, ambas em programas de
pós-graduação ativos.

### Protocolo de resolução

1. Aplicar critério 1 (ORCID) mesmo que suspeite de indisponibilidade
   — alguns casos resolvem porque um dos candidatos tem e o outro
   não, e a obra citada tem ORCID atribuído.
2. Conferir metadados do artigo específico: coautores do artigo,
   afiliação declarada no momento da publicação, e-mail de
   correspondência quando informado.
3. Se persiste ambiguidade, **interromper a geração** e pedir
   verificação manual ao pesquisador. A interrupção segue o mesmo
   protocolo de §4.2 do checklist (intrusão da memória paramétrica,
   passos 1-4): parar, sinalizar, aguardar decisão humana, não
   tentar corrigir sozinho.
4. **Nunca chutar**. Atribuir a qualquer um dos candidatos sem
   confirmação é exatamente o red flag (iv) do checklist
   (sobrenome comum sem desambiguação) — erro bibliográfico que o
   pipeline existe para prevenir.
5. Documentar a ambiguidade no metadado do BibTeX quando resolvida,
   para que a decisão não precise ser refeita em sessões futuras.

### Regra de ouro

Em caso de empate irredutível depois dos cinco critérios de §3 e
dos fallbacks de §4, a decisão correta é parar, não adiantar por
plausibilidade. O custo de parar é baixo (uma mensagem ao
pesquisador); o custo de atribuir errado é erro em Dim. 2 conteúdo
afirmado substantivo e não-detectável por script.

## 6. Desambiguação intra-autoral — mesma pessoa, fases distintas

Caso oposto ao §5: a mesma pessoa produziu em momentos teóricos
distintos, e o texto precisa distinguir as posições sem colapsá-las
em "um único autor" monolítico.

### Exemplos canônicos

- **Heleieth Saffioti**: *A mulher na sociedade de classes* (1969)
  articula marxismo ortodoxo com crítica à condição feminina;
  *Gênero, patriarcado, violência* (2004) adota vocabulário de
  patriarcado e articula teoria feminista contemporânea. Citar
  "(Saffioti, 1969)" e "(Saffioti, 2004)" em paráfrase conjunta
  de convergência achata 35 anos de reformulação teórica.
- **Raewyn Connell**: publicações pré-2006 assinadas como
  "R. W. Connell" (pré-transição); pós-2006 como "Raewyn Connell"
  — mesma pessoa, bibliografia politicamente sensível na
  apresentação do nome.
- **Michel Foucault**: fase arqueológica (*As palavras e as
  coisas*, 1966; *Arqueologia do saber*, 1969) vs. genealógica
  (*Vigiar e punir*, 1975; *História da sexualidade I*, 1976) vs.
  ética (*História da sexualidade II-III*, 1984). Citar
  "(Foucault, 1969)" e "(Foucault, 1976)" evoca conteúdos
  incomparáveis.
- **Judith Butler**: *Gender Trouble* (1990) vs. *Bodies that
  Matter* (1993) vs. *Giving an Account of Oneself* (2005) —
  evolução de posição em performatividade, materialidade e ética
  do reconhecimento.
- **Pierre Bourdieu**: sociologia rural (anos 1960) vs.
  *La distinction* (1979) vs. intervenção política tardia
  (anos 1990-2000) — mesmo habitus conceitual, posições
  empiricamente distintas.

### Protocolo

1. Identificar que trata-se da mesma pessoa — ORCID, Lattes, bio
   editorial resolvem.
2. **Não colapsar fases em uma única atribuição**. Citar sempre
   com o ano específico da obra ("Saffioti, 2004"), e quando o
   argumento o exigir, sinalizar a fase ("Saffioti em sua fase
   pós-1990", "Foucault genealógico").
3. Distinção explícita é necessária quando:
   - O texto cita posições de fases diferentes do mesmo autor e
     essas posições diferem substantivamente.
   - A evolução teórica do autor é parte do argumento
     (genealogia conceitual — exceção 2 de §3 do template
     argumentativo).
4. **Mudança de nome**: autores que publicaram sob nomes diferentes
   (R. W. → Raewyn Connell; autoras brasileiras com mudança de
   sobrenome após casamento/divórcio) — usar o nome que aparece
   na obra citada, mas documentar no Zotero que se trata da mesma
   pessoa. Em trabalhos sobre gênero ou identidade, a apresentação
   do nome pode ter peso político: respeitar o nome atual
   preferido pela pessoa, mas citar cada obra pelo nome com que
   foi publicada.
5. **Conflação intra-autoral silenciosa** — citar "Saffioti (1969;
   2004) sustenta que (…)" em paráfrase única de convergência sem
   marcar a distância teórica entre as duas obras — é conflação
   mesmo dentro da obra da mesma pessoa. Classificação v2: **Dim. 2
   conteúdo afirmado + Dim. 3 conceitual** (distinção importante em
   relação a pastiche intra-autoral, que combina **elementos
   bibliográficos** em vez de fases teóricas — ver
   `_taxonomy-v2-design.md §8.2` e `SKILL.md` glossário). Exige
   marcador de contraste ou de evolução.

## 7. Cross-references

- **Regra 3 do SKILL.md** (zero conflação de autores): este arquivo
  é o procedimento operacional da regra.
- **§3 do checklist** (checklist pré-geração): validação do BibTeX
  envolve passar qualquer entrada com sobrenome na lista §2 por
  este protocolo antes de qualquer prosa.
- **§4.2 do checklist**, sinal (ii) (citação sem chave ou chave
  inventada): relacionado — chave inventada para homônimo é um
  caminho pelo qual a intrusão paramétrica aparece.
- **§4.3 do checklist** (contraste teórico obrigatório): quando a
  desambiguação revela que dois autores do mesmo sobrenome
  pertencem a correntes divergentes, §4.3 passa a valer para
  qualquer paráfrase que os mencione.
- **§7 do checklist**, red flag (iv) (autor com sobrenome comum
  sem ORCID ou afiliação): aplicação operacional direta deste
  arquivo.
- **Módulos de domínio** (condicionais no diretório): quando
  presentes, `references/domain-*/theoretical-currents-*.md`
  trazem listas específicas de autores canônicos por área, com as
  tradições teóricas correspondentes. A desambiguação de autores
  por sobrenome (§2-§5) é universal; a atribuição de corrente
  teórica por autor (ex.: "Connell é tradição sociológica
  estrutural") é tarefa dos módulos de domínio.
