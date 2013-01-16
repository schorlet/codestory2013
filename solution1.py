#-*- coding:utf-8 -*-

# monnaie = { 1: '1', 7: '7', 11: '11', 21: '21' }
monnaie = { 1: 'foo', 7: 'bar', 11: 'qix', 21: 'baz' }

def solution(montant, pieces = None):
    """
    >>> solution(0)
    []

    >>> solution(1)
    [{'foo': 1}]

    >>> solution(7)
    [{'bar': 1}, {'foo': 7}]

    >>> solution(23)
    [{'foo': 2, 'baz': 1}, {'foo': 5, 'bar': 1, 'qix': 1}, {'foo': 12, 'qix': 1}, {'foo': 1, 'qix': 2}, {'foo': 16, 'bar': 1}, {'foo': 9, 'bar': 2}, {'foo': 2, 'bar': 3}, {'foo': 23}]

    >>> solution(26)
    [{'foo': 5, 'baz': 1}, {'foo': 8, 'bar': 1, 'qix': 1}, {'foo': 1, 'bar': 2, 'qix': 1}, {'foo': 15, 'qix': 1}, {'foo': 4, 'qix': 2}, {'foo': 19, 'bar': 1}, {'foo': 12, 'bar': 2}, {'foo': 5, 'bar': 3}, {'foo': 26}]

    >>> solution(58)
    [{'bar': 1, 'foo': 19, 'baz': 1, 'qix': 1}, {'bar': 2, 'foo': 12, 'baz': 1, 'qix': 1}, {'bar': 3, 'foo': 5, 'baz': 1, 'qix': 1}, {'foo': 26, 'baz': 1, 'qix': 1}, {'bar': 1, 'foo': 8, 'baz': 1, 'qix': 2}, {'bar': 2, 'foo': 1, 'baz': 1, 'qix': 2}, {'foo': 15, 'baz': 1, 'qix': 2}, {'foo': 4, 'baz': 1, 'qix': 3}, {'bar': 1, 'foo': 30, 'baz': 1}, {'bar': 2, 'foo': 23, 'baz': 1}, {'bar': 3, 'foo': 16, 'baz': 1}, {'bar': 4, 'foo': 9, 'baz': 1}, {'bar': 5, 'foo': 2, 'baz': 1}, {'foo': 37, 'baz': 1}, {'foo': 5, 'baz': 2, 'qix': 1}, {'bar': 1, 'foo': 9, 'baz': 2}, {'bar': 2, 'foo': 2, 'baz': 2}, {'foo': 16, 'baz': 2}, {'foo': 40, 'bar': 1, 'qix': 1}, {'foo': 33, 'bar': 2, 'qix': 1}, {'foo': 26, 'bar': 3, 'qix': 1}, {'foo': 19, 'bar': 4, 'qix': 1}, {'foo': 12, 'bar': 5, 'qix': 1}, {'foo': 5, 'bar': 6, 'qix': 1}, {'foo': 47, 'qix': 1}, {'foo': 29, 'bar': 1, 'qix': 2}, {'foo': 22, 'bar': 2, 'qix': 2}, {'foo': 15, 'bar': 3, 'qix': 2}, {'foo': 8, 'bar': 4, 'qix': 2}, {'foo': 1, 'bar': 5, 'qix': 2}, {'foo': 36, 'qix': 2}, {'foo': 18, 'bar': 1, 'qix': 3}, {'foo': 11, 'bar': 2, 'qix': 3}, {'foo': 4, 'bar': 3, 'qix': 3}, {'foo': 25, 'qix': 3}, {'foo': 7, 'bar': 1, 'qix': 4}, {'bar': 2, 'qix': 4}, {'foo': 14, 'qix': 4}, {'foo': 3, 'qix': 5}, {'foo': 51, 'bar': 1}, {'foo': 44, 'bar': 2}, {'foo': 37, 'bar': 3}, {'foo': 30, 'bar': 4}, {'foo': 23, 'bar': 5}, {'foo': 16, 'bar': 6}, {'foo': 9, 'bar': 7}, {'foo': 2, 'bar': 8}, {'foo': 58}]

    >>> solution(100)
    [{'bar': 1, 'foo': 61, 'baz': 1, 'qix': 1}, {'bar': 2, 'foo': 54, 'baz': 1, 'qix': 1}, {'bar': 3, 'foo': 47, 'baz': 1, 'qix': 1}, {'bar': 4, 'foo': 40, 'baz': 1, 'qix': 1}, {'bar': 5, 'foo': 33, 'baz': 1, 'qix': 1}, {'bar': 6, 'foo': 26, 'baz': 1, 'qix': 1}, {'bar': 7, 'foo': 19, 'baz': 1, 'qix': 1}, {'bar': 8, 'foo': 12, 'baz': 1, 'qix': 1}, {'bar': 9, 'foo': 5, 'baz': 1, 'qix': 1}, {'foo': 68, 'baz': 1, 'qix': 1}, {'bar': 1, 'foo': 50, 'baz': 1, 'qix': 2}, {'bar': 2, 'foo': 43, 'baz': 1, 'qix': 2}, {'bar': 3, 'foo': 36, 'baz': 1, 'qix': 2}, {'bar': 4, 'foo': 29, 'baz': 1, 'qix': 2}, {'bar': 5, 'foo': 22, 'baz': 1, 'qix': 2}, {'bar': 6, 'foo': 15, 'baz': 1, 'qix': 2}, {'bar': 7, 'foo': 8, 'baz': 1, 'qix': 2}, {'bar': 8, 'foo': 1, 'baz': 1, 'qix': 2}, {'foo': 57, 'baz': 1, 'qix': 2}, {'bar': 1, 'foo': 39, 'baz': 1, 'qix': 3}, {'bar': 2, 'foo': 32, 'baz': 1, 'qix': 3}, {'bar': 3, 'foo': 25, 'baz': 1, 'qix': 3}, {'bar': 4, 'foo': 18, 'baz': 1, 'qix': 3}, {'bar': 5, 'foo': 11, 'baz': 1, 'qix': 3}, {'bar': 6, 'foo': 4, 'baz': 1, 'qix': 3}, {'foo': 46, 'baz': 1, 'qix': 3}, {'bar': 1, 'foo': 28, 'baz': 1, 'qix': 4}, {'bar': 2, 'foo': 21, 'baz': 1, 'qix': 4}, {'bar': 3, 'foo': 14, 'baz': 1, 'qix': 4}, {'bar': 4, 'foo': 7, 'baz': 1, 'qix': 4}, {'bar': 5, 'baz': 1, 'qix': 4}, {'foo': 35, 'baz': 1, 'qix': 4}, {'bar': 1, 'foo': 17, 'baz': 1, 'qix': 5}, {'bar': 2, 'foo': 10, 'baz': 1, 'qix': 5}, {'bar': 3, 'foo': 3, 'baz': 1, 'qix': 5}, {'foo': 24, 'baz': 1, 'qix': 5}, {'bar': 1, 'foo': 6, 'baz': 1, 'qix': 6}, {'foo': 13, 'baz': 1, 'qix': 6}, {'foo': 2, 'baz': 1, 'qix': 7}, {'bar': 1, 'foo': 72, 'baz': 1}, {'bar': 2, 'foo': 65, 'baz': 1}, {'bar': 3, 'foo': 58, 'baz': 1}, {'bar': 4, 'foo': 51, 'baz': 1}, {'bar': 5, 'foo': 44, 'baz': 1}, {'bar': 6, 'foo': 37, 'baz': 1}, {'bar': 7, 'foo': 30, 'baz': 1}, {'bar': 8, 'foo': 23, 'baz': 1}, {'bar': 9, 'foo': 16, 'baz': 1}, {'bar': 10, 'foo': 9, 'baz': 1}, {'bar': 11, 'foo': 2, 'baz': 1}, {'foo': 79, 'baz': 1}, {'bar': 1, 'foo': 40, 'baz': 2, 'qix': 1}, {'bar': 2, 'foo': 33, 'baz': 2, 'qix': 1}, {'bar': 3, 'foo': 26, 'baz': 2, 'qix': 1}, {'bar': 4, 'foo': 19, 'baz': 2, 'qix': 1}, {'bar': 5, 'foo': 12, 'baz': 2, 'qix': 1}, {'bar': 6, 'foo': 5, 'baz': 2, 'qix': 1}, {'foo': 47, 'baz': 2, 'qix': 1}, {'bar': 1, 'foo': 29, 'baz': 2, 'qix': 2}, {'bar': 2, 'foo': 22, 'baz': 2, 'qix': 2}, {'bar': 3, 'foo': 15, 'baz': 2, 'qix': 2}, {'bar': 4, 'foo': 8, 'baz': 2, 'qix': 2}, {'bar': 5, 'foo': 1, 'baz': 2, 'qix': 2}, {'foo': 36, 'baz': 2, 'qix': 2}, {'bar': 1, 'foo': 18, 'baz': 2, 'qix': 3}, {'bar': 2, 'foo': 11, 'baz': 2, 'qix': 3}, {'bar': 3, 'foo': 4, 'baz': 2, 'qix': 3}, {'foo': 25, 'baz': 2, 'qix': 3}, {'bar': 1, 'foo': 7, 'baz': 2, 'qix': 4}, {'bar': 2, 'baz': 2, 'qix': 4}, {'foo': 14, 'baz': 2, 'qix': 4}, {'foo': 3, 'baz': 2, 'qix': 5}, {'bar': 1, 'foo': 51, 'baz': 2}, {'bar': 2, 'foo': 44, 'baz': 2}, {'bar': 3, 'foo': 37, 'baz': 2}, {'bar': 4, 'foo': 30, 'baz': 2}, {'bar': 5, 'foo': 23, 'baz': 2}, {'bar': 6, 'foo': 16, 'baz': 2}, {'bar': 7, 'foo': 9, 'baz': 2}, {'bar': 8, 'foo': 2, 'baz': 2}, {'foo': 58, 'baz': 2}, {'bar': 1, 'foo': 19, 'baz': 3, 'qix': 1}, {'bar': 2, 'foo': 12, 'baz': 3, 'qix': 1}, {'bar': 3, 'foo': 5, 'baz': 3, 'qix': 1}, {'foo': 26, 'baz': 3, 'qix': 1}, {'bar': 1, 'foo': 8, 'baz': 3, 'qix': 2}, {'bar': 2, 'foo': 1, 'baz': 3, 'qix': 2}, {'foo': 15, 'baz': 3, 'qix': 2}, {'foo': 4, 'baz': 3, 'qix': 3}, {'bar': 1, 'foo': 30, 'baz': 3}, {'bar': 2, 'foo': 23, 'baz': 3}, {'bar': 3, 'foo': 16, 'baz': 3}, {'bar': 4, 'foo': 9, 'baz': 3}, {'bar': 5, 'foo': 2, 'baz': 3}, {'foo': 37, 'baz': 3}, {'foo': 5, 'baz': 4, 'qix': 1}, {'bar': 1, 'foo': 9, 'baz': 4}, {'bar': 2, 'foo': 2, 'baz': 4}, {'foo': 16, 'baz': 4}, {'foo': 82, 'bar': 1, 'qix': 1}, {'foo': 75, 'bar': 2, 'qix': 1}, {'foo': 68, 'bar': 3, 'qix': 1}, {'foo': 61, 'bar': 4, 'qix': 1}, {'foo': 54, 'bar': 5, 'qix': 1}, {'foo': 47, 'bar': 6, 'qix': 1}, {'foo': 40, 'bar': 7, 'qix': 1}, {'foo': 33, 'bar': 8, 'qix': 1}, {'foo': 26, 'bar': 9, 'qix': 1}, {'foo': 19, 'bar': 10, 'qix': 1}, {'foo': 12, 'bar': 11, 'qix': 1}, {'foo': 5, 'bar': 12, 'qix': 1}, {'foo': 89, 'qix': 1}, {'foo': 71, 'bar': 1, 'qix': 2}, {'foo': 64, 'bar': 2, 'qix': 2}, {'foo': 57, 'bar': 3, 'qix': 2}, {'foo': 50, 'bar': 4, 'qix': 2}, {'foo': 43, 'bar': 5, 'qix': 2}, {'foo': 36, 'bar': 6, 'qix': 2}, {'foo': 29, 'bar': 7, 'qix': 2}, {'foo': 22, 'bar': 8, 'qix': 2}, {'foo': 15, 'bar': 9, 'qix': 2}, {'foo': 8, 'bar': 10, 'qix': 2}, {'foo': 1, 'bar': 11, 'qix': 2}, {'foo': 78, 'qix': 2}, {'foo': 60, 'bar': 1, 'qix': 3}, {'foo': 53, 'bar': 2, 'qix': 3}, {'foo': 46, 'bar': 3, 'qix': 3}, {'foo': 39, 'bar': 4, 'qix': 3}, {'foo': 32, 'bar': 5, 'qix': 3}, {'foo': 25, 'bar': 6, 'qix': 3}, {'foo': 18, 'bar': 7, 'qix': 3}, {'foo': 11, 'bar': 8, 'qix': 3}, {'foo': 4, 'bar': 9, 'qix': 3}, {'foo': 67, 'qix': 3}, {'foo': 49, 'bar': 1, 'qix': 4}, {'foo': 42, 'bar': 2, 'qix': 4}, {'foo': 35, 'bar': 3, 'qix': 4}, {'foo': 28, 'bar': 4, 'qix': 4}, {'foo': 21, 'bar': 5, 'qix': 4}, {'foo': 14, 'bar': 6, 'qix': 4}, {'foo': 7, 'bar': 7, 'qix': 4}, {'bar': 8, 'qix': 4}, {'foo': 56, 'qix': 4}, {'foo': 38, 'bar': 1, 'qix': 5}, {'foo': 31, 'bar': 2, 'qix': 5}, {'foo': 24, 'bar': 3, 'qix': 5}, {'foo': 17, 'bar': 4, 'qix': 5}, {'foo': 10, 'bar': 5, 'qix': 5}, {'foo': 3, 'bar': 6, 'qix': 5}, {'foo': 45, 'qix': 5}, {'foo': 27, 'bar': 1, 'qix': 6}, {'foo': 20, 'bar': 2, 'qix': 6}, {'foo': 13, 'bar': 3, 'qix': 6}, {'foo': 6, 'bar': 4, 'qix': 6}, {'foo': 34, 'qix': 6}, {'foo': 16, 'bar': 1, 'qix': 7}, {'foo': 9, 'bar': 2, 'qix': 7}, {'foo': 2, 'bar': 3, 'qix': 7}, {'foo': 23, 'qix': 7}, {'foo': 5, 'bar': 1, 'qix': 8}, {'foo': 12, 'qix': 8}, {'foo': 1, 'qix': 9}, {'foo': 93, 'bar': 1}, {'foo': 86, 'bar': 2}, {'foo': 79, 'bar': 3}, {'foo': 72, 'bar': 4}, {'foo': 65, 'bar': 5}, {'foo': 58, 'bar': 6}, {'foo': 51, 'bar': 7}, {'foo': 44, 'bar': 8}, {'foo': 37, 'bar': 9}, {'foo': 30, 'bar': 10}, {'foo': 23, 'bar': 11}, {'foo': 16, 'bar': 12}, {'foo': 9, 'bar': 13}, {'foo': 2, 'bar': 14}, {'foo': 100}]
    """
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


if __name__ == '__main__':
    for i in range(1, 101):
        print solution(i)
