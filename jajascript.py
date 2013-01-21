#-*- coding:utf-8 -*-
from operator import itemgetter
from collections import defaultdict
from collections import deque

def mapper_commandes(commandes):
    vols_map, prix_map = dict(), dict()
    depart_map = defaultdict(list)
    for commande in commandes:
        vols_map[commande['VOL']] = {
                'PRIX': commande['PRIX'], 'DEPART': commande['DEPART'],
                'FIN': commande['DEPART'] + commande['DUREE'] }
        prix_map[commande['VOL']] = commande['PRIX']
        depart_map[commande['DEPART']].append(commande['VOL'])
    return vols_map, prix_map, depart_map

def trier_departs(depart_map):
    return deque(depart_map.keys())

def rechercher_vols_apres(departs, depart_map, fin):
    test = 0
    for depart in departs:
        if depart >= fin:
            vols = depart_map[depart]
            yield next(iter(vols))
            test += 1
            if test > 2:
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

    >>> commandes = [{'PRIX': 13, 'DEPART': 0, 'VOL': 'puny-violin-24', 'DUREE': 4}, {'PRIX': 10, 'DEPART': 1, 'VOL': 'fantastic-stardom-58', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 2, 'VOL': 'exuberant-linesman-34', 'DUREE': 6}, {'PRIX': 19, 'DEPART': 4, 'VOL': 'unsightly-khaki-48', 'DUREE': 5}, {'PRIX': 21, 'DEPART': 5, 'VOL': 'annoying-missionary-38', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['puny-violin-24', 'annoying-missionary-38'], 'gain': 34}

    >>> commandes = [{'PRIX': 8, 'DEPART': 0, 'VOL': 'soft-penniless-43', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 1, 'VOL': 'teeny-tiny-walkietalkie-33', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 2, 'VOL': 'tall-tyranny-72', 'DUREE': 6}, {'PRIX': 16, 'DEPART': 4, 'VOL': 'excited-supervisor-94', 'DUREE': 5}, {'PRIX': 30, 'DEPART': 5, 'VOL': 'crowded-graveyard-80', 'DUREE': 2}, {'PRIX': 7, 'DEPART': 5, 'VOL': 'purring-comedienne-91', 'DUREE': 4}, {'PRIX': 10, 'DEPART': 6, 'VOL': 'black-groundhog-18', 'DUREE': 2}, {'PRIX': 4, 'DEPART': 7, 'VOL': 'doubtful-risk-19', 'DUREE': 6}, {'PRIX': 20, 'DEPART': 9, 'VOL': 'miniature-hamper-11', 'DUREE': 5}, {'PRIX': 1, 'DEPART': 10, 'VOL': 'fierce-sneaker-70', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['teeny-tiny-walkietalkie-33', 'crowded-graveyard-80', 'miniature-hamper-11'], 'gain': 59}

    >>> commandes = [{'PRIX': 14, 'DEPART': 0, 'VOL': 'grumpy-rubberstamp-77', 'DUREE': 4}, {'PRIX': 3, 'DEPART': 1, 'VOL': 'ancient-backstage-29', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 2, 'VOL': 'raspy-whey-63', 'DUREE': 6}, {'PRIX': 12, 'DEPART': 4, 'VOL': 'lazy-hill-19', 'DUREE': 5}, {'PRIX': 8, 'DEPART': 5, 'VOL': 'narrow-romance-18', 'DUREE': 2}, {'PRIX': 8, 'DEPART': 5, 'VOL': 'enchanting-stepmother-18', 'DUREE': 4}, {'PRIX': 4, 'DEPART': 6, 'VOL': 'hungry-revenge-29', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 7, 'VOL': 'testy-somebody-42', 'DUREE': 6}, {'PRIX': 7, 'DEPART': 9, 'VOL': 'scrawny-rudder-35', 'DUREE': 5}, {'PRIX': 30, 'DEPART': 10, 'VOL': 'old-fashioned-cardboard-81', 'DUREE': 2}, {'PRIX': 15, 'DEPART': 10, 'VOL': 'weary-harmonica-51', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 11, 'VOL': 'deafening-label-85', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 12, 'VOL': 'bloody-symbol-63', 'DUREE': 6}, {'PRIX': 19, 'DEPART': 14, 'VOL': 'squealing-rob-21', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 15, 'VOL': 'worried-violin-2', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['grumpy-rubberstamp-77', 'lazy-hill-19', 'old-fashioned-cardboard-81', 'squealing-rob-21'], 'gain': 75}

    >>> commandes = [{'PRIX': 9, 'DEPART': 0, 'VOL': 'fat-tycoon-6', 'DUREE': 4}, {'PRIX': 2, 'DEPART': 1, 'VOL': 'colorful-rhino-5', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 2, 'VOL': 'gigantic-rectangle-77', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 4, 'VOL': 'crazy-merrygoround-57', 'DUREE': 5}, {'PRIX': 28, 'DEPART': 5, 'VOL': 'clumsy-railing-40', 'DUREE': 2}, {'PRIX': 15, 'DEPART': 5, 'VOL': 'fat-graphic-94', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 6, 'VOL': 'fancy-dot-24', 'DUREE': 2}, {'PRIX': 4, 'DEPART': 7, 'VOL': 'high-pitched-zenith-87', 'DUREE': 6}, {'PRIX': 6, 'DEPART': 9, 'VOL': 'faint-calendar-81', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 10, 'VOL': 'muddy-commando-39', 'DUREE': 2}, {'PRIX': 12, 'DEPART': 10, 'VOL': 'moaning-comedienne-45', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 11, 'VOL': 'dangerous-bellows-42', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 12, 'VOL': 'brave-mustang-70', 'DUREE': 6}, {'PRIX': 5, 'DEPART': 14, 'VOL': 'hurt-net-43', 'DUREE': 5}, {'PRIX': 24, 'DEPART': 15, 'VOL': 'unusual-killer-75', 'DUREE': 2}, {'PRIX': 8, 'DEPART': 15, 'VOL': 'short-pastrami-79', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 16, 'VOL': 'graceful-windsurfing-55', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 17, 'VOL': 'adventurous-twinkle-28', 'DUREE': 6}, {'PRIX': 6, 'DEPART': 19, 'VOL': 'shrill-flax-62', 'DUREE': 5}, {'PRIX': 21, 'DEPART': 20, 'VOL': 'young-soprano-62', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['fat-tycoon-6', 'clumsy-railing-40', 'muddy-commando-39', 'unusual-killer-75', 'young-soprano-62'], 'gain': 95}

    >>> commandes = [{'PRIX': 6, 'DEPART': 0, 'VOL': 'expensive-zombie-63', 'DUREE': 4}, {'PRIX': 3, 'DEPART': 1, 'VOL': 'defiant-amphetamine-87', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 2, 'VOL': 'glamorous-waltz-67', 'DUREE': 6}, {'PRIX': 18, 'DEPART': 4, 'VOL': 'large-machinist-50', 'DUREE': 5}, {'PRIX': 14, 'DEPART': 5, 'VOL': 'black-polyester-26', 'DUREE': 2}, {'PRIX': 13, 'DEPART': 5, 'VOL': 'doubtful-detective-44', 'DUREE': 4}, {'PRIX': 7, 'DEPART': 6, 'VOL': 'breakable-saturn-23', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 7, 'VOL': 'horrible-dime-6', 'DUREE': 6}, {'PRIX': 13, 'DEPART': 9, 'VOL': 'kind-welt-59', 'DUREE': 5}, {'PRIX': 10, 'DEPART': 10, 'VOL': 'rapid-verb-86', 'DUREE': 2}, {'PRIX': 11, 'DEPART': 10, 'VOL': 'grumpy-somewhere-64', 'DUREE': 4}, {'PRIX': 1, 'DEPART': 11, 'VOL': 'outstanding-dude-52', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 12, 'VOL': 'gleaming-sunbather-69', 'DUREE': 6}, {'PRIX': 21, 'DEPART': 14, 'VOL': 'confused-windowpane-85', 'DUREE': 5}, {'PRIX': 27, 'DEPART': 15, 'VOL': 'wild-bifocal-73', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 15, 'VOL': 'modern-handgun-67', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 16, 'VOL': 'poor-slogan-89', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 17, 'VOL': 'muddy-flowerpot-66', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 19, 'VOL': 'angry-grass-40', 'DUREE': 5}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'wrong-surgery-17', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'immense-spaniel-90', 'DUREE': 4}, {'PRIX': 10, 'DEPART': 21, 'VOL': 'panicky-steam-40', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 22, 'VOL': 'brainy-ulcer-30', 'DUREE': 6}, {'PRIX': 18, 'DEPART': 24, 'VOL': 'fine-waiver-78', 'DUREE': 5}, {'PRIX': 22, 'DEPART': 25, 'VOL': 'mushy-newscaster-11', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['expensive-zombie-63', 'large-machinist-50', 'kind-welt-59', 'wild-bifocal-73', 'wrong-surgery-17', 'mushy-newscaster-11'], 'gain': 96}

    >>> commandes = [{'PRIX': 10, 'DEPART': 0, 'VOL': 'wonderful-macrame-43', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 1, 'VOL': 'grotesque-sprawl-83', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 2, 'VOL': 'strange-mousetrap-58', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 4, 'VOL': 'ashamed-linebacker-28', 'DUREE': 5}, {'PRIX': 7, 'DEPART': 5, 'VOL': 'long-airline-80', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 5, 'VOL': 'voiceless-values-39', 'DUREE': 4}, {'PRIX': 7, 'DEPART': 6, 'VOL': 'dark-chalkboard-14', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 7, 'VOL': 'clumsy-visor-47', 'DUREE': 6}, {'PRIX': 22, 'DEPART': 9, 'VOL': 'outstanding-jackpot-29', 'DUREE': 5}, {'PRIX': 19, 'DEPART': 10, 'VOL': 'elated-sideburns-49', 'DUREE': 2}, {'PRIX': 13, 'DEPART': 10, 'VOL': 'hushed-hairstylist-38', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 11, 'VOL': 'foolish-bike-13', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 12, 'VOL': 'hurt-cookout-25', 'DUREE': 6}, {'PRIX': 10, 'DEPART': 14, 'VOL': 'confused-fiddle-51', 'DUREE': 5}, {'PRIX': 28, 'DEPART': 15, 'VOL': 'gigantic-sheet-32', 'DUREE': 2}, {'PRIX': 12, 'DEPART': 15, 'VOL': 'silent-rattler-22', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 16, 'VOL': 'uninterested-seacoast-53', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 17, 'VOL': 'famous-stipend-17', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 19, 'VOL': 'horrible-beaver-60', 'DUREE': 5}, {'PRIX': 25, 'DEPART': 20, 'VOL': 'tall-guy-23', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'dangerous-cap-42', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 21, 'VOL': 'stupid-fishhook-65', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 22, 'VOL': 'helpful-shipyard-67', 'DUREE': 6}, {'PRIX': 22, 'DEPART': 24, 'VOL': 'lazy-buckle-85', 'DUREE': 5}, {'PRIX': 2, 'DEPART': 25, 'VOL': 'successful-cat-12', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 25, 'VOL': 'stupid-dinner-41', 'DUREE': 4}, {'PRIX': 2, 'DEPART': 26, 'VOL': 'motionless-student-82', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 27, 'VOL': 'short-life-17', 'DUREE': 6}, {'PRIX': 8, 'DEPART': 29, 'VOL': 'immense-rattle-89', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 30, 'VOL': 'square-sisterhood-91', 'DUREE': 2}]
    >>> optimize(commandes)
    {'path': ['wonderful-macrame-43', 'dark-chalkboard-14', 'outstanding-jackpot-29', 'gigantic-sheet-32', 'tall-guy-23', 'lazy-buckle-85', 'square-sisterhood-91'], 'gain': 127}
    """
    if len(commandes) == 0:
        return { 'gain': 0, 'path': list() }

    vols_map, prix_map, depart_map = mapper_commandes(commandes)
    departs = trier_departs(depart_map)
    precedents = {}

    while departs:
        depart = departs.popleft()
        vols = depart_map[depart]
        for vol in vols:
            commande = vols_map[vol]
            depart, fin = commande['DEPART'], commande['FIN']

            # suppression du vol de depart_map
            depart_map[depart].remove(vol)
            if not depart_map[depart]:
                del depart_map[depart]

            # recherche des commandes suivantes
            vols_apres = rechercher_vols_apres(departs, depart_map, fin)
            for vol_apres in vols_apres:
                if vol_apres in precedents:
                    somme_prix = prix_map[vol] + vols_map[vol_apres]['PRIX']
                    if somme_prix > prix_map[vol_apres]:
                        prix_map[vol_apres] = somme_prix
                        precedents[vol_apres] = vol
                    elif somme_prix == prix_map[vol_apres]:
                        # truc hyper bizarre
                        if vol[-2:] < precedents[vol_apres][-2:]:
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
    commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': i } for i in range(1, 10000)]
    import random
    random.shuffle(commandes)
    print optimize(commandes)
