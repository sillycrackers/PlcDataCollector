

# PLC object for setting up PlcConnection object
class Plc:
    def __init__(self, name='', ip_address='', trigger_tag='', ack_tag='', tags=[], excel_file_name='', excel_file_location=''):
        self.name = name
        self.ip_address = ip_address
        self.trigger_tag = trigger_tag
        self.ack_tag = ack_tag
        self.tags = tags
        self.excel_file_name = excel_file_name
        self.excel_file_location = excel_file_location
        self.file_path = f"{excel_file_location}\\{excel_file_name}.xlsx"

