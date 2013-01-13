#-*- coding:utf-8 -*-
import itertools
from operator import itemgetter
from collections import defaultdict
from pprint import pprint

def mapper_commandes_par_vol_prix_depart(commandes):
    """map des commandes indexées par VOL,
    map des PRIX indexées par VOL,
    map des VOL indexées par DEPART"""
    vols_map, prix_map, depart_map = dict(), dict(), defaultdict(list)
    for commande in commandes:
        vols_map[commande['VOL']] = {
                'PRIX': commande['PRIX'],
                'DEPART': commande['DEPART'],
                'FIN': commande['DEPART'] + commande['DUREE'] }
        prix_map[commande['VOL']] = commande['PRIX']
        depart_map[commande['DEPART']].append(commande['VOL'])
    return vols_map, prix_map, depart_map

def trier_vols_par_depart(depart_map):
    """iterateur des VOL triées par DEPART"""
    for depart, vols in sorted(depart_map.items()):
        yield next(iter(vols))

def rechercher_vols_apres(depart_map, fin):
    """iterateur des VOL triées par DEPART avec DEPART >= fin"""
    def drop(depart_vols):
        return depart_vols[0] < fin

    vols_apres = itertools.dropwhile(drop, sorted(depart_map.items()))
    for depart, vols in vols_apres:
        yield next(iter(vols))

def solution(commandes):
    print 'nb_commandes:', len(commandes)
    vols_map, prix_map, depart_map = mapper_commandes_par_vol_prix_depart(commandes)
    vols = trier_vols_par_depart(depart_map)
    precedents = {}

    for vol in vols:
        commande = vols_map[vol]
        depart, fin = commande['DEPART'], commande['FIN']

        # suppression du vol de depart_map
        depart_map[depart].remove(vol)
        if not depart_map[depart]:
            del depart_map[depart]

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
    # print vol, vols_map[vol]

    while vol in precedents:
        vol = precedents[vol]
        # print '  ', vol, vols_map[vol]
        resultat['path'].insert(0, vol)

    print resultat
    print

if __name__ == '__main__':
    solution([
        { 'VOL': 'MONAD42', 'DEPART': 0, 'DUREE': 5, 'PRIX': 10 },
        { 'VOL': 'META18', 'DEPART': 3, 'DUREE': 7, 'PRIX': 14 },
        { 'VOL': 'LEGACY01', 'DEPART': 5, 'DUREE': 9, 'PRIX': 8 },
        { 'VOL': 'YAGNI17', 'DEPART': 5, 'DUREE': 9, 'PRIX': 7 }
    ])
    commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': 1000 - i } for i in range(1, 1000)]
    import random
    random.shuffle(commandes)
    solution(commandes)
    # {'path': ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512'], 'gain': 8977}



