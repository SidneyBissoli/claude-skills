# -*- coding: utf-8 -*-
"""Motor de comentarios .docx: ler, transplantar, reautorar, verificar.

Biblioteca pura — sem MCP, sem dependencia de cliente. As interfaces (skill via
CLI, servidor MCP) sao cascas finas sobre este modulo. A logica mora aqui uma
vez so.

Por que isto existe: um comentario do Word nao e um registro, e sete lugares no
pacote OOXML —

    word/comments.xml            texto, autor, iniciais, data
    word/commentsExtended.xml    paraId, estado resolvido, encadeamento
    word/commentsIds.xml         durableId
    word/commentsExtensible.xml  metadados de data
    word/document.xml            a ancora: commentRangeStart/End + commentReference
    [Content_Types].xml          4 overrides
    word/_rels/document.xml.rels 4 relationships

python-docx nao escreve nada disso, e o Office-Word-MCP-Server so LE comentarios
(get_all_comments, get_comments_by_author, get_comments_for_paragraph). Uma
ancora orfa — commentRangeStart sem End, ou Reference apontando para id
inexistente — abre no Word sem erro visivel e perde o comentario em silencio.
Por isso `verify` e obrigatorio no fluxo, nao opcional.
"""
import copy
import difflib
import os
import re
import shutil
import unicodedata
import zipfile
from collections import OrderedDict

from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'
W15 = '{http://schemas.microsoft.com/office/word/2012/wordml}'
CT = '{http://schemas.openxmlformats.org/package/2006/content-types}'
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'

