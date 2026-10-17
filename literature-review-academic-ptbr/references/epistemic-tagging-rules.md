# Regras de marcação epistêmica

## 0. Quando consultar este documento

Este arquivo formaliza as quatro tags epistêmicas referidas na regra
6 do SKILL.md e nos §4.1 e §4.2 do checklist. É consultado durante
a **geração de cada afirmação factual** (para decidir qual tag
aplicar) e na **conversão do rascunho de trabalho para a versão
final** (para traduzir tags em citações formatadas no estilo do
entregável).

Consulta seletiva, não integral. O pesquisador (ou Claude em
autorrevisão) volta ao ponto específico:

- §1 para as definições das quatro tags.
- §2 para a matriz de obrigatoriedade (qual tipo de afirmação
  exige qual tag).
- §3 para as proibições explícitas.
- §4 para o formato canônico.
- §5 para exemplos corretos e incorretos.
- §6 para o protocolo de conversão para Vancouver/ABNT/APA.
- §7 para interação com as outras regras da skill.
- §8 para regra nominal de **verificação ativa de conceitos-âncora
  canônicos mobilizados via apud** (Frente 2 / Teste 03), com catálogo
  inicial expansível.

As tags vivem **ao lado** do verbatim lateral (regra 7 do SKILL.md),
não o substituem. Verbatim é evidência textual da fonte; tag é
declaração epistêmica sobre a afirmação.

## 1. As quatro tags — definições canônicas

### [SOURCED: <chave>]

**Uso**: paráfrase ou afirmação derivada de **passagem específica
em uma fonte do corpus curado**. A chave é o identificador BibTeX
da fonte em `references.bib` (ou equivalente no Zotero).

Forma canônica com verbatim (paráfrase de obra específica —
obrigatório pela regra 7 do SKILL.md):

```
[SOURCED: <chave_bibtex> | verbatim: "<trecho até 25 palavras>" p.<página>]
```

Forma canônica sem verbatim (atribuição ampla a uma obra, sem
paráfrase de passagem — mais raro, usado para referenciar o
conjunto da obra ou posição geral do autor):

```
[SOURCED: <chave_bibtex>]
```

Multi-fonte (mesma afirmação sustentada por múltiplas fontes — usar
com parcimônia; no mais das vezes é preferível separar em
afirmações sequenciais com tags individuais):

```
[SOURCED: <chave1>, <chave2>]
```

#### Elegibilidade — quando cada variante cabe

Três variantes criam três atalhos se não houver regra dura de quando
cada uma se aplica. Regras:

**Com verbatim (default obrigatório).** Situações:
- Paráfrase de obra específica (caso-base).
- Citação indireta (discurso reportado da fonte, mesmo sem aspas).
- Dado estatístico de fonte única.

**Sem verbatim (exceção controlada).** Situações:
- Metadado da própria obra (título, ano, país do estudo, desenho
  metodológico, N declarado no abstract) — recuperável diretamente
  do BibTeX, sem necessidade de verbatim.
- Atribuição canônica de conceito ao autor que o cunhou (ex.: "o
  conceito de masculinidade hegemônica (Connell, 2005)" sem
  paráfrase do texto de Connell).

**Multi-fonte (exceção controlada).** Situação: afirmação de padrão
convergente em tópico-frase (§1 T1 do template argumentativo), em
que nenhuma fonte individual afirma o padrão nos termos exatos do
pesquisador. **Regra dura**: cada chave agregada em multi-fonte deve
ter aparição individual em outro ponto do texto com `[SOURCED]` +
verbatim. Só pode entrar em multi-fonte o que já está
individualmente verificado. Caso contrário, é conflação ou atalho
preguiçoso.

### [INFERRED from <chave1>, <chave2>, ...]

**Uso**: afirmação **sintética** que combina ≥2 fontes `[SOURCED]`
para concluir algo que nenhuma delas afirma isoladamente. É a voz
do autor da revisão em T3 (síntese crítica, ver §1 do template
argumentativo) quando apoiada em evidência múltipla.

Forma canônica:

```
[INFERRED from <chave1>, <chave2>, ..., <chaveN>]
```

