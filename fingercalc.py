from config import (
    ALPHABET,
    Finger,
    FingerStat,
    FingerLayout,
    Modifier,
    key_to_finger,
)
from collections import Counter, defaultdict


def count_keys_by_modifiers(key_mods: list[str],
                            modifiers: dict[Modifier, Finger],
                            factor: int = 1) -> list[tuple[Finger, int]]:
    def to_list(obj: list[str] | str) -> list[str]:
        if isinstance(obj, str):
            return [obj]
        return obj

    score = Counter()
    for mod in key_mods:
        for finger in to_list(modifiers[mod]):
            score[finger] += factor
    return score


def count_to_score(stat: FingerStat, fing_layout: FingerLayout
                   ) -> dict[Finger, int]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    def _addictive_merge_dicts(*sources: dict[str, int]) -> dict[str, int]:
        result = defaultdict(int)
        for sorce in sources:
            for key, value in sorce.items():
                result[key] += value
        return result

    layout, modifiers = fing_layout
    key_finger = key_to_finger(layout)
    score = defaultdict(int)
    for finger in Finger:
        score[finger.value]

    for key, amount in stat.items():
        finger, mods = key_finger[key]
        mods_score = count_keys_by_modifiers(mods, modifiers, amount)
        score[finger] += amount
        score = _addictive_merge_dicts(score, mods_score)

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
