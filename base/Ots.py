from base.Interfaces import Interfaces
from typing import List


class Ots:
    def __init__(self, _interfaces: List[Interfaces] = None):
        self.id = int
        self.interfacesList = _interfaces
