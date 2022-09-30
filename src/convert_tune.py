"""
convert_tune.py
---------------
converts tune from numerical pitches/durations to a colourful blanket!
"""

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

from read_tune import TrebleScore


class BlanketDesign():
    # colour scheme
    # rest colour
    # dimensions
    # etc
    pass
    # (compose_blanket does not currently utilize this)


def compose_blanket(score: TrebleScore):
    pitches = score.pitches
    durations = score.durations
    # visual magic!
    for part in range(len(pitches)):
        width = 10
        length_multiplier = 10
        rest_pitch = np.min(pitches) - score.pitch_range
        note_divider = np.full((width, 1), rest_pitch)
        part_blanket_sections = []
        part_pitches = pitches[part, :]
        part_durations = durations[part, :]
        for note in range(len(pitches[part])):
            if pitches[part, note] != 9999:
                pitch = part_pitches[note]
            else:
                pitch = rest_pitch
            blanket_section = np.full(
                (width, part_durations[note] * length_multiplier), pitch
            )
            part_blanket_sections.append(blanket_section)
            part_blanket_sections.append(note_divider)
        del part_blanket_sections[-1]
        part_blanket = np.concatenate(part_blanket_sections, axis=1)
        if True:
            # visualize part
            plt.figure()  # figsize=(,)
            plt.contourf(part_blanket, score.pitch_range)
            plt.tick_params(
                axis='both',        # both x & y axes
                which='both',       # both major & minor ticks
                left=False,         # no ticks along left edge
                bottom=False,       # no ticks along bottom edge
                labelleft=False,    # no labels along left edge
                labelbottom=False   # no labels along bottom edge
            )
            plt.show()


if __name__ == "__main__":
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')

    spring = TrebleScore(tune_path)
    compose_blanket(spring)
