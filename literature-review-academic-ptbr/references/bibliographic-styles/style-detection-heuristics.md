# Heurísticas de detecção de estilo bibliográfico

## 0. Quando consultar este documento

Este arquivo é consultado no **Passo 0, ponto 3** do fluxo obrigatório
(diagnóstico inicial de estilo bibliográfico) sempre que o pesquisador
não tenha declarado explicitamente qual estilo adotar. Produz uma
recomendação — Vancouver numérico, ABNT autor-data, ou APA 7 — com
base em três fontes de sinal, em ordem decrescente de confiabilidade:

1. Periódico-alvo informado (§2 — heurística primária).
2. Instituto destinatário ou tipo de entregável (§3 — heurística
   secundária).
3. Assinatura de formato em trechos colados pelo pesquisador
   (§4 — heurística terciária).

Se nenhuma heurística conclui, cai no protocolo de pergunta explícita
(§6). A árvore de decisão em §5 integra as três heurísticas.

**Princípio geral**: a autoridade final é o documento de instruções
ao autor do periódico-alvo, não este arquivo. Este registry é um
ponto de partida; nunca substitui a consulta às instruções vigentes
do periódico.

## 1. Os três estilos em uma visão

### Vancouver numérico

Citação: `[1]`, `[2,3]`, `[4-6]` no texto. Lista numerada por ordem
de aparição. Padrão ICMJE/NLM. Predomínio: saúde pública,
biomedicina, enfermagem clínica, psiquiatria, epidemiologia.

### ABNT autor-data (NBR 10520:2023 + NBR 6023:2018)

Citação: `(SILVA, 2020)` — sobrenome em caixa alta, vírgula antes do
ano; com página: `(SILVA, 2020, p. 45)`. Lista alfabética por
sobrenome do primeiro autor. Predomínio: ciências sociais brasileiras,
humanidades, direito, educação, administração pública, maior parte
das pós-graduações brasileiras, relatórios técnicos institucionais
brasileiros.

### APA 7

Citação: `(Silva, 2020)` — sobrenome em caixa mista, vírgula antes
do ano; com página: `(Silva, 2020, p. 45)`; múltiplos autores:
`(Silva & Souza, 2020)` com ampersand. Lista alfabética. Predomínio:
psicologia internacional, psicometria, educação internacional,
administração internacional, algumas revistas brasileiras
interdisciplinares.

Detalhes de cada estilo — ordem autoral, grafia de maiúsculas,
abreviação de periódico, uso de *et al.*, hierarquia de metadados
na lista de referências — ficam nos módulos específicos quando
presentes no diretório: `vancouver-numeric.md`,
`vancouver-brazilian-conventions.md`, `abnt-nbr-6023-2018.md`,
`abnt-nbr-10520-2023.md`, `apa-7.md`.

## 2. Heurística primária — registry por periódico-alvo

Quando o pesquisador informa o periódico-alvo, esta tabela é
consultada primeiro. Os itens estão agrupados por estilo; a quarta
categoria marca periódicos de estilo variável que exigem verificação
caso a caso.

### Vancouver numérico

- Revista de Saúde Pública (RSP)
- Cadernos de Saúde Pública (CSP)
- Ciência & Saúde Coletiva (C&SC)
- Revista Brasileira de Epidemiologia (RBE)
- Revista Brasileira de Psiquiatria (RBP)
- Revista Panamericana de Salud Pública
- Periódicos internacionais de biomedicina em geral (BMJ, The
  Lancet, NEJM, JAMA e suas famílias)
- Cochrane Database of Systematic Reviews

### ABNT autor-data (NBR 10520 + NBR 6023)

Ciências sociais, humanidades, antropologia, estudos de gênero,
sociologia:
- Dados — Revista de Ciências Sociais
- Revista Brasileira de Ciências Sociais (RBCS)
- Mana — Estudos de Antropologia Social
- Cadernos Pagu
- Revista Estudos Feministas
- Horizontes Antropológicos
- Sociologias

Políticas públicas, administração, opinião pública:
- Revista de Administração Pública (RAP)
- Revista do Serviço Público (RSP-ENAP)
- Opinião Pública
- Revista de Administração Contemporânea (RAC)

Contextos institucionais brasileiros (ver também §3):
- Teses e dissertações em PPGs brasileiras (padrão geral)
- Projetos de pesquisa submetidos a CAPES, CNPq, FAPs regionais
- Relatórios técnicos de casas legislativas, IPEA, FIOCRUZ, ministérios
  (em geral — verificar manual institucional quando existir)

### APA 7

- Periódicos internacionais de psicologia, psicometria, educação e
  administração que seguem APA
- Algumas revistas brasileiras interdisciplinares (confirmar caso
  a caso)

