#-*- coding:utf-8 -*-

# monnaie = { 1: '1', 7: '7', 11: '11', 21: '21' }
monnaie = { 1: 'foo', 7: 'bar', 11: 'qix', 21: 'baz' }

def solution(montant, pieces = None):
    compositions = []

    if not montant:
        return compositions

    if not pieces:
        pieces = sorted(monnaie.keys(), reverse = True)

    for piece in pieces:
        if piece > montant:
            continue

        if piece == 1:
            composition = {monnaie[piece]: montant}
            compositions.append(composition)
            break

        nb_pieces = montant // piece
        for nb_piece in range(1, nb_pieces + 1):
            reste = montant - (piece * nb_piece)

            if reste:
                suite_compositions = solution(reste, pieces[pieces.index(piece) + 1:])

                for suite_composition in suite_compositions:
                    composition = {monnaie[piece]: nb_piece}
                    composition.update(suite_composition)
                    compositions.append(composition)
            else:
                composition = {monnaie[piece]: nb_piece}
                compositions.append(composition)
                break

    return compositions


if __name__ == "__main__":
    for i in range(1, 101):
        print solution(i)

