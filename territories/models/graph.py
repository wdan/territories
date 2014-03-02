# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractGraph():
    __metaclass__ = ABCMeta

    @abstractmethod
    def import_nodes():
        pass

    @abstractmethod
    def import_edges():
        pass

    @abstractmethod
    def import_communities():
        pass
