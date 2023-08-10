from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

import pytermgui as ptg
from pytermgui import Widget, PixelMatrix
from sidebar import get_sidebar
from plot import PlotWidget
import numpy as np 

def _process_arguments(argv: list[str] | None = None) -> Namespace:
    """Processes command line arguments.

    Note that you don't _have to_ use the bultin argparse module for this; it
    is just what the module uses.

    Args:
        argv: A list of command line arguments, not including the binary path
            (sys.argv[0]).
    """

    parser = ArgumentParser(description="My first PTG application.")

    return parser.parse_args(argv)


def _configure_widgets() -> None:
    """Defines all the global widget configurations.

    Some example lines you could use here:

        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)


def _define_layout() -> ptg.Layout:
    """Defines the application layout.

    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("header", height=1)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("body")

    # A slot in the same row as body, using the full non-occupied height and
    # 20% of the terminal's height.
    layout.add_slot("sidebar", width=0.2)

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("footer", height=1)

    return layout


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            "Timol",
            box="EMPTY",
        )

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)

        footer = ptg.Window(ptg.Button("Quit", lambda *_: manager.stop()), box="EMPTY")

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"
        manager.add(footer, assign="footer")

        sidebar = get_sidebar()
        plot = PlotWidget()
        # plot = Widget()
        # m = ["black", "blue", "black", "black", "white"]
        # plot = PixelMatrix.from_matrix(m*10)

        manager.add(sidebar, assign="sidebar")
        window = ptg.Window(plot)
        manager.add(window, assign="body")
        plot.parent = window

        plot.set_spheres(
            np.array([
                [1,0,0],
                [0,1,0],
                [0,0,1],
                [0,0,0],
            ]),
            [.5,.5,.5,.5],
            ["blue", "red", "orange", "white"]
        )

        # plot.select()


    ptg.tim.print("[!gradient(210)]Goodbye!")


if __name__ == "__main__":
    main(sys.argv[1:])
