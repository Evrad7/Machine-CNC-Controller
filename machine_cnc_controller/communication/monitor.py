"""Background helpers to monitor the state of the serial connexion."""
from __future__ import annotations

import time
from threading import Thread
from typing import Any, Callable, Optional


class CheckConnexion(Thread):
    """Poll a serial connexion and trigger a callback when it closes."""

    def __init__(
        self,
        connexion: Any,
        *,
        on_disconnect: Optional[Callable[[], None]] = None,
        poll_interval: float = 0.05,
    ) -> None:
        super().__init__(daemon=True)
        self._wrapped_connexion = connexion
        self._on_disconnect = on_disconnect
        self._poll_interval = poll_interval
        self._running = True

    def _serial(self) -> Any:
        return getattr(self._wrapped_connexion, "connexion", self._wrapped_connexion)

    def stop(self) -> None:
        """Stop polling the connexion."""
        self._running = False

    def run(self) -> None:  # pragma: no cover - thread code is hard to test here
        while self._running:
            connexion = self._serial()
            if connexion is None:
                break

            if hasattr(connexion, "is_open"):
                is_open = bool(getattr(connexion, "is_open"))
            elif hasattr(connexion, "isOpen"):
                is_open = bool(connexion.isOpen())
            else:
                # If the serial object does not expose an explicit state assume
                # the connection is alive.
                is_open = True

            if not is_open:
                if self._on_disconnect is not None:
                    self._on_disconnect()
                break

            time.sleep(self._poll_interval)
