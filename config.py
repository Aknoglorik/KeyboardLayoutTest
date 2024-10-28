from enum import StrEnum, auto
from collections import Counter

import tomllib


ALPHABET = (
    '1234567890'
    'йцукенгшщзхъфывапролджэячсмитьбюё'
    'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    ' \t\n'
)


type FingerStat = Counter
type Key = str
type FingerLayout = dict[Finger, list[Key]]


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


def assert_layout(layout: FingerLayout) -> bool:
    '''
    @brief Функция проверки `полноценности` раскладки (т.е. наличия всех
    символов, алфавита)
    '''
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


def load_layout(fname: str) -> FingerLayout:
    '''
    @brief Загружает toml-конфиг для раскладки из указанного файла.
    '''
    with open(fname, 'rb') as f:
        layout = tomllib.load(f)
    assert_layout(layout)
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
