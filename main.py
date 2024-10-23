from config import (
    Finger,
    FingerStat,
    FingerLayout,
    load_layout,
)
from fingercalc import get_info_from_file
from gui import plot_by_stat
# from test import test_app


def count_to_score(stat: FingerStat, layout: FingerLayout
                   ) -> dict[Finger, int]:
    '''
    @brief На основе полученной `статистики` подсчитывает кол-во очков для
    '''
    pass


def main() -> None:
    '''
    @brief отсюда будут вызываться основные функции И подсчитываться "Очки"
    согласно ТЗ, которые будут переданы в функции gui.py
    '''

    QWERTY_LAYOUT: FingerLayout = load_layout(r'testlayouts/qwerty.toml')

    statistics = get_info_from_file('war_and_peace.txt')
    finger_stress = count_to_score(statistics, QWERTY_LAYOUT)

    plot_by_stat(finger_stress)


if __name__ == '__main__':
    main()
