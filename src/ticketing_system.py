from enum import StrEnum, auto


def transmit(receiver, ticket):

    receiver.q.put(ticket)
    receiver.event_generate("<<CheckQueue>>")

class TicketPurpose(StrEnum):

    # ("message":str, Alarm active:bool)
    UPDATE_ALARMS = "update_alarms"
    # (state:bool,"plc.name:str")
    TOGGLE_INDICATOR = "toggle_indicator"

    POPULATE_INDICATORS = "populate_indicators"

    ACTIVE_ALARMS_CLEAR = "active_alarms_clear"

    SHOW_WAIT_CURSOR = "show_wait_cursor"

    SHOW_NORMAL_CURSOR = "show_normal_cursor"

    # (AnimatedLabel: object,column : int, row : int)
    SHOW_ANIMATED_LABEL = "show_animated_label"
    # (AnimatedLabel: object,column : int, row : int)
    HIDE_ANIMATED_LABEL = "hide_animated_label"

    OUTPUT_MESSAGE = "output_message"

class Ticket:
    def __init__(self, purpose: TicketPurpose, value):
        self.purpose = purpose
        self.value = value


