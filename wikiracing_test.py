import unittest

from wikiracing import WikiRacer


class WikiRacerTest(unittest.TestCase):

    racer = WikiRacer()

    def test_correct_path(self):
        correct_data = {'title': 'Рим', 'distance': 2, 'parent':
            {'title': 'Якопо Понтормо', 'distance': 1, 'parent':
                {'title': 'Дружба', 'distance': 0, 'parent': None}
             }}
        actual_path = ['Дружба', 'Якопо Понтормо', 'Рим']
        self.assertEqual(self.racer.print_path(correct_data), actual_path)

    def test_1(self):
        path = self.racer.find_path('Дружба', 'Рим')
        self.assertEqual(path, ['Дружба', 'Якопо Понтормо', 'Рим'])

    def test_2(self):
        path = self.racer.find_path('Мітохондріальна ДНК', 'Вітамін K')
        self.assertEqual(path, ['Мітохондріальна ДНК', 'Бактерії', 'Вітамін K'])

    def test_3(self):
        path = self.racer.find_path('Марка (грошова одиниця)', 'Китайський календар')
        self.assertEqual(path, ['Марка (грошова одиниця)', '1915', 'Китайський календар'])

    def test_4(self):
        path = self.racer.find_path('Фестиваль', 'Пілястра')
        self.assertEqual(path, ['Фестиваль', 'Замок (споруда)', 'Атріум', 'Пілястра'])

    def test_5(self):
        path = self.racer.find_path('Дружина (військо)', '6 жовтня')
        self.assertEqual(path, ['Дружина (військо)', 'Друга світова війна', '6 жовтня'])


if __name__ == '__main__':
    unittest.main()
