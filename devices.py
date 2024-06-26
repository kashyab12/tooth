from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage
from pprint import pprint
from dataclasses import dataclass
from typing import List
from enum import StrEnum
from bleak import BleakScanner
import asyncio

class BluezAdapter1Keys(StrEnum):
    interface = "org.bluez.Adapter1"
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
    interface = "org.bluez.Device1"
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

def get_connected_devices(all_devs: List[Device1ServiceObject]):
    return list(filter(lambda dev: dev.connected, all_devs))

def get_devices_history():
    sys_bus = QDBusConnection.systemBus()
    manager = QDBusInterface('org.bluez', "/", "org.freedesktop.DBus.ObjectManager", sys_bus)
    reply = manager.call("GetManagedObjects")
    if reply.type() != QDBusMessage.MessageType.ReplyMessage: exit(-1)
    ble_obj_paths = reply.arguments()[0]
    connected_bl_devs = []
    # pprint(ble_obj_paths)
    for obj_path, ifaces in ble_obj_paths.items():
        if "hci0" not in obj_path or BluezDevice1Keys.interface not in ifaces.keys(): continue
        conn_dev_info = ifaces[BluezDevice1Keys.interface]
        bl_dev = Device1ServiceObject(adapter=conn_dev_info.get(BluezDevice1Keys.adapter), address=conn_dev_info.get(BluezDevice1Keys.address), 
                                    address_type=conn_dev_info.get(BluezDevice1Keys.address_type), alias=conn_dev_info.get(BluezDevice1Keys.alias), 
                                    blocked=conn_dev_info.get(BluezDevice1Keys.blocked),obj_class=conn_dev_info.get(BluezDevice1Keys.obj_class), 
                                    connected=conn_dev_info.get(BluezDevice1Keys.connected), icon=conn_dev_info.get(BluezDevice1Keys.icon),
                                    legacy_pairing=conn_dev_info.get(BluezDevice1Keys.legacy_pairing), modalias=conn_dev_info.get(BluezDevice1Keys.modalias),
                                    name=conn_dev_info.get(BluezDevice1Keys.name), paired=conn_dev_info.get(BluezDevice1Keys.paired), 
                                    services_resolved=conn_dev_info.get(BluezDevice1Keys.services_resolved), trusted=conn_dev_info.get(BluezDevice1Keys.trusted),
                                    uuids=conn_dev_info.get(BluezDevice1Keys.uuids)
                                    )
        if bl_dev.trusted: connected_bl_devs.append(bl_dev)
    
    return connected_bl_devs

async def scan_devices(not_connected_devices: List[Device1ServiceObject]):
    stop_event = asyncio.Event()
    def callback(device, adv_data):
        if adv_data is None: return
        print(device)
        if any(device.address == history_dev.address for history_dev in not_connected_devices): 
            print(f"Inside: {device}")
    async with BleakScanner(callback) as scanner:
        await stop_event.wait()

all_devices = get_devices_history()
connected_devices = get_connected_devices(all_devices)
not_connected_devices = [history_dev for history_dev in all_devices if history_dev not in connected_devices]
asyncio.run(scan_devices(not_connected_devices))