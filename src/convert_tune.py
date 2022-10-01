"""
convert_tune.py
---------------
converts tune from numerical pitches/durations to a colourful blanket!
"""

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

from read_tune import TrebleScore


debug_switch = False


class BlanketDesign():
    # colour scheme
    # rest colour
    # dimensions
    # etc
    pass
    # (compose_blanket does not currently utilize this)


def compose_blanket(score: TrebleScore):
    # visual magic!
    pitches = score.pitches
    durations = score.durations
    width = 10
    length_multiplier = 10
    rest_pitch = np.min(pitches) - (score.pitch_range // 5 + 2)
    note_divider = np.full((width, 1), rest_pitch - 2 * score.pitch_range // 5)

    for part in range(len(pitches)):
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
        if debug_switch:
            out_path = Path(__file__).resolve().parent.parent.joinpath('output')
            out_path.mkdir(exist_ok=True)
            with open(out_path.joinpath('test_tune_blanket.txt'), 'w') as file_out:
                for i in range(len(part_blanket)):
                    for j in range(len(part_blanket[i])):
                        file_out.write(str(part_blanket[i, j]) + "  ")
                    file_out.write("\n")
        if True:
            # visualize part
            plt.figure()  # figsize=(,)
            plt.contourf(part_blanket, int(score.pitch_range * 1.5))
            plt.tick_params(
                axis='both', which='both',
                left=False, bottom=False,
                labelleft=False, labelbottom=False
            )
            plt.show()


if __name__ == "__main__":
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    # tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')
    tune_path = tune_dir.joinpath('true_romance_verse.musicxml')
    melody = TrebleScore(tune_path)
    compose_blanket(melody)
