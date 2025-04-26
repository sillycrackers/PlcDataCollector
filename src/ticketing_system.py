from enum import Enum, auto


def transmit(receiver, ticket):

    receiver.q.put(ticket)
    receiver.event_generate("<<CheckQueue>>")

class TicketPurpose(Enum):

    # ("message":str, Alarm active:bool)
    UPDATE_ALARMS = auto()
    # (state:bool,"plc.name:str")
    TOGGLE_INDICATOR = auto()

    POPULATE_INDICATORS = auto()

    ACTIVE_ALARMS_CLEAR = auto()

    SHOW_WAIT_CURSOR = auto()

    SHOW_NORMAL_CURSOR = auto()

    # (AnimatedLabel: object,column : int, row : int)
    SHOW_ANIMATED_LABEL = auto()
    # (AnimatedLabel: object,column : int, row : int)
    HIDE_ANIMATED_LABEL = auto()

    OUTPUT_MESSAGE = auto()

class Ticket:
    def __init__(self, purpose: TicketPurpose, value):
        self.purpose = purpose
        self.value = value


