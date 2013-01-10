#-*- coding:utf-8 -*-

def solution(montant):
    monnaie = { '1': 'foo', '7': 'bar', '11': 'qix', '21': 'baz'}
    permutations = ((21,11,7,1), (21,11,1), (21,7,1), (21,1), (11,7,1), (11,1), (7,1), (1,0))
    compositions = []

    if not montant:
        return compositions

    for permutation in permutations:
        change = montant
        # print '--permutation', permutation
        composition = {}
        total = 0

        for piece in permutation:
            if piece == 0:
                break

            if piece > change:
                break

            nb_pieces, change = change // piece, change % piece
            if nb_pieces:
                # print '  %d * %d = %d + %d' % (piece, nb_pieces, piece * nb_pieces, change)
                composition[monnaie[str(piece)]] = nb_pieces
                total += piece * nb_pieces

            if not change:
                break

        if total == montant:
            compositions.append(composition)
            if piece > 1:
                break

    return compositions


if __name__ == "__main__":
    print solution(1)
    print solution(7)
    print solution(8)
    print solution(11)
    print solution(21)
