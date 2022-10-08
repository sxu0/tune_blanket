"""
read_tune.py
------------
reads melody from musicxml file and returns pitch & rhythm info.
limitations (for now): partwise (as opposed to timewise),
treble clef, single tempo/time signature, less common tuplets.

sources
-------
* musicxml file conventions:
https://www.w3.org/2021/06/musicxml40/tutorial/hello-world/
* built-in python module for xml files:
https://docs.python.org/3/library/xml.etree.elementtree.html
"""


import warnings
from xml.etree import ElementTree

import numpy as np
from pathlib import Path


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
        self.no_parts = 0
        # read xml file
        tree = ElementTree.parse(musicxml_path)
        root = tree.getroot()
        if root.tag == "score-partwise":
            pass
        elif root.tag == "score-timewise":
            warnings.warn("Timewise scores are not yet supported.")
        for part in root.iter("part"):
            self.no_parts += 1
            part_pitches, part_durations = [], []
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
                        duration = int(note.find("duration").text)
                        if note.find("tie") is None:
                            pass
                        elif note.find("tie").attrib["type"] == "stop":
                            part_durations[-1] += duration
                            continue
                        part_pitches.append(note_pitch.num)
                        part_durations.append(duration)
                    for rest in note.iter("rest"):
                        duration = int(note.find("duration").text)
                        if len(part_pitches) > 0 and part_pitches[-1] == 9999:
                            part_durations[-1] += duration
                        else:
                            part_pitches.append(9999)
                            part_durations.append(duration)
            self.pitches.append(part_pitches)
            self.durations.append(part_durations)
        self.pitches = np.array(self.pitches)
        self.durations = np.array(self.durations)
        # crop continuous rests at end of score
        (self.pitches, self.durations) = self.groom_tail()
        # verify same number of pitches and durations have been recorded
        if np.size(self.pitches) != np.size(self.durations):
            warnings.warn("Unequal numbers of pitches and durations recorded!")
            print("\t({0} note pitches/rests recorded & "\
                "{1} note/rest durations recorded across all parts)".format(
                    np.size(self.pitches), np.size(self.durations)
                )
            )
        # calculate pitch range in number of semitones
        self.pitch_range = self.find_pitch_range()

    def find_pitch_range(self):
        # finds range of pitches in number of semitones
        pitches_sans_rests = self.pitches[self.pitches != 9999]
        pitch_range = np.max(pitches_sans_rests) - np.min(pitches_sans_rests)
        return pitch_range

    def groom_tail(self):
        # deletes empty measures at end of score
        tail_rests_parts = []
        for i in range(self.no_parts):
            tail_rests = 0
            for j in range(len(self.pitches[i])-1, -1, -1):
                if j == len(self.pitches[i]) - 1:
                    if self.pitches[i][j] == 9999:
                        tail_rests += 1
                elif self.pitches[i][j] == 9999 and self.pitches[i][j+1] == 9999:
                    tail_rests += 1
            tail_rests_parts.append(tail_rests)
        tail_length = min(tail_rests_parts)
        if tail_length == 0:
            return self.pitches, self.durations
        else:
            return self.pitches[:, :-tail_length], self.durations[:, :-tail_length]
