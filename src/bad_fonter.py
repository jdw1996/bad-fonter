#!/usr/bin/env python3
#
# Created by Joseph Winters
# October 2019
#

import os
import sys
import configparser

USAGE = "{} config_file glyph_dir [output_filename]".format(sys.argv[0])
ERROR_WRONG_NUMBER_OF_ARGUMENTS = "Usage Error: Incorrect number of arguments provided."
ERROR_MISSING_CONFIG_FILE = "Usage Error: The config file specified cannot be found."
ERROR_MISSING_GLYPH_DIRECTORY = "Usage Error: The glyph directory specified cannot be found."

COMMAND_STARTFONT = "STARTFONT 2.1"
COMMAND_DESCRIPTION = "FONT"
COMMAND_SIZE = "SIZE"
COMMAND_FONTBOUNDINGBOX = "FONTBOUNDINGBOX"
COMMAND_NUM_CHARS = "CHARS"
COMMAND_ENDFONT = "ENDFONT"

SECTION_DESCRIPTION = "Description"
SECTION_METRICS = "Metrics"

KEY_FOUNDRY = "Foundry"
KEY_FAMILY_NAME = "FamilyName"
KEY_WEIGHT_NAME = "WeightName"
KEY_SLANT = "Slant"
KEY_SETWIDTH_NAME = "SetwidthName"
KEY_ADD_STYLE_NAME = "AddStyleName"
KEY_POINT_SIZE = "PointSize"
KEY_RESOLUTION_X = "ResolutionX"
KEY_RESOLUTION_Y = "ResolutionY"
KEY_SPACING = "Spacing"
KEY_CHARSET_REGISTRY = "CharsetRegistry"
KEY_CHARSET_ENCODING = "CharsetEncoding"
KEY_BASELINE_OFFSET = "BaselineOffset"

FALLBACK_FOUNDRY = ""
FALLBACK_FAMILY_NAME = "Test"
FALLBACK_WEIGHT_NAME = "medium"
FALLBACK_SLANT = "r"
FALLBACK_SETWIDTH_NAME = "normal"
FALLBACK_ADD_STYLE_NAME = ""
FALLBACK_POINT_SIZE = "12"
FALLBACK_RESOLUTION_X = "75"
FALLBACK_RESOLUTION_Y = "75"
FALLBACK_SPACING = "c"
FALLBACK_CHARSET_REGISTRY = "iso10646"
FALLBACK_CHARSET_ENCODING = "1"
FALLBACK_BASELINE_OFFSET = -3

class BDFWriter:

    def __init__(self, config_filename, glyph_dir, output_filename):
        self.read_config(config_filename)
        self.glyph_dir = glyph_dir
        self.output_filename = output_filename
        with open(os.listdir(self.glyph_dir)[0], "r") as c:
            lines = c.readlines()
            self.character_height = len(lines)
            self.character_width = len(lines[0])

    def __enter__(self):
        self.output_file = open(output_filename, "w")
        self.output_file.write("{}\n".format(COMMAND_STARTFONT))
        return self

    def __exit__(self):
        self.output_file.write(COMMAND_ENDFONT)
        self.output_file.close()

    def read_config(self, config_filename):
        parser = configparser.ConfigParser()
        parser.read(config_filename)

        # Get settings used in font description.
        self.foundry = parser.get(SECTION_DESCRIPTION, KEY_FOUNDRY, fallback=FALLBACK_FOUNDRY)
        self.family_name = parser.get(SECTION_DESCRIPTION, KEY_FAMILY_NAME, fallback=FALLBACK_FAMILY_NAME)
        self.weight_name = parser.get(SECTION_DESCRIPTION, KEY_WEIGHT_NAME, fallback=FALLBACK_WEIGHT_NAME)
        self.slant = parser.get(SECTION_DESCRIPTION, KEY_SLANT, fallback=FALLBACK_SLANT)
        self.setwidth_name = parser.get(SECTION_DESCRIPTION, KEY_SETWIDTH_NAME, fallback=FALLBACK_SETWIDTH_NAME)
        self.add_style_name = parser.get(SECTION_DESCRIPTION, KEY_ADD_STYLE_NAME, fallback=FALLBACK_ADD_STYLE_NAME)
        self.point_size = parser.get(SECTION_DESCRIPTION, KEY_POINT_SIZE, fallback=FALLBACK_POINT_SIZE)
        self.resolution_x = parser.get(SECTION_DESCRIPTION, KEY_RESOLUTION_X, fallback=FALLBACK_RESOLUTION_X)
        self.resolution_y = parser.get(SECTION_DESCRIPTION, KEY_RESOLUTION_Y, fallback=FALLBACK_RESOLUTION_Y)
        self.spacing = parser.get(SECTION_DESCRIPTION, KEY_SPACING, fallback=FALLBACK_SPACING)
        self.charset_registry = parser.get(SECTION_DESCRIPTION, KEY_CHARSET_REGISTRY, fallback=FALLBACK_CHARSET_REGISTRY)
        self.charset_encoding = parser.get(SECTION_DESCRIPTION, KEY_CHARSET_ENCODING, fallback=FALLBACK_CHARSET_ENCODING)

        # Get settings for font dimensions.
        self.baseline_offset = parser.getint(
            SECTION_METRICS, KEY_BASELINE_OFFSET, fallback=FALLBACK_BASELINE_OFFSET
        )

    def create_font_name(self):
        name_parts = [
            self.foundry,
            self.family_name,
            self.weight_name,
            self.slant,
            self.setwidth_name,
            self.add_style_name,
            self.point_size // 10,
            self.point_size,
            self.resolution_x,
            self.resolution_y,
            self.spacing,
            self.character_width,
            self.charset_registry,
            self.charset_encoding
        ]
        return "-" + "-".join(name_parts)

    def generate_preamble(self):
        with open(self.output_filename, "w") as f:
            f.write("{} {}\n".format(COMMAND_DESCRIPTION, self.create_font_name()))
            f.write("{} {} {} {}\n".format(
                COMMAND_SIZE, self.point_size // 10, self.resolution_x, self.resolution_y
            ))
            f.write("{} {} {} {} {}\n".format(
                COMMAND_FONTBOUNDINGBOX,
                self.character_width, self.character_height, 0, self.baseline_offset
            ))
            f.write("{} {}\n".format(COMMAND_NUM_CHARS, len(os.listdir(self.glyph_dir))))

    def generate_character(self, glyph_filename):
        glyph_name = glyph_filename.split(".")[0]
        # TODO: Translate to the correct glyph name.
        with open(glyph_filename, "r") as f:
            pass
            # TODO: Read in the glyph
        # TODO: Determine necessary properties of the glyph.
        # TODO: Write the glyph and its properties to file.

    def generate_characters(self):
        for glyph_filename in os.listdir(self.glyph_dir):
            self.generate_character(glyph_filename)

    def generate(self):
        self.generate_preamble()
        self.generate_characters()

if __name__ == "__main__":
    if len(sys.argv) not in (3,4):
        print(ERROR_WRONG_NUMBER_OF_ARGUMENTS, file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    config_filename = sys.argv[1]
    if not os.path.isfile(config_filename):
        print(ERROR_MISSING_CONFIG_FILE, file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(2)

    glyph_dir = sys.argv[2]
    if not os.path.isdir(glyph_dir):
        print(ERROR_MISSING_GLYPH_DIRECTORY, file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) == 4:
        output_filename = sys.argv[3]
    else:
        output_filename = "a.bdf"

    with BDFWriter(config_filename, glyph_dir, output_filename) as b:
        b.generate()
