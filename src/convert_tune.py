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
    # length multiplier & divider thickness (!)
    # etc
    pass
    # (compose_blanket does not currently utilize this)


def compose_blanket(score: TrebleScore, fig_name: str = ""):
    # visual magic!
    pitches = score.pitches
    durations = score.durations
    width = 2
    length_multiplier = 10
    divider_thickness = 2
    # turns out divider_thickness is an important parameter
    # (or rather, divider_thickness relative to length_multiplier)
    # vivaldi theme looks much better with it set to 1
    # whereas true romance verse looks much better with it set to 2
    # despite the 2 having similar {note + rest} count
    # sooo remember to include it in BlanketDesign class!
    rest_pitch = np.min(pitches) - (score.pitch_range // 5 + 2)
    note_divider = np.full(
        (width, divider_thickness), rest_pitch - 2 * score.pitch_range // 5
    )
    # output directory
    out_path = Path(__file__).resolve().parent.parent.joinpath('output')
    out_path.mkdir(exist_ok=True)
    # tile pitches according to durations
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
        # debug mode
        if debug_switch:
            with open(out_path.joinpath('tune_blanket_part.txt'), 'w') as file_out:
                for i in range(len(part_blanket)):
                    for j in range(len(part_blanket[i])):
                        file_out.write(str(part_blanket[i, j]) + "  ")
                    file_out.write("\n")
        # visualize part
        if True:
            plt.figure()  # figsize=(,)
            plt.contourf(part_blanket, int(score.pitch_range * 1.5))
            plt.tick_params(
                axis='both', which='both',
                left=False, bottom=False,
                labelleft=False, labelbottom=False
            )
            if fig_name != "":
                plt.savefig(out_path.joinpath(fig_name), dpi=1024)
            plt.show()


if __name__ == "__main__":
    debug_switch = False
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    # tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')
    tune_path = tune_dir.joinpath('true_romance_verse.musicxml')
    melody = TrebleScore(tune_path)
    compose_blanket(melody)
