from config import FingerStat
from collections import Counter


def isRussian(ch: str) -> str:
    '''
    @brief Проверка символа на принадлежность к русскому алфавиту.
    '''
    if len(ch) > 1:
        raise ValueError('Char must have len 1!')
    return ('а' <= ch <= 'я') or ch == 'ё'


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
