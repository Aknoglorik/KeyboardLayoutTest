from asyncio import Future
import asyncio

from enum import StrEnum, auto
from collections import Counter

import tomllib

import logging as log
from typing import NoReturn


ALPHABET = (
    '1234567890'
    'йцукенгшщзхъфывапролджэячсмитьбюё'
    'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    ' \t\n'
)


type FingerStat = Counter
type Key = str
type FingerLayout = tuple[dict[Finger, list[Key]], dict[Modifier, Finger]]


class Finger(StrEnum):
    RPinky = auto()
    RRing = auto()
    RMiddle = auto()
    RIndex = auto()
    RThumb = auto()
    LPinky = auto()
    LRing = auto()
    LMiddle = auto()
    LIndex = auto()
    LThumb = auto()


class Modifier(StrEnum):
    LShift = auto()
    LAlt = auto()
    LCtr = auto()
    RShift = auto()
    RAlt = auto()
    RCtr = auto()
    SwitchLayout = auto()


def assert_layout(layout: FingerLayout) -> None | NoReturn:
    '''
    @brief Функция проверки `полноценности` раскладки (т.е. наличия всех
    символов, алфавита)
    '''
    layout = layout[0]
    layout_alphabet = ''.join([
        letter_info['letter']
        for finger_info in layout.values()
        for letter_info in finger_info['keys']
    ])

    if (set_a := set(ALPHABET)) != (set_al := set(layout_alphabet)):
        raise ValueError(
            'Не найдены следующие символы: ' +
            ', '.join(set_a.difference(set_al)) +
            '\nЛишнее символы:' +
            ', '.join(set_al.difference(set_a))
        )
    if len(ALPHABET) != len(layout_alphabet):
        raise ValueError(
            f'Количество символов в расскладке не соответсвует. '
            f'Должно быть {len(ALPHABET)}, получено {len(layout_alphabet)}'
        )


def assert_modifiers(modifiers: dict[Modifier, Finger]) -> None | NoReturn:
    mods = set(modifiers.keys())
    layout_mods = set([mod.value for mod in Modifier])
    if layout_mods != mods:
        raise ValueError(
            'Sets are not equals!\n'
            f'{mods}\n'
            f'{layout_mods}\n'
        )


async def _load_layout(fname: str, future: Future) -> None:
    log.info('Start read layout: %s', fname)
    with open(fname, 'rb') as f:
        data = tomllib.load(f)

    modifiers = data.pop('modifiers')
    layout = (data, modifiers)
    try:
        assert_modifiers(modifiers)
        assert_layout(layout)
    except ValueError as e:
        future.cancel(str(e))
        return

    log.info('End read layout: %s', fname)
    future.set_result(layout)


def load_layout(fname: str) -> Future[FingerLayout]:
    '''
    @brief Загружает toml-конфиг для раскладки из указанного файла.
    '''
    layout = Future()
    asyncio.create_task(_load_layout(fname, layout))

    return layout


def key_to_finger(layout: FingerLayout
                  ) -> dict[Key, tuple[Finger, list[Modifier]]]:
    '''
    @brief На основе полученной раскладки формирует словарь
    `Клавиша-(палец, модификаторы)`.
    '''
    data = {}
    for finger_name, finger_info in layout.items():
        for letter_info in finger_info['keys']:
            data[letter_info['letter']] = (
                [finger_name, letter_info['modifiers']]
            )
    return data