A listagem explícita das fontes combinadas é **obrigatória** —
`[INFERRED]` sem fontes é inválido. Se a síntese é apoiada por
apenas uma fonte, trocar por `[SOURCED]`. Se a síntese não tem
fontes, é opinião; usar `[UNCERTAIN]` ou reformular sem afirmação
factual.

### [UNCERTAIN: <descrição + plano>]

**Uso**: afirmação com confiança baixa — o autor da revisão
suspeita da asserção mas não tem base firme no corpus para
afirmá-la nem evidência para removê-la imediatamente. Requer
**plano de resolução**.

Forma canônica:

```
[UNCERTAIN: <o que é incerto>; plano: <verificar / remover /
manter com nota>]
```

Toda `[UNCERTAIN]` deve ser resolvida antes da versão final (§6,
Fase 2). Não é catchall para "não quero checar agora" — é
sinalizador temporário com compromisso de resolução.

### [GENERAL KNOWLEDGE]

**Uso**: conhecimento de domínio público amplamente compartilhado
na área, **não controverso**, sem data, estatística ou nome próprio
específicos. Raro em revisão de literatura — a maior parte do que
parece "conhecimento geral" na verdade é afirmação que exige
atribuição.

Forma canônica:

```
[GENERAL KNOWLEDGE]
```

Sem qualificador adicional. Se o pesquisador sente necessidade de
qualificar, a afirmação não é `[GENERAL KNOWLEDGE]` — trocar por
`[SOURCED]` ou `[UNCERTAIN]`.

Teste de elegibilidade — duas condições cumulativas:

1. A afirmação apareceria, com formulação equivalente, em um **manual
   introdutório internacional** do campo, publicado por editora
   acadêmica reconhecida, sem citação.
2. A afirmação **não** depende de especificidade nacional. Fatos
   sobre SUS, ESF, DATASUS, legislação brasileira, instituições
   nacionais — mesmo parecendo senso comum em saúde coletiva
   brasileira — exigem `[SOURCED]`, porque não passam o teste (1):
   não aparecem em manual introdutório internacional, só em manual
   brasileiro específico. Extensão análoga para política brasileira,
   sistema educacional, judiciário, regulação de mercado nacional,
   convenções específicas de ciências sociais BR.

Se ambas as condições forem satisfeitas, a afirmação é candidata a
`[GENERAL KNOWLEDGE]`. Caso contrário, é `[SOURCED]` ou `[UNCERTAIN]`.
Ver §3 para a proibição explícita sobre especificidade nacional.

## 2. Matriz de obrigatoriedade — qual tag para cada tipo de afirmação

| Tipo de afirmação                                                     | Tag obrigatória                               | Exemplo (abreviado)                                                 |
|-----------------------------------------------------------------------|-----------------------------------------------|---------------------------------------------------------------------|
| Estatística específica (percentual, coeficiente, N, magnitude)        | `[SOURCED]` + verbatim                        | *"a prevalência foi 26,3%"*                                         |
| Data específica (histórica ou contemporânea)                          | `[SOURCED]`                                   | *"em 1988, o SUS foi instituído"*                                   |
| Nome próprio atribuído (autor, obra, programa, política)              | `[SOURCED]` quando atributiva                 | *"Connell cunhou o termo X"*                                        |
| Citação direta entre aspas                                            | `[SOURCED]` + página + verbatim               | *"'(…)' (p. 832)"*                                                  |
| Paráfrase de obra específica                                          | `[SOURCED]` + verbatim                        | *"A obra define X como (…)"*                                        |
| Atribuição ampla a tradição teórica                                   | `[SOURCED]` sem verbatim                      | *"A tradição sociológica estrutural sustenta (…)"*                  |
| Metadado da obra (título, ano, país, desenho, N declarado)            | `[SOURCED]` sem verbatim                      | *"Estudo randomizado com 1.200 participantes em São Paulo"*         |
| Síntese combinando ≥2 fontes `[SOURCED]`                              | `[INFERRED from k1, k2, ...]`                 | *"A convergência indica que (…)"*                                   |
| Metacomentário do pesquisador sobre a literatura revista              | `[INFERRED from <síntese da revisão>]`        | *"A literatura sobre X é escassa no contexto BR"*                   |
| Afirmação factual sem apoio no corpus mas suspeita correta            | `[UNCERTAIN]` + plano de resolução            | *"Indícios apontam para (…)"*                                       |
| Conhecimento internacional compartilhado, sem data/estatística/nome   | `[GENERAL KNOWLEDGE]`                         | *"A água é solvente universal"* (exemplo neutro)                    |
| Qualquer afirmação factual não encaixável acima                       | `[UNCERTAIN]` (default defensivo)             | —                                                                   |

