import asyncio

from config import (
    Finger,
    FingerLayout,
    load_layout,
)
from fingercalc import (
    get_info_from_file,
    count_to_score,
    calc_penalty,
    get_bust_orders,
    BustOrder,
)
from gui import plot_by_stat
# from test import test_app

import sys
import csv

import logging as log


def normolize_finger_stress(finger_stress: dict[Finger, int]
                            ) -> dict[Finger, float]:
    total = sum(finger_stress.values())
    return {
        finger: stress / total * 100
        for finger, stress in finger_stress.items()
    }


def rate_bust_order(text: str, *layouts: list[FingerLayout]
                    ) -> tuple[dict[BustOrder, int], dict[BustOrder, int]]:
    '''
    @brief Подсчитывает кол-во слов которые можно перебрать одной рукой.
    @detailed Подсчитывает кол-во слов которые можно перебрать одной рукой для
    любого количества рассладок (чтобы пройти файл за один раз). При этом
    учитывается только 'прямой' перебор (т.к. он легче [пианисты знают]).
    @return Возращает список очков для каждой раскладки
    '''
    lscores = [{
            BustOrder.DIRECT: 0,
            BustOrder.REVERSE: 0,
            BustOrder.NONE: 0
        }
        for _ in layouts
    ]
    rscores = [{
            BustOrder.DIRECT: 0,
            BustOrder.REVERSE: 0,
            BustOrder.NONE: 0
        }
        for _ in layouts
    ]

    for word in text.split():
        orders = get_bust_orders(word.strip(), *layouts)
        for i, order in enumerate(orders):
            lorder, rorder = order
            rscores[i][rorder] += 1
            lscores[i][lorder] += 1

    return lscores, rscores


def rate_most_common_digramms(*layouts: list[FingerLayout]
                              ) -> tuple[list[int], int]:
    '''
    @brief Подсчет удобных и неудобных приколов.
    '''
    with open(r'books/sortchbukw.csv', encoding='utf-8',
              newline='') as csv_file:

        reader = csv.reader(csv_file, delimiter=',')
        digramms = ''
        for line in reader:
            digramms += line[1].strip() + '\n'

    scores_most = rate_bust_order(
        digramms,
        *layouts
    )
    log.info(
        'Очки за перебор одной рукой наиболее распространенных диграмм\n'
        '\t Левая рука %s\n'
        '\t Правая рука %s\n',
        scores_most[0],
        scores_most[1]
    )
    return scores_most


async def main() -> None:
    '''
    @brief отсюда будут вызываться основные функции И подсчитываться "Очки"
    согласно ТЗ, которые будут переданы в функции gui.py
    '''

    QWERTY_LAYOUT: asyncio.Future = load_layout(r'testlayouts/qwerty.toml')
    PHON_LAYOUT: asyncio.Future = load_layout(r'testlayouts/phonetikal.toml')
    DIKTOR_LAYOUT: asyncio.Future = load_layout(r'testlayouts/diktor.toml')

    statistics: asyncio.Future = get_info_from_file('books/war_and_peace.txt')
    dt_statistics: asyncio.Future = get_info_from_file('books/1grams-3.txt')

    try:
        layouts = await asyncio.gather(
            QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT
        )
        QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT = layouts

    except asyncio.CancelledError as e:
        log.error('Не удалось загрузить расскладку:\n %s', e)
        sys.exit(1)

    rate_most_common_digramms(QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT)

    statistics, dt_statistics = await asyncio.gather(
        statistics, dt_statistics
    )

    statistics, most_common_digramms, _ = statistics
    _, digramms, threegramms = dt_statistics

    most_common_digramms = '\n'.join(most_common_digramms.keys())
    digramms = '\n'.join(digramms.keys())
    threegramms = '\n'.join(threegramms.keys())

    # lab4
    scores_most = rate_bust_order(
        most_common_digramms,
        QWERTY_LAYOUT,
        PHON_LAYOUT,
        DIKTOR_LAYOUT
    )
    log.info(
        'Очки за перебор одной рукой наиболее распространенных диграмм\n'
        '\t Левая рука %s\n'
        '\t Правая рука %s\n',
        scores_most[0],
        scores_most[1]
    )

    # lab5
    scores_dig = rate_bust_order(
        digramms,
        QWERTY_LAYOUT,
        PHON_LAYOUT,
        DIKTOR_LAYOUT
    )
    log.info(
        'Очки за перебор одной рукой диграмм из 1grams-3\n'
        '\t Левая рука %s\n'
        '\t Правая рука %s\n',
        scores_dig[0],
        scores_dig[1]
    )

    scores_three = rate_bust_order(
        threegramms,
        QWERTY_LAYOUT,
        PHON_LAYOUT,
        DIKTOR_LAYOUT
    )
    log.info(
        'Очки за перебор одной рукой триграмм из 1grams-3\n'
        '\t Левая рука %s\n'
        '\t Правая рука %s\n',
        scores_three[0],
        scores_three[1]
    )

    task_qwerty = count_to_score(statistics, QWERTY_LAYOUT)
    task_phon = count_to_score(statistics, PHON_LAYOUT)
    task_diktor = count_to_score(statistics, DIKTOR_LAYOUT)

    finger_stress_qwerty, finger_stress_phon, finger_stress_diktor = (
        await asyncio.gather(task_qwerty, task_phon, task_diktor)
    )

    scores = [scores_most, scores_dig, scores_three]
    finger_penalty_qwerty, finger_penalty_phon, finger_penalty_diktor = list(
        map(
            lambda x: calc_penalty(*x),
            zip(
                (statistics, statistics, statistics),
                (QWERTY_LAYOUT, PHON_LAYOUT, DIKTOR_LAYOUT),
            )
        )
    )

    log.info('Штрафы\n\tЙЦУКЕН: %s\n\t Фонетический: %s\n\t Диктор: %s',
             finger_penalty_qwerty,
             finger_penalty_phon,
             finger_penalty_diktor)

    plot_by_stat(
        scores,
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
