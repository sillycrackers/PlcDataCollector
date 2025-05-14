from enum import StrEnum, auto

class RunMethodType(StrEnum):

    COLLECT_DATA = auto()
    CHECK_PLC_CONN = auto()