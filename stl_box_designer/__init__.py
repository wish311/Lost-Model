"""Top level package for STL box designer."""

from .main_window import MainWindow, launch
from .box_model import BoxModel
from .compartment import CompartmentSystem
from .cutout import CutoutPattern
from .splitter import AutoSplitter

try:  # Optional PyQt dependency for GUI components
    from .main_window import MainWindow, launch  # type: ignore
except Exception:  # pragma: no cover - GUI not required for tests
    MainWindow = None  # type: ignore

    def launch():  # type: ignore
        raise ImportError("PyQt5 is required for GUI features")

__all__ = [
    'MainWindow',
    'launch',
    'BoxModel',
    'CompartmentSystem',
    'CutoutPattern',
    'AutoSplitter',
]