PARTS = {
    'word/comments.xml': (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml',
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments'),
    'word/commentsExtended.xml': (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml',
        'http://schemas.microsoft.com/office/2011/relationships/commentsExtended'),
    'word/commentsIds.xml': (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml',
        'http://schemas.microsoft.com/office/2016/09/relationships/commentsIds'),
    'word/commentsExtensible.xml': (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtensible+xml',
        'http://schemas.microsoft.com/office/2018/08/relationships/commentsExtensible'),
}


def _txt(el):
    return ''.join(t.text or '' for t in el.iter(W + 't'))


def _norm(s):
    return ' '.join((s or '').split())


# ------------------------------------------------------------------ leitura

def read_parts(path):
    """Todas as partes XML do pacote, como dict nome -> bytes."""
    with zipfile.ZipFile(path) as z:
        return OrderedDict((n, z.read(n)) for n in z.namelist())


def paragraphs(doc_root):
    """Lista de elementos w:p na ordem do documento."""
    return list(doc_root.iter(W + 'p'))


def list_comments(path):
    """Comentarios do documento, com autor, texto e ancora localizada.

    Cada item traz `par_ini`/`off_ini` e `par_fim`/`off_fim`: indice do
    paragrafo e deslocamento em caracteres dentro do texto daquele paragrafo.
    Offsets, e nao apenas o texto, porque a ancora pode ser um trecho no meio de
    um paragrafo e o mesmo trecho pode ocorrer mais de uma vez.
    """
    parts = read_parts(path)
    if 'word/comments.xml' not in parts:
        return []
    croot = etree.fromstring(parts['word/comments.xml'])
    meta = {}
    for c in croot.findall(W + 'comment'):
        meta[c.get(W + 'id')] = dict(
            id=c.get(W + 'id'), author=c.get(W + 'author') or '',
            initials=c.get(W + 'initials') or '', date=c.get(W + 'date') or '',
            text=_norm(' '.join(_txt(p) for p in c.findall(W + 'p'))),
            element=c)

    droot = etree.fromstring(parts['word/document.xml'])
    pars = paragraphs(droot)
    idx = {id(p): i for i, p in enumerate(pars)}
    pos = {}
    for i, p in enumerate(pars):
        run = 0
        for el in p.iter():
            if el.tag == W + 't':
                run += len(el.text or '')
            elif el.tag == W + 'commentRangeStart':
                pos.setdefault(el.get(W + 'id'), {})['ini'] = (i, run)
            elif el.tag == W + 'commentRangeEnd':
                pos.setdefault(el.get(W + 'id'), {})['fim'] = (i, run)

    out = []
    for cid, m in meta.items():
        p = pos.get(cid, {})
        ini, fim = p.get('ini'), p.get('fim')
        anchor = ''
        if ini and fim:
            if ini[0] == fim[0]:
                anchor = _txt(pars[ini[0]])[ini[1]:fim[1]]
            else:
                bits = [_txt(pars[ini[0]])[ini[1]:]]
                bits += [_txt(pars[k]) for k in range(ini[0] + 1, fim[0])]
                bits.append(_txt(pars[fim[0]])[:fim[1]])
                anchor = ' '.join(bits)
        m = dict(m)
        m.pop('element')
        m.update(par_ini=ini[0] if ini else None, off_ini=ini[1] if ini else None,
                 par_fim=fim[0] if fim else None, off_fim=fim[1] if fim else None,
                 anchor=_norm(anchor))
        out.append(m)
    return out


# ------------------------------------------------------- alinhamento/candidato

# Nomes de recorte que variam entre versoes estaduais de um mesmo documento:
# as 27 UFs e seus gentilicos. Documentos de outro recorte (municipios, paises)
# passam termos proprios em `extra`.
_UFS = [
    ('Acre', 'acreano'), ('Alagoas', 'alagoano'), ('Amapá', 'amapaense'),
    ('Amazonas', 'amazonense'), ('Bahia', 'baiano'), ('Ceará', 'cearense'),
    ('Distrito Federal', 'brasiliense'), ('Espírito Santo', 'capixaba'),
    ('Goiás', 'goiano'), ('Maranhão', 'maranhense'),
    ('Mato Grosso do Sul', 'sul-mato-grossense'), ('Mato Grosso', 'mato-grossense'),
    ('Minas Gerais', 'mineiro'), ('Pará', 'paraense'), ('Paraíba', 'paraibano'),
    ('Paraná', 'paranaense'), ('Pernambuco', 'pernambucano'), ('Piauí', 'piauiense'),
    ('Rio de Janeiro', 'fluminense'), ('Rio Grande do Norte', 'potiguar'),
    ('Rio Grande do Sul', 'gaúcho'), ('Rondônia', 'rondoniense'),
    ('Roraima', 'roraimense'), ('Santa Catarina', 'catarinense'),
    ('São Paulo', 'paulista'), ('Sergipe', 'sergipano'), ('Tocantins', 'tocantinense'),
]


def _recortes():
    termos = set()
    for nome, gent in _UFS:
        for t in (nome, gent, gent[:-1] + 'a' if gent.endswith('o') else gent):
            termos.add(t)
            termos.add(unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode())
    termos.discard('Para')  # "Pará" sem acento e a preposicao em inicio de frase
    # mais longo primeiro: "Mato Grosso do Sul" antes de "Mato Grosso"
    return sorted(termos, key=len, reverse=True)


_RECORTES = _recortes()


def neutral(s, extra=()):
    """Neutraliza o que varia entre versoes de um documento: numeros e nomes de
    recorte (UF, gentilico e o que vier em `extra`)."""
    s = re.sub(r'\d[\d.,]*', '#', s or '')
    for termo in sorted(extra, key=len, reverse=True):
        s = s.replace(termo, '@')
    for termo in _RECORTES:
        s = s.replace(termo, '@')
    return s.lower()


def match_paragraph(src_text, dst_pars):
    """Indice e escore do paragrafo de destino equivalente a src_text."""
    ns = neutral(src_text)
    best, score = None, 0.0
    for i, p in enumerate(dst_pars):
        r = difflib.SequenceMatcher(None, ns, neutral(p)).ratio()
        if r > score:
            best, score = i, r
    return best, score


def map_span(src_par, dst_par, ini, fim):
    """Mapeia o intervalo [ini,fim) do paragrafo de origem para o de destino.

    Usa o alinhamento caractere a caractere entre os dois paragrafos, e nao
    busca literal: a ancora costuma diferir exatamente no ponto onde a versao
    troca o nome do estado ou o numero, que e onde a busca literal falharia.
    """
    sm = difflib.SequenceMatcher(None, src_par, dst_par)
    d_ini = d_fim = None
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if d_ini is None and i2 > ini:
            d_ini = j1 + max(0, min(ini - i1, j2 - j1))
        if i2 >= fim:
            d_fim = j1 + max(0, min(fim - i1, j2 - j1))
            break
    if d_ini is None:
        d_ini = 0
    if d_fim is None or d_fim < d_ini:
        d_fim = len(dst_par)
    return d_ini, d_fim


def locate_span(anchor, dst_par):
    """Onde a ancora cai dentro do paragrafo de destino, por blocos casados.

    Nem sempre a ancora corresponde ao paragrafo inteiro: uma versao pode fundir
    num unico paragrafo o que outra escreve em dois, e mapear posicao relativa
    recorta o comeco errado do paragrafo. Alinhar por blocos de texto em comum
    encontra o trecho onde quer que ele esteja, e os pontos em que as versoes
    divergem (o gentilico, o numero) simplesmente nao entram nos blocos.
    """
    sm = difflib.SequenceMatcher(None, anchor, dst_par, autojunk=False)
    blocos = [b for b in sm.get_matching_blocks() if b.size >= 4]
    if not blocos:
        return None, None, 0.0
    ini = blocos[0].b
    fim = blocos[-1].b + blocos[-1].size
    cobertura = sum(b.size for b in blocos) / max(1, len(anchor))
    return ini, fim, round(cobertura, 3)


def candidates(src_docx, dst_docx, ids=None):
    """Para cada comentario da origem, o trecho equivalente no destino.

    Classifica em EXATO (o texto da ancora existe literalmente), QUASE
    (paragrafo equivalente com escore alto), DUVIDOSO e SEM_TEXTO. A
    classificacao existe para separar o que pode ser inserido sem supervisao do
    que precisa de decisao humana — inserir comentario em ancora errada e um
    defeito que nao aparece na leitura e chega ao publico.
    """
    src = list_comments(src_docx)
    if ids is not None:
        ids = {str(i) for i in ids}
        src = [c for c in src if c['id'] in ids]
    droot = etree.fromstring(read_parts(dst_docx)['word/document.xml'])
    dpars = [_txt(p) for p in paragraphs(droot)]
    sroot = etree.fromstring(read_parts(src_docx)['word/document.xml'])
    spars = [_txt(p) for p in paragraphs(sroot)]
    full = ' '.join(_norm(' '.join(dpars)).split())

    out = []
    for c in src:
        r = dict(comment=c, par=None, ini=None, fim=None, trecho='', score=0.0)
        if c['par_ini'] is None or not c['anchor']:
            r['classe'] = 'SEM_TEXTO'
            out.append(r)
            continue
        pi, pf = c['par_ini'], c['par_fim']
        j, score = match_paragraph(spars[pi], dpars)
        r['score'] = round(score, 3)
        if j is None:
            r['classe'] = 'DUVIDOSO'
            out.append(r)
            continue
        bruto = spars[pi][c['off_ini']:(c['off_fim'] if pi == pf else len(spars[pi]))]
        a, b, cob = locate_span(bruto, dpars[j])
        if a is None:
            a, b = map_span(spars[pi], dpars[j], c['off_ini'],
                            c['off_fim'] if pi == pf else len(spars[pi]))
            cob = 0.0
        r.update(par=j, ini=a, fim=b, trecho=_norm(dpars[j][a:b]), cobertura=cob)
        if _norm(c['anchor']) and _norm(c['anchor']) in full:
            r['classe'] = 'EXATO'
        elif cob >= 0.80:
            r['classe'] = 'QUASE'
        else:
            r['classe'] = 'DUVIDOSO'
        if pi != pf:
            r['multiparagrafo'] = True
        out.append(r)
    return out


# ------------------------------------------------------------------- escrita

NS_MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
NS_W15 = 'http://schemas.microsoft.com/office/word/2012/wordml'
NS_W16CID = 'http://schemas.microsoft.com/office/word/2016/wordml/cid'
NS_W16 = 'http://schemas.microsoft.com/office/word/2018/wordml'
NS_W16CEX = 'http://schemas.microsoft.com/office/word/2018/wordml/cex'
W15C = '{' + NS_W15 + '}'
W16CID = '{' + NS_W16CID + '}'
W16CEX = '{' + NS_W16CEX + '}'
XMLSPACE = '{http://www.w3.org/XML/1998/namespace}space'

DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

EMPTY = {
    'word/comments.xml':
        DECL + '<w:comments xmlns:w="' + W[1:-1] + '" xmlns:w14="' + W14[1:-1] + '"/>',
    'word/commentsExtended.xml':
        DECL + '<w15:commentsEx mc:Ignorable="w15" xmlns:mc="' + NS_MC +
        '" xmlns:w15="' + NS_W15 + '"/>',
    'word/commentsIds.xml':
        DECL + '<w16cid:commentsIds mc:Ignorable="w16cid" xmlns:mc="' + NS_MC +
        '" xmlns:w16cid="' + NS_W16CID + '"/>',
    'word/commentsExtensible.xml':
        DECL + '<w16cex:commentsExtensible xmlns:w16="' + NS_W16 +
        '" xmlns:w16cex="' + NS_W16CEX + '" mc:Ignorable="w16 w16cex" xmlns:mc="' +
        NS_MC + '"/>',
}


def ensure_parts(parts):
    """Cria as quatro partes de comentario e as REGISTRA, se faltarem.

    Um destino que nunca teve comentario nao tem nenhuma delas, nem o override
    em [Content_Types].xml, nem o relationship em document.xml.rels. Faltando
    qualquer um dos dois registros o Word ignora a parte em silencio: o arquivo
    abre normalmente e os comentarios simplesmente nao existem. E por isso que
    `verify` confere os sete lugares, e nao so o comments.xml.
    """
    for name, blob in EMPTY.items():
        if name not in parts:
            parts[name] = blob.encode('utf-8')

    ct = etree.fromstring(parts['[Content_Types].xml'])
    have = set(o.get('PartName') for o in ct.findall(CT + 'Override'))
    for name in PARTS:
        if '/' + name not in have:
            o = etree.SubElement(ct, CT + 'Override')
            o.set('PartName', '/' + name)
            o.set('ContentType', PARTS[name][0])
    parts['[Content_Types].xml'] = etree.tostring(
        ct, xml_declaration=True, encoding='UTF-8', standalone=True)

    rels = etree.fromstring(parts['word/_rels/document.xml.rels'])
    have = set(r.get('Target') for r in rels.findall(REL + 'Relationship'))
    used = set(r.get('Id') for r in rels.findall(REL + 'Relationship'))
    n = 900
    for name in PARTS:
        target = name.split('/', 1)[1]
        if target in have:
            continue
        while ('rId%d' % n) in used:
            n += 1
        r = etree.SubElement(rels, REL + 'Relationship')
        r.set('Id', 'rId%d' % n)
        r.set('Type', PARTS[name][1])
        r.set('Target', target)
        used.add('rId%d' % n)
    parts['word/_rels/document.xml.rels'] = etree.tostring(
        rels, xml_declaration=True, encoding='UTF-8', standalone=True)
    return parts


def used_para_ids(parts):
    used = set()
    for name in ('word/document.xml', 'word/comments.xml'):
        if name in parts:
            for p in etree.fromstring(parts[name]).iter(W + 'p'):
                v = p.get(W14 + 'paraId')
                if v:
                    used.add(v.upper())
    return used


def new_para_id(used, seed):
    """paraId hexadecimal de 8 digitos, deterministico e livre."""
    v = (int(seed) * 2654435761) % (1 << 32)
    while True:
        s = '%08X' % v
        if s != '00000000' and s not in used:
            used.add(s)
            return s
        v = (v + 1) % (1 << 32)


def _runs(par):
    """Runs do paragrafo em ordem, ignorando os que nao carregam texto."""
    return [r for r in par.iter(W + 'r') if r.find(W + 't') is not None]


def _split_at(par, offset):
    """Garante uma fronteira de run no deslocamento dado, dentro do paragrafo.

    Devolve o run que TERMINA nessa fronteira (None se a fronteira e o inicio).
    A ancora quase nunca comeca na fronteira de um run: o Word fatia o texto por
    formatacao e por marca de revisao, e um trecho comentado normalmente comeca
    no meio de um pedaco.
    """
    if offset <= 0:
        return None
    acc = 0
    for r in _runs(par):
        n = len(_txt(r))
        if acc + n == offset:
            return r
        if acc + n > offset:
            corte = offset - acc
            novo = copy.deepcopy(r)
            ts, tn = r.find(W + 't'), novo.find(W + 't')
            texto = ts.text or ''
            ts.text, tn.text = texto[:corte], texto[corte:]
            ts.set(XMLSPACE, 'preserve')
            tn.set(XMLSPACE, 'preserve')
            r.addnext(novo)
            return r
        acc += n
    return None


def _ref_run(cid):
    ref = etree.Element(W + 'r')
    rpr = etree.SubElement(ref, W + 'rPr')
    st = etree.SubElement(rpr, W + 'rStyle')
    st.set(W + 'val', 'CommentReference')
    cr = etree.SubElement(ref, W + 'commentReference')
    cr.set(W + 'id', str(cid))
    return ref


def _mark(tag, cid):
    el = etree.Element(W + tag)
    el.set(W + 'id', str(cid))
    return el


def anchor_text(par, ini, fim, cid):
    """Ancora o comentario no intervalo [ini, fim) do texto do paragrafo.

    Divide no FIM antes de dividir no INICIO: a ordem importa, porque dividir
    no inicio primeiro insere um run novo e desloca o deslocamento do fim.
    """
    fim = min(fim, len(_txt(par)))
    ini = max(0, min(ini, fim))
    _split_at(par, fim)
    _split_at(par, ini)
    runs, acc, dentro = _runs(par), 0, []
    for r in runs:
        n = len(_txt(r))
        if acc >= ini and acc + n <= fim and n:
            dentro.append(r)
        acc += n
    if not dentro:
        dentro = runs[:1]
    if not dentro:
        return False
    dentro[0].addprevious(_mark('commentRangeStart', cid))
    dentro[-1].addnext(_mark('commentRangeEnd', cid))
    for el in par.iter(W + 'commentRangeEnd'):
        if el.get(W + 'id') == str(cid):
            el.addnext(_ref_run(cid))
            break
    return True


def find_drawing(pars, nth):
    """(paragrafo, run) da n-esima imagem do documento, contada em ordem.

    Contar uma imagem por paragrafo nao serve: um cabecalho pode concentrar
    varios logotipos num paragrafo so, e a imagem comentada ser a n-esima do
    documento. O contador tem de percorrer os runs, nao os paragrafos.
    """
    n = 0
    for p in pars:
        for r in p.iter(W + 'r'):
            if list(r.iter(W + 'drawing')):
                n += 1
                if n == nth:
                    return p, r
    return None, None


def anchor_drawing(par, cid, run=None):
    """Ancora o comentario numa imagem: no run dado, ou no primeiro do paragrafo."""
    alvo = run
    if alvo is None:
        for r in par.iter(W + 'r'):
            if list(r.iter(W + 'drawing')):
                alvo = r
                break
    if alvo is None:
        return False
    alvo.addprevious(_mark('commentRangeStart', cid))
    alvo.addnext(_mark('commentRangeEnd', cid))
    for el in par.iter(W + 'commentRangeEnd'):
        if el.get(W + 'id') == str(cid):
            el.addnext(_ref_run(cid))
            break
    return True


def new_comment_element(texto, cid=0, author='', initials='', date=''):
    """Monta um <w:comment> do zero, com o texto dado.

    Transplantar copia o elemento da origem e preserva a formatacao; criar um
    comentario novo precisa montar a estrutura minima que o Word espera: um
    paragrafo cujo primeiro run carrega o estilo CommentReference e o
    <w:annotationRef/>, sem o qual o balao aparece sem a marca de referencia.
    """
    c = etree.Element(W + 'comment')
    c.set(W + 'id', str(cid))
    c.set(W + 'author', author)
    c.set(W + 'initials', initials)
    if date:
        c.set(W + 'date', date)
    p = etree.SubElement(c, W + 'p')
    r1 = etree.SubElement(p, W + 'r')
    rpr = etree.SubElement(r1, W + 'rPr')
    st = etree.SubElement(rpr, W + 'rStyle')
    st.set(W + 'val', 'CommentReference')
    etree.SubElement(r1, W + 'annotationRef')
    r2 = etree.SubElement(p, W + 'r')
    t = etree.SubElement(r2, W + 't')
    t.text = texto
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return c


def add_comment_record(parts, src_comment_el, cid, author, initials, date):
    """Acrescenta o <w:comment> e as tres partes irmas, com ids proprios.

    O elemento vem da origem por copia profunda para preservar a formatacao do
    texto do comentario; so id, autor, iniciais e os paraId sao reescritos.
    """
    croot = etree.fromstring(parts['word/comments.xml'])
    novo = copy.deepcopy(src_comment_el)
    novo.set(W + 'id', str(cid))
    novo.set(W + 'author', author)
    novo.set(W + 'initials', initials)
    if date:
        novo.set(W + 'date', date)

    used = used_para_ids(parts)
    ids = []
    for i, p in enumerate(novo.findall(W + 'p')):
        pid = new_para_id(used, int(cid) * 97 + i + 1)
        p.set(W14 + 'paraId', pid)
        ids.append(pid)
    croot.append(novo)
    parts['word/comments.xml'] = etree.tostring(
        croot, xml_declaration=True, encoding='UTF-8', standalone=True)

    if not ids:
        return parts
    ultimo = ids[-1]

    ex = etree.fromstring(parts['word/commentsExtended.xml'])
    e = etree.SubElement(ex, W15C + 'commentEx')
    e.set(W15C + 'paraId', ultimo)
    e.set(W15C + 'done', '0')
    parts['word/commentsExtended.xml'] = etree.tostring(
        ex, xml_declaration=True, encoding='UTF-8', standalone=True)

    cid_root = etree.fromstring(parts['word/commentsIds.xml'])
    c = etree.SubElement(cid_root, W16CID + 'commentId')
    c.set(W16CID + 'paraId', ultimo)
    c.set(W16CID + 'durableId', ultimo)
    parts['word/commentsIds.xml'] = etree.tostring(
        cid_root, xml_declaration=True, encoding='UTF-8', standalone=True)

    cx = etree.fromstring(parts['word/commentsExtensible.xml'])
    x = etree.SubElement(cx, W16CEX + 'commentExtensible')
    x.set(W16CEX + 'durableId', ultimo)
    x.set(W16CEX + 'dateUtc', (date or '').replace('Z', '') + 'Z' if date else '')
    if not date:
        del x.attrib[W16CEX + 'dateUtc']
    parts['word/commentsExtensible.xml'] = etree.tostring(
        cx, xml_declaration=True, encoding='UTF-8', standalone=True)
    return parts


def save(parts, destino):
    """Grava o pacote. Escreve em temporario e so entao substitui o destino."""
    tmp = destino + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, blob in parts.items():
            z.writestr(name, blob)
    shutil.move(tmp, destino)
    return destino


# ------------------------------------------------------------- operacoes

# Regra da skill: o original e imutavel. Toda gravacao vai para um arquivo NOVO
# (`saida`), que nao pode ser a entrada nem um arquivo existente. A unica
# excecao e `na_copia=True`: a entrada JA E a copia de trabalho criada nesta
# tarefa (por exemplo, depois da edicao de texto) e pode ser regravada.

def _destino_da_gravacao(entrada, saida, na_copia):
    """(caminho, None) onde gravar, ou (None, erro) se a regra for violada."""
    if na_copia:
        return entrada, None
    if not saida:
        return None, ('regra da copia: informe `saida` (arquivo novo) ou '
                      '`na_copia=True` se a entrada ja e a copia de trabalho')
    if os.path.exists(saida):
        if os.path.exists(entrada) and os.path.samefile(saida, entrada):
            return None, 'regra da copia: `saida` e o proprio arquivo de entrada'
        return None, 'regra da copia: `saida` ja existe, nao sobrescrevo: %s' % saida
    return saida, None


def _publicar(parts, destino, esperado=None):
    """Grava em temporario ao lado do destino, verifica e so entao move."""
    tmp = destino + '.novo'
    save(parts, tmp)
    ok, probs, resumo = verify(tmp, esperado=esperado)
    if not ok:
        os.remove(tmp)
        return False, probs, None
    shutil.move(tmp, destino)
    return True, [], resumo


def add_comment(path, trecho, comment_text, author, initials='', date='',
                occurrence=0, apply=True, saida=None, na_copia=False):
    """Cria um comentario ancorado na N-esima ocorrencia de `anchor_text`.

    Operacao de alto nivel: fica no motor, e nao nas cascas, para que a skill
    (linha de comando) e o servidor MCP nao mantenham duas implementacoes que
    divergem com o tempo.

    Com `apply`, grava em `saida` (arquivo novo) ou, com `na_copia=True`, na
    propria copia de trabalho; sempre via temporario e so se `verify` passar.
    """
    if apply:
        destino, erro = _destino_da_gravacao(path, saida, na_copia)
        if erro:
            return dict(ok=False, erro=erro)
    parts = read_parts(path)
    ensure_parts(parts)
    root = etree.fromstring(parts['word/document.xml'])
    pars = paragraphs(root)
    existentes = list_comments(path)
    cid = max([int(c['id']) for c in existentes], default=-1) + 1

    achados = 0
    alvo = None
    for i, p in enumerate(pars):
        t = _txt(p)
        pos = t.find(trecho)
        while pos >= 0:
            if achados == occurrence:
                alvo = (i, pos, pos + len(trecho))
                break
            achados += 1
            pos = t.find(trecho, pos + 1)
        if alvo:
            break
    if not alvo:
        return dict(ok=False, erro='trecho nao encontrado: %r' % trecho[:60])

    i, ini, fim = alvo
    if not anchor_text(pars[i], ini, fim, cid):
        return dict(ok=False, erro='nao foi possivel ancorar')
    parts['word/document.xml'] = etree.tostring(
        root, xml_declaration=True, encoding='UTF-8', standalone=True)
    el = new_comment_element(comment_text, cid, author, initials, date)
    add_comment_record(parts, el, cid, author, initials, date)

    if not apply:
        return dict(ok=True, ensaio=True, id=cid, paragrafo=i,
                    ancora=trecho)
    ok, probs, resumo = _publicar(parts, destino)
    if not ok:
        return dict(ok=False, erro='verificacao falhou', problemas=probs[:6])
    return dict(ok=True, id=cid, paragrafo=i, ancora=trecho, resumo=resumo,
                arquivo=destino)


def transplant(origem, destino, ids, author, initials='', imagens=None,
               apply=False, saida=None, na_copia=False):
    """Copia comentarios de `origem` para o documento `destino`, reautorando.

    `imagens` mapeia id -> n para ancorar na n-esima imagem do documento, para
    comentarios cuja ancora nao tem texto.

    Sem `apply`, devolve o plano sem gravar nada. Com `apply`, grava o
    resultado em `saida` (arquivo novo; `destino` fica intacto) ou, com
    `na_copia=True`, no proprio `destino`, que entao tem de ser a copia de
    trabalho desta tarefa. Sempre via temporario e so se `verify` passar.
    """
    if apply:
        gravar_em, erro = _destino_da_gravacao(destino, saida, na_copia)
        if erro:
            return dict(ok=False, erro=erro, linhas=[])
    imagens = {str(k): v for k, v in (imagens or {}).items()}
    ids = [str(i) for i in ids]
    src_parts = read_parts(origem)
    src_croot = etree.fromstring(src_parts['word/comments.xml'])
    src_el = {c.get(W + 'id'): c for c in src_croot.findall(W + 'comment')}
    src_meta = {c['id']: c for c in list_comments(origem)}
    cands = {c['comment']['id']: c for c in candidates(origem, destino, ids=ids)}

    parts = read_parts(destino)
    ensure_parts(parts)
    root = etree.fromstring(parts['word/document.xml'])
    dpars = paragraphs(root)
    existentes = list_comments(destino)
    cid = max([int(c['id']) for c in existentes], default=-1) + 1

    linhas = []
    for i in ids:
        nth = imagens.get(i)
        if nth:
            par, run = find_drawing(dpars, nth)
            if par is None:
                linhas.append(dict(id=i, estado='falhou',
                                   detalhe='imagem #%d nao encontrada' % nth))
                continue
            ok = anchor_drawing(par, cid, run)
            onde = 'imagem #%d' % nth
            classe = 'IMAGEM'
        else:
            r = cands.get(i)
            if not r or r['par'] is None:
                linhas.append(dict(id=i, estado='falhou',
                                   detalhe='sem trecho equivalente no destino'))
                continue
            ok = anchor_text(dpars[r['par']], r['ini'], r['fim'], cid)
            onde = r['trecho'][:80]
            classe = r['classe']
        if not ok:
            linhas.append(dict(id=i, estado='falhou', detalhe='nao foi possivel ancorar'))
            continue
        parts['word/document.xml'] = etree.tostring(
            root, xml_declaration=True, encoding='UTF-8', standalone=True)
        add_comment_record(parts, src_el[i], cid, author, initials,
                           src_meta[i]['date'])
        linhas.append(dict(id=i, estado='ok', novo_id=cid, classe=classe, ancora=onde))
        cid += 1

    parts['word/document.xml'] = etree.tostring(
        root, xml_declaration=True, encoding='UTF-8', standalone=True)
    inseridos = sum(1 for l in linhas if l['estado'] == 'ok')
    if not apply:
        return dict(ok=True, ensaio=True, inseridos=inseridos, linhas=linhas)
    ok, probs, resumo = _publicar(parts, gravar_em)
    if not ok:
        return dict(ok=False, erro='verificacao falhou', problemas=probs[:6],
                    linhas=linhas)
    return dict(ok=True, inseridos=inseridos, linhas=linhas, resumo=resumo,
                arquivo=gravar_em)


# ---------------------------------------------------------------- verificacao

def verify(path, esperado=None):
    """Confere os sete lugares. Devolve (ok, problemas, resumo).

    Uma ancora orfa nao impede o arquivo de abrir: o Word simplesmente perde o
    comentario, sem aviso. Por isso a verificacao nao pergunta "abriu?", e sim
    se cada id tem Start, End e Reference, se cada um tem registro nas quatro
    partes, e se os dois registros de pacote existem.
    """
    probs = []
    try:
        parts = read_parts(path)
    except Exception as e:
        return False, ['pacote ilegivel: %s' % e], {}

    for name in PARTS:
        if name not in parts:
            probs.append('falta a parte %s' % name)
    ct = etree.fromstring(parts['[Content_Types].xml'])
    have = set(o.get('PartName') for o in ct.findall(CT + 'Override'))
    for name in PARTS:
        if '/' + name not in have:
            probs.append('falta override de %s em [Content_Types].xml' % name)
    rels = etree.fromstring(parts['word/_rels/document.xml.rels'])
    alvos = set(r.get('Target') for r in rels.findall(REL + 'Relationship'))
    for name in PARTS:
        if name.split('/', 1)[1] not in alvos:
            probs.append('falta relationship de %s' % name)

    if 'word/comments.xml' not in parts:
        return not probs, probs, {}
    croot = etree.fromstring(parts['word/comments.xml'])
    ids = set(c.get(W + 'id') for c in croot.findall(W + 'comment'))
    droot = etree.fromstring(parts['word/document.xml'])
    st = [e.get(W + 'id') for e in droot.iter(W + 'commentRangeStart')]
    en = [e.get(W + 'id') for e in droot.iter(W + 'commentRangeEnd')]
    rf = [e.get(W + 'id') for e in droot.iter(W + 'commentReference')]

    for i in sorted(ids):
        if st.count(i) != 1:
            probs.append('comentario %s: %d commentRangeStart (esperado 1)' % (i, st.count(i)))
        if en.count(i) != 1:
            probs.append('comentario %s: %d commentRangeEnd (esperado 1)' % (i, en.count(i)))
        if rf.count(i) != 1:
            probs.append('comentario %s: %d commentReference (esperado 1)' % (i, rf.count(i)))
    for i in set(st) | set(en) | set(rf):
        if i not in ids:
            probs.append('ancora aponta para comentario %s inexistente' % i)

    npar = len(etree.fromstring(parts['word/commentsExtended.xml']))
    nids = len(etree.fromstring(parts['word/commentsIds.xml']))
    if npar != len(ids):
        probs.append('commentsExtended tem %d registros para %d comentarios' % (npar, len(ids)))
    if nids != len(ids):
        probs.append('commentsIds tem %d registros para %d comentarios' % (nids, len(ids)))
    if esperado is not None and len(ids) != esperado:
        probs.append('esperados %d comentarios, encontrados %d' % (esperado, len(ids)))

    resumo = dict(comentarios=len(ids), starts=len(st), ends=len(en), refs=len(rf))
    return not probs, probs, resumo
