from struct import pack, unpack

from database.world.WorldDatabaseManager import WorldDatabaseManager
from network.packet.PacketWriter import *
from utils.GameTextFormatter import GameTextFormatter


class PageTextQueryHandler(object):

    @staticmethod
    def handle(world_session, socket, reader):
        if len(reader.data) >= 4:  # Avoid handling empty page text query packet
            page_id = unpack('<I', reader.data[:4])[0]
            keep_looking = True
            data = b''

            while keep_looking:
                page = WorldDatabaseManager.page_text_get_by_id(page_id)
                data = pack('<I', page_id)

                if page:
                    page_text_bytes = PacketWriter.string_to_bytes(GameTextFormatter.format(world_session.player_mgr,
                                                                                            page.text))
                    page_id = page.next_page
                    data += pack(
                        '%usI' % len(page_text_bytes),
                        page_text_bytes,
                        page_id
                    )

                    if page_id <= 0:
                        keep_looking = False
                else:
                    missing_page_bytes = PacketWriter.string_to_bytes('Item page missing.')
                    data += pack(
                        '%usI' % len(missing_page_bytes),
                        missing_page_bytes,
                        0
                    )

                    keep_looking = False

            socket.sendall(PacketWriter.get_packet(OpCode.SMSG_PAGE_TEXT_QUERY_RESPONSE, data))

        return 0
