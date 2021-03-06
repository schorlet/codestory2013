#-*- coding:utf-8 -*-
"""
http://stackoverflow.com/questions/3243234/algorithm-to-find-the-maximum-sum-in-a-sequence-of-overlapping-intervals
"""

from operator import itemgetter
from bisect import bisect_left


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
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['puny-violin-24', 'annoying-missionary-38'], 'gain': 34}

    >>> commandes = [{'PRIX': 8, 'DEPART': 0, 'VOL': 'soft-penniless-43', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 1, 'VOL': 'teeny-tiny-walkietalkie-33', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 2, 'VOL': 'tall-tyranny-72', 'DUREE': 6}, {'PRIX': 16, 'DEPART': 4, 'VOL': 'excited-supervisor-94', 'DUREE': 5}, {'PRIX': 30, 'DEPART': 5, 'VOL': 'crowded-graveyard-80', 'DUREE': 2}, {'PRIX': 7, 'DEPART': 5, 'VOL': 'purring-comedienne-91', 'DUREE': 4}, {'PRIX': 10, 'DEPART': 6, 'VOL': 'black-groundhog-18', 'DUREE': 2}, {'PRIX': 4, 'DEPART': 7, 'VOL': 'doubtful-risk-19', 'DUREE': 6}, {'PRIX': 20, 'DEPART': 9, 'VOL': 'miniature-hamper-11', 'DUREE': 5}, {'PRIX': 1, 'DEPART': 10, 'VOL': 'fierce-sneaker-70', 'DUREE': 2}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['teeny-tiny-walkietalkie-33', 'crowded-graveyard-80', 'miniature-hamper-11'], 'gain': 59}

    >>> commandes = [{'PRIX': 14, 'DEPART': 0, 'VOL': 'grumpy-rubberstamp-77', 'DUREE': 4}, {'PRIX': 3, 'DEPART': 1, 'VOL': 'ancient-backstage-29', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 2, 'VOL': 'raspy-whey-63', 'DUREE': 6}, {'PRIX': 12, 'DEPART': 4, 'VOL': 'lazy-hill-19', 'DUREE': 5}, {'PRIX': 8, 'DEPART': 5, 'VOL': 'narrow-romance-18', 'DUREE': 2}, {'PRIX': 8, 'DEPART': 5, 'VOL': 'enchanting-stepmother-18', 'DUREE': 4}, {'PRIX': 4, 'DEPART': 6, 'VOL': 'hungry-revenge-29', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 7, 'VOL': 'testy-somebody-42', 'DUREE': 6}, {'PRIX': 7, 'DEPART': 9, 'VOL': 'scrawny-rudder-35', 'DUREE': 5}, {'PRIX': 30, 'DEPART': 10, 'VOL': 'old-fashioned-cardboard-81', 'DUREE': 2}, {'PRIX': 15, 'DEPART': 10, 'VOL': 'weary-harmonica-51', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 11, 'VOL': 'deafening-label-85', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 12, 'VOL': 'bloody-symbol-63', 'DUREE': 6}, {'PRIX': 19, 'DEPART': 14, 'VOL': 'squealing-rob-21', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 15, 'VOL': 'worried-violin-2', 'DUREE': 2}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['grumpy-rubberstamp-77', 'lazy-hill-19', 'old-fashioned-cardboard-81', 'squealing-rob-21'], 'gain': 75}

    >>> commandes = [{'PRIX': 9, 'DEPART': 0, 'VOL': 'fat-tycoon-6', 'DUREE': 4}, {'PRIX': 2, 'DEPART': 1, 'VOL': 'colorful-rhino-5', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 2, 'VOL': 'gigantic-rectangle-77', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 4, 'VOL': 'crazy-merrygoround-57', 'DUREE': 5}, {'PRIX': 28, 'DEPART': 5, 'VOL': 'clumsy-railing-40', 'DUREE': 2}, {'PRIX': 15, 'DEPART': 5, 'VOL': 'fat-graphic-94', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 6, 'VOL': 'fancy-dot-24', 'DUREE': 2}, {'PRIX': 4, 'DEPART': 7, 'VOL': 'high-pitched-zenith-87', 'DUREE': 6}, {'PRIX': 6, 'DEPART': 9, 'VOL': 'faint-calendar-81', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 10, 'VOL': 'muddy-commando-39', 'DUREE': 2}, {'PRIX': 12, 'DEPART': 10, 'VOL': 'moaning-comedienne-45', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 11, 'VOL': 'dangerous-bellows-42', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 12, 'VOL': 'brave-mustang-70', 'DUREE': 6}, {'PRIX': 5, 'DEPART': 14, 'VOL': 'hurt-net-43', 'DUREE': 5}, {'PRIX': 24, 'DEPART': 15, 'VOL': 'unusual-killer-75', 'DUREE': 2}, {'PRIX': 8, 'DEPART': 15, 'VOL': 'short-pastrami-79', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 16, 'VOL': 'graceful-windsurfing-55', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 17, 'VOL': 'adventurous-twinkle-28', 'DUREE': 6}, {'PRIX': 6, 'DEPART': 19, 'VOL': 'shrill-flax-62', 'DUREE': 5}, {'PRIX': 21, 'DEPART': 20, 'VOL': 'young-soprano-62', 'DUREE': 2}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['fat-tycoon-6', 'clumsy-railing-40', 'muddy-commando-39', 'unusual-killer-75', 'young-soprano-62'], 'gain': 95}

    >>> commandes = [{'PRIX': 6, 'DEPART': 0, 'VOL': 'expensive-zombie-63', 'DUREE': 4}, {'PRIX': 3, 'DEPART': 1, 'VOL': 'defiant-amphetamine-87', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 2, 'VOL': 'glamorous-waltz-67', 'DUREE': 6}, {'PRIX': 18, 'DEPART': 4, 'VOL': 'large-machinist-50', 'DUREE': 5}, {'PRIX': 14, 'DEPART': 5, 'VOL': 'black-polyester-26', 'DUREE': 2}, {'PRIX': 13, 'DEPART': 5, 'VOL': 'doubtful-detective-44', 'DUREE': 4}, {'PRIX': 7, 'DEPART': 6, 'VOL': 'breakable-saturn-23', 'DUREE': 2}, {'PRIX': 6, 'DEPART': 7, 'VOL': 'horrible-dime-6', 'DUREE': 6}, {'PRIX': 13, 'DEPART': 9, 'VOL': 'kind-welt-59', 'DUREE': 5}, {'PRIX': 10, 'DEPART': 10, 'VOL': 'rapid-verb-86', 'DUREE': 2}, {'PRIX': 11, 'DEPART': 10, 'VOL': 'grumpy-somewhere-64', 'DUREE': 4}, {'PRIX': 1, 'DEPART': 11, 'VOL': 'outstanding-dude-52', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 12, 'VOL': 'gleaming-sunbather-69', 'DUREE': 6}, {'PRIX': 21, 'DEPART': 14, 'VOL': 'confused-windowpane-85', 'DUREE': 5}, {'PRIX': 27, 'DEPART': 15, 'VOL': 'wild-bifocal-73', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 15, 'VOL': 'modern-handgun-67', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 16, 'VOL': 'poor-slogan-89', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 17, 'VOL': 'muddy-flowerpot-66', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 19, 'VOL': 'angry-grass-40', 'DUREE': 5}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'wrong-surgery-17', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'immense-spaniel-90', 'DUREE': 4}, {'PRIX': 10, 'DEPART': 21, 'VOL': 'panicky-steam-40', 'DUREE': 2}, {'PRIX': 2, 'DEPART': 22, 'VOL': 'brainy-ulcer-30', 'DUREE': 6}, {'PRIX': 18, 'DEPART': 24, 'VOL': 'fine-waiver-78', 'DUREE': 5}, {'PRIX': 22, 'DEPART': 25, 'VOL': 'mushy-newscaster-11', 'DUREE': 2}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['expensive-zombie-63', 'large-machinist-50', 'kind-welt-59', 'wild-bifocal-73', 'panicky-steam-40', 'mushy-newscaster-11'], 'gain': 96}
    >>> # {'path': ['expensive-zombie-63', 'large-machinist-50', 'kind-welt-59', 'wild-bifocal-73', 'wrong-surgery-17', 'mushy-newscaster-11'], 'gain': 96}

    >>> commandes = [{'PRIX': 10, 'DEPART': 0, 'VOL': 'wonderful-macrame-43', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 1, 'VOL': 'grotesque-sprawl-83', 'DUREE': 2}, {'PRIX': 5, 'DEPART': 2, 'VOL': 'strange-mousetrap-58', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 4, 'VOL': 'ashamed-linebacker-28', 'DUREE': 5}, {'PRIX': 7, 'DEPART': 5, 'VOL': 'long-airline-80', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 5, 'VOL': 'voiceless-values-39', 'DUREE': 4}, {'PRIX': 7, 'DEPART': 6, 'VOL': 'dark-chalkboard-14', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 7, 'VOL': 'clumsy-visor-47', 'DUREE': 6}, {'PRIX': 22, 'DEPART': 9, 'VOL': 'outstanding-jackpot-29', 'DUREE': 5}, {'PRIX': 19, 'DEPART': 10, 'VOL': 'elated-sideburns-49', 'DUREE': 2}, {'PRIX': 13, 'DEPART': 10, 'VOL': 'hushed-hairstylist-38', 'DUREE': 4}, {'PRIX': 9, 'DEPART': 11, 'VOL': 'foolish-bike-13', 'DUREE': 2}, {'PRIX': 1, 'DEPART': 12, 'VOL': 'hurt-cookout-25', 'DUREE': 6}, {'PRIX': 10, 'DEPART': 14, 'VOL': 'confused-fiddle-51', 'DUREE': 5}, {'PRIX': 28, 'DEPART': 15, 'VOL': 'gigantic-sheet-32', 'DUREE': 2}, {'PRIX': 12, 'DEPART': 15, 'VOL': 'silent-rattler-22', 'DUREE': 4}, {'PRIX': 5, 'DEPART': 16, 'VOL': 'uninterested-seacoast-53', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 17, 'VOL': 'famous-stipend-17', 'DUREE': 6}, {'PRIX': 4, 'DEPART': 19, 'VOL': 'horrible-beaver-60', 'DUREE': 5}, {'PRIX': 25, 'DEPART': 20, 'VOL': 'tall-guy-23', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 20, 'VOL': 'dangerous-cap-42', 'DUREE': 4}, {'PRIX': 6, 'DEPART': 21, 'VOL': 'stupid-fishhook-65', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 22, 'VOL': 'helpful-shipyard-67', 'DUREE': 6}, {'PRIX': 22, 'DEPART': 24, 'VOL': 'lazy-buckle-85', 'DUREE': 5}, {'PRIX': 2, 'DEPART': 25, 'VOL': 'successful-cat-12', 'DUREE': 2}, {'PRIX': 10, 'DEPART': 25, 'VOL': 'stupid-dinner-41', 'DUREE': 4}, {'PRIX': 2, 'DEPART': 26, 'VOL': 'motionless-student-82', 'DUREE': 2}, {'PRIX': 3, 'DEPART': 27, 'VOL': 'short-life-17', 'DUREE': 6}, {'PRIX': 8, 'DEPART': 29, 'VOL': 'immense-rattle-89', 'DUREE': 5}, {'PRIX': 13, 'DEPART': 30, 'VOL': 'square-sisterhood-91', 'DUREE': 2}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['wonderful-macrame-43', 'voiceless-values-39', 'outstanding-jackpot-29', 'gigantic-sheet-32', 'tall-guy-23', 'lazy-buckle-85', 'square-sisterhood-91'], 'gain': 130}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 6, 'VOL': 'combative-railroad-26'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 7, 'VOL': 'distinct-scoreboard-20'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 5, 'VOL': 'bewildered-ruler-27'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 14, 'VOL': 'lonely-hash-44'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 5, 'VOL': 'old-fashioned-cheek-80'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 7, 'VOL': 'puny-hangman-14'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 8, 'VOL': 'powerful-windburn-77'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 7, 'VOL': 'excited-crow-64'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 18, 'VOL': 'attractive-sifter-65'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 28, 'VOL': 'hushed-smugness-54'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 9, 'VOL': 'curved-honeycomb-79'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 6, 'VOL': 'successful-sty-8'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'excited-pushcart-3'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 18, 'VOL': 'fragile-umbrella-58'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 12, 'VOL': 'courageous-cook-94'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 6, 'VOL': 'obedient-strictness-29'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 9, 'VOL': 'lovely-jug-62'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 7, 'VOL': 'soft-architect-17'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'famous-quiche-15'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 13, 'VOL': 'hungry-farmyard-60'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 15, 'VOL': 'difficult-ballpoint-88'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 7, 'VOL': 'cautious-sucker-70'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 3, 'VOL': 'outrageous-grail-50'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 13, 'VOL': 'whispering-bank-4'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 4, 'VOL': 'fragile-gourmet-29'}, {'DEPART': 25, 'DUREE': 4, 'PRIX': 14, 'VOL': 'better-monochrome-78'}, {'DEPART': 26, 'DUREE': 2, 'PRIX': 4, 'VOL': 'rich-blackboard-2'}, {'DEPART': 27, 'DUREE': 6, 'PRIX': 5, 'VOL': 'jealous-gunrunner-90'}, {'DEPART': 29, 'DUREE': 5, 'PRIX': 22, 'VOL': 'bad-thinner-80'}, {'DEPART': 30, 'DUREE': 2, 'PRIX': 18, 'VOL': 'homeless-flax-8'}, {'DEPART': 30, 'DUREE': 4, 'PRIX': 9, 'VOL': 'scrawny-coffin-96'}, {'DEPART': 31, 'DUREE': 2, 'PRIX': 10, 'VOL': 'clean-squeamishness-98'}, {'DEPART': 32, 'DUREE': 6, 'PRIX': 2, 'VOL': 'ancient-sunbonnet-53'}, {'DEPART': 34, 'DUREE': 5, 'PRIX': 14, 'VOL': 'cruel-picnic-77'}, {'DEPART': 35, 'DUREE': 2, 'PRIX': 10, 'VOL': 'loud-race-24'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['distinct-scoreboard-20', 'lonely-hash-44', 'hushed-smugness-54', 'fragile-umbrella-58', 'difficult-ballpoint-88', 'better-monochrome-78', 'bad-thinner-80', 'cruel-picnic-77'], 'gain': 132}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 14, 'VOL': 'little-bucket-35'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 3, 'VOL': 'uptight-restoration-24'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 7, 'VOL': 'confused-web-9'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 9, 'VOL': 'busy-shore-53'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 21, 'VOL': 'faint-baker-5'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 8, 'VOL': 'smoggy-eyelash-78'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 7, 'VOL': 'agreeable-shelter-98'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 4, 'VOL': 'dangerous-peddle-12'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 5, 'VOL': 'powerful-creator-54'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 8, 'VOL': 'average-crumb-29'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 10, 'VOL': 'blue-power-47'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 10, 'VOL': 'modern-string-15'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 5, 'VOL': 'evil-tofu-27'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 13, 'VOL': 'late-wintergreen-67'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 23, 'VOL': 'witty-container-85'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 12, 'VOL': 'stupid-blackberry-48'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 1, 'VOL': 'defiant-bazooka-91'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 4, 'VOL': 'ill-rank-26'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'colossal-mandible-59'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 26, 'VOL': 'Early-sheriff-11'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 6, 'VOL': 'testy-tweet-41'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 8, 'VOL': 'adorable-sweatshirt-70'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 7, 'VOL': 'low-wardroom-29'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 15, 'VOL': 'enthusiastic-vigor-50'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 8, 'VOL': 'vivacious-butterfly-86'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['little-bucket-35', 'faint-baker-5', 'modern-string-15', 'witty-container-85', 'Early-sheriff-11', 'enthusiastic-vigor-50'], 'gain': 109}
    >>> # {'path': ['little-bucket-35', 'faint-baker-5', 'blue-power-47', 'witty-container-85', 'Early-sheriff-11', 'enthusiastic-vigor-50'], 'gain': 109}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 7, 'VOL': 'horrible-menopause-42'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 9, 'VOL': 'naughty-cheesecloth-36'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 1, 'VOL': 'anxious-pedal-56'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 14, 'VOL': 'skinny-file-31'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 11, 'VOL': 'sleepy-schoolwork-96'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 6, 'VOL': 'hungry-theorem-97'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 5, 'VOL': 'excited-sign-35'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'mysterious-bonbon-64'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 8, 'VOL': 'crazy-saffron-82'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 15, 'VOL': 'friendly-socket-92'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 7, 'VOL': 'naughty-dartboard-94'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 2, 'VOL': 'silent-hotel-42'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 4, 'VOL': 'confused-shoestring-10'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 5, 'VOL': 'spotless-glycerine-1'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 3, 'VOL': 'zealous-musician-93'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 8, 'VOL': 'blushing-fingernail-50'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 5, 'VOL': 'careful-dolphin-69'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 4, 'VOL': 'angry-frown-64'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 7, 'VOL': 'determined-peekaboo-48'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 16, 'VOL': 'crooked-wrecker-57'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 12, 'VOL': 'soft-snapdragon-31'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 9, 'VOL': 'tiny-trackandfield-83'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 4, 'VOL': 'kind-cookout-88'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 10, 'VOL': 'unusual-rigor-89'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 13, 'VOL': 'clever-pumpkin-18'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['naughty-cheesecloth-36', 'skinny-file-31', 'friendly-socket-92', 'blushing-fingernail-50', 'crooked-wrecker-57', 'clever-pumpkin-18'], 'gain': 75}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 15, 'VOL': 'crowded-dough-46'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 6, 'VOL': 'thankful-surface-13'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 3, 'VOL': 'curved-smallpox-20'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 22, 'VOL': 'funny-text-42'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 2, 'VOL': 'testy-second-14'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 9, 'VOL': 'drab-whiff-57'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 3, 'VOL': 'upset-bar-44'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 3, 'VOL': 'dark-warlord-74'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 11, 'VOL': 'frightened-toenail-76'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 1, 'VOL': 'nervous-species-77'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 13, 'VOL': 'harsh-pun-98'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 8, 'VOL': 'poised-scraper-31'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 4, 'VOL': 'clean-crater-70'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 6, 'VOL': 'blue-shoplifter-45'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 2, 'VOL': 'fast-greenhouse-13'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 7, 'VOL': 'cooperative-bifocal-57'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 5, 'VOL': 'fierce-monster-15'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 3, 'VOL': 'famous-rabblerouser-36'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 13, 'VOL': 'high-architect-70'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 28, 'VOL': 'filthy-hive-98'}, {'DEPART': 20, 'DUREE': 4, 'PRIX': 14, 'VOL': 'eager-strictness-49'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 8, 'VOL': 'thundering-sideline-71'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 3, 'VOL': 'nutty-terrier-42'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 10, 'VOL': 'tender-birdhouse-69'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 18, 'VOL': 'cruel-performance-4'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['crowded-dough-46', 'funny-text-42', 'harsh-pun-98', 'cooperative-bifocal-57', 'filthy-hive-98', 'cruel-performance-4'], 'gain': 103}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 12, 'VOL': 'anxious-reggae-48'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 7, 'VOL': 'soft-lice-38'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 1, 'VOL': 'evil-sewer-71'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 11, 'VOL': 'long-plane-91'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 30, 'VOL': 'lively-trunk-35'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 15, 'VOL': 'crazy-peacock-53'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 7, 'VOL': 'disturbed-trapdoor-81'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'melodic-gentleman-75'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 16, 'VOL': 'faint-gasp-61'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 19, 'VOL': 'distinct-blob-61'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 6, 'VOL': 'hilarious-spectrum-49'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 9, 'VOL': 'clever-grinder-68'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'beautiful-stockbroker-39'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 5, 'VOL': 'flipped-out-ram-9'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 8, 'VOL': 'chubby-marmot-45'}, {'DEPART': 15, 'DUREE': 4, 'PRIX': 11, 'VOL': 'hollow-paprika-52'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 3, 'VOL': 'dangerous-chimp-9'}, {'DEPART': 17, 'DUREE': 6, 'PRIX': 7, 'VOL': 'magnificent-injury-43'}, {'DEPART': 19, 'DUREE': 5, 'PRIX': 8, 'VOL': 'energetic-magnesium-1'}, {'DEPART': 20, 'DUREE': 2, 'PRIX': 13, 'VOL': 'precious-cockroach-71'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['anxious-reggae-48', 'lively-trunk-35', 'distinct-blob-61', 'hollow-paprika-52', 'precious-cockroach-71'], 'gain': 85}

    >>> commandes = [{'DEPART': 0, 'DUREE': 4, 'PRIX': 8, 'VOL': 'mysterious-trio-77'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 4, 'VOL': 'dead-evergreen-68'}, {'DEPART': 2, 'DUREE': 6, 'PRIX': 6, 'VOL': 'shy-racket-99'}, {'DEPART': 4, 'DUREE': 5, 'PRIX': 6, 'VOL': 'victorious-penalty-91'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 4, 'VOL': 'expensive-penguin-82'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 15, 'VOL': 'MISTY-REHAB-89'}, {'DEPART': 6, 'DUREE': 2, 'PRIX': 2, 'VOL': 'vast-flake-75'}, {'DEPART': 7, 'DUREE': 6, 'PRIX': 1, 'VOL': 'muddy-pawn-10'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 15, 'VOL': 'annoyed-spout-51'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 18, 'VOL': 'thankful-harvester-74'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 6, 'VOL': 'sore-watch-81'}, {'DEPART': 11, 'DUREE': 2, 'PRIX': 2, 'VOL': 'cooperative-trek-11'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'naughty-underdog-75'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 20, 'VOL': 'fair-womb-75'}, {'DEPART': 15, 'DUREE': 2, 'PRIX': 21, 'VOL': 'nice-pauper-66'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['mysterious-trio-77', 'MISTY-REHAB-89', 'thankful-harvester-74', 'nice-pauper-66'], 'gain': 62}

    >>> commandes = [{'DEPART': 1, 'DUREE': 6, 'PRIX': 5, 'VOL': 'annoying-meteorologist-37'}, {'DEPART': 3, 'DUREE': 10, 'PRIX': 6, 'VOL': 'frightened-rank-51'}, {'DEPART': 2, 'DUREE': 5, 'PRIX': 6, 'VOL': 'terrible-babysitter-90'}, {'DEPART': 8, 'DUREE': 3, 'PRIX': 1, 'VOL': 'faithful-metropolis-59'}, {'DEPART': 7, 'DUREE': 5, 'PRIX': 14, 'VOL': 'rich-virtuoso-18'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 2, 'VOL': 'troubled-helicopter-43'}, {'DEPART': 2, 'DUREE': 9, 'PRIX': 12, 'VOL': 'precious-romance-42'}, {'DEPART': 0, 'DUREE': 9, 'PRIX': 4, 'VOL': 'low-gray-24'}, {'DEPART': 7, 'DUREE': 3, 'PRIX': 6, 'VOL': 'stupid-gnat-35'}, {'DEPART': 8, 'DUREE': 18, 'PRIX': 6, 'VOL': 'husky-mine-92'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['terrible-babysitter-90', 'rich-virtuoso-18'], 'gain': 20}

    >>> commandes = [{'DEPART': 3, 'DUREE': 7, 'PRIX': 22, 'VOL': 'eager-union-14'}, {'DEPART': 4, 'DUREE': 8, 'PRIX': 11, 'VOL': 'quiet-pizzeria-2'}, {'DEPART': 4, 'DUREE': 8, 'PRIX': 6, 'VOL': 'clever-sandblaster-59'}, {'DEPART': 3, 'DUREE': 1, 'PRIX': 14, 'VOL': 'awful-mockingbird-28'}, {'DEPART': 4, 'DUREE': 8, 'PRIX': 6, 'VOL': 'miniature-wastebasket-37'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['awful-mockingbird-28', 'quiet-pizzeria-2'], 'gain': 25}

    >>> commandes = [{'DEPART': 4, 'DUREE': 3, 'PRIX': 8, 'VOL': 'crazy-puzzle-25'}, {'DEPART': 4, 'DUREE': 7, 'PRIX': 7, 'VOL': 'splendid-windshield-95'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 4, 'VOL': 'wide-eyed-mice-57'}, {'DEPART': 1, 'DUREE': 9, 'PRIX': 12, 'VOL': 'puny-twilight-76'}, {'DEPART': 1, 'DUREE': 20, 'PRIX': 6, 'VOL': 'miniature-tourism-82'}, {'DEPART': 8, 'DUREE': 3, 'PRIX': 23, 'VOL': 'combative-tiling-58'}, {'DEPART': 5, 'DUREE': 8, 'PRIX': 17, 'VOL': 'poor-albacore-47'}, {'DEPART': 9, 'DUREE': 9, 'PRIX': 3, 'VOL': 'fat-spy-63'}, {'DEPART': 5, 'DUREE': 2, 'PRIX': 13, 'VOL': 'foolish-thirst-41'}, {'DEPART': 6, 'DUREE': 11, 'PRIX': 3, 'VOL': 'gleaming-narrator-63'}, {'DEPART': 14, 'DUREE': 5, 'PRIX': 20, 'VOL': 'sore-tannery-39'}, {'DEPART': 11, 'DUREE': 10, 'PRIX': 4, 'VOL': 'faint-mush-77'}, {'DEPART': 13, 'DUREE': 6, 'PRIX': 3, 'VOL': 'tall-bookcase-37'}, {'DEPART': 13, 'DUREE': 4, 'PRIX': 6, 'VOL': 'zealous-nursery-87'}, {'DEPART': 13, 'DUREE': 15, 'PRIX': 2, 'VOL': 'soft-mariner-51'}, {'DEPART': 15, 'DUREE': 1, 'PRIX': 4, 'VOL': 'hilarious-herd-14'}, {'DEPART': 19, 'DUREE': 9, 'PRIX': 15, 'VOL': 'helpless-quintet-80'}, {'DEPART': 18, 'DUREE': 10, 'PRIX': 10, 'VOL': 'doubtful-rivalry-68'}, {'DEPART': 19, 'DUREE': 6, 'PRIX': 8, 'VOL': 'powerful-cornmeal-61'}, {'DEPART': 18, 'DUREE': 20, 'PRIX': 6, 'VOL': 'hurt-crap-55'}, {'DEPART': 23, 'DUREE': 3, 'PRIX': 28, 'VOL': 'attractive-serf-19'}, {'DEPART': 20, 'DUREE': 9, 'PRIX': 4, 'VOL': 'homeless-poplar-58'}, {'DEPART': 23, 'DUREE': 2, 'PRIX': 5, 'VOL': 'outstanding-slope-98'}, {'DEPART': 23, 'DUREE': 9, 'PRIX': 8, 'VOL': 'successful-food-6'}, {'DEPART': 23, 'DUREE': 5, 'PRIX': 6, 'VOL': 'important-brunette-88'}, {'DEPART': 29, 'DUREE': 10, 'PRIX': 14, 'VOL': 'homeless-warhead-59'}, {'DEPART': 28, 'DUREE': 3, 'PRIX': 9, 'VOL': 'large-shopkeeper-55'}, {'DEPART': 27, 'DUREE': 1, 'PRIX': 10, 'VOL': 'average-puffin-34'}, {'DEPART': 26, 'DUREE': 6, 'PRIX': 10, 'VOL': 'bewildered-marine-8'}, {'DEPART': 28, 'DUREE': 3, 'PRIX': 1, 'VOL': 'lovely-schoolwork-21'}, {'DEPART': 31, 'DUREE': 3, 'PRIX': 24, 'VOL': 'determined-patio-11'}, {'DEPART': 32, 'DUREE': 10, 'PRIX': 13, 'VOL': 'aggressive-shredder-37'}, {'DEPART': 33, 'DUREE': 1, 'PRIX': 4, 'VOL': 'real-den-51'}, {'DEPART': 33, 'DUREE': 1, 'PRIX': 8, 'VOL': 'brief-evergreen-50'}, {'DEPART': 34, 'DUREE': 18, 'PRIX': 6, 'VOL': 'grotesque-babe-89'}, {'DEPART': 36, 'DUREE': 9, 'PRIX': 9, 'VOL': 'scrawny-picnic-52'}, {'DEPART': 35, 'DUREE': 2, 'PRIX': 20, 'VOL': 'cautious-rack-94'}, {'DEPART': 36, 'DUREE': 6, 'PRIX': 7, 'VOL': 'zealous-cherry-13'}, {'DEPART': 39, 'DUREE': 7, 'PRIX': 10, 'VOL': 'innocent-script-25'}, {'DEPART': 35, 'DUREE': 7, 'PRIX': 1, 'VOL': 'wide-eyed-alcohol-54'}, {'DEPART': 40, 'DUREE': 3, 'PRIX': 23, 'VOL': 'dizzy-rancher-93'}, {'DEPART': 44, 'DUREE': 9, 'PRIX': 14, 'VOL': 'elegant-keypunch-69'}, {'DEPART': 40, 'DUREE': 2, 'PRIX': 6, 'VOL': 'blue-mimosa-58'}, {'DEPART': 42, 'DUREE': 4, 'PRIX': 13, 'VOL': 'tame-crossbar-57'}, {'DEPART': 43, 'DUREE': 5, 'PRIX': 6, 'VOL': 'lively-backup-34'}, {'DEPART': 48, 'DUREE': 7, 'PRIX': 21, 'VOL': 'time-ringworm-5'}, {'DEPART': 48, 'DUREE': 1, 'PRIX': 20, 'VOL': 'obedient-video-40'}, {'DEPART': 49, 'DUREE': 3, 'PRIX': 9, 'VOL': 'dark-aircraft-32'}, {'DEPART': 49, 'DUREE': 5, 'PRIX': 7, 'VOL': 'important-accelerator-83'}, {'DEPART': 48, 'DUREE': 19, 'PRIX': 2, 'VOL': 'resonant-tinsel-67'}, {'DEPART': 50, 'DUREE': 7, 'PRIX': 3, 'VOL': 'funny-wife-20'}, {'DEPART': 52, 'DUREE': 9, 'PRIX': 9, 'VOL': 'mysterious-newsprint-96'}, {'DEPART': 50, 'DUREE': 10, 'PRIX': 3, 'VOL': 'quiet-jaw-30'}, {'DEPART': 54, 'DUREE': 10, 'PRIX': 12, 'VOL': 'disturbed-tether-99'}, {'DEPART': 50, 'DUREE': 15, 'PRIX': 3, 'VOL': 'alive-hedgehog-26'}, {'DEPART': 55, 'DUREE': 10, 'PRIX': 10, 'VOL': 'beautiful-venus-50'}, {'DEPART': 55, 'DUREE': 6, 'PRIX': 23, 'VOL': 'hurt-symbolism-29'}, {'DEPART': 57, 'DUREE': 10, 'PRIX': 5, 'VOL': 'relieved-quiz-70'}, {'DEPART': 56, 'DUREE': 7, 'PRIX': 9, 'VOL': 'mute-target-46'}, {'DEPART': 56, 'DUREE': 7, 'PRIX': 5, 'VOL': 'miniature-xenophobia-49'}, {'DEPART': 62, 'DUREE': 2, 'PRIX': 17, 'VOL': 'high-grater-60'}, {'DEPART': 63, 'DUREE': 4, 'PRIX': 19, 'VOL': 'disgusted-raider-5'}, {'DEPART': 64, 'DUREE': 10, 'PRIX': 2, 'VOL': 'inexpensive-sparrow-75'}, {'DEPART': 60, 'DUREE': 6, 'PRIX': 6, 'VOL': 'vivacious-slaughterhouse-82'}, {'DEPART': 64, 'DUREE': 7, 'PRIX': 4, 'VOL': 'soft-fungus-89'}, {'DEPART': 67, 'DUREE': 2, 'PRIX': 22, 'VOL': 'sleepy-goatee-88'}, {'DEPART': 69, 'DUREE': 6, 'PRIX': 15, 'VOL': 'light-nitpicker-13'}, {'DEPART': 66, 'DUREE': 3, 'PRIX': 6, 'VOL': 'old-fashioned-porter-31'}, {'DEPART': 66, 'DUREE': 7, 'PRIX': 6, 'VOL': 'mammoth-rap-81'}, {'DEPART': 65, 'DUREE': 14, 'PRIX': 5, 'VOL': 'excited-pedicure-52'}, {'DEPART': 72, 'DUREE': 9, 'PRIX': 6, 'VOL': 'bad-ragamuffin-18'}, {'DEPART': 73, 'DUREE': 7, 'PRIX': 14, 'VOL': 'dizzy-feather-88'}, {'DEPART': 74, 'DUREE': 6, 'PRIX': 3, 'VOL': 'ancient-yachtsman-6'}, {'DEPART': 73, 'DUREE': 8, 'PRIX': 13, 'VOL': 'ugly-mosquito-74'}, {'DEPART': 73, 'DUREE': 9, 'PRIX': 1, 'VOL': 'tense-across-36'}, {'DEPART': 79, 'DUREE': 7, 'PRIX': 25, 'VOL': 'courageous-sleepwalker-56'}, {'DEPART': 79, 'DUREE': 3, 'PRIX': 17, 'VOL': 'dull-sociology-23'}, {'DEPART': 79, 'DUREE': 7, 'PRIX': 5, 'VOL': 'fragile-van-78'}, {'DEPART': 75, 'DUREE': 7, 'PRIX': 14, 'VOL': 'repulsive-hockey-61'}, {'DEPART': 76, 'DUREE': 7, 'PRIX': 1, 'VOL': 'time-tomcat-3'}, {'DEPART': 80, 'DUREE': 10, 'PRIX': 12, 'VOL': 'vivacious-question-4'}, {'DEPART': 83, 'DUREE': 1, 'PRIX': 22, 'VOL': 'short-gap-57'}, {'DEPART': 81, 'DUREE': 7, 'PRIX': 10, 'VOL': 'victorious-row-52'}, {'DEPART': 84, 'DUREE': 5, 'PRIX': 8, 'VOL': 'colorful-striker-78'}, {'DEPART': 84, 'DUREE': 19, 'PRIX': 6, 'VOL': 'uninterested-traveller-65'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['wide-eyed-mice-57', 'foolish-thirst-41', 'combative-tiling-58', 'sore-tannery-39', 'attractive-serf-19', 'average-puffin-34', 'large-shopkeeper-55', 'determined-patio-11', 'cautious-rack-94', 'dizzy-rancher-93', 'lively-backup-34', 'obedient-video-40', 'dark-aircraft-32', 'hurt-symbolism-29', 'disgusted-raider-5', 'sleepy-goatee-88', 'light-nitpicker-13', 'dull-sociology-23', 'short-gap-57', 'colorful-striker-78'], 'gain': 335}

    >>> commandes = [{'DEPART': 1, 'DUREE': 8, 'PRIX': 4, 'VOL': 'delightful-ramp-80'}, {'DEPART': 4, 'DUREE': 2, 'PRIX': 11, 'VOL': 'average-knitter-8'}, {'DEPART': 3, 'DUREE': 5, 'PRIX': 4, 'VOL': 'colorful-brunette-27'}, {'DEPART': 4, 'DUREE': 3, 'PRIX': 12, 'VOL': 'fast-pound-41'}, {'DEPART': 3, 'DUREE': 1, 'PRIX': 6, 'VOL': 'young-lyrics-88'}, {'DEPART': 6, 'DUREE': 6, 'PRIX': 22, 'VOL': 'modern-raindrop-88'}, {'DEPART': 8, 'DUREE': 4, 'PRIX': 14, 'VOL': 'filthy-zucchini-49'}, {'DEPART': 9, 'DUREE': 5, 'PRIX': 9, 'VOL': 'enchanting-teacup-18'}, {'DEPART': 6, 'DUREE': 4, 'PRIX': 14, 'VOL': 'colossal-starboard-93'}, {'DEPART': 7, 'DUREE': 11, 'PRIX': 4, 'VOL': 'beautiful-urination-33'}, {'DEPART': 10, 'DUREE': 8, 'PRIX': 1, 'VOL': 'enchanting-janitor-35'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 6, 'VOL': 'brave-sleepyhead-62'}, {'DEPART': 10, 'DUREE': 7, 'PRIX': 3, 'VOL': 'little-gravel-1'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 11, 'VOL': 'enchanting-firefly-46'}, {'DEPART': 13, 'DUREE': 10, 'PRIX': 4, 'VOL': 'witty-nature-64'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['young-lyrics-88', 'average-knitter-8', 'colossal-starboard-93', 'enchanting-firefly-46', 'witty-nature-64'], 'gain': 46}

    >>> commandes = [{'DEPART': 3, 'DUREE': 3, 'PRIX': 18, 'VOL': 'excited-banker-30'}, {'DEPART': 1, 'DUREE': 10, 'PRIX': 12, 'VOL': 'fantastic-liquor-24'}, {'DEPART': 2, 'DUREE': 9, 'PRIX': 1, 'VOL': 'easy-salon-3'}, {'DEPART': 0, 'DUREE': 2, 'PRIX': 12, 'VOL': 'massive-check-11'}, {'DEPART': 2, 'DUREE': 5, 'PRIX': 3, 'VOL': 'drab-landlord-86'}, {'DEPART': 5, 'DUREE': 5, 'PRIX': 2, 'VOL': 'friendly-cylinder-78'}, {'DEPART': 7, 'DUREE': 9, 'PRIX': 22, 'VOL': 'amused-zoo-82'}, {'DEPART': 9, 'DUREE': 10, 'PRIX': 10, 'VOL': 'loud-significant-92'}, {'DEPART': 9, 'DUREE': 7, 'PRIX': 9, 'VOL': 'different-tangent-32'}, {'DEPART': 9, 'DUREE': 4, 'PRIX': 5, 'VOL': 'annoying-steak-74'}, {'DEPART': 11, 'DUREE': 1, 'PRIX': 15, 'VOL': 'combative-player-77'}, {'DEPART': 12, 'DUREE': 10, 'PRIX': 6, 'VOL': 'friendly-quicksand-30'}, {'DEPART': 14, 'DUREE': 3, 'PRIX': 3, 'VOL': 'magnificent-quote-76'}, {'DEPART': 13, 'DUREE': 1, 'PRIX': 14, 'VOL': 'crazy-stockroom-70'}, {'DEPART': 12, 'DUREE': 1, 'PRIX': 7, 'VOL': 'cautious-hyacinth-32'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['massive-check-11', 'excited-banker-30', 'combative-player-77', 'cautious-hyacinth-32', 'crazy-stockroom-70', 'magnificent-quote-76'], 'gain': 69}

    >>> commandes = [{'DEPART': 1, 'DUREE': 7, 'PRIX': 17, 'VOL': 'encouraging-dishcloth-63'}, {'DEPART': 4, 'DUREE': 2, 'PRIX': 17, 'VOL': 'gleaming-business-21'}, {'DEPART': 4, 'DUREE': 8, 'PRIX': 9, 'VOL': 'glamorous-coin-86'}, {'DEPART': 1, 'DUREE': 2, 'PRIX': 6, 'VOL': 'mammoth-liver-53'}, {'DEPART': 3, 'DUREE': 14, 'PRIX': 2, 'VOL': 'bright-vestibule-52'}, {'DEPART': 9, 'DUREE': 8, 'PRIX': 21, 'VOL': 'flipped-out-war-57'}, {'DEPART': 9, 'DUREE': 10, 'PRIX': 14, 'VOL': 'curious-stadium-44'}, {'DEPART': 7, 'DUREE': 4, 'PRIX': 6, 'VOL': 'happy-loiterer-11'}, {'DEPART': 9, 'DUREE': 7, 'PRIX': 11, 'VOL': 'annoying-sausage-14'}, {'DEPART': 9, 'DUREE': 16, 'PRIX': 1, 'VOL': 'happy-battalion-95'}, {'DEPART': 13, 'DUREE': 7, 'PRIX': 10, 'VOL': 'graceful-starlight-76'}, {'DEPART': 13, 'DUREE': 6, 'PRIX': 5, 'VOL': 'rich-statue-40'}, {'DEPART': 11, 'DUREE': 6, 'PRIX': 7, 'VOL': 'panicky-banknote-56'}, {'DEPART': 10, 'DUREE': 4, 'PRIX': 15, 'VOL': 'jolly-plan-96'}, {'DEPART': 11, 'DUREE': 20, 'PRIX': 5, 'VOL': 'teeny-motor-8'}, {'DEPART': 18, 'DUREE': 3, 'PRIX': 4, 'VOL': 'repulsive-ruby-78'}, {'DEPART': 16, 'DUREE': 8, 'PRIX': 5, 'VOL': 'shy-grits-38'}, {'DEPART': 18, 'DUREE': 1, 'PRIX': 4, 'VOL': 'screeching-mirage-27'}, {'DEPART': 17, 'DUREE': 9, 'PRIX': 9, 'VOL': 'elegant-slumlord-16'}, {'DEPART': 18, 'DUREE': 12, 'PRIX': 3, 'VOL': 'dangerous-firefighter-38'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 9, 'VOL': 'average-wineglass-39'}, {'DEPART': 24, 'DUREE': 3, 'PRIX': 10, 'VOL': 'fantastic-thief-62'}, {'DEPART': 24, 'DUREE': 7, 'PRIX': 4, 'VOL': 'colorful-locust-46'}, {'DEPART': 21, 'DUREE': 2, 'PRIX': 9, 'VOL': 'mute-tail-93'}, {'DEPART': 24, 'DUREE': 1, 'PRIX': 1, 'VOL': 'spotless-marriage-94'}, {'DEPART': 29, 'DUREE': 9, 'PRIX': 23, 'VOL': 'thankful-polygamy-90'}, {'DEPART': 27, 'DUREE': 9, 'PRIX': 16, 'VOL': 'witty-socket-7'}, {'DEPART': 28, 'DUREE': 8, 'PRIX': 4, 'VOL': 'excited-treasury-18'}, {'DEPART': 26, 'DUREE': 6, 'PRIX': 15, 'VOL': 'horrible-termite-43'}, {'DEPART': 25, 'DUREE': 19, 'PRIX': 2, 'VOL': 'puny-martian-42'}, {'DEPART': 32, 'DUREE': 2, 'PRIX': 29, 'VOL': 'unsightly-smog-80'}, {'DEPART': 34, 'DUREE': 7, 'PRIX': 6, 'VOL': 'moaning-back-48'}, {'DEPART': 33, 'DUREE': 6, 'PRIX': 10, 'VOL': 'powerful-slipper-39'}, {'DEPART': 30, 'DUREE': 10, 'PRIX': 6, 'VOL': 'steep-cowhide-51'}, {'DEPART': 34, 'DUREE': 20, 'PRIX': 6, 'VOL': 'expensive-judo-47'}, {'DEPART': 35, 'DUREE': 3, 'PRIX': 8, 'VOL': 'melodic-barracuda-85'}, {'DEPART': 35, 'DUREE': 1, 'PRIX': 5, 'VOL': 'ugly-statistic-39'}, {'DEPART': 35, 'DUREE': 4, 'PRIX': 3, 'VOL': 'stormy-drugstore-65'}, {'DEPART': 37, 'DUREE': 7, 'PRIX': 14, 'VOL': 'healthy-goalpost-69'}, {'DEPART': 36, 'DUREE': 12, 'PRIX': 2, 'VOL': 'victorious-anger-47'}]
    >>> # random.shuffle(commandes)
    >>> # le shuffle pète tout, car plusieurs combinaisons possibles pour le même gain
    >>> optimize(commandes)
    {'path': ['mammoth-liver-53', 'gleaming-business-21', 'flipped-out-war-57', 'screeching-mirage-27', 'mute-tail-93', 'spotless-marriage-94', 'horrible-termite-43', 'unsightly-smog-80', 'ugly-statistic-39', 'healthy-goalpost-69'], 'gain': 121}

    >>> commandes = [{'DEPART': 1, 'DUREE': 8, 'PRIX': 21, 'VOL': 'deep-marrow-92'}, {'DEPART': 3, 'DUREE': 1, 'PRIX': 14, 'VOL': 'disgusted-stepson-62'}, {'DEPART': 4, 'DUREE': 8, 'PRIX': 4, 'VOL': 'flat-smallpox-13'}, {'DEPART': 3, 'DUREE': 2, 'PRIX': 7, 'VOL': 'horrible-bowl-81'}, {'DEPART': 2, 'DUREE': 2, 'PRIX': 6, 'VOL': 'ugliest-pen-76'}, {'DEPART': 9, 'DUREE': 9, 'PRIX': 15, 'VOL': 'delightful-gourmet-23'}, {'DEPART': 8, 'DUREE': 8, 'PRIX': 23, 'VOL': 'modern-metro-48'}, {'DEPART': 5, 'DUREE': 4, 'PRIX': 8, 'VOL': 'crooked-rifle-70'}, {'DEPART': 6, 'DUREE': 8, 'PRIX': 8, 'VOL': 'nice-sheriff-93'}, {'DEPART': 8, 'DUREE': 5, 'PRIX': 7, 'VOL': 'prickly-tractor-25'}, {'DEPART': 11, 'DUREE': 3, 'PRIX': 9, 'VOL': 'disturbed-therapy-66'}, {'DEPART': 10, 'DUREE': 7, 'PRIX': 16, 'VOL': 'nervous-mockingbird-94'}, {'DEPART': 12, 'DUREE': 6, 'PRIX': 7, 'VOL': 'crazy-coyote-67'}, {'DEPART': 12, 'DUREE': 3, 'PRIX': 15, 'VOL': 'crazy-wildflower-56'}, {'DEPART': 14, 'DUREE': 16, 'PRIX': 5, 'VOL': 'defiant-workbench-57'}, {'DEPART': 19, 'DUREE': 3, 'PRIX': 2, 'VOL': 'encouraging-revolution-54'}, {'DEPART': 19, 'DUREE': 7, 'PRIX': 17, 'VOL': 'condemned-salt-41'}, {'DEPART': 17, 'DUREE': 9, 'PRIX': 8, 'VOL': 'real-reversal-69'}, {'DEPART': 16, 'DUREE': 10, 'PRIX': 10, 'VOL': 'chubby-armrest-35'}, {'DEPART': 16, 'DUREE': 9, 'PRIX': 6, 'VOL': 'good-porter-52'}, {'DEPART': 23, 'DUREE': 6, 'PRIX': 25, 'VOL': 'faint-leadership-82'}, {'DEPART': 24, 'DUREE': 5, 'PRIX': 15, 'VOL': 'easy-drug-2'}, {'DEPART': 24, 'DUREE': 3, 'PRIX': 8, 'VOL': 'elated-revolution-63'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 7, 'VOL': 'defiant-guava-20'}, {'DEPART': 20, 'DUREE': 13, 'PRIX': 6, 'VOL': 'puzzled-puppeteer-7'}, {'DEPART': 25, 'DUREE': 2, 'PRIX': 9, 'VOL': 'comfortable-genius-61'}, {'DEPART': 28, 'DUREE': 2, 'PRIX': 14, 'VOL': 'old-joker-99'}, {'DEPART': 26, 'DUREE': 3, 'PRIX': 2, 'VOL': 'black-chess-79'}, {'DEPART': 27, 'DUREE': 5, 'PRIX': 10, 'VOL': 'grieving-raindrop-1'}, {'DEPART': 27, 'DUREE': 1, 'PRIX': 3, 'VOL': 'wandering-sentence-58'}, {'DEPART': 30, 'DUREE': 6, 'PRIX': 11, 'VOL': 'dark-stink-64'}, {'DEPART': 33, 'DUREE': 10, 'PRIX': 6, 'VOL': 'nervous-witticism-78'}, {'DEPART': 33, 'DUREE': 6, 'PRIX': 6, 'VOL': 'gigantic-letter-10'}, {'DEPART': 32, 'DUREE': 10, 'PRIX': 7, 'VOL': 'annoyed-treadmill-94'}, {'DEPART': 33, 'DUREE': 1, 'PRIX': 5, 'VOL': 'crazy-landlord-15'}, {'DEPART': 35, 'DUREE': 8, 'PRIX': 7, 'VOL': 'energetic-sickness-63'}, {'DEPART': 38, 'DUREE': 8, 'PRIX': 9, 'VOL': 'impossible-weaponry-83'}, {'DEPART': 37, 'DUREE': 2, 'PRIX': 8, 'VOL': 'selfish-paperwork-17'}, {'DEPART': 35, 'DUREE': 10, 'PRIX': 15, 'VOL': 'proud-iceskate-18'}, {'DEPART': 36, 'DUREE': 1, 'PRIX': 6, 'VOL': 'kind-toucan-96'}, {'DEPART': 40, 'DUREE': 4, 'PRIX': 21, 'VOL': 'raspy-swordsman-31'}, {'DEPART': 41, 'DUREE': 6, 'PRIX': 4, 'VOL': 'cooperative-coffee-42'}, {'DEPART': 44, 'DUREE': 3, 'PRIX': 8, 'VOL': 'grumpy-linesman-43'}, {'DEPART': 44, 'DUREE': 8, 'PRIX': 15, 'VOL': 'gorgeous-alcoholic-67'}, {'DEPART': 41, 'DUREE': 2, 'PRIX': 7, 'VOL': 'adventurous-bed-78'}, {'DEPART': 49, 'DUREE': 3, 'PRIX': 4, 'VOL': 'thoughtless-throat-41'}, {'DEPART': 46, 'DUREE': 9, 'PRIX': 6, 'VOL': 'quick-snorkel-20'}, {'DEPART': 48, 'DUREE': 5, 'PRIX': 10, 'VOL': 'comfortable-mint-21'}, {'DEPART': 48, 'DUREE': 7, 'PRIX': 14, 'VOL': 'wicked-banana-15'}, {'DEPART': 48, 'DUREE': 4, 'PRIX': 5, 'VOL': 'cautious-museum-77'}, {'DEPART': 52, 'DUREE': 7, 'PRIX': 24, 'VOL': 'homely-ally-98'}, {'DEPART': 51, 'DUREE': 8, 'PRIX': 7, 'VOL': 'famous-thanksgiving-72'}, {'DEPART': 53, 'DUREE': 6, 'PRIX': 8, 'VOL': 'awful-pasture-68'}, {'DEPART': 53, 'DUREE': 9, 'PRIX': 6, 'VOL': 'blue-eyed-taco-68'}, {'DEPART': 53, 'DUREE': 9, 'PRIX': 3, 'VOL': 'creepy-choir-40'}, {'DEPART': 59, 'DUREE': 8, 'PRIX': 9, 'VOL': 'helpful-xerox-87'}, {'DEPART': 55, 'DUREE': 6, 'PRIX': 19, 'VOL': 'aggressive-wishbone-82'}, {'DEPART': 59, 'DUREE': 8, 'PRIX': 1, 'VOL': 'doubtful-fence-78'}, {'DEPART': 59, 'DUREE': 1, 'PRIX': 9, 'VOL': 'depressed-dresser-55'}, {'DEPART': 56, 'DUREE': 9, 'PRIX': 2, 'VOL': 'ancient-squid-31'}, {'DEPART': 62, 'DUREE': 3, 'PRIX': 27, 'VOL': 'high-pitched-theorist-20'}, {'DEPART': 61, 'DUREE': 4, 'PRIX': 9, 'VOL': 'eager-android-49'}, {'DEPART': 63, 'DUREE': 2, 'PRIX': 3, 'VOL': 'deafening-repayment-64'}, {'DEPART': 64, 'DUREE': 8, 'PRIX': 9, 'VOL': 'annoyed-mathematician-24'}, {'DEPART': 62, 'DUREE': 18, 'PRIX': 2, 'VOL': 'muddy-serum-96'}, {'DEPART': 65, 'DUREE': 2, 'PRIX': 25, 'VOL': 'thoughtless-workbook-28'}, {'DEPART': 65, 'DUREE': 9, 'PRIX': 17, 'VOL': 'clean-southerner-92'}, {'DEPART': 66, 'DUREE': 7, 'PRIX': 2, 'VOL': 'melodic-windsurfing-32'}, {'DEPART': 66, 'DUREE': 6, 'PRIX': 11, 'VOL': 'gigantic-jet-55'}, {'DEPART': 66, 'DUREE': 20, 'PRIX': 7, 'VOL': 'embarrassed-train-91'}, {'DEPART': 70, 'DUREE': 1, 'PRIX': 13, 'VOL': 'comfortable-vacation-12'}, {'DEPART': 72, 'DUREE': 5, 'PRIX': 9, 'VOL': 'sleepy-screwball-65'}, {'DEPART': 71, 'DUREE': 7, 'PRIX': 7, 'VOL': 'amused-trek-20'}, {'DEPART': 71, 'DUREE': 2, 'PRIX': 10, 'VOL': 'hilarious-jibe-36'}, {'DEPART': 70, 'DUREE': 3, 'PRIX': 3, 'VOL': 'dull-seaport-85'}, {'DEPART': 75, 'DUREE': 9, 'PRIX': 17, 'VOL': 'ugly-aeroplane-37'}, {'DEPART': 75, 'DUREE': 8, 'PRIX': 20, 'VOL': 'crowded-mugger-17'}, {'DEPART': 76, 'DUREE': 9, 'PRIX': 10, 'VOL': 'prickly-hitch-23'}, {'DEPART': 79, 'DUREE': 2, 'PRIX': 11, 'VOL': 'breakable-pound-86'}, {'DEPART': 76, 'DUREE': 9, 'PRIX': 6, 'VOL': 'bored-onion-86'}, {'DEPART': 84, 'DUREE': 6, 'PRIX': 24, 'VOL': 'resonant-harvest-80'}, {'DEPART': 84, 'DUREE': 3, 'PRIX': 11, 'VOL': 'high-biceps-47'}, {'DEPART': 81, 'DUREE': 5, 'PRIX': 8, 'VOL': 'eager-sophomore-38'}, {'DEPART': 80, 'DUREE': 6, 'PRIX': 8, 'VOL': 'anxious-values-2'}, {'DEPART': 81, 'DUREE': 2, 'PRIX': 6, 'VOL': 'young-cell-91'}, {'DEPART': 89, 'DUREE': 8, 'PRIX': 11, 'VOL': 'clear-head-83'}, {'DEPART': 89, 'DUREE': 10, 'PRIX': 22, 'VOL': 'noisy-cutoffs-37'}, {'DEPART': 86, 'DUREE': 4, 'PRIX': 7, 'VOL': 'adventurous-stick-39'}, {'DEPART': 85, 'DUREE': 3, 'PRIX': 7, 'VOL': 'drab-text-53'}, {'DEPART': 85, 'DUREE': 13, 'PRIX': 2, 'VOL': 'uninterested-bedroom-37'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['disgusted-stepson-62', 'crooked-rifle-70', 'nervous-mockingbird-94', 'condemned-salt-41', 'wandering-sentence-58', 'old-joker-99', 'dark-stink-64', 'kind-toucan-96', 'selfish-paperwork-17', 'raspy-swordsman-31', 'gorgeous-alcoholic-67', 'homely-ally-98', 'depressed-dresser-55', 'high-pitched-theorist-20', 'thoughtless-workbook-28', 'comfortable-vacation-12', 'hilarious-jibe-36', 'crowded-mugger-17', 'high-biceps-47', 'noisy-cutoffs-37'], 'gain': 294}

    >>> commandes = [{'DEPART': 3, 'DUREE': 3, 'PRIX': 14, 'VOL': 'energetic-helmet-49'}, {'DEPART': 4, 'DUREE': 10, 'PRIX': 12, 'VOL': 'anxious-prizefight-76'}, {'DEPART': 2, 'DUREE': 9, 'PRIX': 6, 'VOL': 'brief-sponge-66'}, {'DEPART': 2, 'DUREE': 1, 'PRIX': 10, 'VOL': 'tired-dimple-30'}, {'DEPART': 1, 'DUREE': 1, 'PRIX': 7, 'VOL': 'expensive-rent-32'}, {'DEPART': 9, 'DUREE': 6, 'PRIX': 30, 'VOL': 'frail-washer-22'}, {'DEPART': 5, 'DUREE': 8, 'PRIX': 17, 'VOL': 'anxious-mice-23'}, {'DEPART': 9, 'DUREE': 7, 'PRIX': 9, 'VOL': 'perfect-trigger-30'}, {'DEPART': 6, 'DUREE': 9, 'PRIX': 14, 'VOL': 'arrogant-memory-62'}, {'DEPART': 8, 'DUREE': 12, 'PRIX': 6, 'VOL': 'silent-handbag-74'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['expensive-rent-32', 'tired-dimple-30', 'energetic-helmet-49', 'frail-washer-22'], 'gain': 61}

    >>> commandes = [{'DEPART': 0, 'DUREE': 8, 'PRIX': 26, 'VOL': 'tiny-beech-51'}, {'DEPART': 1, 'DUREE': 1, 'PRIX': 21, 'VOL': 'gorgeous-cello-93'}, {'DEPART': 2, 'DUREE': 2, 'PRIX': 4, 'VOL': 'beautiful-herb-77'}, {'DEPART': 3, 'DUREE': 5, 'PRIX': 6, 'VOL': 'cautious-tendon-25'}, {'DEPART': 1, 'DUREE': 9, 'PRIX': 5, 'VOL': 'long-wrench-65'}, {'DEPART': 7, 'DUREE': 10, 'PRIX': 12, 'VOL': 'colorful-frank-71'}, {'DEPART': 7, 'DUREE': 2, 'PRIX': 17, 'VOL': 'thankful-logjam-66'}, {'DEPART': 6, 'DUREE': 8, 'PRIX': 4, 'VOL': 'selfish-helicopter-77'}, {'DEPART': 7, 'DUREE': 10, 'PRIX': 11, 'VOL': 'cute-styrofoam-72'}, {'DEPART': 8, 'DUREE': 14, 'PRIX': 2, 'VOL': 'helpful-azalea-51'}, {'DEPART': 11, 'DUREE': 9, 'PRIX': 26, 'VOL': 'long-mariner-5'}, {'DEPART': 14, 'DUREE': 1, 'PRIX': 4, 'VOL': 'drab-whiff-76'}, {'DEPART': 14, 'DUREE': 9, 'PRIX': 4, 'VOL': 'wide-eyed-business-56'}, {'DEPART': 13, 'DUREE': 6, 'PRIX': 8, 'VOL': 'amused-thundercloud-19'}, {'DEPART': 12, 'DUREE': 11, 'PRIX': 6, 'VOL': 'precious-ranger-38'}, {'DEPART': 17, 'DUREE': 8, 'PRIX': 8, 'VOL': 'chubby-therapy-6'}, {'DEPART': 19, 'DUREE': 8, 'PRIX': 13, 'VOL': 'repulsive-wildcat-27'}, {'DEPART': 18, 'DUREE': 10, 'PRIX': 8, 'VOL': 'helpless-macaw-41'}, {'DEPART': 17, 'DUREE': 1, 'PRIX': 10, 'VOL': 'grotesque-tailgate-12'}, {'DEPART': 16, 'DUREE': 2, 'PRIX': 5, 'VOL': 'friendly-backyard-49'}]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['gorgeous-cello-93', 'beautiful-herb-77', 'thankful-logjam-66', 'drab-whiff-76', 'grotesque-tailgate-12', 'repulsive-wildcat-27'], 'gain': 69}

    >>> commandes = [{'DEPART': 2, 'DUREE': 2, 'PRIX': 7, 'VOL': 'huge-wintergreen-82'}, {'DEPART': 1, 'DUREE': 3, 'PRIX': 8, 'VOL': 'nutty-chisel-69'}, {'DEPART': 0, 'DUREE': 2, 'PRIX': 7, 'VOL': 'screeching-jogger-9'}, {'DEPART': 0, 'DUREE': 8, 'PRIX': 7, 'VOL': 'puny-acrobat-13'}, {'DEPART': 0, 'DUREE': 18, 'PRIX': 5, 'VOL': 'purring-kid-30'}, {'DEPART': 7, 'DUREE': 4, 'PRIX': 12, 'VOL': 'quaint-pecan-5'}, {'DEPART': 7, 'DUREE': 2, 'PRIX': 9, 'VOL': 'inexpensive-plasterboard-57'}, {'DEPART': 8, 'DUREE': 6, 'PRIX': 5, 'VOL': 'wild-screwdriver-37'}, {'DEPART': 5, 'DUREE': 6, 'PRIX': 12, 'VOL': 'big-seafood-10'}, {'DEPART': 8, 'DUREE': 19, 'PRIX': 3, 'VOL': 'curious-shortchange-59'}, {'DEPART': 10, 'DUREE': 2, 'PRIX': 3, 'VOL': 'bloody-tuttifrutti-11'}, {'DEPART': 11, 'DUREE': 4, 'PRIX': 5, 'VOL': 'mysterious-springtime-12'}, {'DEPART': 13, 'DUREE': 6, 'PRIX': 9, 'VOL': 'aggressive-preschooler-58'}, {'DEPART': 13, 'DUREE': 1, 'PRIX': 10, 'VOL': 'wide-pit-81'}, {'DEPART': 13, 'DUREE': 3, 'PRIX': 3, 'VOL': 'blushing-mayonnaise-26'}, {'DEPART': 18, 'DUREE': 3, 'PRIX': 25, 'VOL': 'short-jackrabbit-62'}, {'DEPART': 16, 'DUREE': 4, 'PRIX': 19, 'VOL': 'fair-keg-43'}, {'DEPART': 18, 'DUREE': 2, 'PRIX': 1, 'VOL': 'dark-palace-64'}, {'DEPART': 19, 'DUREE': 4, 'PRIX': 7, 'VOL': 'bright-dolt-78'}, {'DEPART': 16, 'DUREE': 8, 'PRIX': 4, 'VOL': 'old-fashioned-sandwich-35'}, {'DEPART': 21, 'DUREE': 6, 'PRIX': 21, 'VOL': 'helpless-vow-77'}, {'DEPART': 20, 'DUREE': 8, 'PRIX': 14, 'VOL': 'testy-somewhere-96'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 1, 'VOL': 'jittery-ferret-12'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 6, 'VOL': 'tough-flag-45'}, {'DEPART': 22, 'DUREE': 6, 'PRIX': 4, 'VOL': 'faithful-rhinestone-74'}, {'DEPART': 27, 'DUREE': 9, 'PRIX': 21, 'VOL': 'troubled-shrewdness-28'}, {'DEPART': 29, 'DUREE': 4, 'PRIX': 17, 'VOL': 'proud-rubble-25'}, {'DEPART': 27, 'DUREE': 1, 'PRIX': 8, 'VOL': 'elegant-sandlot-15'}, {'DEPART': 27, 'DUREE': 8, 'PRIX': 11, 'VOL': 'stupid-glue-25'}, {'DEPART': 28, 'DUREE': 12, 'PRIX': 1, 'VOL': 'beautiful-bike-51'}, {'DEPART': 30, 'DUREE': 10, 'PRIX': 5, 'VOL': 'worried-archery-14'}, {'DEPART': 30, 'DUREE': 6, 'PRIX': 10, 'VOL': 'vast-tentacle-84'}, {'DEPART': 33, 'DUREE': 9, 'PRIX': 6, 'VOL': 'friendly-polygamy-1'}, {'DEPART': 32, 'DUREE': 1, 'PRIX': 8, 'VOL': 'clean-bullfighting-87'}, {'DEPART': 31, 'DUREE': 13, 'PRIX': 1, 'VOL': 'hungry-slothfulness-3'}]
    >>> # random.shuffle(commandes)
    >>> # le shuffle pète tout, car plusieurs combinaisons possibles pour le même gain
    >>> optimize(commandes)
    {'path': ['screeching-jogger-9', 'huge-wintergreen-82', 'inexpensive-plasterboard-57', 'bloody-tuttifrutti-11', 'wide-pit-81', 'short-jackrabbit-62', 'helpless-vow-77', 'elegant-sandlot-15', 'proud-rubble-25', 'friendly-polygamy-1'], 'gain': 113}

    >>> commandes = [{ 'VOL': 'VOL0', 'DEPART': 0, 'DUREE': 5, 'PRIX': 15 },
    ...     { 'VOL': 'VOL1', 'DEPART': 4, 'DUREE': 5, 'PRIX': 18 },
    ...     { 'VOL': 'VOL2', 'DEPART': 8, 'DUREE': 13, 'PRIX': 19 },
    ...     { 'VOL': 'VOL3', 'DEPART': 10, 'DUREE': 5, 'PRIX': 12 },
    ...     { 'VOL': 'VOL4', 'DEPART': 25, 'DUREE': 5, 'PRIX': 25 }]
    >>> random.shuffle(commandes)
    >>> optimize(commandes)
    {'path': ['VOL0', 'VOL2', 'VOL4'], 'gain': 59}
    """
    if len(commandes) == 0:
        return {'gain': 0, 'path': list()}

    nb_commandes = len(commandes)
    commandes = sorted(commandes, key=itemgetter('DEPART'))
    commandes = list(enumerate(commandes))

    prix = [0] * nb_commandes
    departs = [0] * nb_commandes
    suivants = {}
    vols = {}

    prix_precedent = 0
    prix_max_index = nb_commandes
    prix_suivants = {}

    while commandes:
        i, commande = commandes.pop()
        departs[i] = commande['DEPART']
        vols[i] = commande['VOL']
        #
        fin = commande['DEPART'] + commande['DUREE']
        j = bisect_left(departs, fin, lo=i + 1, hi=nb_commandes)
        prix_suivant = 0
        if j < nb_commandes:
            prix_suivant = prix[j]
            suivants[i] = prix_suivants[prix_suivant]
        #
        somme_ij = commande['PRIX'] + prix_suivant
        prix[i] = max(somme_ij, prix_precedent)
        #
        if not prix[i] in prix_suivants:
            prix_suivants[prix[i]] = i
        #
        if prix[i] > prix_precedent:
            prix_max_index = i
        #
        # print ('-- max(%d + %d, %d) = %d'%(commande['PRIX'], prix_suivant,
            # prix_precedent, prix[i]))
        prix_precedent = prix[i]

    resultat = {'gain': prix[prix_max_index], 'path': list()}
    resultat['path'].append(vols[prix_max_index])

    while prix_max_index in suivants:
        prix_max_index = suivants[prix_max_index]
        resultat['path'].append(vols[prix_max_index])

    return resultat

if __name__ == '__main__':
    import random
    commandes = [{'VOL': 'VOL0', 'DEPART': 0, 'DUREE': 5, 'PRIX': 15},
                {'VOL': 'VOL1', 'DEPART': 4, 'DUREE': 5, 'PRIX': 18},
                {'VOL': 'VOL2', 'DEPART': 8, 'DUREE': 13, 'PRIX': 19},
                {'VOL': 'VOL3', 'DEPART': 10, 'DUREE': 5, 'PRIX': 12},
                {'VOL': 'VOL4', 'DEPART': 25, 'DUREE': 5, 'PRIX': 25}]
    random.shuffle(commandes)
    print optimize(commandes)

    commandes = [{'VOL': str(x), 'DEPART': x, 'DUREE': x, 'PRIX': x}
                    for x in range(1, 50000)]
    random.shuffle(commandes)
    print optimize(commandes)
