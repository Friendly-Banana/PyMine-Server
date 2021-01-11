"""Contains packets related to the chat."""

from __future__ import annotations
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = (
    'PlayChatMessageClientBound',
    'PlayChatMessageServerBound',
    'PlayTabCompleteClientBound',
    'PlayTabCompleteServerBound',
)


class PlayChatMessageClientBound(Packet):
    """A chat message from the server to the client (Server -> Client)

    :param Chat data: The actual chat data.
    :param int position: Where on the GUI the message is to be displayed.
    :param uuid.UUID sender: Unknown, see here: https://wiki.vg/Protocol#Chat_Message_.28clientbound.29.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr data:
    :attr position:
    :attr sender:
    """

    id = 0x0E
    to = 1

    def __init__(self, data: Chat, position: int, sender: uuid.UUID) -> None:
        super().__init__()

        self.data = data
        self.position = position
        self.sender = sender

    def encode(self) -> bytes:
        return Buffer.pack_chat(self.data) + Buffer.pack('b', self.position) + Buffer.pack_uuid(self.sender)


class PlayChatMessageServerBound(Packet):
    """A chat message from a client to the server. Can be a command. (Client -> Server)

    :param str message: The raw text sent by the client.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr message:
    """

    id = 0x03
    to = 0

    def __init__(self, message: str) -> None:
        super().__init__()

        self.message = message

    @classmethod
    def decode(cls, buf: Buffer) -> PlayChatMessageServerBound:
        return cls(buf.unpack_string())


class PlayTabCompleteServerBound(Packet):
    """Used when a client wants to tab complete a chat message. (Client -> Server)

    :param int transaction_id: Number generated by the client.
    :param str text: All text behind/to the left of the cursor.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr transaction_id:
    :attr text:
    """

    id = 0x06
    to = 0

    def __init__(self, transaction_id: int, text: str) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.text = text

    @classmethod
    def decode(cls, buf: Buffer) -> PlayTabCompleteServerBound:
        return cls(buf.unpack_varint(), buf.unpack_string())


class PlayTabCompleteClientBound(Packet):
    """"TODO: make good docstring. (Server -> Client)"""

    id = 0xF
    to = 1

    def __init__(self, transaction_id: int, start: int, matches: list) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.start = start
        self.matches = matches

        # Matches should be something like:
        # [
        #     [
        #         matching element,
        #         tooltip
        #     ],
        #     ...
        # ]

    def encode(self):
        out = Buffer.pack_varint(self.id) + Buffer.pack_varint(self.start) + \
            Buffer.pack_varint(self.length) + Buffer.pack_varint(len(self.matches))

        for m in self.matches:
            out += Buffer.pack_string(m[0])

            if len(m) > 1:
                out += Buffer.pack('?', True) + Buffer.pack_chat(Chat(m[1]))
            else:
                out += Buffer.pack('?', False)

        return out
