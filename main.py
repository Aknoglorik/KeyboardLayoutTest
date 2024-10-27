from config import (
    Finger,
    FingerStat,
    FingerLayout,
    load_layout,
    key_to_finger,
)
from fingercalc import get_info_from_file
from gui import plot_by_stat
# from test import test_app

from collections import defaultdict


def count_to_score(stat: FingerStat, layout: FingerLayout
                   ) -> dict[Finger, int]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    key_finger = key_to_finger(layout)
    score = defaultdict(int)

    for key, amount in stat.items():
        finger = key_finger[key]
        score[finger] += amount

    return score


def normolize_finger_stress(finger_stress: dict[Finger, int]
                            ) -> dict[Finger, float]:
    total = sum(finger_stress.values())
    return {
        finger: stress / total * 100
        for finger, stress in finger_stress.items()
    }


def main() -> None:
    '''
    @brief отсюда будут вызываться основные функции И подсчитываться "Очки"
    согласно ТЗ, которые будут переданы в функции gui.py
    '''

    QWERTY_LAYOUT: FingerLayout = load_layout(r'testlayouts/qwerty.toml')

    statistics = get_info_from_file('books/war_and_peace.txt')
    finger_stress = normolize_finger_stress(
        count_to_score(statistics, QWERTY_LAYOUT)
    )

    plot_by_stat(finger_stress)


if __name__ == '__main__':
    main()
