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
    Key,
    KeyInfo,
    key_to_finger,
)
from collections import Counter, defaultdict
from functools import partial
from enum import Enum, auto

import logging as log


class BustOrder(Enum):
    # Невозможно
    NONE = auto()
    # Для левой руки слева направо, для правой руки наоборот
    DIRECT = auto()
    # Для левой руки справа налево, для правой руки наоборот
    REVERSE = auto()


class LayoutOrders:
    lfinger_order = [
        Finger.LPinky.value, Finger.LRing.value, Finger.LMiddle.value,
        Finger.LIndex.value, Finger.LThumb.value
    ]

    rev_lfinger_order = [
        Finger.LThumb.value, Finger.LIndex.value, Finger.LMiddle.value,
        Finger.LRing.value, Finger.LPinky.value
    ]

    rfinger_order = [
        Finger.RPinky.value, Finger.RRing.value, Finger.RMiddle.value,
        Finger.RIndex.value, Finger.RThumb.value
    ]

    rev_rfinger_order = [
        Finger.RThumb.value, Finger.RIndex.value, Finger.RMiddle.value,
        Finger.RRing.value, Finger.RPinky.value
    ]

    @classmethod
    def check_text_bust_order(cls, text: str, key_finger: dict[Key, KeyInfo]):
        prev_finger, mods, _ = key_finger[text[0]]
        if mods:
            return BustOrder.NONE, BustOrder.NONE

        left_hand_direct = prev_finger in cls.lfinger_order
        left_hand_reverse = True
        right_hand_direct = prev_finger in cls.rfinger_order
        right_hand_reverse = True

        for letter in text[1:]:
            next_finger, mods, _ = key_finger[letter]
            if mods:
                return BustOrder.NONE, BustOrder.NONE

            left_hand_direct = (
                left_hand_direct and
                is_continue_row(
                    prev_finger,
                    next_finger,
                    cls.lfinger_order
                )
            )
            left_hand_reverse = (
                left_hand_reverse and
                is_continue_row(
                    prev_finger,
                    next_finger,
                    cls.rev_lfinger_order
                )
            )
            right_hand_direct = (
                right_hand_direct and
                is_continue_row(
                    prev_finger,
                    next_finger,
                    cls.rfinger_order
                )
            )
            right_hand_reverse = (
                right_hand_reverse and
                is_continue_row(
                    prev_finger,
                    next_finger,
                    cls.rev_rfinger_order
                )
            )
            prev_finger = next_finger

        return cls._transform_bool_2_enum(
            left_hand_direct, left_hand_reverse,
            right_hand_direct, right_hand_reverse
        )

    @staticmethod
    def _transform_bool_2_enum(
        left_hand_direct: bool, left_hand_reverse: bool,
        right_hand_direct: bool, right_hand_reverse: bool
                               ) -> tuple[BustOrder, BustOrder]:

        if left_hand_direct:
            left_hand = BustOrder.DIRECT
        elif left_hand_reverse:
            left_hand = BustOrder.REVERSE
        else:
            left_hand = BustOrder.NONE

        if right_hand_direct:
            right_hand = BustOrder.DIRECT
        elif right_hand_reverse:
            right_hand = BustOrder.REVERSE
        else:
            right_hand = BustOrder.NONE

        return left_hand, right_hand


def is_continue_row[T](prev_: T, next_: T, row: list[T]) -> bool:
    if prev_ not in row or next_ not in row:
        return False
    return row.index(prev_) < row.index(next_)


def get_bust_orders(text: str, *finger_layouts: list[FingerLayout]
                    ) -> list[tuple[BustOrder, BustOrder]]:
    '''
    @return возвращает лист состоящий из кортежей, где i-ый элеемент отвечает
    на вопрос "можно ли перебрать текст одной рукой" для i-ой раскладки. Кортеж
    состоит из:
        - [0] способ перебора правой рукой
        - [1] способ перебора левой рукой
    '''
    filtred_text = ''.join(filter(isRussian, text))
    if len(filtred_text) < 2 or filtred_text != text:
        return [(BustOrder.NONE, BustOrder.NONE) for _ in finger_layouts]

    layouts = list(map(lambda fl: fl[0], finger_layouts))
    key_fingers = list(map(key_to_finger, layouts))

    return list(map(
        partial(LayoutOrders.check_text_bust_order, text),
        key_fingers
    ))


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


async def _count_to_score(symbols: Counter, finger_layout: FingerLayout,
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

    for key, amount in symbols.items():
        await asyncio.sleep(0)
        finger, mods, finger_score = key_finger[key]
        mods_score = count_keys_by_modifiers(mods, modifiers, amount)
        score[finger] += amount * (1 + finger_score)
        score = _addictive_merge_dicts(score, mods_score)

    log.info('End count score')
    future.set_result(score)


def count_to_score(symbols: Counter, finger_layout: FingerLayout
                   ) -> Future[dict[Finger, int]]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    score = Future()
    asyncio.create_task(_count_to_score(symbols, finger_layout, score))

    return score


def isRussian(ch: str) -> str:
    '''
    @brief Проверка символа на принадлежность к русскому алфавиту.
    '''
    if len(ch) > 1:
        raise ValueError('Char must have len 1!')
    return ch in ALPHABET


def count_ngramms(text: str, n: int) -> Counter:
    if n < 1:
        raise ValueError('ngramm cant have size less that 1.')

    ngramms = Counter()
    for word in text.strip().split():
        for i in range(len(word) - n + 1):
            ngramm = word[i:i+n]
            ngramms[ngramm] += 1

    return ngramms


async def _get_info_from_file(fname: str, future: Future) -> None:
    log.info('Start read file: %s', fname)

    symbols = Counter()
    digramms = Counter()
    threegramms = Counter()
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
            digramms.update(count_ngramms(filtred_line, 2))
            threegramms.update(count_ngramms(filtred_line, 3))

    log.info('End read file: %s', fname)
    future.set_result((symbols, digramms, threegramms))


def get_info_from_file(fname: str) -> Future[FingerStat]:
    '''
    @brief Из файла подсчитывается кол-во символов и диграмм.
    '''
    statistic = Future()
    asyncio.create_task(_get_info_from_file(fname, statistic))

    return statistic
