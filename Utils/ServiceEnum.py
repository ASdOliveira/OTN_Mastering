from enum import Enum


class ServiceEnum(Enum):
    NONE = None
    ONLY_ROUTE = "1+0",
    MAIN_ROUTE_AND_BACKUP = "1+1",
    MAIN_ROUTE_AND_RESTORATION = "1+R",
    MAIN_ROUTE_AND_BACKUP_AND_RESTORATION = "1+1+R"
