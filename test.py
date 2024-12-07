import unittest
import config
import fingercalc
from unittest import IsolatedAsyncioTestCase

events = []

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


class TestFingerCalc(IsolatedAsyncioTestCase):
    '''
    @brief Класс для тестирования корректности функций рассчета кол-ва нажатий.
    '''
class TestLayoutOrders(IsolatedAsyncioTestCase) :
    async def test_get_bust_orders(self):   
        '''
        @brief возвращает лист состоящий из кортежей, где i-ый элеемент отвечает на
        вопрос "можно ли перебрать текст одной рукой" для i-ой раскладки. Кортеж
        состоит из:
            - [0] способ перебора правой рукой
            - [1] способ перебора левой рукой
        '''
        qwerty_layout = await config.load_layout(r'testlayouts/qwerty.toml')
        diktor_layout = await config.load_layout(r'testlayouts/diktor.toml')
        phon_layout = await config.load_layout(r'testlayouts/phonetikal.toml')
    
        result = [(fingercalc.BustOrder.DIRECT,fingercalc.BustOrder.NONE)]
        my_date1 = fingercalc.get_bust_orders('фыва',qwerty_layout)
        my_date2 = fingercalc.get_bust_orders('заря',diktor_layout)
        my_date3 = fingercalc.get_bust_orders('рома',phon_layout)
        my_date4 = fingercalc.get_bust_orders('вася',phon_layout,qwerty_layout)
    
        self.assertEqual(result, my_date1, my_date2)                                     
        pass

    def test_isRussian(self):
        '''
        @brief Проверка символа на принадлежность к русскому алфавиту.
        '''
        self.assertFalse(fingercalc.isRussian('w'))
        self.assertTrue(fingercalc.isRussian('е'))
        self.assertTrue(fingercalc.isRussian('й'))
        pass

    async def test_get_info_from_file(self):
        '''
        @brief Передать в соответсвующую функцю имя файла (файл небольшой для
        теста) после сравнить правильность полученных результатов с уже
        известными.
        '''
        my_stat = await fingercalc.get_info_from_file('test1.txt')
        my_stat = my_stat[0]
        correct_stat = {
            'а': 1,
            'б': 1,
            'в': 1,
            'г': 1,
            'д': 1,
            'е': 1,
            'ё': 1,
            'ж': 1,
            'з': 1,
            'и': 1,
            'й': 1,
            'к': 1,
            'л': 1,
            'м': 1,
            'н': 1,
            'о': 1,
            'п': 1,
            'р': 1,
            'с': 1,
            'т': 1,
            'у': 1,
            'ф': 1,
            'х': 1,
            'ц': 1,
            'ч': 1,
            'ш': 1,
            'щ': 1,
            'ъ': 1,
            'ы': 1,
            'ь': 1,
            'э': 1,
            'ю': 1,
            'я': 1,
        }
        self.assertCountEqual(my_stat.items(), correct_stat.items())

    async def test_count_to_score(self):
        '''
        @brief Принятие "Раскладки" (load_layout) и статистики нажатия на
        клавиши (get_info_from_file) и подсчитывание кол-ва нажатий пальцем.
        '''
        QWERTY_LAYOUT = await config.load_layout(r'testlayouts/qwerty.toml')
        text = await fingercalc.get_info_from_file('testfiles/test.txt')
        my_date = await fingercalc.count_to_score(text, QWERTY_LAYOUT)
        date = {
          'lpinky': 0,
          'lring': 0,
          'lmiddle': 0,
          'lindex': 5,
          'lthumb': 1,
          'rpinky': 1,
          'rring': 0,
          'rmiddle': 0,
          'rindex': 1,
          'rthumb': 0,
        }
        self.assertCountEqual(date.items(), my_date.items())


if __name__ == "__main__":
    unittest.main()
