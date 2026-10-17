---
name: docx-tabelas-validadas
description: >-
  Extrai tabelas de arquivos .docx para CSV com verificação obrigatória por dupla
  rota de leitura, checagem de somas, de marginais e de universo amostral, antes
  de qualquer análise. Use SEMPRE que o usuário anexar ou mencionar um .docx
  contendo tabelas de resultados — anexos de pesquisa, tabelas simples, tabelas
  cruzadas, relatórios do DataSenado, tabulações do IBGE ou do DATASUS — e pedir
  para ler, conferir, registrar, extrair, tabular, comparar ou validar os números.
  Use também quando o pedido for confrontar tabelas cruzadas contra marginais,
  verificar se dois documentos batem, ou "registrar os dados de forma confiável".
  Não use para editar ou comentar .docx (use docx-revisao) nem para .pdf ou .xlsx.
---

# Extração validada de tabelas em .docx

Ler tabela de .docx é fácil; ler **sem erro silencioso** não é. Um desalinhamento
de linha ou coluna produz um número plausível e errado, que não se distingue do
certo por inspeção. Esta skill existe para tornar esse erro detectável.

O princípio é simples: **nenhum número entra na análise sem ter sido lido duas
vezes por caminhos independentes e sem ter passado por checagens aritméticas que
o desalinhamento quebraria.**

Corolário, aprendido da pior maneira: **checagem que não roda não é checagem que
passou.** "0 falhas" só significa alguma coisa acompanhado de quantas checagens
eram possíveis. Ver *Cobertura* abaixo — é a primeira coisa a ler no relatório e
a primeira a reportar ao usuário.

## Fluxo

### 1. Rodar o extrator antes de olhar os números

```bash
python "${CLAUDE_SKILL_DIR}/scripts/extract_docx_tables.py" ENTRADA.docx \
    --out-dir ./outputs --prefix anexoN
```

O script falha ruidosamente em vez de entregar dado suspeito:

- **Dupla rota.** Lê as tabelas pelo modelo de objetos do `python-docx` e,
  separadamente, percorrendo o `word/document.xml` cru com `lxml`. Compara célula
  a célula, na ordem do documento. Se divergir em uma célula sequer, aborta com
  código 2 e **não grava nada**.
- **Soma vertical.** Para cada coluna com linha `Total`, soma o corpo e compara.
  Percentuais admitem ±2 de arredondamento; contagens têm de bater exatamente.
  Reconhece célula empacotada (`9% (±5,8%)`), não só a forma simples.
- **Marginal horizontal.** Soma os subgrupos e compara com a última coluna.
  Contagens exatas; populações com tolerância de uma unidade por parcela. Roda só
  em linhas inteiramente numéricas, então tabelas cuja última coluna é outra
  população (Brasil ao lado de UF) se autoexcluem. É a checagem que pega
  desalinhamento **horizontal**, que a soma vertical não pega.
- **Soma horizontal (tabela sem linha `Total`).** Tabela-matriz — categorias em
  coluna, um item por linha — nao tem linha `Total` e por isso e invisivel a soma
  vertical, que pula a tabela inteira. Agrupa as colunas pelo primeiro nivel do
  cabecalho e soma as percentuais por linha. Conjunto exaustivo fecha em 100;
  multipla resposta nao fecha em nenhuma linha; fechar em **algumas** linhas e a
  assinatura do desalinhamento. Tabela que nem assim possa ser checada e contada
  e reportada em stderr — nao desaparece no denominador.
- **Universo.** Sinaliza tabela cuja base excede a amostra completa do documento.
  Toda tabela é a amostra inteira ou um recorte dela; base acima da moda é
  universo diferente. Nenhuma aritmética interna enxerga isso — uma tabela com a
  geografia trocada é perfeitamente consistente consigo mesma.
- **Inventário de layout e supressão.** Estruturas de cabeçalho descobertas sem
  hardcode; células suprimidas (`x`) contadas e reportadas por subgrupo.

### 2. Cobertura vem antes de falhas

O relatório abre pela cobertura: quantas colunas tinham `Total` **com total
declarado** e quantas foram efetivamente checadas. Colunas cujo `Total` é traço
(margem de erro, tipicamente) ficam fora do denominador — o documento declara que
não há total; não é lacuna de verificação. Célula suprimida no corpo, sim, conta
contra a cobertura.

