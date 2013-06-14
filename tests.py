# coding=utf-8
from decimal import Decimal
import unittest2 as unittest
from amverb import AmountVerbally, IncorrectNumber


class AmountVerballyTest(unittest.TestCase):
    def setUp(self):
        self.av = AmountVerbally()

    def test_verbal_for_numbers_from_11_to_19(self):
        numbers = [u'jedenaście', u'dwanaście', u'trzynaście', u'czternaście', u'piętnaście',
                   u'szesnaście', u'siedemnaście', u'osiemnaście', u'dziewiętnaście']
        for i, number in enumerate(numbers, 11):
            self.assertEqual(self.av._verbal(i), number)

    def test_verbal_for_number_21(self):
        self.assertEqual(self.av._verbal(21), u'dwadzieścia jeden')

    def test_verbal_for_number_148(self):
        self.assertEqual(self.av._verbal(148), u'sto czterdzieści osiem')

    def test_verbal_for_number_235(self):
        self.assertEqual(self.av._verbal(235), u'dwieście trzydzieści pięć')

    def test_verbal_for_number_305(self):
        self.assertEqual(self.av._verbal(305), u'trzysta pięć')

    def test_verbal_for_number_418(self):
        self.assertEqual(self.av._verbal(418), u'czterysta osiemnaście')

    def test_verbal_for_number_574(self):
        self.assertEqual(self.av._verbal(574), u'pięćset siedemdziesiąt cztery')

    def test_verbal_for_number_614(self):
        self.assertEqual(self.av._verbal(614), u'sześćset czternaście')

    def test_verbal_for_number_782(self):
        self.assertEqual(self.av._verbal(782), u'siedemset osiemdziesiąt dwa')

    def test_verbal_for_number_857(self):
        self.assertEqual(self.av._verbal(857), u'osiemset pięćdziesiąt siedem')

    def test_verbal_for_number_913(self):
        self.assertEqual(self.av._verbal(913), u'dziewięćset trzynaście')

    def test_fraction_suffix_variant_1(self):
        self.av._fraction = 1
        self.assertIn('grosz', self.av._fraction_verbally())

    def test_fraction_suffix_variant_2(self):
        for i in [2, 3, 4, 22, 23, 24]:
            expected_suffix = 'grosze'
            self.av._fraction = i
            suffix = self.av._fraction_verbally()[1]
            if suffix != expected_suffix:
                raise AssertionError('"%s %s" != "%s %s"' % (i, suffix, i, expected_suffix))

    def test_fraction_suffix_variant_3(self):
        for i in [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
            expected_suffix = 'groszy'
            self.av._fraction = i
            suffix = self.av._fraction_verbally()[1]
            if suffix != expected_suffix:
                raise AssertionError('"%s %s" != "%s %s"' % (i, suffix, i, expected_suffix))

    def test_omit_empty_suffixes(self):
        self.av._main = 1000000234
        self.av._fraction = 0
        amount_in_words = u'jeden miliard dwieście trzydzieści cztery złote i zero groszy'
        self.assertEqual(self.av.verbally(), amount_in_words)

    def test_omit_zero_for_big_amounts(self):
        self.av._main = 1000
        self.av._fraction = 0
        amount_in_words = u'jeden tysiąc złotych i zero groszy'
        self.assertEqual(self.av.verbally(), amount_in_words)

    def test_sanity_for_main_currency(self):
        self.av._main = 0
        self.av._fraction = 1
        amount_in_words = u'zero złotych i jeden grosz'
        self.assertEqual(self.av.verbally(), amount_in_words)

    def test_amount_not_provided_main(self):
        self.av._fraction = 0
        self.assertRaises(IncorrectNumber, self.av.verbally)

    def test_amount_not_provided_fraction(self):
        self.av._main = 0
        self.assertRaises(IncorrectNumber, self.av.verbally)

    def test_amount_accepts_integer_numbers(self):
        self.av.amount(1)
        self.assertEqual(self.av._main, 1)
        self.assertEqual(self.av._fraction, 0)

    def test_amount_accepts_float_numbers(self):
        self.av.amount(2.03)
        self.assertEqual(self.av._main, 2)
        self.assertEqual(self.av._fraction, 3)
        self.av.amount(4.5)
        self.assertEqual(self.av._main, 4)
        self.assertEqual(self.av._fraction, 50)

    def test_amount_accepts_decimal_numbers(self):
        self.av.amount(Decimal(6))
        self.assertEqual(self.av._main, 6)
        self.assertEqual(self.av._fraction, 0)

    def test_amount_accepts_valid_string_numbers(self):
        self.av.amount('7')
        self.assertEqual(self.av._main, 7)
        self.assertEqual(self.av._fraction, 0)

    def test_amount_accepts_valid_string_numbers_with_comma(self):
        self.av.amount('8,09')
        self.assertEqual(self.av._main, 8)
        self.assertEqual(self.av._fraction, 9)

    def test_amount_fractional_currency_too_big(self):
        self.assertRaises(IncorrectNumber, self.av.amount, '0.123')

    def test_invalid_number(self):
        self.assertRaises(IncorrectNumber, self.av.amount, '0xa')

    def test_too_big_number(self):
        self.assertRaises(IncorrectNumber, self.av.amount, 1200300400500)


if __name__ == '__main__':
    unittest.main()
