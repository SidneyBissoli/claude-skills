# Comentários em .docx (referência da skill docx-revisao)

Ler quando o pedido envolver comentários. A regra da cópia do `SKILL.md` vale
aqui também e é imposta pelo motor: nenhuma operação grava no arquivo de
entrada.

Um comentário do Word não é um registro: são **sete lugares** no pacote OOXML, e
esquecer qualquer um deles produz um arquivo que abre normalmente e perde o
comentário em silêncio.

| lugar | papel |
|---|---|
| `word/comments.xml` | texto, autor, iniciais, data |
| `word/commentsExtended.xml` | `paraId`, estado resolvido, encadeamento de respostas |
| `word/commentsIds.xml` | `durableId` |
| `word/commentsExtensible.xml` | metadados de data |
| `word/document.xml` | a âncora: `commentRangeStart` + `commentRangeEnd` + `commentReference` |
| `[Content_Types].xml` | um override por parte |
| `word/_rels/document.xml.rels` | um relationship por parte |

`python-docx` não escreve nada disso. O `Office-Word-MCP-Server` só **lê**
comentários (`get_all_comments`, `get_comments_by_author`,
`get_comments_for_paragraph`) — não cria. Por isso a parte de comentários tem
motor próprio, `scripts/docx_comments.py`, biblioteca Python pura.

## Arquitetura: motor e cascas

```
scripts/docx_comments.py          ← o motor: toda a lógica de OOXML
      ├── scripts/transplantar.py            casca CLI (esta skill)
      └── docx-comentarios-mcp              casca MCP (projeto à parte; Desktop, claude.ai)
```

**A lógica nunca mora na interface.** As duas cascas chamam as mesmas funções;
uma regra nova sobre OOXML muda no motor e as duas acompanham. Se você se
flagrar copiando lógica para uma casca, a arquitetura foi violada — mova para o
motor.

Operações de alto nível, as que as cascas chamam:

| função | o que faz |
|---|---|
| `list_comments(path)` | comentários com autor, texto e âncora localizada (parágrafo + offsets) |
| `candidates(origem, destino, ids)` | onde cada comentário cairia no destino, classificado |
| `transplant(origem, destino, ids, author, ...)` | copia comentários entre documentos, reautorando |
| `add_comment(path, trecho, texto, author, ...)` | cria comentário novo ancorado num trecho |
| `verify(path)` | integridade nas sete partes |

`transplant` e `add_comment` com `apply=False` devolvem o plano sem tocar em
nada. Com `apply=True` exigem um destino de gravação:

- `saida=<arquivo novo>`: o motor recusa se for o próprio arquivo de entrada ou
  um arquivo que já existe;
- `na_copia=True`: só quando a entrada JÁ É a cópia de trabalho criada nesta
  tarefa (por exemplo, depois de editar o texto nela).

Em ambos os casos gravam num temporário, rodam `verify` e só então movem o
resultado para o lugar; se a verificação falhar, nada é gravado.

## Fluxo

### 1. Ler antes de propor qualquer coisa

```bash
python scripts/docx_comments.py   # importar como módulo
```

`list_comments(path)` devolve, por comentário: id, autor, iniciais, data, texto,
**e a âncora localizada** — `par_ini`/`off_ini` e `par_fim`/`off_fim`, índice de
parágrafo e deslocamento em caracteres. Offsets, não apenas o texto, porque a
âncora costuma ser um trecho no meio de um parágrafo e o mesmo trecho pode
ocorrer mais de uma vez.

### 2. Ensaiar o transplante e submeter os candidatos ao usuário

```bash
python scripts/transplantar.py ORIGEM.docx --para DEST1.docx DEST2.docx \
    --ids 5 21 27 --autor "Nome Sobrenome" [--iniciais NS] [--imagem 6=4] \
    [--sufixo _comentado | --na-copia]
```

Sem `--aplicar` nada é gravado: é ensaio. Cada destino gera uma cópia nova,
`<destino><sufixo>.docx` (padrão `_comentado`), e o ensaio mostra o nome de
cada uma: **confirme os nomes com o usuário junto com os candidatos.** O
relatório classifica cada comentário em cada destino:

| classe | significado | conduta |
|---|---|---|
| `EXATO` | o texto da âncora existe literalmente no destino | inserir |
| `QUASE` | cobertura ≥ 0,80 do trecho por blocos casados | inserir, mostrando o trecho |
| `DUVIDOSO` | cobertura baixa | **perguntar ao usuário** |
| `SEM_TEXTO` | âncora sobre imagem ou elemento sem texto | usar `--imagem id=n` |

**Mostre os trechos e peça confirmação nos DUVIDOSO.** Escrever heurística para
adivinhar esses casos custa mais que a revisão humana e acerta menos. Comentário
ancorado no trecho errado é defeito que não aparece na leitura e chega ao
público.

### 3. Aplicar, com a verificação como condição

```bash
python scripts/transplantar.py ... --aplicar
```

Grava num temporário, roda `verify`, e **só então** cria a cópia. Se a
verificação acusar qualquer problema o temporário é descartado e nada é criado.
Os destinos nunca mudam. Se uma cópia com o mesmo nome já existe, o comando
recusa e sai com código 1: escolha outro `--sufixo` com o usuário.

### 4. Verificar, e não perguntar se "abriu"

`verify(path)` confere os sete lugares: cada id com exatamente um
`commentRangeStart`, um `End` e um `Reference`; nenhuma âncora apontando para
comentário inexistente; contagem batendo entre `comments.xml`,
`commentsExtended` e `commentsIds`; overrides e relationships presentes.

