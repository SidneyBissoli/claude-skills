# -*- coding: utf-8 -*-
"""Transplanta comentarios de um .docx para outros, reautorando.

Casca fina sobre docx_comments.py: a logica de OOXML e a regra da copia moram
la; aqui so ficam os argumentos e o relatorio.

    python transplantar.py ORIGEM.docx --para DEST1.docx DEST2.docx \
        --ids 5 21 27 --autor "Nome" [--iniciais XX] [--imagem 6=4] \
        [--sufixo _comentado | --na-copia] [--aplicar]

Os destinos nunca sao alterados: cada um gera uma copia nova,
<destino><sufixo>.docx, ao lado dele. `--na-copia` grava no proprio destino e
so serve quando ele JA E a copia de trabalho desta tarefa.

Sem --aplicar, apenas relata o que faria e o nome de cada copia: e um ensaio.
Nada e gravado se a verificacao final acusar problema.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_comments as dc


def nome_da_copia(destino, sufixo):
    base, ext = os.path.splitext(destino)
    return base + sufixo + (ext or '.docx')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('origem')
    ap.add_argument('--para', nargs='+', required=True)
    ap.add_argument('--ids', nargs='+', required=True)
    ap.add_argument('--autor', required=True)
    ap.add_argument('--iniciais', default='')
    ap.add_argument('--imagem', nargs='*', default=[],
                    help='mapeia id=n para ancorar na n-esima imagem (ex: 6=4)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--sufixo', default='_comentado',
                   help='sufixo da copia criada para cada destino')
    g.add_argument('--na-copia', action='store_true',
                   help='o destino ja e a copia de trabalho: gravar nele')
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    imagens = {}
    for par in a.imagem:
        k, _, v = par.partition('=')
        imagens[k] = int(v)

    total, falhas = 0, 0
    for destino in a.para:
        saida = None if a.na_copia else nome_da_copia(destino, a.sufixo)
        r = dc.transplant(a.origem, destino, a.ids, a.autor, a.iniciais,
                          imagens, apply=a.aplicar, saida=saida,
                          na_copia=a.na_copia)
        print('=== %s -> %s' % (os.path.basename(destino),
                                 os.path.basename(saida or destino)))
        for l in r.get('linhas', []):
            if l['estado'] == 'ok':
                print('   c%-3s OK id=%-4s %s: %r' % (l['id'], l['novo_id'],
                                                    l['classe'], l['ancora'][:60]))
            else:
                print('   c%-3s FALHOU     %s' % (l['id'], l['detalhe']))
        if not r['ok']:
            falhas += 1
            print('   NAO GRAVADO: %s' % r['erro'])
            for p in r.get('problemas', [])[:10]:
                print('     - %s' % p)
        elif r.get('ensaio'):
            print('   (ensaio: nada gravado) inseriria %d' % r['inseridos'])
        else:
            print('   gravado e verificado: %d comentarios em %s'
                  % (r['inseridos'], r['arquivo']))
            total += r['inseridos']
    print('\ntotal inserido: %d' % total)
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
