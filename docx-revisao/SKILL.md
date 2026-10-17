---
name: docx-revisao
description: >-
  Revisão de arquivos .docx locais, no texto e nos comentários, sempre numa
  cópia: o original nunca é alterado. Texto (substituir, reescrever trechos,
  formatar, mexer em parágrafos e tabelas) vai pelo servidor MCP do Word
  (Office-Word-MCP-Server); comentários (listar quem comentou o quê, inserir
  balões ancorados em trechos, anotar a fonte de cada número, transplantar
  observações de um documento para versões parecidas, trocar o autor dos
  balões, conferir se sobreviveram a uma edição) vão pelo motor Python da
  skill, que monta as partes OOXML que o Word exige e verifica cada âncora. Use
  sempre que o usuário pedir para editar, corrigir, revisar, comentar ou
  anotar um documento Word, ou mandar um caminho terminado em .docx para
  manipulação, mesmo sem citar a skill. Típico em pareceres, manuscritos,
  releases e relatórios revisados por várias pessoas. Não use para só extrair
  ou conferir números de tabelas (use docx-tabelas-validadas) nem para .pdf ou
  .xlsx. NUNCA grave no arquivo original; NUNCA invente o nome da cópia sem
  confirmar com o usuário.
---

# Revisão de .docx: texto e comentários

## Regra única: o original é imutável

**Toda alteração vai para uma cópia, e o arquivo de partida nunca é
regravado.** Vale para texto e para comentários, sem exceção. Erros de
edição, mal-entendidos sobre o pedido e bugs das ferramentas não podem
corromper o documento de partida: documentos institucionais, manuscritos e
relatórios técnicos raramente têm versionamento fora do disco do usuário, e
perder o original costuma ser irreversível.

- **Nome da cópia:** se o usuário não disser, propor e confirmar antes de
  criar. Preferência: `<nome>_revisado.docx` para texto, `<nome>_comentado.docx`
  só para comentários, `<nome>_<AAAA-MM-DD>.docx` quando houver várias rodadas.
- **Uma cópia de trabalho por tarefa.** Criada a cópia, as operações seguintes
  da mesma tarefa (outra substituição, os comentários depois do texto) vão
  nela. Não criar uma cópia nova a cada passo.
- **Nunca sobrescrever** uma cópia que já existe de antes da tarefa: escolher
  outro nome com o usuário.

## Roteamento

| O pedido mexe em | Ferramenta | Onde está o detalhe |
|---|---|---|
| texto, formatação, parágrafos, tabelas | servidor MCP `word` | abaixo, *Texto* |
| comentários (ler, criar, transplantar, reautorar) | `scripts/docx_comments.py` e `scripts/transplantar.py` | `references/comentarios.md` |
| os dois | texto primeiro, depois os comentários **na mesma cópia** (`na_copia=True` / `--na-copia`) | os dois acima |

Comentários e texto têm motores diferentes porque o servidor MCP do Word só
**lê** comentários: não cria. O motor de comentários impõe a regra da cópia
sozinho: recusa gravar na entrada e recusa sobrescrever arquivo existente.

## Texto

### 1. Inspecionar o original

`get_document_outline` no arquivo de partida. Reportar em poucas linhas:
número de parágrafos, títulos principais e tabelas. Confirmar o plano de edição
com o usuário antes de criar qualquer arquivo; é aí que se corrige escopo.

### 2. Criar a cópia

`copy_document(origem, destino)`, com o nome confirmado. A cópia preserva a
formatação: o `copy_document` clona a estrutura inteira (estilos, cabeçalhos e
rodapés, tabelas, imagens, numeração e os comentários que já existiam).

### 3. Editar a cópia

Ferramentas, da mais para a menos robusta:

1. **`search_and_replace`**: primeira escolha para substituições. Não depende de
   índices.
2. **`format_text`**: ajustes de formatação pontuais. Índices mudam depois de
   inserções e remoções.
3. **`add_paragraph`, `delete_paragraph`**: só quando necessário. Depois de
   qualquer operação que mude a quantidade de parágrafos, **reinspecionar** com
   `get_document_outline` antes da próxima edição que dependa de índice.
4. **`add_table`, `format_table`, `merge_table_cells` etc.**: tabelas, com a
   mesma cautela com índices.

### 4. Verificar e reportar

- `get_document_text` na cópia e conferir que cada alteração pretendida está lá.
- Se houver comentários no documento, `list_comments` (motor) antes e depois:
  edição de texto pode apagar a âncora de um balão.
- Reportar: quantas alterações, um antes/depois curto de cada tipo e o caminho
  absoluto da cópia final.

### Limitações do servidor MCP do Word

Dizer ao usuário quando aparecerem:

- **Controle de alterações** pode não ser preservado em todas as operações.
- **WordArt, SmartArt, equações e campos calculados** passam para a cópia como
  estão, mas não são editáveis.
- **Estilos personalizados** só funcionam se já existirem no original.
- **Cabeçalhos e rodapés** são preservados, mas editá-los tem suporte parcial.

Em documento de formatação muito complexa ou em revisão editorial final, tratar
o resultado como ponto de partida e recomendar uma revisão manual.

## Comentários

Ler `references/comentarios.md` antes de qualquer operação com comentários. O
resumo do fluxo:

1. `list_comments` no documento de partida (autor, texto, âncora com offsets).
2. Ensaio (`apply=False`, ou o `transplantar.py` sem `--aplicar`), que mostra
   onde cada comentário cairia e o nome da cópia. **Mostrar os candidatos
   `DUVIDOSO` e o nome da cópia ao usuário e esperar a confirmação.**
3. Aplicar com `saida=<cópia nova>` ou, se a cópia de trabalho já existe,
   `na_copia=True`.
4. `verify` na cópia, mais releitura dos comentários gravados (autor e âncora).

## Quando parar e perguntar

Se houver dúvida sobre qual arquivo é o original, qual o nome da cópia, o que
exatamente alterar ou onde um comentário deve cair, **parar e perguntar**. Não
improvisar nome, não adivinhar substituição, não ancorar num parágrafo
aproximado. Uma pergunta a mais custa pouco; editar o arquivo errado ou
ancorar no trecho errado custa caro e chega ao leitor.

## Dependências

Servidor MCP `word` para o texto. Para os comentários, `lxml` (obrigatória) e
`python-docx` (verificação independente); instalar só se o `import` falhar.
