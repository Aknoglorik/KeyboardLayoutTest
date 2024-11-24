import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from config import Finger
import random

class StatisticDrawer:
    def __init__(self, labels, loads1, loads2, loads3, txt_name, layout, layout2, layout3):
        self.labels = labels
        self.loads1 = loads1
        self.loads2 = loads2
        self.loads3 = loads3

        self.layout = layout
        self.layout2 = layout2
        self.layout3 = layout3

        self.txt_name = txt_name

        self.num_groups = len(labels)
        self.width = 0.3
        self.x_pos = list(range(self.num_groups))

        self.colors_list = [
            'red',
            'blue',
            'green',
            'black',
        ]
    
    def draw_value(self, bars, ax):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)),
                    ha='center', va='bottom')
    
    def draw_bars(self, ax, position, name):
        bars1 = ax.bar([i - self.width for i in self.x_pos[position]], self.loads1[position], self.width, label=self.layout, color=self.colors_list[0])
        bars2 = ax.bar(self.x_pos[position], self.loads2[position], self.width, label=self.layout2, color=self.colors_list[1])
        bars3 = ax.bar([i + self.width for i in self.x_pos[position]], self.loads3[position], self.width, label=self.layout3, color=self.colors_list[2])
        
        ax.set_ylabel('Проценты нагрузки (%)')
        ax.set_title(f'Нагрузка на {name} руке')
        ax.set_xticks(self.x_pos[position])
        ax.set_xticklabels(self.labels[position])
        ax.legend()

        self.draw_value(bars1, ax)
        self.draw_value(bars2, ax)
        self.draw_value(bars3, ax)

    def show_result(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f'Нагрузка на пальцы\n Текст - {self.txt_name}', fontsize=16)
        
        self.draw_bars(ax1, slice(None, 4), 'левой')
        self.draw_bars(ax2, slice(4, None), 'правой')
        
        plt.tight_layout()
        plt.show()


def plot_by_stat(statistic: dict[Finger, int], statistic2: dict[Finger, int],
                 statistic3: dict[Finger, int],
                 layout: str, layout2: str, layout3: str, txt_name: str):
    '''
    @brief Функция для построенния графиков сравнения статистик нажатия на
    клавиши, при разных раскладках.
    '''

    loads1 = [statistic[name.value] for name in
                (Finger.LPinky, Finger.LRing, Finger.LMiddle, Finger.LIndex,
                Finger.RIndex, Finger.RMiddle, Finger.RRing, Finger.RPinky)]

    loads2 = [statistic2[name.value] for name in
                (Finger.LPinky, Finger.LRing, Finger.LMiddle, Finger.LIndex,
                Finger.RIndex, Finger.RMiddle, Finger.RRing, Finger.RPinky)]
    
    loads3 = [statistic3[name.value] for name in
                (Finger.LPinky, Finger.LRing, Finger.LMiddle, Finger.LIndex,
                Finger.RIndex, Finger.RMiddle, Finger.RRing, Finger.RPinky)]

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

    draw = StatisticDrawer(labels, loads1, loads2, loads3, txt_name, layout, layout2, layout3)
    draw.show_result()

if __name__ == '__main__':
    statistic = {member: random.randint(1, 100) for member in Finger}
    plot_by_stat(statistic)
