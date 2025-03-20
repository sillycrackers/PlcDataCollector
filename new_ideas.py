class NewPlc:
    def __init__(self, name='', ip_address='', excel_file_name='', excel_file_location=''):
        self.name = name
        self.udt = UdtTag()
        self.ip_address = ip_address
        self.excel_file_name = excel_file_name
        self.excel_file_location = excel_file_location
        self.file_path = f"{excel_file_location}\\{excel_file_name}"


class UdtTag:
    def __init__(self):
        self.trigger = "Python.Trigger"
        self.acknowledge = "Python.Acknowledge"
        self.sheet_select = "0"
        self.tag_list = []