Abaixo de `COVERAGE_MIN` (80%) o script grava os arquivos mas grita em stderr.
Divergência de rota é prova de corrupção e aborta; cobertura baixa é prova de
ignorância sobre o formato da célula e avisa.

**Reportar ao usuário: cobertura, falhas de soma, falhas de marginal, tabelas
acima do teto de universo, células suprimidas.** Não uma garantia genérica de que
"deu certo".

### 3. Interpretar não fechamento pelo padrão, não pelo caso

O relatório agrupa falhas de marginal por assinatura de subgrupos e classifica:

| padrão | leitura provável |
|---|---|
| consistente (0 falhas) | ok |
| sistemático (≥90% não fecha) | categoria de não-resposta excluída do cruzamento |
| pontual (≤10%) ou errático | desalinhamento — investigar |

Falha sistemática costuma ser característica da base, não erro. Falha errática é
a assinatura do bug. A distinção é do pesquisador, mas o script tem de apresentá-la
já agrupada — cru, "centenas de falhas" parece catástrofe e é estrutura.

### 4. Consultar o CSV, nunca a memória

Toda pergunta posterior sobre um valor específico é respondida consultando
`<prefix>_tidy.csv`, não recitando de memória. Números lidos há muitas mensagens
não são confiáveis por recordação, ainda que tenham sido extraídos corretamente.

Vale também para conversa anterior: transcrição de sessão passada é memória, não
fonte. Se o CSV não estiver no contêiner, pedir o `.docx` — e, se existir, também
o CSV antigo, que permite testar reprodutibilidade da extração entre sessões.

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `<prefix>_tidy.csv` | formato longo: `tabela_n, tabela_idx, titulo, coluna, categoria, valor, fonte_nota` |
| `<prefix>_wide/tabela_NNN.csv` | grade impressa de cada tabela, uma por arquivo |
| `<prefix>_report.md` | cobertura, checagens e inventário |

O campo `valor` guarda o **texto literal** da célula (`"±2,9%"`, `"1.234.567"`,
`"2,31 p.p."`). Converter para numérico é decisão de análise, feita depois e de
forma auditável contra a origem. Não converter na extração.

`coluna` é o caminho hierárquico do cabeçalho (`<Região> > Margem de erro`),
o que resolve cabeçalhos de dois níveis sem ambiguidade.

## Confronto entre anexos (marginais vs. cruzamentos)

Extrair os dois anexos e rodar:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/confront_annexes.py" \
    SIMPLES_tidy.csv CRUZADO_tidy.csv \
    --label-map ./label_map.csv --out ./outputs
