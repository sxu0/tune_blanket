"""
main.py
-------
magic headquarters
"""

from pathlib import Path

from read_tune import TrebleScore
from convert_tune import BlanketDesign, compose_blanket

if __name__ == "__main__":
    tune_dir = Path(__file__).resolve().parent.parent.joinpath('tune')
    # tune_path = tune_dir.joinpath('vivaldi_spring_main_theme.musicxml')
    # tune_path = tune_dir.joinpath('true_romance_verse.musicxml')
    # tune_path = tune_dir.joinpath('dvorak_9_english_horn_solo.musicxml')
    # tune_path = tune_dir.joinpath('bohemian_rhapsody_guitar_solo.musicxml')
    # tune_path = tune_dir.joinpath('twinkle_twinkle_little_star.musicxml')
    # tune_path = tune_dir.joinpath('still_got_the_blues_guitar_solo_triplet_version.musicxml')
    # tune_path = tune_dir.joinpath('sunset_road_excerpt.musicxml')
    # tune_path = tune_dir.joinpath('krommer_concerto_for_2_clarinets_excerpt.musicxml')
    tune_path = tune_dir.joinpath('bach_fugue_in_Bb+_excerpt_parts.musicxml')
    melody = TrebleScore(tune_path)
    pattern = BlanketDesign()
    # fav colourmaps so far: 'viridis' (default), 'ocean', 'Purples'
    # add '_r' to end of colourmap names to reverse the colour scale
    pattern.colour_blanket('Purples_r', 4, 1)
    compose_blanket(melody, pattern, 'bach_fugue_in_Bb+_excerpt_parts2.png')
