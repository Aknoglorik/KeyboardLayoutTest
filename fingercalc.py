from config import (
    ALPHABET,
    Finger,
    FingerStat,
    FingerLayout,
    key_to_finger,
)
from collections import Counter, defaultdict


def count_to_score(stat: FingerStat, layout: FingerLayout
                   ) -> dict[Finger, int]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    key_finger = key_to_finger(layout)
    score = defaultdict(int)
    for finger in Finger:
        score[finger.value]

    for key, amount in stat.items():
        finger, _ = key_finger[key]
        score[finger] += amount

    return score


def isRussian(ch: str) -> str:
    '''
    @brief Проверка символа на принадлежность к русскому алфавиту.
    '''
    if len(ch) > 1:
        raise ValueError('Char must have len 1!')
    return ch in ALPHABET


def get_info_from_file(fname: str) -> FingerStat:
    '''
    @brief Из файла подсчитывается кол-во символов и лексем.
    '''
    statistic: FingerStat = Counter()
    with open(fname, 'rt', encoding='utf-8') as file:
        for line in file:
            statistic.update(
                filter(isRussian, line)
            )
    return statistic
