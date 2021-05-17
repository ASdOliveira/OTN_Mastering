
class Slot:
    __id = 0
    __index = 0
    __demandCode = 0
    __busy = False
    __tsReuseRestoration = False

    def getId(self):
        return self.__id

    def setId(self, newId):
        self.__id = newId

    def getIndex(self):
        return self.__index

    def setIndex(self, newIndex):
        self.__index = newIndex

    def getDemandCode(self):
        return self.__demandCode

    def setDemandCode(self, newDemandCode):
        self.__demandCode = newDemandCode

    def isTsReuseRestoration(self):
        return self.__tsReuseRestoration

    def setTsReuseRestoration(self, newTsReuseRestoration):
        self.__tsReuseRestoration = newTsReuseRestoration

    def isBusy(self):
        return self.__busy

    def setBusy(self, newBusy):
        self.__busy = newBusy