```

As marginais do anexo cruzado têm de reproduzir o anexo simples. É a checagem mais
forte disponível: valida milhares de células contra documento independente, não
contra aritmética interna.

O pareamento é por questão + população, normalizando o recorte geográfico do
título. Duas armadilhas:

- **Rótulo divergente entre anexos.** A mesma questão às vezes aparece com
  enunciado diferente nos dois documentos. Não é adivinhável; vive em
  `label_map.csv`, que pertence à pesquisa e fica junto dos dados dela, não na
  skill (formato em `scripts/label_map.example.csv`; a última linha mostra o
  muitos-para-um). Questão sem par é reportada, nunca descartada
  em silêncio — se for só redação, acrescentar a linha no mapa.
- **Supressão assimétrica.** Um anexo publica o que o outro suprime com `x`. Sai
  como "sem contraparte", não como divergência, e é achado a reportar.

Discrepância é achado a reportar, não a corrigir por conta própria — pode ser
arredondamento, ponderação diferente ou erro real, e a distinção é do pesquisador.

## Quando a checagem falha por limite do script

Distinguir **defeito do dado** de **limite da ferramenta** é parte do fluxo, não
consequência dele. Se uma checagem falha, não fecha ou não roda porque o script
não reconhece um formato — e não porque o número está errado — a correção do
script é entregável da tarefa, junto com o relatório:

1. demonstrar que é limite da ferramenta, medindo (magnitude do gap, contagem por
   grupo, célula de origem no `.docx`), nunca por inspeção dos primeiros casos;
2. corrigir o script e re-rodar;
3. registrar a lição em *Armadilhas conhecidas* abaixo;
4. **não** silenciar o achado: relatório automático com falso positivo gravado em
   disco é pior que falha ruidosa, porque alguém vai lê-lo sem contexto.

A distinção entre erro de dado e limite de script é do pesquisador; apresentar a
evidência que permite fazê-la é do script.

## Armadilhas conhecidas

- **`id()` de elemento lxml não é identidade.** O lxml cria proxies sob demanda e
  reaproveita endereços de memória. Usar `id(cell._tc)` para detectar mesclagem
  colapsa células distintas e o erro é silencioso. Usar `getroottree().getpath()`.
- **Valor repetido não é mesclagem.** Duas colunas com `9%` lado a lado não são
  célula mesclada. Só a estrutura XML (`gridSpan`, `vMerge`) decide isso.
- **Quebra de linha dentro da célula.** `Amostra<br/>Observada` vira
  `"AmostraObservada"` se o `<w:br>` for ignorado. O script insere espaço nos
  elementos `br`, `tab` e `cr`.
- **`row.cells` repete a mesma célula em mesclagem horizontal.** A grade impressa
  quer essa repetição; a contagem de células físicas, não.
- **Célula empacotada escapa do parser ingênuo.** `^(\d+)%$` não casa
  `9% (±5,8%)`. Assim um documento inteiro pode passar com zero checagens
  executadas e cara de aprovado. Qualquer formato novo de célula é candidato ao
  mesmo — por isso a cobertura é reportada.
- **Múltipla resposta não soma 100%.** Tabelas de "assinale todas" têm percentuais
  somando bem acima de 100. A checagem só se aplica quando existe linha `Total`
  que declara o total esperado.
- **Base declarada ≠ base efetiva.** Cruzamento por variável que exclui
  não-declarantes (renda, religião) tem subgrupos somando menos que a marginal em
  todas as tabelas. É estrutura, e muda o denominador de qualquer comparação entre
  anexos naquela variável.
- **Cabeçalho plano no anexo simples.** Um confronto que indexa colunas só
  quando o cabeçalho é hierárquico (`... > Sim`) fica cego para anexos de
  cabeçalho plano (`Estimativa | Margem de erro | ...`): quase todas as questões
  saem como "sem coluna Estimativa", zero pareadas, com cara de documentos
  incompatíveis. Indexar sempre pela folha do caminho.

- **Taxa de falha não distingue arredondamento de desalinhamento.** `Amostra
  Ponderada` é soma de valores arredondados: erra por 1 unidade em bases de
  milhares. Classificar só pela taxa marca esses casos como ERRÁTICO. Medir a
  magnitude do gap antes de classificar.

- **Rótulo de população pode divergir entre anexos.** Um anexo identifica a
  subpopulação no título; o outro deixa no título a população ampla e joga o
  filtro para a nota de rodapé. O pareamento por título casa a tabela errada e
  produz divergência espúria em massa. Conferir a nota de rodapé antes de
  concluir que dois anexos discordam.

- **Tabela sem linha `Total` sai do denominador da cobertura e não aparece.**
  Se a soma vertical pula a tabela inteira quando não há linha `Total`, e a
  cobertura só conta colunas de tabelas que a têm, o relatório pode dizer
  **100%** com uma fração grande das células do documento fora de toda
  checagem. É 100% do que a ferramenta enxerga, que é outra coisa.
  Tabelas-matriz ("Quais destes serviços você conhece?", com os itens em linha e
  as categorias em coluna) não têm linha `Total`. A checagem que falta é
  horizontal: agrupar colunas pelo primeiro nível do cabeçalho e somar as
  percentuais por linha. Conjunto exaustivo fecha em 100; múltipla resposta não
  fecha em linha alguma; **fechar em algumas linhas e não em outras é
  desalinhamento**. Tabela que sobra sem verificação alguma é contada e gritada
  em stderr, com o número de células.

- **Nota de rodapé pode explicar o não fechamento inteiro.** Uma nota do tipo
  "a coluna do total inclui quem respondeu 'Não sei/Prefiro não responder'"
  declara que a marginal absorve uma categoria que não existe como linha: ela
  não pode fechar. Quando todos os não fechamentos são déficit e todos estão em
  tabelas com essa nota, e nenhuma tabela com a nota fecha, é estrutura
  declarada. O script classifica esses casos à parte e os mantém visíveis;
  déficit SEM a nota, ou qualquer excesso, continua saindo como inexplicado, que
  é onde o desalinhamento apareceria. Ler a contagem bruta de não fechamentos
  sem esse agrupamento é confundir estrutura com defeito.

- **A subpopulação pode estar só na nota.** Um anexo nomeia a subpopulação no
  título e na nota; outro deixa a população ampla em todos os títulos e declara
  o filtro apenas numa nota ("Respostas filtradas para <subgrupo>"). Parear por
  título casa a tabela filtrada com a não filtrada e produz divergências que são
  artefato do pareamento, não discordância entre documentos. Pior: se o outro
  anexo publica AS DUAS versões da mesma questão, o par errado fica
  indistinguível do certo pelo título. A população modal do anexo é o universo
  padrão; qualquer outra coisa, dita no título ou na nota, é subpopulação e
  entra na chave. Dois filtros distintos no mesmo anexo colidiriam, e o script
  marca como ambíguo em vez de comparar errado.

- **A mesma questão aparece como matriz num anexo e decomposta no outro.** Um
  anexo publica "Tipo de X" como UMA tabela-matriz (itens em linha, categorias
  em coluna); o outro publica "Tipo de X [Item A]" como questão própria. São
  transpostas uma da outra: `matriz[item][Sim]` é a mesma célula que
  `decomposto[Sim]` da marginal. Parear só por texto deixa essas questões sem
  par, justamente na forma cuja única outra checagem é interna. Tentar a
  decomposição `<base> [<item>]` contra a matriz `<base>` resolve e vale como
  verificação contra documento independente.

- **`label_map.csv` é fallback, e muitos-para-um.** Aplicado
  incondicionalmente, o mapa reescreve também os pares que já casavam: traduzir
  `[... autorização?]` em `[... autorização]` conserta um anexo e DESPAREIA
  outro, em que os dois lados já traziam a mesma forma. Tentar a questão como
  escrita primeiro e consultar o mapa só quando nada parear. E a mesma questão
  do cruzado pode corresponder a redações diferentes em anexos diferentes, então
  o mapa aceita várias linhas com a mesma origem e tenta cada uma; 1:1 obrigaria
  um anexo a perder.

- **Recorte geográfico fixo no código pareia um caso e zero nos demais.** Uma
  regex que nomeia o recorte do primeiro documento testado ("<Estado>|<Região>|
  Brasil") pareia tudo nele e **nada**, em silêncio, nos outros recortes, com a
  cara de documentos incompatíveis e não de uma ferramenta calibrada para um
  caso. Se o título termina em `- <escopo> - <ano>`, derivar por POSIÇÃO (o
  último segmento é o ano, o anterior é o escopo) resolve para qualquer recorte.
  O escopo permanece NA chave, na forma canônica antes da vírgula: sem isso, o
  anexo simples de um recorte pareia com o cruzado de outro e a diferença sai
  como divergência. Manter um teste negativo: simples de um recorte contra
  cruzado de outro tem de parear zero.

- **Supressão assimétrica é achado, não ruído.** Um anexo publica uma
  estimativa apoiada em pouquíssimas observações (margem de erro maior que a
  própria estimativa); o outro suprime a mesma marginal com `x`. O critério de
  não divulgação foi aplicado num anexo e não no outro. Sai como "sem
  contraparte" no confronto e precisa chegar ao pesquisador: é uma estimativa
  que não deveria ser usada.

- **Traço no corpo é zero; traço no `Total` é ausência de total.** O mesmo `-`
  significa coisas diferentes conforme a linha. Tratar os dois como célula
  suprimida bloqueia a checagem de toda coluna que tenha uma categoria sem
  casos, justamente as colunas onde um desalinhamento passaria batido. A prova
  de que é limite da ferramenta, e não do dado, está na própria linha `Total`:
  `a + b + - = Total` só fecha com `-` = 0.

- **Não generalizar a partir das primeiras linhas de um diagnóstico.** Ao listar
  divergências, imprimir a contagem por grupo, não os primeiros N casos. Foi assim
  que dois problemas distintos viraram um só na leitura.

## Dependências

`python-docx`, `lxml`. Ambos costumam já estar disponíveis; instalar apenas se o
`import` falhar.
