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

FONT_START_LINE = "STARTFONT 2.1"
FONT_END_LINE = "ENDFONT"

class BDFWriter:

    def __init__(self, config_filename, glyph_dir, output_filename):
        self.read_config(config_filename)
        self.glyph_dir = glyph_dir
        self.output_filename = output_filename

    def __enter__(self):
        self.output_file = open(output_filename, "w")
        self.output_file.write(FONT_START_LINE)
        return self

    def __exit__(self):
        self.output_file.write(FONT_END_LINE)
        self.output_file.close()

    def read_config(self, config_filename):
        parser = configparser.ConfigParser()
        parser.read(config_filename)
        # TODO: Read specific config options.

    def generate_preamble(self):
        pass
        # TODO: Generate preamble from settings and write to file.

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
