from struct import pack, unpack

from network.packet.PacketWriter import *
from utils.constants.ItemCodes import InventoryError


class ReadItemHandler(object):

    @staticmethod
    def handle(world_session, socket, reader):
        if len(reader.data) >= 2:  # Avoid handling empty read item packet
            bag, slot = unpack('<2B', reader.data[:2])
            # Seems like bag is always 255 and CMSG_READ_ITEM is only called if the item is in the backpack, weird.
            item = world_session.player_mgr.inventory.get_backpack().get_item(slot)
            data = b''

            # TODO: Better handling of this: check if player can use item, etc.
            if item:
                data += pack('<2Q', item.guid, item.guid)
                socket.sendall(PacketWriter.get_packet(OpCode.SMSG_READ_ITEM_OK, data))
            else:
                world_session.player_mgr.send_equip_error(InventoryError.EQUIP_ERR_ITEM_NOT_FOUND)

        return 0
