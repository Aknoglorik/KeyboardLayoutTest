import unittest

import fingercalc


class TestConfig(unittest.TestCase):
    '''
    @brief Класс для тестирования корректности сформированных данных.
    '''

    def test_layout(self):
        '''
        @brief Проверить что в LAYOUT_QWERTY у разных пальцев нет одинаковых
        клавиш.

        @warning Возможно это бесполезная функция... Лучше ее пока не делать.
        '''
        pass


class TestFingerCalc(unittest.TestCase):
    '''
    @brief Класс для тестирования корректности функций рассчета кол-ва нажатий.
    '''
    def test_isRussian(self):
        '''
        @brief Проверка символа на принадлежность к русскому алфавиту.
        '''
        self.assertFalse(fingercalc.isRussian('w'))
        self.assertTrue(fingercalc.isRussian('е'))
        self.assertTrue(fingercalc.isRussian('й'))
        pass

    def test_get_info_from_file(self):
        '''
        @brief Передать в соответсвующую функцю имя файла (файл небольшой для
        теста) после сравнить правильность полученных результатов с уже
        известными.
        '''
        my_stat = fingercalc.get_info_from_file('test1.txt')
        correct_stat = {
            'ф': 1,
            'я': 2,
            'ч': 3,
            'ц': 4,
        }
        self.assertCountEqual(my_stat, correct_stat)


if __name__ == "__main__":
    unittest.main()
