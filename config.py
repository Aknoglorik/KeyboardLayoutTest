from enum import StrEnum, auto
from collections import Counter
import tomllib


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


type FingerStat = Counter
type Key = str
type FingerLayout = dict[Finger, list[Key]]

# TODO! В будущем
# type Lexigram = dict[str, float]  # Лексиграмма - процент
# type Key = tuple[str, int]  # Клавиша - штраф


def load_layout(fname: str) -> FingerLayout:
    '''
    @brief Загружает toml-конфиг для раскладки из указанного файла.
    '''
    with open(fname, "rb") as f:
        data = tomllib.load(f)
    return data


def key_to_finger(layout: FingerLayout) -> dict[Key, Finger]:
    '''
    @brief На основе полученной раскладки формирует словарь `Клавиша-палец`.
    '''
    data = {
        key: finger_name
        for finger_name, info in layout.items()
        for key in info['keys']
    }
    return data
