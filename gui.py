import matplotlib.pyplot as plt
from config import Finger
import random

def plot_by_stat(statistic: dict[Finger, int]): 

    keys = list(statistic.keys())
    values = list(statistic.values())

    loads2 = [
        statistic[Finger.RPinky.value()],
        statistic[Finger.RRing.value()],
        statistic[Finger.RMiddle.value()],
        statistic[Finger.RIndex.value()]
    ]

    loads1 = [
        statistic[Finger.LPinky.value()],
        statistic[Finger.LRing.value()],
        statistic[Finger.LMiddle.value()],
        statistic[Finger.LIndex.value()],
    ]
    
    labels2 = [
        Finger.RPinky,
        Finger.RRing,
        Finger.RMiddle,
        Finger.RIndex,
    ]

    labels1 = [
        Finger.LPinky,
        Finger.LRing,
        Finger.LMiddle,
        Finger.LIndex,
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # на всякий через файл
    ''' 
    with open('loads.txt', 'r') as file:
        data = file.read().strip()

    loads = list(map(float, data.split()))

    '''

    # color=['blue', 'green', 'red', 'purple', 'yellow']

    ax1.barh(labels1[::-1], loads1[::-1], color=['blue', 'green', 'red', 'purple'], height=0.25)

    ax1.set_xlabel('Проценты нагрузки (%)')
    ax1.set_ylabel('Название пальца')
    ax1.set_title('Нагрузка на левой руке')

    ax2.barh(labels2[::-1], loads2[::-1], color=['blue', 'green', 'red', 'purple'], height=0.25)

    ax2.set_xlabel('Проценты нагрузки (%)')
    #ax2.set_ylabel('Название пальца')
    ax2.set_title('Нагрузка на правой руке')

    fig.suptitle('Нагрузка на пальцы')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    max_load = max(values) + 10
    ax1.set_xlim(0, max_load)
    ax2.set_xlim(0, max_load)

    plt.show()


if __name__ == '__main__':
    # пока рандом
    statistic = {member: random.randint(1, 100) for member in Finger}
    plot_by_stat(statistic)