import asyncio

from config import (
    Finger,
    FingerLayout,
    load_layout,
)
from fingercalc import (
    get_info_from_file,
    count_to_score,
    get_bust_orders,
    BustOrder
)
from gui import plot_by_stat
# from test import test_app

import sys

import logging as log


def normolize_finger_stress(finger_stress: dict[Finger, int]
                            ) -> dict[Finger, float]:
    total = sum(finger_stress.values())
    return {
        finger: stress / total * 100
        for finger, stress in finger_stress.items()
    }


def rate_bust_order(*layouts: list[FingerLayout]) -> list[int]:
    '''
    @brief Подсчитывает кол-во слов которые можно перебрать одной рукой.
    @detailed Подсчитывает кол-во слов которые можно перебрать одной рукой для
    любого количества рассладко (чтобы пройти файл за один раз). При этом если
    перебор 'прямой', то начисляется 2 очка, а если же перебор 'обратный', то 1
    (т.к. он сложнее [пианисты знают]).
    @return Возращает список очков для каждой раскладки
    '''
    log.info('Начало подсчета очков за перебор слов одной рукой.')

    score = [0 for _ in layouts]
    with open('books/1grams-3.txt', 'rt', encoding='utf-8') as file:
        for line in file:
            orders = get_bust_orders(line.strip(), *layouts)

            for i, order in enumerate(orders):
                lorder, rorder = order
                if BustOrder.DIRECT in (lorder, rorder):
                    score[i] += 2
                if BustOrder.REVERSE in (lorder, rorder):
                    score[i] += 1
    return score


async def main() -> None:
    '''
    @brief отсюда будут вызываться основные функции И подсчитываться "Очки"
    согласно ТЗ, которые будут переданы в функции gui.py
    '''

    QWERTY_LAYOUT: asyncio.Future = load_layout(r'testlayouts/qwerty.toml')
    PHON_LAYOUT: asyncio.Future = load_layout(r'testlayouts/phonetikal.toml')
    DIKTOR_LAYOUT: asyncio.Future = load_layout(r'testlayouts/diktor.toml')

    statistics: asyncio.Future = get_info_from_file('books/war_and_peace.txt')

    try:
        layouts = await asyncio.gather(
            QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT
        )
        QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT = layouts

    except asyncio.CancelledError as e:
        log.error('Не удалось загрузить расскладку:\n %s', e)
        sys.exit(1)

    statistics = await statistics

    score_list = rate_bust_order(QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT)

    log.info(
        'Очки за перебор одной рукой\n'
        '\tЙЦУКЕН: %s\n'
        '\tФонетический: %s\n'
        '\tДиктор: %s\n',
        *score_list
    )

    task_qwerty = count_to_score(statistics, QWERTY_LAYOUT)
    task_phon = count_to_score(statistics, PHON_LAYOUT)
    task_diktor = count_to_score(statistics, DIKTOR_LAYOUT)

    finger_stress_qwerty, finger_stress_phon, finger_stress_diktor = list(
        map(
            normolize_finger_stress,
            await asyncio.gather(task_qwerty, task_phon, task_diktor)
        )
    )

    plot_by_stat(
        score_list,
        finger_stress_qwerty,
        finger_stress_phon,
        finger_stress_diktor,
        layout='ЙЦУКЕН',
        layout2='Русский фонетический',
        layout3='Диктор',
        txt_name='Война и мир',
    )


class FGColors:
    red = "\033[31m"
    yellow = "\033[33m"
    green = "\033[32m"
    reset = "\033[0m"


if __name__ == "__main__":
    fmt = (f'{FGColors.green}%(threadName)10s %(levelname)8s:'
           f'{FGColors.yellow}[%(filename)18s:%(lineno)3s - %(funcName)20s() ]'
           f'{FGColors.reset}:\n%(asctime)s %(message)s')

    log.basicConfig(format=fmt,
                    encoding='utf-8',
                    datefmt='%H:%M:%S',
                    level=log.INFO)

    asyncio.run(main())
