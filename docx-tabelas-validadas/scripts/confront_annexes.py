#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confront a crossed-tables annex against the simple-tables annex it derives from.

The marginal column of every crossing must reproduce the simple table for the
same question. This is the strongest available check on the crossed annex: it
validates thousands of cells against an independent document, not against
internal arithmetic.

Pairing is by question text plus population, taken from the table title. Two
things break naive pairing and both are handled here:

  - the geographic scope is written differently in each annex ("<State>,
    <Region> e Brasil" vs. "<State>") and is normalized;
  - the same item is sometimes worded differently in the two annexes. Those are
    not guessable and live in a label map kept with the survey's data (see
    label_map.example.csv for the format). Unpaired questions are reported,
    never silently dropped.

Usage:
    python confront_annexes.py SIMPLES_tidy.csv CRUZADO_tidy.csv \
        [--label-map label_map.csv] [--out DIR]
"""
import argparse, csv, os, re, sys
from collections import defaultdict, Counter

YEAR = re.compile(r'^\d{4}$')
# The population a table describes is not always in its title. One annex may
# name the subpopulation in BOTH the title and a footnote; another may keep the
# broad population in every title and declare the filter only in the note.
# Pairing by title alone then matches the filtered crossed table against the
# UNFILTERED simple one - same question, different universe - and reports
# divergences that are an artefact of the pairing, not a disagreement between
# documents.
FILTER_NOTE = re.compile(r'respostas?\s+filtradas?\s+para', re.I)
SUB = 'SUBPOPULACAO FILTRADA'

# One question, two shapes. One annex publishes "Tipo de X [Item A]" as its own
# simple table; another publishes the whole set as ONE matrix table - items in
# rows, categories in columns, no Total row. The crossed annex always
# decomposes. Pairing by question text alone leaves those questions unpaired,
# which is precisely the shape whose only other
# check is internal (the horizontal sum). The two forms are transposes of each
# other: matrix[item][Sim] is the same cell as decomposed[Sim] of the marginal.
ITEM = re.compile(r'^(.*?)\s*\[([^\]]+)\]\s*$')


PACK = re.compile(r'^\s*(\d+)\s*%\s*\(\s*±\s*([\d.,]+)\s*%\s*\)\s*$')


def load(path):
    rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    cells, titles, notes = defaultdict(dict), {}, {}
    for r in rows:
        cells[(r['tabela_n'], r['coluna'])][r['categoria']] = r['valor']
        titles[r['tabela_n']] = r['titulo']
        notes[r['tabela_n']] = r.get('fonte_nota') or ''
    return cells, titles, notes


def annex_keys(titles, notes):
    """{tabela_n: (questao, populacao @ escopo)} with the subpopulation normalised.

    The modal population of the annex is its default universe; anything else is a
    subpopulation, whether the title says so or only a footnote does. Both forms
    collapse to the same marker so the two annexes pair.

    An annex carrying MORE than one distinct subpopulation would collapse them
    together here. That is not silent: two tables landing on one key makes the
    pairing ambiguous, and the report says so instead of comparing the wrong
    pair. Such a case needs an explicit map, the way `label_map.csv` handles
    divergent question wording.
    """
    parsed = {tn: parse_title(t) for tn, t in titles.items()}
    pops = Counter(p[1].split(' @ ')[0] for p in parsed.values())
    modal = pops.most_common(1)[0][0] if pops else ''
    out = {}
    for tn, (q, pop) in parsed.items():
        head, _, scope = pop.partition(' @ ')
        filtered = (bool(FILTER_NOTE.search(notes.get(tn, '')))
                    or (head and head != modal))
        out[tn] = (q, (SUB + ' @ ' + scope) if filtered else pop)
    return out


def parse_title(t):
    """(question, population @ scope) from a table title, derived by POSITION.

    Titles end in "- <geographic scope> - <year>", and each annex writes the
    scope differently: "<State>, <Region> e Brasil" in the simple one,
    "<State>" in the crossed one. Naming the scopes in a regex works for exactly
    the case it was written for and pairs NOTHING for every other, silently,
    wearing the face of two incompatible documents. Derive it instead: the last
    segment is the year, the one before it is the scope, whatever they happen
    to be called.

    The scope stays IN the key on purpose. Stripping it would let the simple
    annex of one state pair against the crossed annex of another and report the
    difference as divergence.
    """
    t = re.sub(r'^\s*Tabela\s+\d+\s*:\s*', '', t).strip()
    m = re.match(r'^"(.+?)"\s*(.*)$', t, re.S)
    q, rest = (m.group(1), m.group(2)) if m else (t, '')
    segs = [x for x in (seg.strip(' -') for seg in re.split(r'\s+-\s+', rest)) if x]
    if segs and YEAR.match(segs[-1]):
        segs.pop()
    scope = segs.pop().split(',')[0].strip() if segs else ''
    segs = [x for x in segs if not x.lower().startswith('por ')]
    pop = ' - '.join(segs).strip()
    return q.strip(), (pop + ' @ ' + scope if scope else pop)


def split_packed(v):
    m = PACK.match(v or '')
    return (m.group(1) + '%', '±' + m.group(2) + '%') if m else (None, None)


def load_label_map(path):
    """CSV: questao_cruzado,questao_simples — one row per known mismatch.

    Many-to-one on purpose: the SAME crossed question can correspond to
    differently worded simple questions in different annexes (one writes
    "<stem> [<item>]", another writes "<item> (<qualifier>)"). A 1:1 map forces one annex
    to win; a list lets each row be tried until one pairs.
    """
    if not path or not os.path.exists(path):
        return {}
    out = defaultdict(list)
    for r in csv.DictReader(open(path, encoding='utf-8-sig')):
        out[r['questao_cruzado'].strip()].append(r['questao_simples'].strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('simples'); ap.add_argument('cruzado')
    ap.add_argument('--label-map', default=None)
    ap.add_argument('--out', default='.')
    args = ap.parse_args()

    c1, t1, n1 = load(args.simples)
    c2, t2, n2 = load(args.cruzado)
    lmap = load_label_map(args.label_map)

    key1, key2 = annex_keys(t1, n1), annex_keys(t2, n2)
    k1, k2 = defaultdict(list), defaultdict(list)
    for tn, key in key1.items():
        k1[key].append(tn)
    for tn, key in key2.items():
        k2[key].append(tn)

    cols1 = defaultdict(dict)
    for (tn, col) in c1:
        # the simple annex may use a flat header ("Estimativa") or a two-level
        # one ("Estimativa (+- margem de erro) > Sim"). Indexing only the
        # hierarchical form made 89% of the cells invisible to pairing and
        # every question fell out as "sem coluna Estimativa". Index by leaf in
        # both cases.
        cols1[tn][col.split(' > ')[-1]] = c1[(tn, col)]

    comp, unpaired, ambiguous, nocontra = [], [], [], []
    matrix_pairs = 0
    for key0 in sorted(set(k2)):
        # The label map is a FALLBACK, not a rewrite. Applied unconditionally it
        # broke a pair that already matched: the annexes do not all word the
        # question the same way, so translating "[... autorizacao?]" into
        # "[... autorizacao]" fixes one annex and unpairs another, where both
        # sides already carried the same form. Try the question as written
        # first; consult the map only when that finds nothing.
        key = key0
        if key not in k1:
            for alt in lmap.get(key0[0], []):
                if (alt, key0[1]) in k1:
                    key = (alt, key0[1]); break
            else:
                alts = lmap.get(key0[0], [])
                key = (alts[0], key0[1]) if alts else key0
        if key not in k1:
            # the simple annex may hold this question as a matrix table:
            # "<base> [<item>]" decomposed here, "<base>" with <item> as a row there
            m = ITEM.match(key[0])
            base = (m.group(1).strip(), key[1]) if m else None
            if base and base in k1 and len(k1[base]) == 1:
                tn1, item = k1[base][0], m.group(2).strip()
                m1 = cols1.get(tn1, {})
                if any(item in d for d in m1.values()):
                    for tn2 in k2[key0]:
                        marg = [col for (t, col) in c2 if t == tn2][-1:]
                        if not marg:
                            continue
                        for cat, v2 in c2[(tn2, marg[0])].items():
                            if cat in ('Total', 'TOTAL'):
                                continue
                            a = m1.get(cat, {}).get(item)
                            if a is None:
                                nocontra.append((tn1, tn2, f'{item}/{cat}',
                                                 'matriz', a, v2))
                            else:
                                comp.append((tn1, tn2, f'{item}/{cat}', 'matriz',
                                             a, v2, a == v2))
                        matrix_pairs += 1
                    continue
            unpaired.append((key0, len(k2[key0]))); continue
        if len(k1[key]) != 1:
            ambiguous.append((key0, k1[key])); continue
        tn1 = k1[key][0]
        m1 = cols1.get(tn1, {})
        if 'Estimativa' not in m1:
            ambiguous.append((key0, ['sem coluna Estimativa'])); continue
        for tn2 in k2[key0]:
            marg = [col for (t, col) in c2 if t == tn2][-1:]
            marg = [col for (t, col) in c2 if t == tn2 and col == marg[0]]
            if not marg:
                continue
            d2 = c2[(tn2, marg[0])]
            for cat, v2 in d2.items():
                if cat in ('Total', 'TOTAL'):
                    continue
                if cat in m1 and 'Total' in m1[cat]:      # count rows
                    pairs = [(cat, m1[cat].get('Total'), v2)]
                else:
                    e2, mo2 = split_packed(v2)
                    pairs = [('Estimativa', m1['Estimativa'].get(cat), e2),
                             ('Margem de erro',
                              m1.get('Margem de erro', {}).get(cat), mo2)]
                for measure, a, b in pairs:
                    if a is None or b is None:
                        nocontra.append((tn1, tn2, cat, measure, a, b))
                    else:
                        comp.append((tn1, tn2, cat, measure, a, b, a == b))

    difs = [c for c in comp if not c[6]]
    os.makedirs(args.out, exist_ok=True)
    rep = os.path.join(args.out, 'confronto_report.md')
    with open(rep, 'w', encoding='utf-8') as f:
        f.write('# Confronto marginais (cruzado) x tabelas simples\n\n')
        f.write(f'- Questoes pareadas: **{len(set(k2)) - len(unpaired) - len(ambiguous)}** '
                f'de {len(set(k2))}\n')
        f.write(f'- Comparacoes: **{len(comp)}**\n')
        if matrix_pairs:
            f.write(f'- Dessas, pareadas por transposicao matriz/decomposto: '
                    f'**{matrix_pairs}** tabela(s) do cruzado\n')
        f.write(f'- **Divergencias: {len(difs)}**\n')
        f.write(f'- Sem contraparte: {len(nocontra)}\n\n')
        if difs:
            f.write('## Divergencias\n\n')
            for d in difs:
                f.write(f'- T{d[0]}/T{d[1]} [{d[2]}] {d[3]}: '
                        f'simples={d[4]!r} cruzado={d[5]!r}\n')
        if nocontra:
            f.write('\n## Sem contraparte (supressao assimetrica entre anexos)\n\n')
            for tn1, tn2, *_ in Counter((n[0], n[1]) for n in nocontra):
                pass
            for pair, n in Counter((n[0], n[1]) for n in nocontra).most_common(30):
                f.write(f'- T{pair[0]} (simples) / T{pair[1]} (cruzado): {n} celulas\n')
            f.write('\nUm anexo publica o que o outro suprime. Achado a reportar '
                    'a quem produziu as tabelas, nao a conciliar.\n')
        if unpaired:
            f.write('\n## Questoes do cruzado sem par no simples\n\n')
            for key, n in unpaired:
                f.write(f'- [{n} tabelas] {key[0][:100]} | {key[1]}\n')
            f.write('\nSe for so diferenca de redacao, acrescente a linha '
                    'correspondente em label_map.csv.\n')
        if ambiguous:
            f.write('\n## Pareamento ambiguo\n\n')
            for key, v in ambiguous:
                f.write(f'- {key[0][:90]} -> {v}\n')

    print(f'Questoes pareadas: {len(set(k2)) - len(unpaired) - len(ambiguous)}'
          f'/{len(set(k2))} | comparacoes: {len(comp)} | divergencias: {len(difs)}')
    print(f'Sem contraparte: {len(nocontra)} | sem par: {len(unpaired)}')
    print(f'Relatorio: {rep}')
    if difs:
        print('ATENCAO: ha divergencias entre anexos. Reportar, nao conciliar.')


if __name__ == '__main__':
    main()
