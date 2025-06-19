"""Lost Modeler - Board Game & General Tray Generator.

This script provides a PySimpleGUI based interface for generating tray
models.  It focuses on a clean layout with a Boardgame Mode toggle,
configuration persistence and basic export logic.

The actual 3D modelling uses cadquery; a simple preview placeholder is
provided because a full viewer is out of scope.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

import PySimpleGUI as sg

try:
    import cadquery as cq
except Exception:  # pragma: no cover - cadquery optional for tests
    cq = None

CONFIG_FILE = Path.home() / ".lost_modeler_config.json"
DEFAULT_EXPORT = str(Path.home() / "lost_modeler_exports")


@dataclass
class Compartment:
    """Represents a single compartment within a tray."""

    x: float
    y: float
    width: float
    depth: float
    shape: str = "rectangle"
    label: str = ""


@dataclass
class TraySettings:
    """General tray settings."""

    length: float = 100.0
    width: float = 100.0
    height: float = 40.0
    wall: float = 2.0
    compartments: List[Compartment] = field(default_factory=list)
    cutout_pattern: str | None = None


@dataclass
class BoardgameSettings:
    """Additional settings for boardgame mode."""

    card_size: str = "63.5x88"
    sleeved: bool = False
    quantity: int = 0
    token_wells: int = 0


@dataclass
class AppState:
    """Main application state."""

    tray: TraySettings = field(default_factory=TraySettings)
    boardgame: BoardgameSettings = field(default_factory=BoardgameSettings)
    export_dir: str = DEFAULT_EXPORT
    theme: str = "DarkBlue3"
    undo_stack: List[TraySettings] = field(default_factory=list)
    redo_stack: List[TraySettings] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_config() -> AppState:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf8") as f:
            data = json.load(f)
        tray = TraySettings(**data.get("tray", {}))
        boardgame = BoardgameSettings(**data.get("boardgame", {}))
        state = AppState(tray=tray, boardgame=boardgame)
        state.export_dir = data.get("export_dir", DEFAULT_EXPORT)
        state.theme = data.get("theme", "DarkBlue3")
        return state
    return AppState()


def save_config(state: AppState) -> None:
    CONFIG_FILE.write_text(json.dumps(
        {
            "tray": asdict(state.tray),
            "boardgame": asdict(state.boardgame),
            "export_dir": state.export_dir,
            "theme": state.theme,
        },
        indent=2,
    ))


# ---------------------------------------------------------------------------
# CAD helpers
# ---------------------------------------------------------------------------

def build_model(state: AppState) -> cq.Workplane | None:
    """Build a simple tray model with cadquery."""

    if cq is None:
        return None

    t = state.tray
    base = cq.Workplane("XY").box(t.length, t.width, t.height)
    return base


def export_model(model: cq.Workplane, path: str, fmt: str) -> None:
    if fmt.lower() == "stl":
        cq.exporters.export(model, path)
    elif fmt.lower() == "step":
        cq.exporters.export(model, path)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(state: AppState) -> List[str]:
    """Return a list of validation error strings."""

    errors: List[str] = []
    t = state.tray
    if t.wall < 0.8:
        errors.append("Wall thickness < 0.8mm")
    if any(dim <= 0 for dim in (t.length, t.width, t.height)):
        errors.append("Dimensions must be positive")
    # Basic print bed limit check (220x220x250 typical for Ender 3)
    if t.length > 220 or t.width > 220 or t.height > 250:
        errors.append("Tray exceeds common FDM build volume")
    return errors


# ---------------------------------------------------------------------------
# GUI Layout
# ---------------------------------------------------------------------------

def choose_theme() -> str:
    layout = [[sg.Text("Choose theme:"), sg.Radio("Light", "T", key="L"),
               sg.Radio("Dark", "T", default=True, key="D")],
              [sg.Button("OK")]]
    window = sg.Window("Theme", layout, modal=True)
    event, values = window.read()
    window.close()
    return "LightGrey3" if values.get("L") else "DarkBlue3"


def ensure_export_dir(state: AppState) -> None:
    if not Path(state.export_dir).exists():
        Path(state.export_dir).mkdir(parents=True, exist_ok=True)


def make_main_layout(state: AppState) -> List[List[sg.Element]]:
    general_col = [
        [sg.Text("Length"), sg.Input(key="LEN", size=(6, 1),
                                      default_text=state.tray.length)],
        [sg.Text("Width"), sg.Input(key="WID", size=(6, 1),
                                     default_text=state.tray.width)],
        [sg.Text("Height"), sg.Input(key="HEI", size=(6, 1),
                                      default_text=state.tray.height)],
        [sg.Text("Wall"), sg.Input(key="WALL", size=(6, 1),
                                    default_text=state.tray.wall)],
    ]

    boardgame_col = [
        [sg.Text("Card size"), sg.Input(key="CARD", size=(10, 1),
                                        default_text=state.boardgame.card_size)],
        [sg.Checkbox("Sleeved", key="SLEEVE",
                     default=state.boardgame.sleeved)],
        [sg.Text("Quantity"), sg.Input(key="QTY", size=(6, 1),
                                       default_text=state.boardgame.quantity)],
        [sg.Text("Token wells"), sg.Input(key="TOKENS", size=(6, 1),
                                          default_text=state.boardgame.token_wells)],
    ]

    layout = [
        [sg.Checkbox("Boardgame Mode", key="BG", enable_events=True)],
        [sg.Frame("General", general_col)],
        [sg.Frame("Boardgame", boardgame_col, key="BGFRAME",
                  visible=False)],
        [sg.Frame("3D Preview", [[sg.Text("(preview placeholder)",
                                         key="PREVIEW")]])],
        [sg.Button("Validate"), sg.Button("Undo"), sg.Button("Redo"),
         sg.Button("Export"), sg.Button("Exit")],
    ]
    return layout


# ---------------------------------------------------------------------------
# Event Loop
# ---------------------------------------------------------------------------

def run_app() -> None:
    state = load_config()

    if not CONFIG_FILE.exists():
        state.theme = choose_theme()
        folder = sg.popup_get_folder(
            "Choose export folder", default_path=DEFAULT_EXPORT)
        if folder:
            state.export_dir = folder
        ensure_export_dir(state)
        save_config(state)

    sg.theme(state.theme)
    layout = make_main_layout(state)
    window = sg.Window("Lost Modeler", layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "BG":
            window["BGFRAME"].update(visible=values["BG"])
        if event == "Validate":
            apply_values(state, values)
            errs = validate(state)
            sg.popup("Validation", "\n".join(errs) if errs else "No issues")
            update_preview(window, state)
        if event == "Export":
            apply_values(state, values)
            errs = validate(state)
            if errs:
                sg.popup_error("Fix errors before export", "\n".join(errs))
                continue
            fmt = sg.popup_get_text("Export format (STL/STEP)", default_text="STL")
            if fmt:
                model = build_model(state)
                if model is None:
                    sg.popup_error("cadquery not available")
                else:
                    path = os.path.join(state.export_dir,
                                        f"tray.{fmt.lower()}")
                    export_model(model, path, fmt)
                    sg.popup(f"Exported to {path}")
        if event == "Undo":
            if state.undo_stack:
                state.redo_stack.append(state.tray)
                state.tray = state.undo_stack.pop()
                refresh_inputs(window, state)
        if event == "Redo":
            if state.redo_stack:
                state.undo_stack.append(state.tray)
                state.tray = state.redo_stack.pop()
                refresh_inputs(window, state)

    save_config(state)
    window.close()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def apply_values(state: AppState, values: dict) -> None:
    state.undo_stack.append(state.tray)
    state.tray = TraySettings(
        length=float(values["LEN"]),
        width=float(values["WID"]),
        height=float(values["HEI"]),
        wall=float(values["WALL"]),
    )
    state.boardgame = BoardgameSettings(
        card_size=values.get("CARD", ""),
        sleeved=values.get("SLEEVE", False),
        quantity=int(values.get("QTY", 0) or 0),
        token_wells=int(values.get("TOKENS", 0) or 0),
    )
    state.redo_stack.clear()


def refresh_inputs(window: sg.Window, state: AppState) -> None:
    window["LEN"].update(state.tray.length)
    window["WID"].update(state.tray.width)
    window["HEI"].update(state.tray.height)
    window["WALL"].update(state.tray.wall)
    window["CARD"].update(state.boardgame.card_size)
    window["SLEEVE"].update(state.boardgame.sleeved)
    window["QTY"].update(state.boardgame.quantity)
    window["TOKENS"].update(state.boardgame.token_wells)


def update_preview(window: sg.Window, state: AppState) -> None:
    """Placeholder preview update."""

    window["PREVIEW"].update(
        f"Tray {state.tray.length}x{state.tray.width}x{state.tray.height}")


if __name__ == "__main__":  # pragma: no cover - manual execution
    run_app()
