import unittest


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

    def test_get_info_from_file(self):
        '''
        @brief Передать в соответсвующую функцю имя файла (файл небольшой для
        теста) после сравнить правильность полученных результатов с уже
        известными.
        '''
        pass

    def test_count_line(self):
        '''
        @brief Несколько раз передать в соответсвующую функцию разные строчки.
        Сравнить полученные результаты с уже известными.
        '''
        pass


def test_app() -> None:
    unittest.main()
