"""
read_tune.py

Reads melody from musicxml file and returns pitch & rhythm info.
"""

from pathlib import Path
from musicxml_parser.scoreToPianoroll import scoreToPianoroll


# test musicxml_parser package from https://github.com/qsdfo/musicxml_parser
tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')
quantization = 16
pianoroll, articulation = scoreToPianoroll(tune_path, quantization)

out_path = Path(__file__).resolve().parent.parent.joinpath('output')
out_path.mkdir(exist_ok=True)
with open(out_path.joinpath('test_pianoroll.txt'), 'w') as file_out:
    file_out.write(str(pianoroll))
    file_out.write("\n\n")
    file_out.write(str(articulation))
# does not seem to work!


'''
found an excellent tutorial giving a breakdown of musicxml file structure:
https://www.w3.org/2021/06/musicxml40/tutorial/hello-world/
'''
