from base.Ots import Ots
from typing import List


class Site:
    def __init__(self, _ots: List[Ots] = None):
        self.id = 0
        self.OtsList = _ots
