#-*- coding:utf-8 -*-
import itertools
from operator import itemgetter
from collections import defaultdict

def mapper_commandes(commandes):
    """map des commandes indexées par VOL,
    map des PRIX indexées par VOL,
    map des VOL indexées par DEPART"""
    vols_map, prix_map = dict(), dict()
    depart_map = defaultdict(list)
    max_depart = 0
    for commande in commandes:
        if commande['DEPART'] > max_depart:
            max_depart = commande['DEPART']
        vols_map[commande['VOL']] = {
                'PRIX': commande['PRIX'],
                'DEPART': commande['DEPART'],
                'FIN': commande['DEPART'] + commande['DUREE'] }
        prix_map[commande['VOL']] = commande['PRIX']
        depart_map[commande['DEPART']].append(commande['VOL'])
    return vols_map, prix_map, depart_map, max_depart

def trier_vols_par_depart(depart_map):
    """iterateur des VOL triées par DEPART"""
    for depart, vols in sorted(depart_map.items()):
        yield next(iter(vols))

def rechercher_vols_apres(depart_map, fin):
    """iterateur des VOL avec DEPART >= FIN"""
    for depart, vols in depart_map.items():
        if depart >= fin:
            yield next(iter(vols))

def solution(commandes):
    """
    >>> solution([])
    {'path': [], 'gain': 0}

    >>> solution([{ 'VOL': 'MONAD42', 'DEPART': 0, 'DUREE': 5, 'PRIX': 10 }])
    {'path': ['MONAD42'], 'gain': 10}

    >>> solution([
    ...     { 'VOL': 'MONAD42', 'DEPART': 0, 'DUREE': 5, 'PRIX': 10 },
    ...     { 'VOL': 'META18', 'DEPART': 3, 'DUREE': 7, 'PRIX': 14 },
    ...     { 'VOL': 'LEGACY01', 'DEPART': 5, 'DUREE': 9, 'PRIX': 8 },
    ...     { 'VOL': 'YAGNI17', 'DEPART': 5, 'DUREE': 9, 'PRIX': 7 }
    ... ])
    {'path': ['MONAD42', 'LEGACY01'], 'gain': 18}

    >>> import random
    >>> from operator import truediv

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': 1, 'PRIX': 1 } for i in range(1, 10)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 'gain': 9}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': 1000 - i } for i in range(1, 1000)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512'], 'gain': 8977}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': i } for i in range(1, 1000)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '3', '7', '15', '31', '62', '124', '249', '499', '999'], 'gain': 1990}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': truediv(1, i) } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '2', '4', '8', '16', '32', '64'], 'gain': 1.984375}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i * 2, 'PRIX': i } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '3', '11', '33', '99'], 'gain': 147}


    >>> commandes = [{ 'VOL': str(i), 'DEPART': i * 2, 'DUREE': i, 'PRIX': i } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> solution(commandes)
    {'path': ['1', '2', '3', '5', '8', '12', '19', '29', '44', '66', '99'], 'gain': 288}
    """
    # print 'solution2: nb_commandes =', len(commandes)
    if len(commandes) == 0:
        return { 'gain': 0, 'path': list() }

    vols_map, prix_map, depart_map, max_depart = mapper_commandes(commandes)
    vols = trier_vols_par_depart(depart_map)
    precedents = {}

    for vol in vols:
        commande = vols_map[vol]
        depart, fin = commande['DEPART'], commande['FIN']

        # suppression du vol de depart_map
        depart_map[depart].remove(vol)
        if not depart_map[depart]:
            del depart_map[depart]

        if fin > max_depart:
            break

        # recherche des commandes suivantes
        vols_apres = rechercher_vols_apres(depart_map, fin)
        for vol_apres in vols_apres:
            if vol_apres in precedents:
                somme_prix = prix_map[vol] + vols_map[vol_apres]['PRIX']
                if somme_prix > prix_map[vol_apres]:
                    prix_map[vol_apres] = somme_prix
                    precedents[vol_apres] = vol
            else:
                prix_map[vol_apres] = prix_map[vol] + prix_map[vol_apres]
                precedents[vol_apres] = vol

    # for vol, total in sorted(prix_map.items(), key=itemgetter(1)):
        # print total
        # print '  ', vol, vols_map[vol]
        # while vol in precedents:
            # vol = precedents[vol]
            # print '  ', vol, vols_map[vol]

    vol_gain = max(prix_map.items(), key=itemgetter(1))
    resultat = { 'gain': vol_gain[1], 'path': list() }

    vol = vol_gain[0]
    resultat['path'].append(vol)

    while vol in precedents:
        vol = precedents[vol]
        resultat['path'].insert(0, vol)

    return resultat

if __name__ == '__main__':
    import random
    from operator import truediv
    commandes = [{ 'VOL': str(i), 'DEPART': i*2, 'DUREE': i, 'PRIX': i } for i in range(1, 100)]
    random.shuffle(commandes)
    print solution(commandes)