A coluna da direita é **obrigatória**, não sugerida. Afirmações
factuais sem tag no rascunho de trabalho são tratadas como
suspeitas pelo revisor cético (§5.4 do checklist, categoria
"Marcação epistêmica").

Observação sobre metacomentário — linha 9 da tabela. Afirmações como
*"essa literatura é escassa no contexto brasileiro"*, *"há gap em X"*,
*"os estudos variam em qualidade metodológica"* são síntese do
pesquisador sobre o corpus revisado. Não são `[GENERAL KNOWLEDGE]`
(não passam o teste §1) nem `[SOURCED]` (não vêm de uma passagem
individual). São `[INFERRED from <síntese da revisão>]`, em que a
"síntese da revisão" é a própria matriz de síntese ou o conjunto de
chaves revisadas. O pesquisador deve conseguir justificar essa
afirmação apontando para o que a revisão observou.

## 3. Proibições explícitas

### Proibições para [GENERAL KNOWLEDGE]

**Nunca** aplicar `[GENERAL KNOWLEDGE]` em:

- Estatísticas específicas, mesmo quando o número é "conhecido"
  (ex.: prevalência, coeficiente de Gini, taxa de mortalidade).
- Datas específicas, mesmo históricas (ex.: "em 1978 a Conferência
  de Alma-Ata estabeleceu…" — requer `[SOURCED]`).
- Nomes próprios atribuídos a teses, conceitos, políticas ou
  programas (ex.: "Connell formulou masculinidade hegemônica em…"
  — requer `[SOURCED]`).
- Citações diretas.
- Paráfrases de obra específica.
- Achados empíricos recentes.
- Afirmações controversas ou em disputa na área.
- **Especificidade nacional** — instituições, políticas, legislação
  ou programas brasileiros (SUS, ESF, DATASUS, LDB, Constituição
  Federal, LexML, BNDES, IBGE, Banco Central, Portaria CNPq,
  Ministério da Saúde, etc.). Mesmo quando parecem senso comum no
  campo, exigem `[SOURCED]`. Critério do teste de elegibilidade
  (§1): a afirmação apareceria em manual introdutório
  **internacional** do campo, não apenas em manual brasileiro
  específico. Extensão análoga: política brasileira, sistema
  educacional nacional, estrutura do judiciário, regulação de
  mercado, convenções próprias de ciências sociais BR
  (sanitarismo, pacto federativo, reforma sanitária, Movimento
  Negro Unificado, etc.).

A violação desta regra é red flag (vii) do checklist e dispara
abort-and-verify.

### Proibições para [SOURCED]

- `[SOURCED: <chave>]` é **inválida** se `<chave>` não existe no
  corpus curado. Chave fabricada é red flag (ii) do checklist —
  Dim. 1 inexistente-fabricada (ou Dim. 1 pastiche, conforme
  `_taxonomy-v2-design.md §8.1`).
- Paráfrase de obra específica sem verbatim lateral é
  **incompleta**. O verbatim é obrigatório pela regra 7 do
  SKILL.md.

### Proibições para [INFERRED]

- `[INFERRED]` sem listagem das fontes combinadas é inválido.
- `[INFERRED from <única chave>]` é inválido — use `[SOURCED]`.
- `[INFERRED]` não substitui o raciocínio: a síntese inferida deve
  ser defensível a partir das fontes listadas, não extrapolação.

### Proibições para [UNCERTAIN]

- `[UNCERTAIN]` sem plano de resolução é inválido — o plano é
  parte da tag.
- `[UNCERTAIN]` na versão final é proibido. Toda `[UNCERTAIN]` do
  rascunho deve ser resolvida (§6 Fase 2).

## 4. Formato canônico — resumo

```
[SOURCED: <chave>]
[SOURCED: <chave> | verbatim: "<trecho>" p.<página>]
[SOURCED: <chave1>, <chave2>]

[INFERRED from <chave1>, <chave2>, ..., <chaveN>]

[UNCERTAIN: <descrição>; plano: <verificar|remover|manter_com_nota>]

[GENERAL KNOWLEDGE]
```

Convenções:

- Chaves BibTeX seguem a convenção do Zotero/Better BibTeX
  (ex.: `Connell2005`, `SouzaOliveira2018a`).
- Página em `p.N` ou `p.N-M` (range).
- Verbatim em aspas duplas, até 25 palavras, fiel ao texto (sem
  edição silenciosa).
- Separadores: vírgula entre chaves em multi-fonte; ponto-e-vírgula
  entre chaves e descrição em `[UNCERTAIN]`; pipe (`|`) entre chave
  e verbatim em `[SOURCED]`.

## 5. Exemplos de uso correto e incorreto

### Corretos

**Paráfrase de obra específica com verbatim:**

> *"A masculinidade hegemônica não é tipo de pessoa, mas posição
> sempre contestável na hierarquia de gênero (Connell &
> Messerschmidt, 2005)
> [SOURCED: ConnellMesserschmidt2005 | verbatim: "hegemonic
> masculinity was not assumed to be normal in the statistical
> sense; only a minority of men might enact it" p.832]."*

**Síntese combinando duas fontes:**

> *"A convergência entre os estudos em município de pequeno porte
> e os estudos em capitais sugere que a cobertura explica menos
> que o território de atuação da equipe
> [INFERRED from AutorA2020, AutorB2022]."*

**Incerteza com plano de resolução:**

> *"A literatura recente parece convergir para a leitura [X], embora
> o presente corpus não contenha sistematicamente revisões pós-2023
> [UNCERTAIN: se a convergência é confirmada em revisões pós-2023;
> plano: verificar antes da submissão final via OpenAlex +
> atualização do Zotero]."*

**Conhecimento genuinamente geral:**

> *"O Sistema Único de Saúde (SUS) foi instituído pela Constituição
> Federal [GENERAL KNOWLEDGE]."*
>
> Observação: a afirmação é aceitável como `[GENERAL KNOWLEDGE]`
> porque não traz data específica ("1988" exigiria `[SOURCED]`),
> não traz estatística e não é controversa. Se o texto mencionasse
> "em 1988", viraria `[SOURCED]` por causa da data.

### Incorretos

**Estatística como `[GENERAL KNOWLEDGE]` — proibição §3:**

> ✗ *"A prevalência de hipertensão é alta entre adultos
> brasileiros [GENERAL KNOWLEDGE]."*
>
> Problema: "alta" é afirmação qualitativa específica sobre a área;
> "entre adultos brasileiros" é recorte específico. Exige
> `[SOURCED]` com fonte (VIGITEL, PNS, etc.).

**Data + nome + paráfrase como `[GENERAL KNOWLEDGE]` — triplo vetado:**

> ✗ *"Connell formulou masculinidade hegemônica em 1995
> [GENERAL KNOWLEDGE]."*
>
> Problema: data específica, nome próprio atribuído a tese, e
> paráfrase de obra específica — cada um dos três proíbe
> `[GENERAL KNOWLEDGE]` individualmente.

**Chave fabricada — red flag (ii):**

> ✗ *"A reforma sanitária brasileira tem raízes no sanitarismo do
> início do século XX (Silva2021)
> [SOURCED: SilvaHistoriaDaSaude2021]."*
>
> Problema: se `SilvaHistoriaDaSaude2021` não está no
> `references.bib`, a chave foi produzida. Verificar no corpus; se
> ausente, trocar por `[UNCERTAIN]` ou remover a afirmação.

**Paráfrase de obra sem verbatim:**

> ✗ *"Connell define masculinidade hegemônica como posição
> hierárquica (Connell, 2005) [SOURCED: Connell2005]."*
>
> Problema: paráfrase de obra específica sem verbatim lateral viola
> regra 7 do SKILL.md. O trabalho do pesquisador não consegue
> conferir se a paráfrase é fiel.

**`[INFERRED]` sem fontes listadas:**

> ✗ *"O conjunto da literatura aponta para [X] [INFERRED]."*
>
> Problema: listagem obrigatória. Converter para
> `[INFERRED from <chave1>, <chave2>, ...]` ou rebaixar para
> `[UNCERTAIN]`.

**`[UNCERTAIN]` sem plano:**

> ✗ *"Há indícios de que [X] [UNCERTAIN]."*
>
> Problema: sem plano de resolução, a tag não disciplina o trabalho
> pendente. Converter para `[UNCERTAIN: <descrição>; plano: <ação>]`
> ou remover a afirmação.

## 6. Protocolo de conversão para a versão final

A conversão do rascunho de trabalho (com tags + verbatim) para a
versão final (com citações no estilo do entregável, sem tags e sem
verbatim) é feita em quatro fases. O `scripts/style_formatter.py`
automatiza as fases 3-4; as fases 1-2 exigem trabalho humano.

### Fase 1 — Conferência de `[SOURCED]` com verbatim

Para cada `[SOURCED: <chave> | verbatim: "..." p.<página>]`,
conferir a paráfrase contra o verbatim lateral. Marcar uma das
quatro categorias (alinhadas a §5.2 do checklist):

- `FIEL` — a paráfrase reflete o trecho e não extrapola.
- `DISTORÇÃO LEVE` — a paráfrase extrapola em nuance ou omite
  qualificação relevante. Requer reescrita antes da conversão.
- `DISTORÇÃO GRAVE` — a paráfrase diverge substantivamente do
  trecho. Bloqueia conversão; a afirmação deve ser reescrita ou
  removida.
- `INVENÇÃO` — a paráfrase contém elemento não suportado pelo
  trecho nem pelo restante da obra. Bloqueia conversão; remover ou
  substituir por `[UNCERTAIN]` com plano.

Obras-chave e paráfrases em seções de alto risco argumentativo (§5.2
do checklist) recebem conferência 100%; demais seções, ≥20% em
amostra aleatória.

### Fase 2 — Resolução de `[UNCERTAIN]`

Toda `[UNCERTAIN]` do rascunho deve ser resolvida antes da versão
final. Três opções, a escolha depende do plano declarado na tag:

1. **Verificar e promover a `[SOURCED]`**: buscar fonte no
   Zotero/bases, adicionar ao corpus, converter a tag.
2. **Remover a afirmação**: se a verificação falhou ou se a
   afirmação não é essencial ao argumento.
3. **Manter com nota de rodapé explícita**: para incertezas
   substantivas que o texto precisa explicitar (ex.: "os dados
   disponíveis não permitem afirmar [Y]"). A nota substitui a tag.

Uma `[UNCERTAIN]` que chega à versão final sem resolução é falha
de processo, não uso legítimo da tag.

### Fase 3 — Substituição de tags por citações no estilo

Tradução por estilo bibliográfico, aplicada por
`scripts/style_formatter.py` após Fases 1-2 aprovadas.

**Vancouver numérico** (saúde coletiva, biomedicina — RSP, CSP,
C&SC, RBE):

| Tag                                             | Substituição                                                                   |
|-------------------------------------------------|--------------------------------------------------------------------------------|
| `[SOURCED: Smith2020]`                          | `[N]` (número sequencial; entrada adicionada à lista de referências)           |
| `[SOURCED: Smith2020 \| verbatim: "…" p.45]`    | `[N]` (página pode aparecer no texto: *"conforme [N] (p.45)"*)                 |
| `[SOURCED: Smith2020, Jones2021]`               | `[N,M]`                                                                        |
| `[INFERRED from Smith2020, Jones2021]`          | `[N,M]` precedido de frase de síntese no texto                                 |
| `[GENERAL KNOWLEDGE]`                           | sem citação                                                                    |
| `[UNCERTAIN: …]`                                | (deve ter sido resolvida na Fase 2)                                            |

**ABNT autor-data** (NBR 10520:2023 — ciências sociais brasileiras,
humanidades, direito, administração pública, maior parte das
pós-graduações BR):

| Tag                                             | Substituição                                                                   |
|-------------------------------------------------|--------------------------------------------------------------------------------|
| `[SOURCED: Smith2020]`                          | `(SMITH, 2020)`                                                                |
| `[SOURCED: Smith2020 \| verbatim: "…" p.45]`    | `(SMITH, 2020, p. 45)`                                                         |
| `[SOURCED: Smith2020, Jones2021]`               | `(SMITH, 2020; JONES, 2021)`                                                   |
| `[INFERRED from Smith2020, Jones2021]`          | `(SMITH, 2020; JONES, 2021)` precedido de frase de síntese no texto            |
| `[GENERAL KNOWLEDGE]`                           | sem citação                                                                    |
| `[UNCERTAIN: …]`                                | (deve ter sido resolvida na Fase 2)                                            |

**APA 7** (psicologia, psicometria, educação internacional,
administração, algumas revistas BR interdisciplinares):

| Tag                                             | Substituição                                                                   |
|-------------------------------------------------|--------------------------------------------------------------------------------|
| `[SOURCED: Smith2020]`                          | `(Smith, 2020)`                                                                |
| `[SOURCED: Smith2020 \| verbatim: "…" p.45]`    | `(Smith, 2020, p. 45)`                                                         |
| `[SOURCED: Smith2020, Jones2021]`               | `(Smith, 2020; Jones, 2021)`                                                   |
| `[INFERRED from Smith2020, Jones2021]`          | `(Smith, 2020; Jones, 2021)` precedido de frase de síntese no texto            |
| `[GENERAL KNOWLEDGE]`                           | sem citação                                                                    |
| `[UNCERTAIN: …]`                                | (deve ter sido resolvida na Fase 2)                                            |

Detalhes de cada estilo (ordem autoral, abreviação de periódico,
uso de "et al.", grafia de maiúsculas, hierarquia de meta-dados na
lista de referências) ficam em
`references/bibliographic-styles/<estilo>.md` (módulos específicos
quando presentes no diretório).

### Fase 4 — Remoção dos verbatim laterais

Após Fase 1 aprovada, remover todos os verbatim laterais do texto.
**Manter um backup do rascunho com verbatim intacto** — serve como
rastro auditável exigido pela Portaria CNPq 2.664/2026 (art. 9) e é
parte da documentação operacional que sustenta a declaração de uso
de IA (§5.5 do checklist, Templates A/B/C/D).

Ao fim da Fase 4, a versão final não contém tags nem verbatim; a
lista de referências foi gerada a partir das chaves únicas presentes
no texto convertido; o backup do rascunho está arquivado.

**Observação sobre copyright do backup**: o rascunho arquivado com
verbatim é material de auditoria de **uso pessoal**. Não
compartilhar com terceiros sem avaliação de direitos autorais —
verbatim acumulado de múltiplas obras pode exceder o limite de
citação permitido pela LDA (Lei 9.610/98) e pelos regimes de fair
use internacionais. Fornecer **sob demanda** para auditoria externa
(revisor, editor, agência de fomento que solicite), não como anexo
padrão de submissão. A norma é que o backup existe para proteger o
pesquisador em caso de questionamento, não para circular
livremente.

## 7. Interação com outras regras da skill

- **Regra 7 do SKILL.md (verbatim lateral)**: verbatim vive no mesmo
  bracket que `[SOURCED]` quando há paráfrase de obra específica.
  Regra 7 é sobre evidência textual da fonte; este arquivo é sobre
  declaração epistêmica do autor. Os dois coexistem no rascunho;
  a Fase 4 de conversão remove o verbatim mas a fidelidade
  verificada na Fase 1 permanece registrada no backup.

- **§1 T2 do template argumentativo**: cada afirmação em T2 recebe
  tag. Agregação de múltiplas fontes em T2 usa `[SOURCED: k1, k2]`
  ou tags individuais em frases sequenciais.

- **§1 T3 do template argumentativo**: síntese crítica em T3, quando
  combina ≥2 fontes já marcadas `[SOURCED]`, recebe `[INFERRED from k1, k2]`.
  T3 que apenas posiciona a voz do autor sem sintetizar evidência
  externa não recebe tag (é voz autoral, não afirmação factual).

- **§4.1 do checklist (regras de escrita)**: autoconferência a cada
  parágrafo inclui "toda afirmação factual tem marcação epistêmica".
  Este arquivo é a referência que define o que conta como
  "marcação".

- **§4.2 do checklist (intrusão paramétrica)**: datas, estatísticas
  ou nomes próprios sem `[SOURCED]` são sinal (iv) de intrusão da
  memória paramétrica. A matriz em §2 é a regra; o checklist é o
  diagnóstico.

- **§7 do checklist (red flags)**: red flag (vii) —
  `[GENERAL KNOWLEDGE]` em estatística/data/nome/paráfrase — é
  a operacionalização das proibições listadas em §3 deste arquivo.

## 8. Verificação ativa de conceitos-âncora canônicos mobilizados via apud

### 8.1 Justificativa e gatilho

Distorção conceitual operada via apud — autor secundário cita autor
primário, mas a citação distorce a atribuição autoral do conceito —
é vetor difícil de detectar quando o conceito-âncora é **canônico**
e a memória paramétrica do agente subjacente reforça a atribuição
errada. A presença textual do autor primário (mesmo via apud) e a
familiaridade do conceito criam ilusão de fidelidade que nem a Regra
4 do `SKILL.md` (declaração de tradição teórica) nem a Regra 7
(verbatim lateral) cobrem isoladamente — a paráfrase pode ser fiel ao
texto secundário citante ainda que o texto secundário citante esteja
errado sobre a atribuição.

Manifestação canonizadora. **Camada 4 do A4 do Teste 03** (ground
truth v2.0, §3.1 e §5.2 — em
`<pasta-de-referencias>\skill-development\test-reports\teste-03-fase-A.7.2\05-ground-truth-v2.0-final.md`):
o parágrafo-semente atribui o conceito **"olhar de perto e de
dentro"** a Velho via Tavares & Camurça (2004) apud — quando o
conceito é magnaniano (Magnani, "De perto e de dentro: notas para
uma etnografia urbana", *RBCS* v.17 n.49, 2002). O vetor não foi
detectado por nenhum dos dois ambientes do Papel 2 (Claude.ai
navegador Incognito + Claude Desktop Incognito); o Desktop chegou
a propagar o erro ao tratar a inversão objeto/método na direção
contrária à correta. Falso negativo material compartilhado.

### 8.2 Regra nominal

**Sempre que um conceito-âncora canônico aparecer mobilizado via
apud em material auditado** — seja em modo redação (geração própria
da skill) ou em modo diagnóstico (auditoria de texto alheio) —
**acionar §(xii) com prioridade alta para verificação da atribuição
autoral em fonte primária**, ainda que a citação apud esteja
corretamente estruturada e a fonte secundária seja existente
verificável.

A verificação ativa deve sempre exceder a memória paramétrica do
agente. Mesmo quando a memória paramétrica acerta na detecção
periférica (p. ex., reconhece o pastiche), pode errar nos detalhes
da atribuição autoral via apud. §(xii) é o protocolo de fechamento
desse vetor, não um detalhe opcional.

Procedimento operacional ao detectar conceito-âncora em apud:

1. Sinalizar carimbo **"atribuição autoral via apud — verificar
   fonte primária"** no rascunho de trabalho ou no parecer
   diagnóstico, ao lado da paráfrase ou citação afetada.
2. Listar a **obra primária esperada** conforme catálogo da §8.3
   abaixo (ou pesquisa em fonte primária quando o conceito não
   estiver no catálogo).
3. Confrontar a atribuição apud declarada no texto auditado contra
   a obra primária canônica. Três saídas possíveis:
   - *Atribuição correta confirmada* — registrar verificação no
     campo `fonte_desambiguacao` da matriz de síntese (quando
     aplicável) e seguir.
   - *Atribuição cruzada detectada* — classificar como Dim. 2
     conteúdo afirmado + Dim. 3 conceitual (distorção da atribuição
     autoral do conceito); ação corretiva inclui restaurar a
     atribuição autoral correta e revisar paráfrases adjacentes.
   - *Indeterminação após verificação* — registrar como
     `[UNCERTAIN]` com plano de resolução em fonte primária
     externa ao corpus do texto auditado.

### 8.3 Catálogo inicial de conceitos-âncora canônicos

O catálogo abaixo é **expansível**: cresce conforme casos novos
forem detectados em testes futuros e conforme módulos de domínio
(`references/domain-*/theoretical-currents-*.md`) forem
implementados. Inclusão prioritária quando o autor é par-gatilho
forte da Regra 4 do `SKILL.md` ou exemplar canônico da §8.6 do
`_taxonomy-v2-design.md` (variantes de Dim. 2 estrutura de
sustentação argumentativa).

#### Antropologia urbana brasileira (Teste 03 / Fase A.7.2)

**MAGNANI, José Guilherme Cantor** (USP, NAU — etnografia
estrutural-espacial):

- **"pedaço"** — *Festa no pedaço*, 1984 (1ª ed.) / 1998 (2ª ed.).
- **"mancha"** — *Os pedaços da metrópole*, 1998.
- **"trajeto"** — *Os pedaços da metrópole*, 1998.
- **"circuito"** — "Os circuitos dos jovens urbanos", *Tempo Social*
  v.17 n.2, 2005.
- **"pórtico"** — *Da periferia ao centro: trajetórias de pesquisa
  em antropologia urbana*, 2012.
- **"olhar de perto e de dentro"** / **"De perto e de dentro"** —
  "De perto e de dentro: notas para uma etnografia urbana", *RBCS*
  v.17 n.49, 2002.

**VELHO, Gilberto Cardoso Alves** (UFRJ, PPGAS-Museu Nacional —
antropologia das sociedades complexas, fenomenológico-individualista):

- **"campo de possibilidades"** — *Subjetividade e sociedade*, 1981;
  *Projeto e metamorfose*, 1994.
- **"projeto"** — *Projeto e metamorfose*, 1994; *Individualismo e
  cultura*, 1981.
- **"trajetória"** — *Subjetividade e sociedade*, 1981.
- **"metamorfose"** — *Projeto e metamorfose*, 1994.
- **"observando o familiar"** — "Observando o familiar", em *A
  aventura sociológica*, 1978.
- **"antropologia interpretativa"** / **"antropologia das
  sociedades complexas"** — uso programático em vários trabalhos.

### 8.4 Princípio expansível

O catálogo de §8.3 é entrada inicial. A admissão de novas entradas
segue dois critérios:

- *Detecção empírica*: o conceito apareceu mobilizado via apud em
  rodada de teste (ou em sessão real de revisão) e a atribuição
  cruzada foi observada como vetor de risco.
- *Canonicidade do conceito*: o conceito é amplamente reconhecido
  como assinatura do autor na tradição relevante; sua mobilização
  fora dessa tradição típica gera distorção detectável.

Quando módulos de domínio forem implementados
(`references/domain-*/theoretical-currents-*.md`, pendência (i) do
`_phase2-handoff.md`), as entradas do catálogo podem migrar para os
módulos correspondentes, com este arquivo passando a apontar para
eles. Até lá, o catálogo cresce aqui.

### 8.5 Interação com outras regras

- **Regra 4 do SKILL.md** (declaração de tradição teórica): a regra
  nominal de §8 estende a Regra 4 ao caso específico de mobilização
  via apud, em que a tradição declarada do autor primário pode
  divergir da tradição declarada pelo autor secundário citante.
- **Regra 5 do SKILL.md** (prosa argumentativa com marcadores de
  contraste obrigatórios): quando o conceito-âncora canônico de um
  autor é mobilizado via apud para outro autor da mesma vizinhança
  acadêmica (par-gatilho fraco — par institucionalmente vizinho),
  a §8 acopla-se à variante "convergência fabricada entre autores
  de correntes vizinhas" da §8.6 do `_taxonomy-v2-design.md`. A
  ausência de marcador de contraste e a atribuição cruzada via
  apud são sinais convergentes.
- **§(xii)** (verificação manual externa pelo decisor): a regra
  nominal aciona §(xii) com **prioridade alta**, no nível de
  pastiche stricto sensu potencial e refs internas em revisão, e
  acima de Dim. 2 metadados rotineira.
