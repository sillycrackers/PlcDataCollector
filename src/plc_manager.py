
class PlcManager:
    def __init__(self):

        self.connections = {}

    def add_plc_connection(self, plc_connection):
        self.connections[plc_connection.plc.name] = plc_connection

    def delete_plc_connection(self, plc_name):
        del self.connections[plc_name]