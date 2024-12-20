import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from config import Finger
from fingercalc import BustOrder

class StatisticDrawer:
    def __init__(self, labels, loads, txt_name, layouts, score, names):
        self.labels = labels
        self.loads = loads

        self.layouts = layouts
        self.txt_name = txt_name

        self.names = names
        self.score = score

        self.width = 0.3
        self.num_groups = len(labels)
        self.x_pos = list(range(self.num_groups))
        self.x_pos2 = list(range(len(names)))

        self.max_score1 = max(self.loads[0])
        self.max_score2 = max(self.score[2])

        self.colors_list = [
            'red',
            'blue',
            'green',
            'black',
        ]

        self.show_button = True

    def draw_value(self, bars, ax):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(int(height)),
                ha='center',
                va='bottom'
            )

    def draw_bars(self, ax, x_pos, position, loads, layouts, width):
        self.bars1 = ax.bar(
            [i - width for i in x_pos[position]],
            loads[0][position],
            width,
            label=layouts[0],
            color=self.colors_list[0]
        )
        self.bars2 = ax.bar(
            x_pos[position],
            loads[1][position],
            width,
            label=layouts[1],
            color=self.colors_list[1]
        )
        self.bars3 = ax.bar(
            [i + width for i in x_pos[position]],
            loads[2][position],
            width,
            label=layouts[2],
            color=self.colors_list[2]
        )

        self.draw_value(self.bars1, ax)
        self.draw_value(self.bars2, ax)
        self.draw_value(self.bars3, ax)

    def draw_axs(self, ax, position, name, x_pos, loads, labels, max_score):
        self.draw_bars(ax, x_pos, position, loads, self.layouts,
                       self.width)
        ax.set_ylabel('Очки нагрузки')
        ax.set_title(f'Нагрузка на {name} руке')
        ax.set_xticks(x_pos[position])
        ax.set_xticklabels(labels[position])
        ax.legend()

        ax.set_ylim(0, max_score + (max_score/6))

    def click_button(self, event):
        if self.show_button:
            self.ax1.set_visible(False)
            self.ax2.set_visible(False)
            self.title1.set_visible(False)
            if len(self.fig.get_axes()) > 2:
                self.fig.delaxes(self.fig.get_axes()[2])

            self.title2 = self.fig.suptitle(
            'Очки за перебор одной рукой',
            fontsize=16
            )
            self.ax3 = self.fig.add_subplot(1,2,1)
            self.ax4 = self.fig.add_subplot(1,2,2)
            
            self.draw_axs(self.ax3, slice(None, 3), 'левой', self.x_pos2, self.score, self.names, self.max_score2)
            self.draw_axs(self.ax4, slice(3, None), 'правой', self.x_pos2, self.score, self.names, self.max_score2)

            self.show_button = False
        else:
            if len(self.fig.get_axes()) > 2:
                self.fig.delaxes(self.fig.get_axes()[2])
            self.ax3.set_visible(False)
            self.ax4.set_visible(False)
            self.title2.set_visible(False)
            self.ax1.set_visible(True)
            self.ax2.set_visible(True)
            self.title1.set_visible(True)
            self.show_button = True

        plt.gcf().canvas.draw_idle()

    def show_result(self):

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        self.title1 = self.fig.suptitle(
            f'Нагрузка на пальцы\n Текст - {self.txt_name}',
            fontsize=16
        )

        self.draw_axs(self.ax1, slice(None, 4), 'левой', self.x_pos, self.loads, self.labels, self.max_score1)
        self.draw_axs(self.ax2, slice(4, None), 'правой', self.x_pos, self.loads, self.labels, self.max_score1)

        ax_button = plt.axes([0.02, 0.9, 0.1, 0.075])  # l/b/w/h
        button = Button(ax_button, 'switch')
        button.on_clicked(self.click_button)

        plt.tight_layout()
        plt.show()


def plot_by_stat(
        score: list,
        statistic: dict[Finger, int], statistic2: dict[Finger, int],
        statistic3: dict[Finger, int],
        layout: str, layout2: str, layout3: str, txt_name: str,
                ):
    '''
    @brief Функция для построенния графиков сравнения статистик нажатия на
    клавиши, при разных раскладках.
    '''

    fingers = (Finger.LPinky, Finger.LRing, Finger.LMiddle, Finger.LIndex,
               Finger.RIndex, Finger.RMiddle, Finger.RRing, Finger.RPinky)

    loads1 = [statistic[name.value] for name in fingers]
    loads2 = [statistic2[name.value] for name in fingers]
    loads3 = [statistic3[name.value] for name in fingers]
    loads_list = [loads1, loads2, loads3]

   # очки/рука/раскладка
    scores1 = [score[i][j][0].get(BustOrder.DIRECT) for i in range(3) for j in range(2)]
    scores2 = [score[i][j][1].get(BustOrder.DIRECT) for i in range(3) for j in range(2)]
    scores3 = [score[i][j][2].get(BustOrder.DIRECT) for i in range(3) for j in range(2)]
    score_list = [scores1, scores2, scores3]

    layout_list = [layout, layout2, layout3]

    labels = [
        'Мизинец \nleft',
        'Безымянный \nleft',
        'Средний \nleft',
        'Указательный \nleft',
        'Указательный \nright',
        'Средний \nright',
        'Безымянный \nright',
        'Мизинец \nright',
    ]

    names = [
        'Наиболее \nраспространенных диграмм',
        'Диграмм \nиз 1grams-3',
        'Триграмм \nиз 1grams-3'
    ]

    new_names = names *2

    draw = StatisticDrawer(
        labels,
        loads_list,
        txt_name,
        layout_list,
        score_list,
        new_names
    )
    draw.show_result()


if __name__ == '__main__':
    import random

    statistic = {member: random.randint(1, 100) for member in Finger}
    plot_by_stat(statistic)
