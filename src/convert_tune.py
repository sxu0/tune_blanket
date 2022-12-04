"""
convert_tune.py
---------------
converts tune from numerical pitches/durations to a colourful blanket!
"""

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

from read_tune import TrebleScore


class BlanketDesign:

    def __init__(self):
        # set defaults
        self.shape_blanket()
        self.colour_blanket()
        self.save_blanket()

    def shape_blanket(self, div_size=1, len_mult=10):
        self.divider_thickness = div_size
        self.length_multiplier = len_mult

    def colour_blanket(self, colour_map='viridis', colour_mult=1.5):
        self.colour_map = colour_map
        self.colour_range_multiplier = colour_mult

    def save_blanket(self, dims=(6, 4), res=360):
        self.dimensions = dims
        self.resolution = res

    # yet to implement: custom rest colour


def compose_blanket(
    score: TrebleScore, design: BlanketDesign, fig_name: str = "", debug_switch=False
):
    # visual magic!
    width = 2
    if score.no_parts == 1:
        rest_pitch = min(score.pitches) - (score.pitch_range // 5 + 2)
    else:
        rest_pitch = min(min(score.pitches)) - (score.pitch_range // 5 + 2)
    note_divider = np.full(
        (width, design.divider_thickness), rest_pitch - 2 * score.pitch_range // 5
    )
    # output directory
    out_path = Path(__file__).resolve().parent.parent.joinpath('output')
    out_path.mkdir(exist_ok=True)
    # tile pitches according to durations
    for part in range(score.no_parts):
        part_blanket_sections = []
        part_pitches = score.pitches[part]
        part_durations = score.durations[part]
        for note in range(len(part_pitches)):
            if part_pitches[note] != 9999:
                pitch = part_pitches[note]
            else:
                pitch = rest_pitch
            blanket_section = np.full(
                (width, part_durations[note] * design.length_multiplier), pitch
            )
            part_blanket_sections.append(blanket_section)
            part_blanket_sections.append(note_divider)
        del part_blanket_sections[-1]
        part_blanket = np.concatenate(part_blanket_sections, axis=1)
        # debug mode
        if debug_switch:
            # write blanket array to txt file
            with open(out_path.joinpath('tune_blanket_part.txt'), 'w') as file_out:
                for i in range(len(part_blanket)):
                    for j in range(len(part_blanket[i])):
                        file_out.write(str(part_blanket[i, j]) + "  ")
                    file_out.write("\n")
            # visualize part
            plt.figure(figsize=design.dimensions)
            plt.contourf(
                part_blanket,
                int(score.pitch_range * design.colour_range_multiplier),
                cmap=design.colour_map
            )
            plt.tick_params(
                axis='both', which='both',
                left=False, bottom=False,
                labelleft=False, labelbottom=False
            )
            if fig_name != "":
                plt.savefig(out_path.joinpath(fig_name), dpi=design.resolution)
            plt.show()
