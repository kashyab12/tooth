from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import QObject
from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent
from devices import get_connected_devices, get_devices_history
import sys

class DiscoveryAgent(QObject):
    def __init__(self, all_devices, connected_devices):
        super().__init__()
        self.agent = QBluetoothDeviceDiscoveryAgent(self)
        

app = QApplication(sys.argv)

window = QMessageBox()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.
all_devices = get_devices_history()
connected_devices = get_connected_devices(all_devices)
discover = DiscoveryAgent(all_devices, connected_devices)
# Start the event loop.
app.exec()