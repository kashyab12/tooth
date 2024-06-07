from PyQt6.QtBluetooth import QBluetoothDeviceInfo, QBluetoothLocalDevice
from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage
from pprint import pprint
from dataclasses import dataclass
from typing import List
from enum import StrEnum

class BluezAdapter1Keys(StrEnum):
    device_info = "org."
    address = "Address"
    address_type = "AddressType"
    alias = "Alias"
    obj_class = "Class"
    discoverable = "Discoverable"
    discoverable_timeout = "DiscoverableTimeout"
    discovering = "Discovering"
    modalias = "Modalias"
    name = "Name"
    pairable = "Pairable"
    pairable_timeout = "PairableTimeout"
    powered = "Powered"
    roles = "Roles"
    uuids = "UUIDs"
    
class BluezDevice1Keys(StrEnum):
    adapter = "Adapter"
    address = "Address"
    address_type = "AddressType"
    alias = "Alias"
    blocked = "Blocked"
    obj_class = "Class"
    connected = "Connected"
    icon = "Icon"
    legacy_pairing = "LegacyPairing"
    modalias = "Modalias"
    name = "Name"
    paired = "Paired" 
    services_resolved = "ServicesResolved"
    trusted = "Trusted"
    uuids = "UUIDs"


@dataclass
class Device1ServiceObject:
    adapter: str
    address: str # change type to mac
    address_type: str
    alias: str
    blocked: bool
    obj_class: int
    connected: bool
    icon: str
    legacy_pairing: bool
    modalias: str
    name: str
    paired: bool
    services_resolved: bool
    trusted: bool
    uuids: List[str]


dev = QBluetoothLocalDevice()
sys_bus = QDBusConnection.systemBus()
manager = QDBusInterface('org.bluez', "/", "org.freedesktop.DBus.ObjectManager", sys_bus)
reply = manager.call("GetManagedObjects")
if reply.type() != QDBusMessage.MessageType.ReplyMessage: exit(-1)
ble_obj_paths = reply.arguments()[0]
pprint(ble_obj_paths)
for obj_path in ble_obj_paths:
    if not "hci0" in obj_path: continue
    pprint(obj_path)

for conn_dev in dev.connectedDevices():
    print(conn_dev.toString())