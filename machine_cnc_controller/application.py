"""Application entry point for the CNC controller UI."""
from __future__ import annotations

import sys
from typing import Optional, Sequence

from PyQt5.QtWidgets import QApplication

from .gui.main_window import MainWindowSender


def create_application(arguments: Optional[Sequence[str]] = None) -> QApplication:
    """Instantiate the :class:`QApplication` used by the program.

    Parameters
    ----------
    arguments:
        Custom command line arguments to pass to :class:`QApplication`.

    Returns
    -------
    QApplication
        The configured Qt application instance.
    """
    return QApplication(list(arguments) if arguments is not None else sys.argv)


def main(arguments: Optional[Sequence[str]] = None) -> int:
    """Launch the main window of the CNC controller application."""
    app = create_application(arguments)
    main_window = MainWindowSender()
    main_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
