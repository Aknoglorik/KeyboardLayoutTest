import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from config import Finger
import random

class StatisticDrawer:
    def __init__(self, labels, loads, txt_name, layouts, score, names):
        self.labels = labels
        self.loads = loads

        self.layouts = layouts
        self.txt_name = txt_name

        self.names = names
        self.score = [list(x) for x in zip(*score)]

        self.width = 0.3
        self.num_groups = len(labels)
        self.x_pos = list(range(self.num_groups))

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
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)),
                    ha='center', va='bottom')
            
    def draw_bars(self, ax, x_pos, position, loads, layouts, width):
        self.bars1 = ax.bar([i - width for i in x_pos[position]], loads[0][position], width, label=layouts[0], color=self.colors_list[0])
        self.bars2 = ax.bar(x_pos[position], loads[1][position], width, label=layouts[1], color=self.colors_list[1])
        self.bars3 = ax.bar([i + width for i in x_pos[position]], loads[2][position], width, label=layouts[2], color=self.colors_list[2])
        
        self.draw_value(self.bars1, ax)
        self.draw_value(self.bars2, ax)
        self.draw_value(self.bars3, ax) 
         
    def draw_axs(self, ax, position, name):
        
        self.draw_bars(ax, self.x_pos, position, self.loads, self.layouts, self.width)
        
        ax.set_ylabel('Проценты нагрузки (%)')
        ax.set_title(f'Нагрузка на {name} руке')
        ax.set_xticks(self.x_pos[position])
        ax.set_xticklabels(self.labels[position])
        ax.legend()

        ax.set_ylim(0,max(self.loads[0]) + 5)
    
    def click_button(self, event):
        if self.show_button:
            self.ax1.set_visible(False)
            self.ax2.set_visible(False)
            if len(self.fig.get_axes()) > 2:
                self.fig.delaxes(self.fig.get_axes()[2])
            
            ax_single = self.fig.add_subplot(111)
            self.draw_bars(ax_single, list(range(len(self.names))), slice(None), self.score, self.layouts, self.width)
            ax_single.set_ylim(0, max(self.score[2]) + 50)
            ax_single.set_xticks(list(range(len(self.names))))
            ax_single.set_xticklabels(self.names)
            ax_single.legend()

            self.show_button = False
        else:
            if len(self.fig.get_axes()) > 2:
                self.fig.delaxes(self.fig.get_axes()[2])
            self.ax1.set_visible(True)
            self.ax2.set_visible(True)
            self.show_button = True
            
        plt.gcf().canvas.draw_idle()

    def show_result(self):

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.suptitle(f'Нагрузка на пальцы\n Текст - {self.txt_name}', fontsize=16)

        self.draw_axs(self.ax1, slice(None, 4), 'левой')
        self.draw_axs(self.ax2, slice(4, None), 'правой')

        ax_button = plt.axes([0.02, 0.9, 0.1, 0.075])  # l/b/w/h
        button = Button(ax_button, 'switch')
        button.on_clicked(self.click_button)

        plt.tight_layout()
        plt.show()


def plot_by_stat(score: list, 
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

    layout_list = [layout, layout2, layout3]

    labels = [
        f'Мизинец \nleft',
        f'Безымянный \nleft',
        f'Средний \nleft',
        f'Указательный \nleft',
        f'Указательный \nright',
        f'Средний \nright',
        f'Безымянный \nright',        
        f'Мизинец \nright',
    ]

    names = [
        'Очки за перебор одной рукой \nнаиболее распространенных диграмм',
        'Очки за перебор одной рукой \nдиграмм из 1grams-3',
        'Очки за перебор одной рукой \nтриграмм из 1grams-3'
    ]

    draw = StatisticDrawer(labels, loads_list, txt_name, layout_list, score, names)
    draw.show_result()

if __name__ == '__main__':
    statistic = {member: random.randint(1, 100) for member in Finger}
    plot_by_stat(statistic)
