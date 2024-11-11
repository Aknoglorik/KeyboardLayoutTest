from asyncio import Future
import asyncio

from config import (
    ALPHABET,
    RUSSIAN,
    WHITE_SPACES,
    PUNCTUATION,
    Finger,
    FingerStat,
    FingerLayout,
    Modifier,
    key_to_finger,
)
from collections import Counter, defaultdict

import logging as log


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
            if mod == Modifier.SwitchLayout:
                score[finger] += 2*factor
            else:
                score[finger] += factor
    return score


async def _count_to_score(stat: FingerStat, finger_layout: FingerLayout,
                          future: Future) -> dict[Finger, int]:

    def _addictive_merge_dicts(*sources: dict[str, int]) -> dict[str, int]:
        result = defaultdict(int)
        for sorce in sources:
            for key, value in sorce.items():
                result[key] += value
        return result

    log.info('Start counting score')

    layout, modifiers = finger_layout
    key_finger = key_to_finger(layout)
    score = dict.fromkeys([finger.value for finger in Finger], 0)

    symbols, digramms = stat

    for key, amount in symbols.items():
        await asyncio.sleep(0)
        finger, mods = key_finger[key]
        mods_score = count_keys_by_modifiers(mods, modifiers, amount)
        score[finger] += amount
        score = _addictive_merge_dicts(score, mods_score)

    log.info('End count score')
    future.set_result(score)


def count_to_score(stat: FingerStat, finger_layout: FingerLayout
                   ) -> Future[dict[Finger, int]]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    score = Future()
    asyncio.create_task(_count_to_score(stat, finger_layout, score))

    return score


def isRussian(ch: str) -> str:
    '''
    @brief Проверка символа на принадлежность к русскому алфавиту.
    '''
    if len(ch) > 1:
        raise ValueError('Char must have len 1!')
    return ch in ALPHABET


async def _get_info_from_file(fname: str, future: Future) -> None:
    log.info('Start read file: %s', fname)

    def _count_digramms(text: str) -> Counter:
        digramms = Counter()
        for word in text.strip().split():
            for i in range(len(word) - 1):
                digramm = word[i:i+2]
                digramms[digramm] += 1

        return digramms

    symbols = Counter()
    digramms = Counter()
    translate_punct2space = str.maketrans(PUNCTUATION, ' ' * len(PUNCTUATION))

    with open(fname, 'rt', encoding='utf-8') as file:
        for line in file:
            await asyncio.sleep(0)

            symbols.update(filter(isRussian, line))

            punct_less_line = (
                line
                .lower()
                .translate(translate_punct2space)
            )

            filtred_line = ''.join(
                filter(lambda x: x in RUSSIAN+WHITE_SPACES, punct_less_line)
            )
            digramms.update(_count_digramms(filtred_line))

    log.info('End read file: %s', fname)
    future.set_result((symbols, digramms))


def get_info_from_file(fname: str) -> Future[FingerStat]:
    '''
    @brief Из файла подсчитывается кол-во символов и диграмм.
    '''
    statistic = Future()
    asyncio.create_task(_get_info_from_file(fname, statistic))

    return statistic