### Variável — exigem verificação das instruções vigentes

- Psicologia: Reflexão e Crítica — aceita APA/Vancouver/ABNT
  conforme decisão editorial do período
- Psicologia USP
- Estudos de Psicologia (Natal)
- Revistas de educação BR (algumas ABNT, outras APA)
- Revistas interdisciplinares BR (variável)
- Revistas de administração BR (ABNT em grande parte, APA em
  algumas)

### Nota de uso

O registry acima reflete conhecimento corrente e não substitui a
leitura das instruções ao autor do periódico no momento da
submissão. Revistas mudam políticas; este arquivo é extensível —
acrescentar periódicos conforme novos encontros, ou revisar
entradas quando o periódico atualiza o manual.

## 3. Heurística secundária — por instituto destinatário ou tipo de entregável

Quando o periódico-alvo não é conhecido (projeto de pesquisa,
relatório técnico, parecer, entregável institucional), o tipo de
destinatário determina o default.

### Entregáveis acadêmicos brasileiros (default: ABNT)

- **Tese ou dissertação** em PPG brasileira → ABNT, salvo regimento
  específico do programa que autorize APA.
- **Projeto de pesquisa** submetido a CAPES, CNPq, FAPESP, FAPERJ,
  FAPEMIG, outras FAPs → ABNT (padrão nos editais).
- **Relatório de pesquisa** para agência de fomento → ABNT.
- **Parecer técnico** em contexto jurídico (STF, tribunais,
  procuradorias) → ABNT, com convenções específicas da área
  jurídica para legislação e jurisprudência.

### Entregáveis institucionais brasileiros (default: ABNT)

- **Relatório técnico de casa legislativa** (Câmara, Senado,
  assembleias estaduais) → ABNT, com lista enxuta
  priorizando fontes institucionais, legislação (LexML), dados
  primários (Câmara/Senado).
- **Relatório técnico para ministério, IPEA, FIOCRUZ, órgão
  público BR** → ABNT em geral; verificar manual institucional
  quando disponível.

### Entregáveis internacionais (default: depende do campo)

- **Manuscrito para congresso internacional** → depende do campo
  e das instruções do congresso; conferir explicitamente.
- **Relatório para organismo internacional** (OMS/WHO, OCDE, BM,
  OEA, CEPAL, BID) → APA ou Vancouver conforme a área; raramente
  ABNT.
- **Contribuição a livro internacional** → estilo do editor; em
  editoras de ciências sociais frequentemente Chicago ou
  APA-derivado; conferir.

### Regra operacional da heurística secundária

Entregável brasileiro sem periódico-alvo → default ABNT até prova
em contrário. Entregável internacional → nunca ABNT como default;
perguntar ao pesquisador.

## 4. Heurística terciária — assinaturas de formato em trechos colados

Quando o pesquisador cola trechos de referencial teórico, bibliografia
ou artigo modelo sem informar periódico nem destinatário, o formato
da citação visível é sinal forte do estilo-alvo.

### Assinaturas Vancouver

Sinais unívocos:
- `[1]`, `[2,3]`, `[4-6]` inline no texto.
- Numerais sobrescritos após a afirmação: `(...) encontrado⁽¹,²⁾`.
- Lista de referências numerada por ordem de aparição, não
  alfabética.
- Autores na lista: `Silva AB, Souza CD, Costa EF.` (iniciais após
  sobrenome, sem vírgula entre sobrenome e iniciais).

### Assinaturas ABNT

Sinais unívocos:
- `(SILVA, 2020)` — sobrenome em CAIXA ALTA dentro da citação
  parentética.
- `(SILVA; SOUZA; COSTA, 2020)` — três autores, separados por
  ponto-e-vírgula, todos em CAIXA ALTA.
- Com página: `(SILVA, 2020, p. 45)`.
- Lista de referências com autor em CAIXA ALTA no início:
  `SILVA, A. B.; SOUZA, C. D. Título da obra...`
- Lista alfabética.
- Uso de "e" ou ";" entre autores, nunca ampersand.

### Assinaturas APA 7

Sinais unívocos:
- `(Silva, 2020)` — sobrenome em Caixa Mista.
- `(Silva & Souza, 2020)` — ampersand `&` com dois autores.
- `(Silva et al., 2020)` para três ou mais autores desde a
  primeira citação.
- Com página: `(Silva, 2020, p. 45)`.
- Lista de referências com autor em Caixa Mista e vírgula antes
  de `&` entre autores finais: `Silva, A. B., & Souza, C. D. (2020).`
- Título do artigo em caixa baixa (apenas primeira palavra e nomes
  próprios capitalizados); título do periódico em itálico com
  Capitalização Inicial.

### Casos ambíguos

