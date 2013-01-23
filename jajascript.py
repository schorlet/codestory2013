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

def rechercher_vols_apres(vols_map, depart_map, fin):
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
                for vol in vols:
                    yield vol
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
    {'path': ['wonderful-macrame-43', 'voiceless-values-39', 'outstanding-jackpot-29', 'gigantic-sheet-32', 'tall-guy-23', 'lazy-buckle-85', 'square-sisterhood-91'], 'gain': 130}


    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 6, 'VOL': 'combative-railroad-26'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 7, 'VOL': 'distinct-scoreboard-20'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 5, 'VOL': 'bewildered-ruler-27'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 14, 'VOL': 'lonely-hash-44'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 5, 'VOL': 'old-fashioned-cheek-80'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 7, 'VOL': 'puny-hangman-14'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 8, 'VOL': 'powerful-windburn-77'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 7, 'VOL': 'excited-crow-64'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 18, 'VOL': 'attractive-sifter-65'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 28, 'VOL': 'hushed-smugness-54'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 9, 'VOL': 'curved-honeycomb-79'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 6, 'VOL': 'successful-sty-8'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'excited-pushcart-3'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 18, 'VOL': 'fragile-umbrella-58'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 12, 'VOL': 'courageous-cook-94'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 6, 'VOL': 'obedient-strictness-29'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 9, 'VOL': 'lovely-jug-62'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 7, 'VOL': 'soft-architect-17'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'famous-quiche-15'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 13, 'VOL': 'hungry-farmyard-60'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 15, 'VOL': 'difficult-ballpoint-88'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 7, 'VOL': 'cautious-sucker-70'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 3, 'VOL': 'outrageous-grail-50'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 13, 'VOL': 'whispering-bank-4'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 4, 'VOL': 'fragile-gourmet-29'}, {'DEPART': 25, 'DUREE': 4, 'PRIX': 14, 'VOL': 'better-monochrome-78'}, {'DEPART': 26, 'DUREE': 2, 'PRIX': 4, 'VOL': 'rich-blackboard-2'}, {'DEPART': 27, 'DUREE': 6, 'PRIX': 5, 'VOL': 'jealous-gunrunner-90'}, {'DEPART': 29, 'DUREE': 5, 'PRIX': 22, 'VOL': 'bad-thinner-80'}, {'DEPART': 30, 'DUREE': 2, 'PRIX': 18, 'VOL': 'homeless-flax-8'}, {'DEPART': 30, 'DUREE': 4, 'PRIX': 9, 'VOL': 'scrawny-coffin-96'}, {'DEPART': 31, 'DUREE': 2, 'PRIX': 10, 'VOL': 'clean-squeamishness-98'}, {'DEPART': 32, 'DUREE': 6, 'PRIX': 2, 'VOL': 'ancient-sunbonnet-53'}, {'DEPART': 34, 'DUREE': 5, 'PRIX': 14, 'VOL': 'cruel-picnic-77'}, {'DEPART': 35, 'DUREE': 2, 'PRIX': 10, 'VOL': 'loud-race-24'}]
    >>> optimize(commandes)
    {'path': ['distinct-scoreboard-20', 'lonely-hash-44', 'hushed-smugness-54', 'fragile-umbrella-58', 'difficult-ballpoint-88', 'better-monochrome-78', 'bad-thinner-80', 'cruel-picnic-77'], 'gain': 132}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 14, 'VOL': 'little-bucket-35'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 3, 'VOL': 'uptight-restoration-24'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 7, 'VOL': 'confused-web-9'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 9, 'VOL': 'busy-shore-53'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 21, 'VOL': 'faint-baker-5'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 8, 'VOL': 'smoggy-eyelash-78'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 7, 'VOL': 'agreeable-shelter-98'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 4, 'VOL': 'dangerous-peddle-12'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 5, 'VOL': 'powerful-creator-54'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 8, 'VOL': 'average-crumb-29'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 10, 'VOL': 'blue-power-47'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 10, 'VOL': 'modern-string-15'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 5, 'VOL': 'evil-tofu-27'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 13, 'VOL': 'late-wintergreen-67'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 23, 'VOL': 'witty-container-85'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 12, 'VOL': 'stupid-blackberry-48'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 1, 'VOL': 'defiant-bazooka-91'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 4, 'VOL': 'ill-rank-26'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'colossal-mandible-59'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 26, 'VOL': 'Early-sheriff-11'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 6, 'VOL': 'testy-tweet-41'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 8, 'VOL': 'adorable-sweatshirt-70'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 7, 'VOL': 'low-wardroom-29'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 15, 'VOL': 'enthusiastic-vigor-50'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 8, 'VOL': 'vivacious-butterfly-86'}]
    >>> optimize(commandes)
    {'path': ['little-bucket-35', 'faint-baker-5', 'blue-power-47', 'witty-container-85', 'Early-sheriff-11', 'enthusiastic-vigor-50'], 'gain': 109}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 7, 'VOL': 'horrible-menopause-42'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 9, 'VOL': 'naughty-cheesecloth-36'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 1, 'VOL': 'anxious-pedal-56'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 14, 'VOL': 'skinny-file-31'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 11, 'VOL': 'sleepy-schoolwork-96'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 6, 'VOL': 'hungry-theorem-97'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 5, 'VOL': 'excited-sign-35'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'mysterious-bonbon-64'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 8, 'VOL': 'crazy-saffron-82'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 15, 'VOL': 'friendly-socket-92'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 7, 'VOL': 'naughty-dartboard-94'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 2, 'VOL': 'silent-hotel-42'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 4, 'VOL': 'confused-shoestring-10'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 5, 'VOL': 'spotless-glycerine-1'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 3, 'VOL': 'zealous-musician-93'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 8, 'VOL': 'blushing-fingernail-50'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 5, 'VOL': 'careful-dolphin-69'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 4, 'VOL': 'angry-frown-64'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 7, 'VOL': 'determined-peekaboo-48'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 16, 'VOL': 'crooked-wrecker-57'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 12, 'VOL': 'soft-snapdragon-31'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 9, 'VOL': 'tiny-trackandfield-83'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 4, 'VOL': 'kind-cookout-88'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 10, 'VOL': 'unusual-rigor-89'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 13, 'VOL': 'clever-pumpkin-18'}]
    >>> optimize(commandes)
    {'path': ['naughty-cheesecloth-36', 'skinny-file-31', 'friendly-socket-92', 'blushing-fingernail-50', 'crooked-wrecker-57', 'clever-pumpkin-18'], 'gain': 75}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 15, 'VOL': 'crowded-dough-46'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 6, 'VOL': 'thankful-surface-13'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 3, 'VOL': 'curved-smallpox-20'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 22, 'VOL': 'funny-text-42'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 2, 'VOL': 'testy-second-14'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 9, 'VOL': 'drab-whiff-57'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 3, 'VOL': 'upset-bar-44'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 3, 'VOL': 'dark-warlord-74'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 11, 'VOL': 'frightened-toenail-76'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 1, 'VOL': 'nervous-species-77'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 13, 'VOL': 'harsh-pun-98'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 8, 'VOL': 'poised-scraper-31'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 4, 'VOL': 'clean-crater-70'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 6, 'VOL': 'blue-shoplifter-45'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 2, 'VOL': 'fast-greenhouse-13'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 7, 'VOL': 'cooperative-bifocal-57'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 5, 'VOL': 'fierce-monster-15'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 3, 'VOL': 'famous-rabblerouser-36'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'high-architect-70'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 28, 'VOL': 'filthy-hive-98'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 14, 'VOL': 'eager-strictness-49'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 8, 'VOL': 'thundering-sideline-71'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 3, 'VOL': 'nutty-terrier-42'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 10, 'VOL': 'tender-birdhouse-69'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 18, 'VOL': 'cruel-performance-4'}]
    >>> optimize(commandes)
    {'path': ['crowded-dough-46', 'funny-text-42', 'harsh-pun-98', 'cooperative-bifocal-57', 'filthy-hive-98', 'cruel-performance-4'], 'gain': 103}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 12, 'VOL': 'anxious-reggae-48'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 7, 'VOL': 'soft-lice-38'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 1, 'VOL': 'evil-sewer-71'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 11, 'VOL': 'long-plane-91'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 30, 'VOL': 'lively-trunk-35'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 15, 'VOL': 'crazy-peacock-53'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 7, 'VOL': 'disturbed-trapdoor-81'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'melodic-gentleman-75'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 16, 'VOL': 'faint-gasp-61'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 19, 'VOL': 'distinct-blob-61'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 6, 'VOL': 'hilarious-spectrum-49'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 9, 'VOL': 'clever-grinder-68'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'beautiful-stockbroker-39'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 5, 'VOL': 'flipped-out-ram-9'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 8, 'VOL': 'chubby-marmot-45'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 11, 'VOL': 'hollow-paprika-52'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 3, 'VOL': 'dangerous-chimp-9'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 7, 'VOL': 'magnificent-injury-43'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 8, 'VOL': 'energetic-magnesium-1'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 13, 'VOL': 'precious-cockroach-71'}]
    >>> optimize(commandes)
    {'path': ['anxious-reggae-48', 'lively-trunk-35', 'distinct-blob-61', 'hollow-paprika-52', 'precious-cockroach-71'], 'gain': 85}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 8, 'VOL': 'mysterious-trio-77'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 4, 'VOL': 'dead-evergreen-68'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 6, 'VOL': 'shy-racket-99'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 6, 'VOL': 'victorious-penalty-91'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 4, 'VOL': 'expensive-penguin-82'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 15, 'VOL': 'MISTY-REHAB-89'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 2, 'VOL': 'vast-flake-75'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'muddy-pawn-10'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 15, 'VOL': 'annoyed-spout-51'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 18, 'VOL': 'thankful-harvester-74'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 6, 'VOL': 'sore-watch-81'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 2, 'VOL': 'cooperative-trek-11'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'naughty-underdog-75'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 20, 'VOL': 'fair-womb-75'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 21, 'VOL': 'nice-pauper-66'}]
    >>> optimize(commandes)
    {'path': ['mysterious-trio-77', 'MISTY-REHAB-89', 'thankful-harvester-74', 'nice-pauper-66'], 'gain': 62}

    >>> commandes = [{'DEPART': 1, 'DUREE': 6, 'PRIX': 5, 'VOL': 'annoying-meteorologist-37'}, {'DEPART': 3, 'DUREE': 10, 'PRIX': 6, 'VOL': 'frightened-rank-51'}, {'DEPART': 2, 'DUREE': 5, 'PRIX': 6, 'VOL': 'terrible-babysitter-90'}, {'DEPART': 8, 'DUREE': 3, 'PRIX': 1, 'VOL': 'faithful-metropolis-59'}, {'DEPART': 7, 'DUREE': 5, 'PRIX': 14, 'VOL': 'rich-virtuoso-18'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 2, 'VOL': 'troubled-helicopter-43'}, {'DEPART': 2, 'DUREE': 9, 'PRIX': 12, 'VOL': 'precious-romance-42'}, {'DEPART': 0, 'DUREE': 9, 'PRIX': 4, 'VOL': 'low-gray-24'}, {'DEPART': 7, 'DUREE': 3, 'PRIX': 6, 'VOL': 'stupid-gnat-35'}, {'DEPART': 8, 'DUREE': 18, 'PRIX': 6, 'VOL': 'husky-mine-92'}]
    >>> optimize(commandes)
    {'path': ['terrible-babysitter-90', 'rich-virtuoso-18'], 'gain': 20}
    """
    if len(commandes) == 0 or len(commandes) > 10000:
        return { 'gain': 0, 'path': list() }

    vols_map, prix_map, depart_map = mapper_commandes(commandes)
    departs = deque(depart_map.keys())
    max_depart = departs[-1]
    precedents = {}

    while departs:
        depart = departs.popleft()
        vols = depart_map.pop(depart)
        for vol in vols:
            commande = vols_map[vol]
            depart, fin = commande['DEPART'], commande['FIN']
            if fin > max_depart:
                break
            # recherche des commandes suivantes
            vols_apres = rechercher_vols_apres(vols_map, depart_map, fin)
            for vol_apres in vols_apres:
                if vol_apres in precedents:
                    somme_prix = prix_map[vol] + vols_map[vol_apres]['PRIX']
                    if somme_prix > prix_map[vol_apres]:
                        prix_map[vol_apres] = somme_prix
                        precedents[vol_apres] = vol
                else:
                    prix_map[vol_apres] = prix_map[vol] + prix_map[vol_apres]
                    precedents[vol_apres] = vol

    vol_gain = max(prix_map.items(), key=itemgetter(1))
    resultat = { 'gain': vol_gain[1], 'path': list() }

    vol = vol_gain[0]
    resultat['path'].append(vol)

    while vol in precedents:
        vol = precedents[vol]
        resultat['path'].insert(0, vol)

    return resultat

if __name__ == '__main__':
    # commandes = [{ 'VOL': str(i), 'DEPART': i, 'DUREE': i, 'PRIX': i } for i in range(1, 10)]
    # import random
    # random.shuffle(commandes)
    # print optimize(commandes)
    # print {'path': ['1', '2', '4', '9', '19', '39', '78', '156', '312', '624', '1249', '2499', '4999', '9999'], 'gain': 19990}


    print optimize(commandes)
    print {'path': ['annoying-meteorologist-37', 'rich-virtuoso-18'], 'gain': 19}
