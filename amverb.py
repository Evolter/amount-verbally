#!/usr/bin/python
# coding=utf-8
__author__ = 'Evolter'
from decimal import Decimal, InvalidOperation


class IncorrectNumber(Exception):
    pass


class AmountVerbally(object):
    """Presents number as an amount in words with Polish currency."""
    _numbers = [
        {
            1: u'sto', 2: u'dwieście', 3: u'trzysta', 4: u'czterysta', 5: u'pięćset', 6: u'sześćset', 7: u'siedemset',
            8: u'osiemset', 9: u'dziewięćset'
        }, {
            1: u'dziesięć', 2: u'dwadzieścia', 3: u'trzydzieści', 4: u'czterdzieści', 5: u'pięćdziesiąt',
            6: u'sześćdziesiąt', 7: u'siedemdziesiąt', 8: u'osiemdziesiąt', 9: u'dziewięćdziesiąt'
        }, {
            1: u'jeden', 2: u'dwa', 3: u'trzy', 4: u'cztery', 5: u'pięć', 6: u'sześć', 7: u'siedem', 8: u'osiem',
            9: u'dziewięć', 10: u'dziesięć', 11: u'jedenaście', 12: u'dwanaście', 13: u'trzynaście', 14: u'czternaście',
            15: u'piętnaście', 16: u'szesnaście', 17: u'siedemnaście', 18: u'osiemnaście', 19: u'dziewiętnaście'
        }
    ]
    _magnitude = [
        [u'miliard', u'miliardy', u'miliardów'],
        [u'milion', u'miliony', u'milionów'],
        [u'tysiąc', u'tysiące', u'tysięcy']
    ]
    _main_currency = [u'złoty', u'złote', u'złotych']
    _fractional_currency = [u'grosz', u'grosze', u'groszy']

    def __repr__(self):
        try:
            return '%s.%s' % (self._main, self._fraction)
        except AttributeError:
            return 'Amount not provided.'

    def _suffix_variation(self, number):
        if number == 1:
            return 0
        if number % 100 / 10 != 1 and 1 < number % 10 < 5:
            return 1
        return 2

    def _verbal(self, amount):
        hundreds = amount / 100
        amount %= 100
        if amount > 19:
            tens = amount / 10 % 10
            units = amount % 10
        else:
            tens = 0
            units = amount
        numbers = []
        for i, number in enumerate([hundreds, tens, units]):
            if not number:
                continue
            numbers.append(self._numbers[i][number])
        return ' '.join(numbers)

    def _fraction_verbally(self):
        return self._verbal(self._fraction) or 'zero', self._fractional_currency[self._suffix_variation(self._fraction)]

    def _main_verbally(self):
        if not self._main:
            return [('zero', self._main_currency[self._suffix_variation(0)])]
        amount = self._main
        numbers = []
        while True:
            if not amount:
                break
            numbers.append(amount % 1000)
            amount /= 1000
        numbers_and_suffixes = []
        for magnitude_index, number in zip(xrange(3, -1, -1), numbers):
            number_in_words = self._verbal(number)
            suffix_variation = self._suffix_variation(number)
            try:
                suffix = self._magnitude[magnitude_index][suffix_variation]
            except IndexError:
                suffix = self._main_currency[suffix_variation]
                numbers_and_suffixes.append((number_in_words, suffix) if number_in_words else [suffix])
            else:
                if number_in_words:
                    numbers_and_suffixes.append((number_in_words, suffix))
        return numbers_and_suffixes.__reversed__()

    def amount(self, number):
        """Set amount."""
        amount = str(number).replace(',', '.')
        try:
            Decimal(amount)
        except InvalidOperation:
            raise IncorrectNumber('"%s" is not a correct number.' % number)
        try:
            main, fraction = amount.split('.')
        except ValueError:
            self._main = int(amount)
            self._fraction = 0
        else:
            self._main = int(main)
            self._fraction = int(fraction) if len(fraction) > 1 else int(fraction) * 10
        if self._main > 999999999999:
            raise IncorrectNumber('Too big value: "%s" is not supported.' % number)
        if self._fraction > 99:
            raise IncorrectNumber('Fractional currency is too big.')

    def verbally(self):
        """Return amount in words."""
        if not (hasattr(self, '_main') and hasattr(self, '_fraction')):
            raise IncorrectNumber('Number not provided - use "amount" method.')
        main = [' '.join(number_suffix) for number_suffix in self._main_verbally()]
        return u'%s i %s' % (' '.join(main), ' '.join(self._fraction_verbally()))
