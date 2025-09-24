"""Serial communication utilities used by the CNC controller."""
from __future__ import annotations

from typing import List, Optional

import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


def recherchePort() -> List[ListPortInfo]:
    """Return the list of available serial ports."""
    return list(list_ports.comports())


class Connexion:
    """Minimal wrapper around :class:`serial.Serial`.

    The legacy user interface expects an object exposing a ``connexion`` attribute
    whose ``write``/``read`` methods map directly to pySerial. Keeping this wrapper
    allows the rest of the code base to depend on a stable interface while the
    implementation can evolve independently.
    """

    def __init__(self, port: str, baudrate: int) -> None:
        self.port = port
        self.baudrate = baudrate
        self.enConnexion = False
        self.erreur = False
        self.connexion: Optional[serial.Serial] = None

    def connecter(self) -> None:
        """Attempt to open the serial port."""
        self.enConnexion = True
        try:
            self.connexion = serial.Serial(self.port, self.baudrate)
        except serial.SerialException:
            self.erreur = True
            self.connexion = None
        finally:
            self.enConnexion = False
