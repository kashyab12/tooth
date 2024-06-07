from PyQt6.QtBluetooth import QBluetoothDeviceInfo, QBluetoothLocalDevice

dev = QBluetoothLocalDevice()

for conn_dev in dev.connectedDevices():
    print(conn_dev.toString())