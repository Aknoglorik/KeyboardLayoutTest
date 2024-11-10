import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from config import Finger
import random

# letters ?

def plot_by_stat(statistic: dict[Finger, int], statistic2: dict[Finger, int], layout, layout2, txt_name):

    values = list(statistic.values())

    colors_list = [
        'blue',
        'green',
        'red',
        'purple',
    ]

    # inner
    def update_graph(event):
        ax1.clear()
        ax2.clear()

        nonlocal click_button

        if click_button:
            ax1.barh(
                labels_left[::-1],
                loads_left[::-1],
                color=[colors_list[0], colors_list[0], colors_list[1], colors_list[1], \
                    colors_list[2], colors_list[2], colors_list[3], colors_list[3]],
                height=0.5
            )

            ax1.set_xlabel('Проценты нагрузки (%)')
            ax1.set_ylabel('Название пальца')
            ax1.set_title('Нагрузка на левой руке', loc='left')

            ax2.barh(
                labels_right[::-1],
                loads_right[::-1],
                color=[colors_list[0], colors_list[0], colors_list[1], colors_list[1], \
                    colors_list[2], colors_list[2], colors_list[3], colors_list[3]],
                height=0.5
            )

            ax2.set_xlabel('Проценты нагрузки (%)')
            ax2.set_ylabel('Название пальца')
            ax2.set_title('Нагрузка на правой руке', loc='left')

            max_load = max(values) + 5
            ax1.set_xlim(0, max_load)
            ax2.set_xlim(0, max_load)
            
        else:
            loads1 = loads_left + loads_right

            labels_left_alt = [word + ' левый' for word in (s.split()[0] for s in labels_right)]
            labels_right_alt = [word + ' правый' for word in (s.split()[0] for s in labels_right)]
            labels1 = labels_left_alt + labels_right_alt

            ax1.pie(loads1[0::2], labels=labels1[0::2], autopct='%1.1f%%', startangle=140)
            ax1.axis('equal')
            ax1.set_title(f'{layout}')

            ax2.pie(loads1[1::2], labels=labels1[1::2], autopct='%1.1f%%', startangle=140)
            ax2.axis('equal')
            ax2.set_title(f'{layout2}')
            
        click_button = not click_button
        plt.draw()

    loads_right = [
        statistic[Finger.RPinky.value],
        statistic2[Finger.RPinky.value],
        statistic[Finger.RRing.value],
        statistic2[Finger.RRing.value],
        statistic[Finger.RMiddle.value],
        statistic2[Finger.RMiddle.value],
        statistic[Finger.RIndex.value],
        statistic2[Finger.RIndex.value]
    ]

    loads_left = [
        statistic[Finger.LPinky.value],
        statistic2[Finger.LPinky.value],
        statistic[Finger.LRing.value],
        statistic2[Finger.LRing.value],
        statistic[Finger.LMiddle.value],
        statistic2[Finger.LMiddle.value],
        statistic[Finger.LIndex.value],
        statistic2[Finger.LIndex.value],
    ]

    labels_right = [
        f'Мизинец ({layout})',
        f'Мизинец ({layout2})',
        f'Безымянный ({layout})',
        f'Безымянный ({layout2})',
        f'Средний ({layout})',
        f'Средний ({layout2})',
        f'Указательный ({layout})',
        f'Указательный ({layout2})',
    ]

    labels_left = [
        f'Мизинец ({layout})',
        f'Мизинец ({layout2})',
        f'Безымянный ({layout})',
        f'Безымянный ({layout2})',
        f'Средний ({layout})',
        f'Средний ({layout2})',
        f'Указательный ({layout})',
        f'Указательный ({layout2})',
    ]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 12), constrained_layout=True)
    fig.suptitle(
        f'Нагрузка на пальцы\nРаскладки - {layout}, {layout2}\nТекст - {txt_name}'
    )
    
    #fig.tight_layout(rect=[0.05, 0.05, 1, 0.95])
    fig.set_constrained_layout_pads(rect=[0, 0.05, 0.98, 0.9])

    click_button = True
    ax_button = plt.axes([0.05, 0.9, 0.1, 0.075])
    button = Button(ax_button, 'switch')
    button.on_clicked(update_graph)
    update_graph(None)
    
    plt.show()


if __name__ == '__main__':
    statistic = {member: random.randint(1, 100) for member in Finger}
    plot_by_stat(statistic)
