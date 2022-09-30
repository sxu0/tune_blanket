"""
convert_tune.py
---------------
converts tune from numerical pitches/durations to a colourful blanket!
"""

from pathlib import Path
from matplotlib import pyplot as plt

from read_tune import TrebleScore


def compose_blanket():
    # visual magic goes here!
    pass


if __name__ == "__main__":
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')

    spring = TrebleScore(tune_path)
    colours = spring.pitches - spring.pitch_range
    widths = spring.durations
