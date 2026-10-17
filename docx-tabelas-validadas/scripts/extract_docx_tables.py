#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract every table from a .docx into a tidy long CSV, with dual-route verification.

Why two routes: a single extraction pass gives no way to detect a silent parsing
error. This script reads the same tables twice, through independent code paths
(python-docx object model vs. raw OOXML via lxml), and refuses to emit output if
the two disagree on any cell.

Usage:
    python extract_docx_tables.py INPUT.docx --out-dir DIR [--prefix NAME]

Outputs (in DIR):
    <prefix>_tidy.csv       one row per value (table, header path, row label, literal text)
    <prefix>_wide/          one CSV per table, preserving the printed grid
    <prefix>_report.md      layout inventory + verification results
"""
import argparse, csv, os, re, sys, zipfile
from collections import Counter, defaultdict

import docx
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# Below this share of checkable columns actually checked, the run is flagged
# loudly on stderr. Route divergence proves corruption and aborts; low coverage
# proves ignorance of the cell format and warns — the files are still written.
COVERAGE_MIN = 80.0


# ---------------------------------------------------------------- extraction

def norm(s):
    """Collapse all whitespace. Line breaks inside a cell become single spaces."""
    return ' '.join((s or '').split())


def route_a(path):
    """Route A: python-docx object model. Cell identity via absolute XPath.

    Do NOT use id() on lxml elements — lxml builds proxy objects on demand and
    recycles their memory addresses, so id() is not a stable identity and will
    silently collapse distinct cells.
    """
    doc = docx.Document(path)
    tree = doc.element.getroottree()
    out = []
    for ti, t in enumerate(doc.tables):
        seen = set()
        for r in t.rows:
            for c in r.cells:
                key = tree.getpath(c._tc)
                if key in seen:
                    continue
                seen.add(key)
                out.append((ti, norm(c.text)))
    return doc, out


def cell_text_raw(tc):
    """Text of one <w:tc>, joining paragraphs and break elements with a space."""
    parts = []
    for p in tc.iterchildren(W + 'p'):
        buf = []
        for node in p.iter():
            tag = node.tag.split('}')[-1]
            if tag == 't':
                buf.append(node.text or '')
            elif tag in ('br', 'tab', 'cr'):
                buf.append(' ')
        parts.append(''.join(buf))
    return norm(' '.join(parts))


def route_b(path):
    """Route B: raw OOXML. Skips vMerge continuation cells to match route A."""
    with zipfile.ZipFile(path) as z:
        root = etree.fromstring(z.read('word/document.xml'))
    out = []
    for ti, tbl in enumerate(root.find(W + 'body').iterchildren(W + 'tbl')):
        for tr in tbl.iterchildren(W + 'tr'):
            for tc in tr.iterchildren(W + 'tc'):
                vm = tc.find(f'{W}tcPr/{W}vMerge')
                if vm is not None and vm.get(W + 'val') != 'restart':
                    continue
                out.append((ti, cell_text_raw(tc)))
    return out


def verify(a, b):
    """Return (ok, list of (index, route_a_value, route_b_value))."""
    if len(a) != len(b):
        return False, [('LENGTH', len(a), len(b))]
    diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return not diffs, diffs


# ------------------------------------------------------------------- parsing

def grid(t):
    """Printed grid: merged cells repeat their text across the spanned positions."""
    return [[norm(c.text) for c in r.cells] for r in t.rows]


def spans_full_row(t, tree, ridx):
    """True when the row is one merged cell (title / source line)."""
    keys = {tree.getpath(c._tc) for c in t.rows[ridx].cells}
    return len(keys) == 1


def header_depth(g, n_header_max=3):
    """Number of leading rows that are header, by heuristic.

    A header row has an empty first cell (the stub column) and non-empty cells
    to its right. Data rows carry a label in the first cell.
    """
    d = 0
    for r in g[:n_header_max]:
        if r[0] == '' and any(x for x in r[1:]):
            d += 1
        else:
            break
    return d


def parse_table(t, tree, ti):
    g = grid(t)
    if not g:
        return None
    title = g[0][0] if spans_full_row(t, tree, 0) else ''
    source = ''
    end = len(g)
    if len(g) > 1 and spans_full_row(t, tree, len(g) - 1):
        source = g[-1][0]
        end = len(g) - 1
    start = 1 if title else 0
    hd = header_depth(g[start:end])
    header_rows = g[start:start + hd]
    body = g[start + hd:end]
    return dict(idx=ti, title=title, source=source,
                header_rows=header_rows, body=body, grid=g,
                nrow=len(g), ncol=len(g[0]))


def header_path(header_rows, j):
    """Join the header labels above column j, top to bottom, dropping repeats."""
    parts = []
    for hr in header_rows:
        v = hr[j] if j < len(hr) else ''
        if v and (not parts or parts[-1] != v):
            parts.append(v)
    return ' > '.join(parts)


# ---------------------------------------------------------------- validation

INT_RE = re.compile(r'^-?[\d.]+$')
# A percentage cell may be bare ("9%") or packed with its margin of error
# ("9% (±5,8%)"). Both carry the same point estimate. Reading only the bare form
# silently drops every packed column from validation — which is how a document
# can report "0 checagens, 0 falhas" and look verified.
PCT_RE = re.compile(r'^(\d+)\s*%(?:\s*\(±\s*[\d.,]+\s*%?\s*\))?$')
SUPPRESSED = {'x', 'X', '-', '–', '—', ''}
# A dash in the BODY of a count/percentage column is the document writing zero
# (a category with no cases), not a suppressed cell: read as 0, such columns
# close against their declared Total. Treating it as unreadable costs coverage
# and hides the very check that would catch a misalignment there.
# A dash in the TOTAL row still means "this column has no total" (margin of
# error), which is not a verification gap.
DASH = {'-', '–', '—'}

# A marginal column whose own footnote says it absorbs the non-response category
# CANNOT close against the subgroups: the deficit is the non-response. When
# every non-closure is a deficit in a table carrying this note, and no check
# closes in a table that carries it, the correspondence is structure, not error.
# Classified, never silenced: a deficit WITHOUT the note, or any excess, still
# reports as unexplained, which is where misalignment would surface.
NOTE_MARGINAL_NR = re.compile(r'inclui.{0,60}n[aã]o sei', re.I)


def marginal_absorbs_nr(T):
    """True if the table's footnote declares the marginal column to include the
    'Nao sei/Prefiro nao responder' category."""
    return bool(NOTE_MARGINAL_NR.search(T.get('source') or ''))


def as_int(s):
    s = norm(s)
    return int(s.replace('.', '')) if INT_RE.match(s) and s.strip('.') else None


def as_pct(s):
    m = PCT_RE.match(norm(s))
    return int(m.group(1)) if m else None


def is_suppressed(s):
    return norm(s) in SUPPRESSED


def is_dash(s):
    return norm(s) in DASH


def check_totals(tables, total_labels=('Total', 'TOTAL')):
    """Sum each column over the body and compare to the Total row.

    Returns (results, coverage). `coverage` accounts for every column that had a
    Total row available — checked or not, and why not. A check that never ran is
    not a check that passed, and the report must be able to say so.
    """
    results = []
    cov = dict(checkable=0, checked=0, na=0, dash_zero=0, suppressed_col=0,
               skipped=Counter())
    for T in tables:
        if not T['header_rows']:
            continue
        rows = T['body']
        ti_tot = [i for i, r in enumerate(rows) if norm(r[0]) in total_labels]
        if not ti_tot:
            continue
        k = ti_tot[0]
        data, tot = rows[:k], rows[k]
        ncol = len(T['grid'][0])
        nr = marginal_absorbs_nr(T)
        last_leaf = header_path(T['header_rows'], ncol - 1).split(' > ')[-1]
        for j in range(1, ncol):
            label = header_path(T['header_rows'], j) or f'col{j}'
            # the marginal column of a crossed table, when the footnote says it
            # absorbs non-response, is short by exactly that category
            expl = nr and label.split(' > ')[-1] == last_leaf
            cov['checkable'] += 1
            body_cells = [r[j] for r in data]
            if is_dash(tot[j]):
                # the Total cell is a dash: the document itself declares this
                # column has no total (a margin-of-error column, typically).
                # Not a verification gap — excluded from the denominator.
                cov['na'] += 1
                cov['checkable'] -= 1
                cov['skipped']['nao aplicavel — coluna sem total declarado'] += 1
                continue
            dashed = any(is_dash(v) for v in body_cells)
            ints = [0 if is_dash(r[j]) else as_int(r[j]) for r in data]
            target = as_int(tot[j])
            if target is not None and ints and all(v is not None for v in ints):
                s = sum(ints)
                cov['checked'] += 1
                cov['dash_zero'] += 1 if dashed else 0
                results.append(dict(table=T['idx'], column=label, kind='soma',
                                    obtido=s, esperado=target, ok=(s == target),
                                    explicado=(expl and s < target)))
                continue
            pcts = [0 if is_dash(r[j]) else as_pct(r[j]) for r in data]
            tpct = as_pct(tot[j])
            if tpct is not None and pcts and all(v is not None for v in pcts):
                s = sum(pcts)
                cov['checked'] += 1
                cov['dash_zero'] += 1 if dashed else 0
                # allow rounding drift; multiple-response tables are excluded by
                # the requirement that the Total row itself reads 100%
                results.append(dict(table=T['idx'], column=label, kind='percentual',
                                    obtido=s, esperado=tpct,
                                    ok=abs(s - tpct) <= 2,
                                    explicado=(expl and s < tpct)))
                continue
            xs = [v for v in body_cells if norm(v) in ('x', 'X')]
            if xs and len(xs) == len(body_cells):
                # the document itself withheld the whole column (base too small)
                cov['suppressed_col'] += 1
                cov['skipped']['coluna inteira suprimida pelo documento (x)'] += 1
            elif any(is_suppressed(v) for v in body_cells):
                cov['skipped']['celula suprimida no corpo'] += 1
            else:
                cov['skipped']['formato de celula nao reconhecido'] += 1
    return results, cov


def check_marginals(tables, total_labels=('Total', 'TOTAL')):
    """Cross-check: do the subgroup columns add up to the last (marginal) column?

    This is the horizontal counterpart of check_totals. A vertical sum survives a
    column shift; this one does not. It only runs on body rows where every cell is
    a plain integer (observed sample, estimated population), so tables whose last
    column is a different population — Brasil next to a state — self-exclude.

    Non-closure is not automatically an error. A crossing variable that drops
    undeclared cases will miss the marginal in every table, uniformly. Misalignment
    misses erratically. The report groups results by subgroup signature so the two
    are told apart by shape, not by inspection of individual failures.
    """
    results = []
    for T in tables:
        if not T['header_rows'] or T['ncol'] < 3:
            continue
        ncol = T['ncol']
        leaves = [header_path(T['header_rows'], j).split(' > ')[-1]
                  for j in range(1, ncol)]
        sig = ' | '.join(leaves[:-1])
        nr = marginal_absorbs_nr(T)
        for r in T['body']:
            if norm(r[0]) in total_labels:
                continue
            vals = [as_int(v) for v in r[1:]]
            if not vals or any(v is None for v in vals):
                continue
            sub, marg = vals[:-1], vals[-1]
            s = sum(sub)
            # Observed sample counts are true integers and must match exactly.
            # Weighted sample and estimated population are sums of rounded
            # components, so they may drift by up to one unit per parcel
            # regardless of magnitude. Keying tolerance on the magnitude of the
            # marginal (< 10.000 -> tol 0) flags one-unit rounding gaps in
            # `Amostra Ponderada` as if they were misalignment.
            rounded = any(k in norm(r[0]).lower()
                          for k in ('ponderada', 'populacao', 'população',
                                    'estimada'))
            tol = len(sub) if (rounded or marg >= 10_000) else 0
            ok = abs(s - marg) <= tol
            results.append(dict(table=T['idx'], linha=norm(r[0]), assinatura=sig,
                                marginal=leaves[-1], obtido=s, esperado=marg,
                                ok=ok, gap=s - marg,
                                explicado=(not ok and s < marg and nr)))
    return results


def group_columns(T):
    """Columns grouped by the first level of the header path.

    A two-level header ("<Region> > Sim") groups by geography; a flat one
    ("Sim") falls into a single group. Either way the categories that must add
    up live inside one group, never across two.
    """
    g = defaultdict(list)
    for j in range(1, T['ncol']):
        path = header_path(T['header_rows'], j)
        g[path.split(' > ')[0] if ' > ' in path else '(plano)'].append(j)
    return g


def check_horizontal(tables, total_labels=('Total', 'TOTAL')):
    """Rows of a Total-less table must still add to 100% within a header group.

    A table with no `Total` row is invisible to check_totals, which skips it
    whole. That can silently leave a large share of a document's cells outside
    every check while the coverage line still reads 100% --
    the denominator only ever counted columns of tables that HAVE a Total. A
    check that never runs is not a check that passed, and a coverage figure that
    cannot see the omission is worse than no coverage figure at all.

    Keep the columns that are percentages in every body row and add them up per
    row. An exhaustive category set closes at 100; a multiple-response set
    ("assinale todas") does not close at all, uniformly. Neither is a bug. What
    denounces one is a table that closes on SOME rows and not others, which is
    what a misaligned column looks like.
    """
    results = []
    for T in tables:
        if not T['header_rows']:
            continue
        if any(norm(r[0]) in total_labels for r in T['body']):
            continue                      # vertical sum already covers it
        for top, cols in group_columns(T).items():
            pcols = [j for j in cols
                     if all(as_pct(r[j]) is not None for r in T['body'])]
            if len(pcols) < 2:
                continue
            # one unit of rounding drift per parcel, never less than 2
            tol = max(2, len(pcols))
            sums = [sum(as_pct(r[j]) for j in pcols) for r in T['body']]
            hits = [abs(v - 100) <= tol for v in sums]
            pad = ('exaustivo (fecha 100%)' if all(hits) else
                   'nao soma 100 (multipla resposta)' if not any(hits) else
                   'MISTO — investigar')
            results.append(dict(table=T['idx'], grupo=top, colunas=len(pcols),
                                linhas=len(sums), fecham=sum(hits),
                                padrao=pad, ok=(pad != 'MISTO — investigar'),
                                somas=sums))
    return results


def check_universe(tables, total_labels=('Total', 'TOTAL')):
    """Flag tables whose base exceeds the full sample of the document.

    Every table in an annex is the full sample or a filtered subpopulation of it,
    so the modal base is a ceiling: a table reporting *more* observations than the
    whole survey is reporting a different universe. Values below the mode are
    normal and never flagged. This catches an entire table sourced from the wrong
    geography — which internal arithmetic cannot see, because such a table is
    perfectly consistent with itself.

    Returns (mode_base, outliers).
    """
    bases = []
    for T in tables:
        if not T['header_rows']:
            continue
        # layout A (crossed): base counts are rows, the marginal is a column
        for r in T['body']:
            if norm(r[0]) in total_labels:
                continue
            vals = [as_int(v) for v in r[1:]]
            if vals and all(v is not None for v in vals):
                bases.append((T['idx'], norm(r[0]), max(vals)))
        # layout B (simple): base counts are columns, the base is the Total row
        tot = [r for r in T['body'] if norm(r[0]) in total_labels]
        if tot:
            for j in range(1, T['ncol']):
                v = as_int(tot[0][j])
                if v is not None:
                    leaf = header_path(T['header_rows'], j).split(' > ')[-1]
                    bases.append((T['idx'], leaf, v))
    if not bases:
        return None, []
    by_label = defaultdict(list)
    for idx, label, v in bases:
        by_label[label].append((idx, v))
    out, modes = [], {}
    for label, vs in by_label.items():
        if len(vs) < 3:                     # too few to establish a ceiling
            continue
        mode = Counter(v for _, v in vs).most_common(1)[0][0]
        modes[label] = mode
        for idx, v in vs:
            # 1% slack absorbs rounding in weighted population estimates; a
            # wrong universe overshoots by far more than that
            if v > mode * 1.01:
                out.append(dict(table=idx, linha=label, valor=v, teto=mode))
    return modes, out


def count_suppressed(tables):
    """Suppressed cells are information about the document, not noise."""
    c = Counter()
    for T in tables:
        if not T['header_rows']:
            continue
        for r in T['body']:
            for j in range(1, len(r)):
                if norm(r[j]) in ('x', 'X'):
                    c[header_path(T['header_rows'], j).split(' > ')[-1]] += 1
    return c


# ----------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--out-dir', default='.')
    ap.add_argument('--prefix', default=None)
    args = ap.parse_args()

    prefix = args.prefix or re.sub(r'\W+', '_',
                                   os.path.splitext(os.path.basename(args.input))[0]).strip('_')
    os.makedirs(args.out_dir, exist_ok=True)
    wide_dir = os.path.join(args.out_dir, f'{prefix}_wide')
    os.makedirs(wide_dir, exist_ok=True)

    doc, a = route_a(args.input)
    b = route_b(args.input)
    ok, diffs = verify(a, b)
    if not ok:
        sys.stderr.write('VERIFICACAO FALHOU — as duas rotas de leitura divergem.\n')
        for d in diffs[:20]:
            sys.stderr.write(f'  {d}\n')
        sys.stderr.write('Nenhum arquivo foi gravado. Investigue antes de prosseguir.\n')
        sys.exit(2)

    tree = doc.element.getroottree()
    tables = [parse_table(t, tree, i) for i, t in enumerate(doc.tables)]
    tables = [T for T in tables if T]

    # tidy long
    rows = []
    for T in tables:
        m = re.match(r'\s*(?:Tabela|Table)\s+(\d+)\s*[:\-]', T['title'])
        n = int(m.group(1)) if m else None
        for r in T['body']:
            for j in range(1, len(r)):
                rows.append(dict(
                    tabela_n=n, tabela_idx=T['idx'], titulo=T['title'],
                    coluna=header_path(T['header_rows'], j),
                    categoria=r[0], valor=r[j], fonte_nota=T['source']))

    tidy = os.path.join(args.out_dir, f'{prefix}_tidy.csv')
    with open(tidy, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    for T in tables:
        with open(os.path.join(wide_dir, f'tabela_{T["idx"]:03d}.csv'),
                  'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerows(T['grid'])

    checks, cov = check_totals(tables)
    horiz = check_horizontal(tables)
    hbad = [h for h in horiz if not h['ok']]
    # tables that check_totals never looked at, and what became of them
    no_total = [T for T in tables
                if T['header_rows']
                and not any(norm(r[0]) in ('Total', 'TOTAL') for r in T['body'])]
    h_tables = {h['table'] for h in horiz}
    nt_uncov = [T for T in no_total if T['idx'] not in h_tables]
    nt_cells = sum(len(T['body']) * (T['ncol'] - 1) for T in nt_uncov)
    fails = [c for c in checks if not c['ok']]
    xfails = [c for c in fails if not c.get('explicado')]
    marg = check_marginals(tables)
    mfails = [m for m in marg if not m['ok']]
    mxfails = [m for m in mfails if not m.get('explicado')]
    supr = count_suppressed(tables)
    modes, univ = check_universe(tables)
    pct_cov = 100.0 * cov['checked'] / cov['checkable'] if cov['checkable'] else 0.0
    low = cov['checkable'] > 0 and pct_cov < COVERAGE_MIN

    # group marginal results by subgroup signature: uniform non-closure looks
    # structural, erratic non-closure looks like misalignment
    # Rate alone is not enough to tell structure from bug: a group can fail at
    # a low rate and still be pure rounding. Carry the magnitude of the gap so
    # the report can say so instead of shouting ERRATICO at a one-unit drift.
    mgroups = {}
    for m in marg:
        g = mgroups.setdefault(m['assinatura'], [0, 0, [], 0])
        g[0 if m['ok'] else 1] += 1
        if not m['ok']:
            g[2].append(abs(m.get('gap', 0)))
            g[3] += 1 if m.get('explicado') else 0

    shapes = Counter((T['nrow'], T['ncol']) for T in tables)
    hdrs = Counter(tuple(header_path(T['header_rows'], j)
                         for j in range(1, T['ncol'])) for T in tables)

    rep = os.path.join(args.out_dir, f'{prefix}_report.md')
    with open(rep, 'w', encoding='utf-8') as f:
        f.write(f'# Relatorio de extracao — {os.path.basename(args.input)}\n\n')

        f.write('## Cobertura da verificacao\n\n')
        f.write(f'- Colunas com linha `Total` e total declarado: **{cov["checkable"]}** '
                f'(+{cov["na"]} sem total declarado, fora do denominador)\n')
        f.write(f'- Efetivamente checadas: **{cov["checked"]}** '
                f'(**{pct_cov:.1f}%** de cobertura)\n')
        f.write(f'- Tabelas sem linha `Total` (fora da soma vertical): '
                f'**{len(no_total)}** — dessas, {len(no_total) - len(nt_uncov)} '
                f'verificadas pela soma horizontal\n')
        if nt_uncov:
            f.write(f'  - **{len(nt_uncov)} tabela(s) sem verificacao alguma** '
                    f'({nt_cells} celulas): sem linha Total e sem grupo de '
                    f'colunas percentuais\n')
        if cov.get('dash_zero'):
            f.write(f'  - dessas, **{cov["dash_zero"]}** so foram checaveis lendo '
                    'traco no corpo como zero; a linha `Total` confirma a leitura\n')
        if low:
            f.write(f'- **ATENCAO: cobertura abaixo de {COVERAGE_MIN:.0f}%.** '
                    'Ausencia de falha aqui nao e evidencia de acerto.\n')
        for reason, n in cov['skipped'].most_common():
            f.write(f'  - nao checadas — {reason}: {n}\n')
        f.write('\n')

        f.write('## Extracao\n\n')
        f.write(f'- Tabelas: **{len(tables)}**\n')
        f.write(f'- Celulas fisicas conferidas nas duas rotas: **{len(a)}**\n')
        f.write(f'- Divergencias entre rotas: **0**\n')
        f.write(f'- Valores no arquivo longo: **{len(rows)}**\n')
        nn = [r['tabela_n'] for r in rows if r['tabela_n']]
        if nn:
            faltam = sorted(set(range(min(nn), max(nn) + 1)) - set(nn))
            f.write(f'- Numeracao das tabelas: {min(nn)} a {max(nn)}; '
                    f'ausentes: {faltam if faltam else "nenhuma"}\n')
        f.write(f'\n## Checagens de soma vertical (corpo vs. linha Total)\n\n')
        f.write(f'- Executadas: **{len(checks)}**\n')
        f.write(f'- Falhas inexplicadas: **{len(xfails)}**\n')
        if len(fails) != len(xfails):
            f.write(f'- Nao fecham por estrutura declarada na nota da '
                    f'tabela (a coluna marginal absorve a nao-resposta): '
                    f'**{len(fails) - len(xfails)}**\n')
        f.write('\n')
        for c in fails:
            tag = '' if not c.get('explicado') else '  [nota da tabela]'
            f.write(f'  - tabela {c["table"]} / {c["column"]} ({c["kind"]}): '
                    f'obtido {c["obtido"]}, esperado {c["esperado"]}{tag}\n')

        f.write('\n## Checagens de soma horizontal (tabelas sem linha `Total`)\n\n')
        f.write(f'- Executadas: **{len(horiz)}** grupos de colunas\n')
        f.write(f'- Padrao MISTO (investigar): **{len(hbad)}**\n\n')
        if horiz:
            hpad = Counter(h['padrao'] for h in horiz)
            for k, v in hpad.most_common():
                f.write(f'  - {k}: {v}\n')
            for h in hbad:
                f.write(f'  - tabela {h["table"]} / grupo {h["grupo"]}: '
                        f'{h["fecham"]} de {h["linhas"]} linhas fecham em 100% '
                        f'— somas {h["somas"]}\n')
            f.write('\nUm conjunto exaustivo de categorias fecha em 100%; um de '
                    'multipla resposta nao fecha em linha nenhuma. Nenhum dos dois e '
                    'defeito. Defeito e fechar em algumas linhas e nao em outras.\n')

        f.write('\n## Checagens de marginal (subgrupos vs. coluna final)\n\n')
        f.write(f'- Executadas: **{len(marg)}**\n')
        f.write(f'- Nao fecham, inexplicado: **{len(mxfails)}**\n')
        if len(mfails) != len(mxfails):
            f.write(f'- Nao fecham por estrutura declarada na nota da '
                    f'tabela: **{len(mfails) - len(mxfails)}** (o deficit '
                    f'e a nao-resposta que a coluna marginal absorve)\n')
        f.write('\n')
        if mgroups:
            f.write('| fecham | nao fecham | taxa | gap max | padrao | subgrupos |\n'
                    '|---|---|---|---|---|---|\n')
            for sig, (okc, badc, gaps, expl) in sorted(mgroups.items(),
                                                       key=lambda kv: -kv[1][1]):
                rate = badc / (okc + badc)
                gmax = max(gaps) if gaps else 0
                if badc == 0:
                    pad = 'consistente'
                elif expl == badc:
                    pad = 'estrutura declarada na nota da tabela'
                elif gmax <= 2:
                    pad = 'arredondamento (gap <= 2 unidades)'
                elif rate >= 0.9:
                    pad = 'sistematico (provavel estrutura da base)'
                elif rate <= 0.1:
                    pad = 'PONTUAL — investigar'
                else:
                    pad = 'ERRATICO — investigar'
                f.write(f'| {okc} | {badc} | {rate:.0%} | {gmax} | {pad} | '
                        f'{sig[:70]} |\n')
            f.write('\nGap de ate 2 unidades e arredondamento, qualquer que seja '
                    'a taxa. Acima disso: nao fechamento sistematico (taxa alta e '
                    'estavel) costuma indicar categoria de nao-resposta excluida '
                    'do cruzamento; pontual ou erratico e a assinatura de '
                    'desalinhamento. A distincao e do pesquisador.\n')

        f.write('\n## Checagem de universo (base acima da amostra completa)\n\n')
        if modes:
            f.write('- Base modal por linha: '
                    + '; '.join(f'{k} = {v:,}'.replace(',', '.')
                                for k, v in modes.items()) + '\n')
        f.write(f'- Tabelas acima do teto: **{len(univ)}**\n')
        if univ:
            f.write('\nUma tabela nao pode ter mais observacoes que a pesquisa '
                    'inteira. Acima do teto = universo diferente (tipicamente '
                    'outra geografia na coluna errada), e nenhuma checagem '
                    'aritmetica interna enxerga isso.\n\n')
            for u in univ[:40]:
                f.write(f'  - tabela {u["table"]} / {u["linha"]}: '
                        f'{u["valor"]:,} > teto {u["teto"]:,}\n'.replace(',', '.'))

        if supr:
            f.write(f'\n## Celulas suprimidas (`x`): {sum(supr.values())}\n\n')
            for k, v in supr.most_common(15):
                f.write(f'- {k}: {v}\n')

        f.write('\n## Formatos de tabela (linhas x colunas)\n\n')
        for k, v in sorted(shapes.items()):
            f.write(f'- {k[0]} x {k[1]}: {v}\n')
        f.write(f'\n## Estruturas de cabecalho distintas: {len(hdrs)}\n\n')
        for k, v in hdrs.most_common():
            f.write(f'- ({v}x) {" | ".join(k)}\n')

    print(f'OK — rotas identicas em {len(a)} celulas.')
    print(f'Tabelas: {len(tables)} | valores: {len(rows)}')
    print(f'Cobertura: {cov["checked"]}/{cov["checkable"]} colunas checadas '
          f'({pct_cov:.1f}%)'
          + (f' | {cov["suppressed_col"]} colunas suprimidas pelo documento (x)'
             if cov['suppressed_col'] else ''))
    print(f'Soma vertical — falhas inexplicadas: {len(xfails)} '
          f'(+{len(fails) - len(xfails)} explicadas pela nota da tabela)')
    print(f'Marginais: {len(marg)} checagens | nao fecham (inexplicado): '
          f'{len(mxfails)} (+{len(mfails) - len(mxfails)} pela nota)')
    print(f'Soma horizontal (tabelas sem Total): {len(horiz)} grupos | '
          f'padrao MISTO: {len(hbad)}'
          + (f' | {len(nt_uncov)} tabela(s) SEM verificacao alguma'
             if nt_uncov else ''))
    print(f'Universo: {len(univ)} tabela(s) acima do teto de amostra')
    print(f'Saidas: {tidy}\n        {wide_dir}/\n        {rep}')
    if low:
        sys.stderr.write(
            f'\nATENCAO: cobertura de checagem em {pct_cov:.1f}% '
            f'(minimo {COVERAGE_MIN:.0f}%). {cov["checkable"] - cov["checked"]} '
            'colunas nao foram verificadas. Os arquivos foram gravados, mas '
            '"0 falhas" aqui significa "nao examinado", nao "correto". '
            'Leia a secao de cobertura do relatorio antes de usar os dados.\n')
    if xfails:
        print('ATENCAO: ha falhas de soma inexplicadas. Verifique o relatorio '
              'antes de usar os dados.')
    if mxfails:
        print('ATENCAO: ha marginais que nao fecham sem explicacao na nota. '
              'Veja o agrupamento no relatorio.')
    if hbad:
        print('ATENCAO: ha grupo de colunas que fecha em 100% em algumas linhas '
              'e nao em outras — assinatura de desalinhamento. Veja o relatorio.')
    if nt_uncov:
        sys.stderr.write(
            f'\nATENCAO: {len(nt_uncov)} tabela(s) ({nt_cells} celulas) sem '
            'verificacao alguma: nao tem linha Total nem grupo de colunas '
            'percentuais. Os arquivos foram gravados; esses numeros nao foram '
            'conferidos por aritmetica nenhuma.\n')
    if univ:
        print(f'ATENCAO: {len(univ)} tabela(s) com base acima da amostra completa '
              '— provavel universo trocado. Veja o relatorio.')


if __name__ == '__main__':
    main()
