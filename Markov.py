#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import collections


class Markov(object):
    """
    Text generator based on markov chains.
    """

    def __init__(self, prob=True, level=2):
        """
        Never change level after object is created
        """
        self._database = {}
        self._use_prob = prob
        self._level = level

    def _new_entry(self, key, value):
        """
        Add new entry to database
        """
        val_pos = None

        if key in self._database:
            for pos, val in enumerate(self._database[key]):
                if val[0] == value:
                    val_pos = pos

            if val_pos is None:
                self._database[key].append((value, 1))
            else:
                if self._use_prob:
                    new_tuple = (self._database[key][val_pos][0],
                                 self._database[key][val_pos][1] + 1)
                    self._database[key][val_pos] = new_tuple

        else:
            self._database[key] = [(value, 1)]

    def parse(self, text):
        """
        Parse first argument based on level
        """
        if len(text) < self._level + 1:
            raise ValueError

        text = text.split()

        key = collections.deque([text[i] for i in range(self._level)])
        val = text[self._level + 1]
        self._new_entry(tuple(key), val)

        for word in text:
            key.popleft()
            key.append(val)
            val = word
            self._new_entry(tuple(key), val)

    def generate(self, startf=None, endf=None):
        """
        startf and endf must return boolean, they are used to determine
        start and end of generated quote. startf is called at beggining of
        generate without parameters and endf is called after every iteration
        with current quote as parameter
        """
        if startf is None:
            startf = lambda: random.choice(filter(lambda v:
                                           v[0][0].isupper(), self._database))
        if endf is None:
            endf = lambda s: len(s.split()) > 10

        key = startf()
        if self._use_prob:
            value = self._choose_with_prob(self._database[key])
        else:
            value = random.choice(self._database[key])
            value = value[0]
        quote = ""

        for i in range(self._level):
            quote += key[i] + " "

        quote += value

        while True:
            if self._level == 1:
                key = (value, )
            else:
                new_key = []
                for i in range(self._level-1):
                    new_key.append(key[i+1])
                new_key.append(value)
                key = tuple(new_key)

            try:
                if self._use_prob:
                    value = self._choose_with_prob(self._database[key])
                else:
                    value = random.choice(self._database[key])
                    value = value[0]
                quote += " " + value
            except KeyError:
                print "now"
                break

            if endf(quote):
                break

        return quote

    def _choose_with_prob(self, vals):
        sum_of_app = 0
        temp_sum = 0

        for v in vals:
            sum_of_app += v[1]

        choice = random.randint(1, sum_of_app)

        for val in vals:
            temp_sum += val[1]
            if choice <= temp_sum:
                return val[0]

        raise ValueError("choose_with_prob failed")

    def clear_db(self):
        self._database.clear()
