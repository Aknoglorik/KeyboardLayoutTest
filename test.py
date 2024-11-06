import unittest
import config
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
            'а': 1,
            'б': 2,
            'в': 3,
            'г': 4,
            'д': 5,
            'е': 6,
            'ё': 7,
            'ж': 8,
            'з': 9,
            'и': 10,
            'й': 11,
            'к': 12,
            'л': 13,
            'м': 14,
            'н': 15,
            'о': 16,
            'п': 17,
            'р': 18,
            'с': 19,
            'т': 20,
            'у': 21,
            'ф': 22,
            'х': 23,
            'ц': 24,
            'ч': 25,
            'ш': 26,
            'щ': 27,
            'ъ': 28,
            'ы': 29,
            'ь': 30,
            'э': 31,
            'ю': 32,
            'я': 33,
        }
        self.assertCountEqual(my_stat, correct_stat)
    def test_count_to_score(self):
        '''
        @brief Принятие "Раскладки" (load_layout) и статистики нажатия на клавиши
        (get_info_from_file) и подсчитывание кол-ва нажатий пальцем.
        '''
        QWERTY_LAYOUT = config.load_layout(r'testlayouts/qwerty.toml')
        text = fingercalc.get_info_from_file('testfiles/test.txt')
        my_date = fingercalc.count_to_score(text, QWERTY_LAYOUT)
        date = {
          'lpinky': 0,
          'lring': 0,
          'lmiddle': 0,
          'lindex': 5,
          'lthumb': 1,
          'rpinky': 2,
          'rring': 0,
          'rmiddle': 0,
          'rindex': 0,
        }
        self.assertEqual(date, my_date)   
if __name__ == "__main__":
    unittest.main()
