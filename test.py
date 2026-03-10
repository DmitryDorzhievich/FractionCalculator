import unittest
from fractions import Fraction

# импортируем из main.py функции для тестирования
from main import parse_number, calculate, to_mixed

class TestCalculator(unittest.TestCase):

    def test_parse_number(self):
        # целые
        self.assertEqual(parse_number("5"), Fraction(5,1))
        self.assertEqual(parse_number("-3"), Fraction(-3,1))

        # дроби
        self.assertEqual(parse_number("3/4"), Fraction(3,4))
        self.assertEqual(parse_number("-7/8"), Fraction(-7,8))

        # смешанные
        self.assertEqual(parse_number("1 2/3"), Fraction(5,3))
        self.assertEqual(parse_number("-1 1/2"), Fraction(-3,2))

    def test_calculate(self):
        self.assertEqual(calculate("1/2 + 4 5/6"), Fraction(16,3))
        self.assertEqual(calculate("-1 1/2 + 4 5/6"), Fraction(10,3))
        self.assertEqual(calculate("2/3 - 1/6"), Fraction(1,2))
        self.assertEqual(calculate("1 1/2 * 2"), Fraction(3,1))
        self.assertEqual(calculate("3/4 : 1/2"), Fraction(3,2))

    def test_to_mixed(self):
        # проверка выделения целой части
        self.assertEqual(to_mixed(Fraction(31,12)), (2, Fraction(7,12)))
        self.assertEqual(to_mixed(Fraction(-5,3)), (-1, Fraction(2,3)))
        self.assertEqual(to_mixed(Fraction(4,2)), (2, None))

if __name__ == "__main__":
    unittest.main()