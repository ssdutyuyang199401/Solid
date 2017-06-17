from abc import ABCMeta, abstractmethod
from copy import deepcopy
from random import randint, random, shuffle
from collections import deque
from numpy import argmax

class TabuSearch:
    __metaclass__ = ABCMeta

    cur_steps = None

    tabu_size = None
    tabu_list = None

    current = None
    best = None

    max_score = None

    def __init__(self, tabu_size, max_score=None):
        if isinstance(tabu_size, int) and tabu_size > 0:
            self.tabu_size = tabu_size
        else:
            raise TypeError('Tabu size must be a positive integer')

        if max_score is not None:
            if isinstance(max_score, (int, float)):
                self.max_score = float(max_score)
            else:
                raise TypeError('Maximum score must be a numeric type')

    def __str__(self):
        return ('TABU SEARCH: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST SCORE: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.cur_steps, self._score(self.best), str(self.best))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        self.cur_steps = 0
        self.tabu_list = deque(maxlen=self.tabu_size)
        self.current = None
        self.best = None

    @abstractmethod
    def _score(self):
        pass

    @abstractmethod
    def _neighborhood(self):
        pass

    def _best(self, neighborhood):
        return neighborhood[argmax([self._score(x) for x in neighborhood])]

    def tabu_search(self, verbose=True):
        self._clear()
        for i in range(self.max_steps):
            self.cur_steps += 1

            if (i % 100 == 0) and verbose:
                print self

            neighborhood = self._neighborhood()
            neighborhood_best = self._best(neighborhood)

            while True:
                if all([x in self.tabu_list for x in neighborhood]):
                    print "TERMINATING - NO SUITABLE NEIGHBORS"
                    return self.best, self._score(self.best)
                if neighborhood_best in self.tabu_list:
                    if self._score(neighborhood_best) > self._score(self.best):
                        self.tabu_list.append(neighborhood_best)
                        self.best = neighborhood_best
                        break
                    else:
                        neighborhood.remove(neighborhood_best)
                        neighborhood_best = self._best(neighborhood)
                else:
                    self.tabu_list.append(neighborhood_best)
                    self.best = neighborhood_best
                    break

            if self.max_score is not None and self._score(self.best) > self.max_score:
                print "TERMINATING - REACHED MAXIMUM SCORE"
                return self.best, self._score(self.best)
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best, self._score(self.best)