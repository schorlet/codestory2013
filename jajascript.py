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

def rechercher_vols_apres(depart_map, fin, vols_map):
    """iterateur des VOL avec DEPART >= FIN"""
    max_fin, max_fin_ok = 0, False
    for depart, vols in sorted(depart_map.items()):
        if depart >= fin:
            if not max_fin_ok:
                max_fin_ok = True
                for vol in vols:
                    vol_fin = vols_map[vol]['FIN']
                    if vol_fin > max_fin:
                        max_fin = vol_fin
                    yield vol
            elif depart < max_fin:
                yield next(iter(vols))
            else:
                break

def optimize(commandes):
    """
    >>> optimize([])
    {'path': [], 'gain': 0}

    >>> optimize([{ 'VOL': 'MONAD42', 'DEPART': 0, 'DUREE': 5, 'PRIX': 10 }])
    {'path': ['MONAD42'], 'gain': 10}

    >>> optimize([
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
    >>> optimize(commandes)
    {'path': ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 'gain': 9}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': 1000 - i } for i in range(1, 1000)]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512'], 'gain': 8977}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': i } for i in range(1, 1000)]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['1', '3', '7', '15', '31', '62', '124', '249', '499', '999'], 'gain': 1990}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': truediv(1, i) } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['1', '2', '4', '8', '16', '32', '64'], 'gain': 1.984375}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i * 2, 'PRIX': i } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['1', '3', '11', '33', '99'], 'gain': 147}

    >>> commandes = [{ 'VOL': str(i), 'DEPART': i * 2, 'DUREE': i, 'PRIX': i } for i in range(1, 100)]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['1', '2', '3', '5', '8', '12', '19', '29', '44', '66', '99'], 'gain': 288}

    >>> commandes = [
    ...     { 'VOL': 'VOL1', 'DEPART': 0, 'DUREE': 20, 'PRIX': 1 },
    ...     { 'VOL': 'VOL2', 'DEPART': 2, 'DUREE': 2, 'PRIX': 1 },
    ...     { 'VOL': 'VOL3', 'DEPART': 4, 'DUREE': 2, 'PRIX': 1 },
    ...     { 'VOL': 'VOL4', 'DEPART': 6, 'DUREE': 2, 'PRIX': 1 }
    ... ]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['VOL2', 'VOL3', 'VOL4'], 'gain': 3}
    """
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
            continue

        # recherche des commandes suivantes
        vols_apres = rechercher_vols_apres(depart_map, fin, vols_map)
        for vol_apres in vols_apres:
            if vol_apres in precedents:
                somme_prix = prix_map[vol] + vols_map[vol_apres]['PRIX']
                if somme_prix >= prix_map[vol_apres]:
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
    commandes = [{'PRIX': 10, 'DEPART': 0, 'VOL': 'wonderful-macrame-43', 'DUREE': 4},
        {'PRIX': 6, 'DEPART': 1, 'VOL': 'grotesque-sprawl-83', 'DUREE': 2},
        {'PRIX': 5, 'DEPART': 2, 'VOL': 'strange-mousetrap-58', 'DUREE': 6},
        {'PRIX': 4, 'DEPART': 4, 'VOL': 'ashamed-linebacker-28', 'DUREE': 5},
        {'PRIX': 7, 'DEPART': 5, 'VOL': 'long-airline-80', 'DUREE': 2},
        {'PRIX': 10, 'DEPART': 5, 'VOL': 'voiceless-values-39', 'DUREE': 4},
        {'PRIX': 7, 'DEPART': 6, 'VOL': 'dark-chalkboard-14', 'DUREE': 2},
        {'PRIX': 1, 'DEPART': 7, 'VOL': 'clumsy-visor-47', 'DUREE': 6},
        {'PRIX': 22, 'DEPART': 9, 'VOL': 'outstanding-jackpot-29', 'DUREE': 5},
        {'PRIX': 19, 'DEPART': 10, 'VOL': 'elated-sideburns-49', 'DUREE': 2},
        {'PRIX': 13, 'DEPART': 10, 'VOL': 'hushed-hairstylist-38', 'DUREE': 4},
        {'PRIX': 9, 'DEPART': 11, 'VOL': 'foolish-bike-13', 'DUREE': 2},
        {'PRIX': 1, 'DEPART': 12, 'VOL': 'hurt-cookout-25', 'DUREE': 6},
        {'PRIX': 10, 'DEPART': 14, 'VOL': 'confused-fiddle-51', 'DUREE': 5},
        {'PRIX': 28, 'DEPART': 15, 'VOL': 'gigantic-sheet-32', 'DUREE': 2},
        {'PRIX': 12, 'DEPART': 15, 'VOL': 'silent-rattler-22', 'DUREE': 4},
        {'PRIX': 5, 'DEPART': 16, 'VOL': 'uninterested-seacoast-53', 'DUREE': 2},
        {'PRIX': 3, 'DEPART': 17, 'VOL': 'famous-stipend-17', 'DUREE': 6},
        {'PRIX': 4, 'DEPART': 19, 'VOL': 'horrible-beaver-60', 'DUREE': 5},
        {'PRIX': 25, 'DEPART': 20, 'VOL': 'tall-guy-23', 'DUREE': 2},
        {'PRIX': 10, 'DEPART': 20, 'VOL': 'dangerous-cap-42', 'DUREE': 4},
        {'PRIX': 6, 'DEPART': 21, 'VOL': 'stupid-fishhook-65', 'DUREE': 2},
        {'PRIX': 3, 'DEPART': 22, 'VOL': 'helpful-shipyard-67', 'DUREE': 6},
        {'PRIX': 22, 'DEPART': 24, 'VOL': 'lazy-buckle-85', 'DUREE': 5},
        {'PRIX': 2, 'DEPART': 25, 'VOL': 'successful-cat-12', 'DUREE': 2},
        {'PRIX': 10, 'DEPART': 25, 'VOL': 'stupid-dinner-41', 'DUREE': 4},
        {'PRIX': 2, 'DEPART': 26, 'VOL': 'motionless-student-82', 'DUREE': 2},
        {'PRIX': 3, 'DEPART': 27, 'VOL': 'short-life-17', 'DUREE': 6},
        {'PRIX': 8, 'DEPART': 29, 'VOL': 'immense-rattle-89', 'DUREE': 5},
        {'PRIX': 13, 'DEPART': 30, 'VOL': 'square-sisterhood-91', 'DUREE': 2}]
    print optimize(commandes)
    # {'gain': 127, 'path': ['wonderful-macrame-43', 'long-airline-80', 'outstanding-jackpot-29', 'gigantic-sheet-32', 'tall-guy-23', 'lazy-buckle-85', 'square-sisterhood-91']}
    # {'gain': 127, 'path': ['wonderful-macrame-43', 'dark-chalkboard-14', 'outstanding-jackpot-29', 'gigantic-sheet-32', 'tall-guy-23', 'lazy-buckle-85', 'square-sisterhood-91']}
