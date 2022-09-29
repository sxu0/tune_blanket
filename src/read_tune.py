"""
read_tune.py
------------
reads melody from musicxml file and returns pitch & rhythm info.
limitations (for now): partwise (as opposed to timewise),
treble clef, single time signature, single key signature.

sources
---------
* musicxml file conventions tutorial:
https://www.w3.org/2021/06/musicxml40/tutorial/hello-world/
* built-in python module for reading xml files:
https://docs.python.org/3/library/xml.etree.elementtree.html
"""

import warnings

from pathlib import Path
from xml.etree import ElementTree


class TrebleScore:

    clef = "treble"

    class Pitch:

        def __init__(self, step: str, alter: int, octave: int):
            if alter == 0:
                accidental = ""
            elif alter == -1:
                accidental = "b"
            elif alter == 1:
                accidental = "#"
            elif alter == -2:
                accidental = "bb"
            elif alter == 2:
                accidental = "x"
            self.name = step + accidental + str(octave)
            self.letter = step
            self.accidental = alter
            self.octave = octave
            self.num = self.pitch_name_to_num(step, alter, octave)

        def pitch_name_to_num(self, step: str, alter: int, octave: int):
            # conversion to a relative integer system
            # stored as a Pitch attribute
            # 12-tone system where each half step is treated equally
            # (alternatively, could employ a scale-based system)
            # define C4 (middle C) as 0, C3 as -12, C5 as 12, and so on
            step_to_num = {
                'C': 0,
                'D': 2,
                'E': 4,
                'F': 5,
                'G': 7,
                'A': 9,
                'B': 11
            }
            pitch_num = (octave - 4) * 12 + step_to_num[step] + alter
            return pitch_num


    def __init__(self, musicxml_path):
        self.pitches, self.durations = [], []
        # read xml file
        tree = ElementTree.parse(musicxml_path)
        root = tree.getroot()
        if root.tag == "score-partwise":
            pass
        elif root.tag == "score-timewise":
            warnings.warn("Timewise scores are not yet supported.")
        for part in root.iter("part"):
            for measure in part.iter("measure"):
                for attributes in measure.iter("attributes"):
                    for divisions in attributes.iter("divisions"):
                        self.divisions = int(divisions.text)
                    for key in attributes.iter("key"):
                        for fifths in key.iter("fifths"):
                            self.key_circ5 = int(fifths.text)
                    for clef in attributes.iter("clef"):
                        sign = clef.find("sign").text
                        line = clef.find("line").text
                        if sign != "G" or line != "2":
                            warnings.warn(
                                "Non-treble clef scores are not yet supported."
                            )
                for note in measure.iter("note"):
                    for pitch in note.iter("pitch"):
                        step = pitch.find("step").text
                        if pitch.find("alter") is not None:
                            alter = int(pitch.find("alter").text)
                        else:
                            alter = 0
                        octave = int(pitch.find("octave").text)
                        note_pitch = self.Pitch(step, alter, octave)
                        self.pitches.append(note_pitch.num)
                        duration = int(note.find("duration").text)
                        self.durations.append(duration)
                    for rest in note.iter("rest"):
                        self.pitches.append(9999)
                        duration = int(note.find("duration").text)
                        self.durations.append(duration)
        # crop continuous rests at end of score
        (self.pitches, self.durations) = self.groom_tail()
        # verify same number of pitches and durations have been recorded
        if len(self.pitches) != len(self.durations):
            warnings.warn("Unequal numbers of pitches and durations recorded!")
            print("\t({0} note pitches/rests recorded, "\
                "{1} note/rest durations recorded)".format(
                    len(self.pitches), len(self.durations)
                )
            )
        # calculate pitch range in number of semitones
        self.pitch_range = self.find_pitch_range()


    def find_pitch_range(self):
        # finds range of pitches in number of semitones
        pitches_sans_rests = [sound for sound in self.pitches if sound != 9999]
        pitch_range = max(pitches_sans_rests) - min(pitches_sans_rests)
        return pitch_range

    def groom_tail(self):
        # deletes empty measures at end of score
        tail_rests = 0
        for i in range(len(self.pitches)-1, -1, -1):
            if i == len(self.pitches) - 1:
                if self.pitches[i] == 9999:
                    tail_rests += 1
            elif self.pitches[i] == 9999 and self.pitches[i+1] == 9999:
                tail_rests += 1
        if tail_rests == 0:
            return self.pitches, self.durations
        else:
            return self.pitches[:-tail_rests], self.durations[:-tail_rests]




if __name__ == "__main__":
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')

    spring = TrebleScore(tune_path)
    print("\npitches:")
    print(spring.pitches)
    print("\ndurations:")
    print(spring.durations)
    print("\npitch range:\t" + str(spring.pitch_range) + "\n")