- `(Silva, 2020)` em caixa mista — pode ser APA ou ABNT com
  tipografia não estrita (alguns textos brasileiros usam caixa
  mista por preferência editorial). Desambiguador: presença de
  `&` vs. `e`/`;` entre autores; grafia na lista de referências.
- `(Silva, 2020, p. 45)` — compartilhado por APA e ABNT; o
  desambiguador é a grafia do sobrenome no restante do texto.
- Citação com página e sobrenome em caixa mista + ampersand —
  APA é a leitura natural.

Quando a assinatura é ambígua, seguir para §6 (pergunta explícita).

## 5. Árvore de decisão

```
Passo 0, ponto 3 — estilo bibliográfico:
│
├── O pesquisador declarou explicitamente o estilo?
│   ├── SIM → adotar; fim.
│   └── NÃO → próxima pergunta.
│
├── Periódico-alvo informado?
│   ├── SIM → consultar registry §2.
│   │   ├── Listado com estilo confirmado → adotar, recomendar
│   │   │   conferência das instruções vigentes do periódico.
│   │   ├── Listado como "variável" → pedir ao pesquisador que
│   │   │   consulte as instruções atuais do periódico, ou ir
│   │   │   para fallback §6.
│   │   └── Não listado → recomendar consulta às instruções do
│   │       periódico; se indisponível, ir para fallback §6.
│   └── NÃO → próxima pergunta.
│
├── Tipo de entregável identificável?
│   ├── Tese/dissertação/projeto BR → ABNT (§3) — confirmar com
│   │   pesquisador.
│   ├── Relatório de casa legislativa ou órgão público BR → ABNT (§3) —
│   │   confirmar.
│   ├── Relatório para organismo internacional → não é ABNT por
│   │   default; perguntar.
│   └── Não identificável → próxima pergunta.
│
├── Trechos colados com formato de citação visível?
│   ├── SIM → aplicar assinaturas §4.
│   │   ├── [N] → Vancouver.
│   │   ├── (SOBRENOME, ano) caixa alta → ABNT.
│   │   ├── (Sobrenome & Sobrenome, ano) ampersand → APA.
│   │   ├── (Sobrenome, ano) ambíguo → fallback §6.
│   └── NÃO → fallback §6.
```

Árvore aplicada em sequência; primeira resposta conclusiva decide.

## 6. Fallback — protocolo de pergunta explícita

Quando as três heurísticas não concluem, fazer pergunta estruturada
ao pesquisador, com as três opções nomeadas e exemplos:

```
Preciso confirmar o estilo bibliográfico para este entregável,
porque as heurísticas de detecção não chegaram a conclusão
unívoca.

Três opções:

1. Vancouver numérico — citação [1], [2,3]; lista numerada por
   ordem de aparição. Padrão em saúde pública, biomedicina e
   revistas internacionais da área.

2. ABNT autor-data (NBR 10520 + NBR 6023) — citação
   (SILVA, 2020); lista alfabética. Padrão em ciências sociais
   brasileiras, humanidades, administração pública, direito e
   maior parte das pós-graduações BR.

3. APA 7 — citação (Silva, 2020); lista alfabética. Padrão em
   psicologia, psicometria, administração internacional.

Qual estilo adotar?

Se o entregável é para periódico específico, as instruções ao
autor desse periódico são a autoridade final — posso orientar a
consulta se você indicar o nome da revista.
```

Aceitar também resposta não-listada (ex.: Chicago, Harvard,
IEEE, Modelo CAPES específico) quando o pesquisador informa.
Nesse caso, pedir o manual de estilo de referência e registrar
no metadado do entregável para consistência nas sessões
seguintes.

## 7. Sinais de override

As heurísticas acima são default; o pesquisador pode sobrescrevê-las
a qualquer momento:

- **Declaração explícita do pesquisador** em qualquer turno
  ("usar APA neste") → respeitar sem requerer justificativa.
- **Instruções ao autor do periódico que divergem do registry §2**
  → as instruções vigentes mandam; atualizar mentalmente o
  registry (ou, em uso real, atualizar o arquivo).
- **Mudança recente no estilo do periódico** — registry pode estar
  desatualizado; confiar nas instruções vigentes.
- **Preferência pessoal do pesquisador compatível com política do
  periódico** — quando o periódico aceita variantes (comum em
  revistas de psicologia e educação BR), respeitar a escolha do
  pesquisador sem forçar um estilo específico do registry.
- **Entregável híbrido** (ex.: versão em português para revista BR
  + versão em inglês para revista internacional da mesma
  pesquisa) — estilo por versão, não unificar.

Princípio: detecção é para reduzir fricção, não para impor; quando
o pesquisador sabe o que quer, este arquivo não discute.
