#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: Python 3
# Author: fm4d


import random
import shelve



class ObjectLikeDbfilenameShelf():
    """
    Proxy class that allows object-like manipulation with DbfilenameShelf object
    """
    def __init__(self, ds):
        """
        Args:
            ds: DbfilenameShelf object
        """

        super(ObjectLikeDbfilenameShelf, self).__setattr__('_ds', ds)

    def __getattr__(self, name):
        if name in self._ds:
            return self._ds[name]
        else:
            raise AttributeError("{} object has no attribute {}".format(
                self._ds.__class__.__name__, name
            ))

    def __setattr__(self, name, value):
        self._ds[name] = value

    def __delattr__(self, name):
        if name in self._ds:
            del self._ds[name]
        else:
            raise AttributeError("{} object has no attribute {}".format(
                self._ds.__class__.__name__, name
            ))

    def __repr__(self):
        return '\n'.join("{}: {}".format(k, v.order)
                         for k, v in self._ds.items())

    def __iter__(self):
        for key in self._ds.keys():
            yield key

    def close(self):
        self._ds.close()


class WalkByGroup:
    """
    Iterator that walks throught iterable by step_size of elements
    """

    def __init__(self, iterable, step_size):
        """
        Args:
            iterable: iterable object (object that can be turned into iterator)
            step_size: number of elements returned at once
        """

        self.iterator = iter(iterable)
        self.step_size = step_size
        self.buffer = (None, ) + tuple(next(self.iterator) for x in range(step_size-1))

    def __iter__(self):
        return self

    def __next__(self):
        self.buffer = self.buffer[1:] + (next(self.iterator), )
        return self.buffer


def parse(filename, encoding=None):
    """
    !DEMO!
    Simple file parsing generator

    Args:
        filename: absolute or relative path to file on disk
        encoding: encoding string that is passed to open function
    """

    with open(filename, encoding=encoding) as source:
        for line in source:
            for word in line.split():
                yield word


class MarkovChain():
    """
    Class representing single markov chain
    """

    def __init__(self, order, content=None):
        self.order = order
        self.content = {} if content is None else content
        self._start_words = None

    @property
    def startwords(self):
        """
        !DEMO!
        Cached list of keys that can be used to generate sentence.
        """

        if self._start_words is not None:
            return self._start_words
        else:
            self._start_words = list(filter(
                lambda x: str.isupper(x[0][0]) and x[0][-1] not in ['.', '?', '!'],
                self.content.keys()
            ))
            return self._start_words

    def decache(self):
        """
        Deleted cached value of startwords
        """
        self._start_words = None

class MarkovGenerator():
    """
    Class representing markov chain based text generator
    """

    def __init__(self, shelve_file='chains_shelve'):
        """
        Args:
            shelve_file: path to shelve file on disk
        """

        self.ds = shelve.open(shelve_file, writeback=True)
        self.chains = ObjectLikeDbfilenameShelf(self.ds)


    def add_chain(self, name, order):
        """
        Add chain to current shelve file

        Args:
            name: chain name
            order: markov chain order
        """

        if name not in self.chains:
            setattr(self.chains, name, MarkovChain(order=order))
        else:
            raise ValueError("Chain with this name already exists")

    def remove_chain(self, name):
        """
        Remove chain from current shelve file

        Args:
            name: chain name
        """

        if name in self.chains:
            delattr(self.chains, name)
        else:
            raise ValueError("Chain with this name not found")

    def build_chain(self, source, chain):
        """
        Build markov chain from source on top of existin chain

        Args:
            source: iterable which will be used to build chain
            chain: MarkovChain in currently loaded shelve file that
                   will be extended by source
        """

        for group in WalkByGroup(source, chain.order+1):
            pre = group[:-1]
            res = group[-1]

            if pre not in chain.content:
                chain.content[pre] = {res: 1}
            else:
                if res not in chain.content[pre]:
                    chain.content[pre][res] = 1
                else:
                    chain.content[pre][res] += 1

        chain.decache()

    def generate_sentence(self, chain):
        """
        !DEMO!
        Demo function that shows how to generate a simple sentence starting with
        uppercase letter without lenght limit.

        Args:
            chain: MarkovChain that will be used to generate sentence
        """

        def weighted_choice(choices):
            total_weight = sum(weight for val, weight in choices)
            rand = random.uniform(0, total_weight)

            upto = 0
            for val, weight in choices:
                if upto + weight >= rand:
                    return val
                upto += weight

        sentence = list(random.choice(chain.startwords))

        while not sentence[-1][-1] in ['.', '?', '!']:
            sentence.append(
                weighted_choice(
                    chain.content[tuple(sentence[-2:])].items()
                )
            )

        return ' '.join(sentence)

    def close(self):
        """
        Close current shelve db file
        """
        self.chains.close()
