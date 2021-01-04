"""Contains packets related to windows."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayWindowConfirmationClientBound',
    'PlayWindowConfirmationServerBound',
    'PlayClickWindow',
    'PlayCloseWindowButton',
    'PlayCloseWindowServerBound',
    'PlayCloseWindowClientBound',
    'PlayWindowProperty',
    'PlayWindowItems',
    'PlaySetSlot',
)


class PlayWindowConfirmationClientBound(Packet):
    """A packet indicating whether a request from the client was accepted or if there was a problem.
    Server -> Client"""

    id = 0x11
    to = 1

    def __init__(self, window_id: int, action_number: int, accepted: bool) -> None:
        super().__init__()

        self.window_id = window_id
        self.action_number = action_number
        self.accepted = accepted

    def encode(self) -> bytes:
        return Buffer.pack('b', self.window_id) + Buffer.pack('h', self.action_number) + \
            Buffer.pack_bool(self.accepted)


class PlayWindowConfirmationServerBound(Packet):
    """Used by the client to respond to a nearly identical packet by the server. (Client -> Server)

    :param int window_id: The ID of the window/open inventory.
    :param int action_number: The unique number of the action.
    :param bool accepted: Whether the action was allowed or denied.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    :attr action_number:
    :attr accepted:
    """

    id = 0x07
    to = 0

    def __init__(self, window_id: int, action_number: int, accepted: bool) -> None:
        super().__init__()

        self.window_id = window_id
        self.action_number = action_number
        self.accepted = accepted

    @classmethod
    def decode(cls, buf: Buffer) -> PlayWindowConfirmationServerBound:
        return cls(buf.unpack('b'), buf.unpack('h'), buf.unpack_bool())


class PlayClickWindow(Packet):
    """Sent when the client clicks on a slot in a window. (Client -> Server)

    :param int window_id: The ID of the window where the action occurred.
    :param int slot_number: The number of the slot that was clicked.
    :param int button: Description of parameter `button`.
    :param int action_number: Unique number, see here: https://wiki.vg/Protocol#Click_Window_Button.
    :param int mode: The inventory operation mode.
    :param dict slot: The slot item.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    :attr slot_number:
    :attr button:
    :attr action_number:
    :attr mode:
    :attr slot:
    """

    id = 0x09
    to = 0

    def __init__(
            self,
            window_id: int,
            slot_number: int,
            button: int,
            action_number: int,
            mode: int,
            slot: dict) -> None:
        super().__init__()

        self.window_id = window_id
        self.slot_number = slot_number
        self.button = button
        self.action_number = action_number
        self.mode = mode
        self.slot = slot

    @classmethod
    def decode(cls, buf: Buffer) -> PlayClickWindow:
        return cls(
            buf.unpack('B'),
            buf.unpack('h'),
            buf.unpack('b'),
            buf.unpack('h'),
            buf.unpack_varint(),
            buf.unpack_slot()
        )


class PlayCloseWindowButton(Packet):
    """Sent by the client when a window close button is clicked. (Client -> Server)

    :param int window_id: The ID of the window sent by an open window packet.
    :param int button_id: Meaning depends on window type, see here: https://wiki.vg/Protocol#Click_Window_Button.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    :attr button_id:
    """

    id = 0x08
    to = 0

    def __init__(self, window_id: int, button_id: int) -> None:
        super().__init__()

        self.window_id = window_id
        self.button_id = button_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayCloseWindowButton:
        return cls(buf.unpack('b'), buf.unpack('b'))


class PlayCloseWindowServerBound(Packet):
    """Packet sent by the client when it closes a container window. (Client -> Server)

    :param int window_id: The ID of the window that was closed, 0 for player's inventory.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    """

    id = 0x0A
    to = 0

    def __init__(self, window_id: int):
        super().__init__()

        self.window_id = window_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayCloseWindowServerBound:
        return cls(buf.unpack('b'))


class PlayCloseWindowClientBound(Packet):
    """This packet is sent from the server to the client when a window is forcibly closed, such as when a chest is destroyed while it's open. """

    id = 0x12
    to = 1

    def __init__(self, window_id: int) -> None:
        super().__init__()

        self.window_id = window_id

    def encode(self) -> bytes:
        return Buffer.pack('B', self.window_id)


class PlayWindowItems(Packet):
    """Sent by the server when multiple slots in an inventory window are updated (Server -> Client)

    :param list slots: The updated inventory slots.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr slots:
    """

    id = 0x13
    to = 1

    def __init__(self, slots: list) -> None:
        super().__init__()

        self.slots = slots

    def encode(self) -> bytes:
        return Buffer.pack('h', len(self.slots)) + b''.join(Buffer.pack_slot(s) for s in self.slots)


class PlayWindowProperty(Packet):
    """This packet is used to inform the client that part of a GUI window should be updated. ClientboundServer -> Client"""

    id = 0x14
    to = 1

    def __init__(self, window_id: int, prop: int, value: int) -> None:
        super().__init__()

        self.window_id = window_id
        self.prop = prop
        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack('B', self.window_id) + Buffer.pack('h', self.prop) + \
            Buffer.pack('h', self.value)


class PlaySetSlot(Packet):
    """Sent by the server when an item in a slot (in a window) is added/removed."""

    def __init__(self, window_id: int, slot: int, slot_data: dict):
        super.__init__()

        self.win_id = window_id
        self.slot = slot
        self.slot_data = slot_data

    def encode(self):
        return Buffer.pack('b', self.window_id) + Buffer.pack('h', self.slot) + \
            Buffer.pack_slot(self.slot_data)