Complemente com uma leitura por biblioteca de terceiro — abrir o arquivo com
`python-docx` e conferir parágrafos e imagens — e com o round-trip: reler os
comentários gravados e comparar autor e âncora com o pretendido. Três rotas
independentes, porque `verify` é código da própria casa.

## Criar comentários novos

`new_comment_element` monta um `<w:comment>` do zero — transplantar copia o
elemento da origem e preserva a formatação, mas criar exige montar a estrutura
mínima que o Word espera: um parágrafo cujo primeiro run carrega o estilo
`CommentReference` e o `<w:annotationRef/>`, sem o qual o balão aparece sem a
marca de referência.

Na prática use `add_comment(path, trecho, texto, author)`, que localiza o trecho,
ancora, cria o registro nas quatro partes e verifica:

```python
# ensaio
dc.add_comment(original, '29%', 'Tabela N do anexo A: ...',
               'Nome Sobrenome', occurrence=0, apply=False)
# primeiro comentário: cria a cópia
dc.add_comment(original, '29%', 'Tabela N do anexo A: ...',
               'Nome Sobrenome', saida='relatorio_comentado.docx')
# os seguintes: na mesma cópia de trabalho
dc.add_comment('relatorio_comentado.docx', '31%', 'Tabela M ...',
               'Nome Sobrenome', na_copia=True)
```

`occurrence` escolhe qual ocorrência quando o trecho se repete — `29%` costuma
aparecer várias vezes no mesmo documento, e a primeira nem sempre é a certa.

### Padrão: anotar a fonte de cada número

Caso de uso recorrente em release de imprensa e relatório: ancorar em cada número
um comentário dizendo de onde ele saiu ("Tabela N do anexo A"), para o revisor
conferir sem abrir o anexo.

O que esse trabalho ensinou:

- **Ancore no número, não na frase.** Estenda a âncora para incluir o `%` — o
  balão em `29%` lê melhor que em `29`.
- **Não anote o que não vem de tabela.** Ano, "12 meses", "16 anos ou mais",
  telefone de serviço, nível de confiança. Anotar tudo polui e ensina o revisor a
  ignorar os balões.
- **Meça a cobertura ao final:** liste os números que ficaram sem anotação e
  confira que são exatamente os não-anotáveis. Sem isso, um número esquecido não
  se distingue de um número deliberadamente fora do escopo.
- **Número derivado merece a conta, não a tabela.** "Calculado: <parte> /
  <todo> = <percentual>, com os dois termos da Tabela N" vale mais que um
  ponteiro para uma tabela que não traz aquele valor.
- **Número sem fonte no material disponível também recebe anotação**, dizendo
  isso. Silêncio deixa o revisor sem saber se você verificou e não achou, ou se
  nem olhou.

## Reautoração

`--autor` e `--iniciais` reescrevem o autor dos comentários copiados. Preserve a
**data original**: ela registra quando a observação foi feita, e trocá-la apaga
informação real. Se o original tem iniciais vazias, mantenha vazias — replicar a
estrutura é mais fiel que preencher por conta própria.

Quando o usuário pedir um formato de nome condicionado ao original ("se estiver
completo, use o meu completo abreviado"), confira o que o original **de fato**
traz antes de aplicar a regra: autor pode ser um endereço de e-mail, que não é
nem nome completo nem primeiro nome. Pergunte em vez de escolher por ele.

## Armadilhas conhecidas

- **Documento de destino sem nenhum comentário não tem NADA.** Nem as quatro
  partes, nem os overrides, nem os relationships. Faltando qualquer um dos dois
  registros de pacote, o Word ignora a parte em silêncio: o arquivo abre e os
  comentários simplesmente não existem. `ensure_parts` cria os sete.

- **Dividir o run no início antes do fim corrompe o intervalo.** A âncora quase
  nunca começa na fronteira de um `w:r` — o Word fatia o texto por formatação e
  por marca de revisão. Dividir primeiro no início insere um run novo e desloca
  o deslocamento do fim. Divida sempre no FIM primeiro.

- **Mapear posição relativa recorta o trecho errado.** Documentos parecidos não
  são iguais: uma versão estadual pode fundir num só parágrafo o que outra
  escreve em dois, e o mapeamento posicional pega o começo do parágrafo, isto é,
  outra frase. Alinhar por **blocos de texto em comum** (`locate_span`) encontra
  o trecho onde quer que ele esteja, e os pontos em que os documentos divergem
  (o gentílico, o número) simplesmente não entram nos blocos. A normalização
  (`neutral`) já troca números, as 27 UFs e os gentílicos por marcadores; outros
  recortes entram pelo parâmetro `extra`.

- **Contar uma imagem por parágrafo não serve.** Um cabeçalho pode concentrar
  vários logotipos num parágrafo só, e então a imagem comentada é a n-ésima do
  documento, que o contador por parágrafo nunca alcança. Conte por run
  (`find_drawing`).

- **"Vale para todos os documentos" é intenção, não garantia.** Um comentário
  pode não ter onde ancorar porque a frase criticada não existe no outro
  documento. Uma observação marcada "vale para todos" pode ter objeto só em
  parte das versões, porque as outras não trazem a frase comentada. Reporte o
  que ficou de fora **e por quê**;
  não ancore num parágrafo aproximado para não deixar buraco.

- **`ln -s` no Git Bash copia o diretório em vez de linkar.** Vale para a
  instalação da própria skill. O `ls` mostra `drwxr-xr-x` em vez de
  `lrwxrwxrwx`, e as duas cópias divergem em silêncio a partir da primeira
  edição. Use `New-Item -ItemType Junction` no PowerShell e **confirme com teste
  de identidade** — criar um arquivo de um lado e conferir que aparece do outro.
  O que o comando responde não é prova; o teste é.
