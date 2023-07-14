import argparse
import sys
import imageProcessor

# Setup Argument Parsing
parser = argparse.ArgumentParser(
    prog='Glyph Cutter 9000',
    description='Cuts bitmap glyphs to a template type of your choosing.',
    epilog='Written by Alexankitty 2023.',
    add_help=False
)

requiredArgs = parser.add_argument_group('required arguments')
optionalArgs = parser.add_argument_group('optional arguments')

requiredArgs.add_argument(
    '-i','--imagefile',
    help='Path to a bitmap image with glyphs to cut.',
    dest='imageFile',
    required=True)
requiredArgs.add_argument(
    '-s','--size',
    type=int,
    help='Size (in px) of each glyph section to cut.',
    dest='glyphSize',
    required=True)
requiredArgs.add_argument(
    '-k','--kerning',
    type=int,
    help='Amount of space (in px) between each glyph.',
    dest='kerningSize',
    required=True)
requiredArgs.add_argument(
    '-e','--empty',
    type=int,
    help='Amount of space (in px) for glyphs where a cut cannot be found.',
    dest='emptySize',
    required=True)
requiredArgs.add_argument(
    '-o','--output',
    help='Where to save the file once done.',
    dest='outputFile',
    required=True)
optionalArgs.add_argument(
    '-t','--templatefile',
    dest='templateFile',
    help='Path to a template text file to tell this program how to build the cuts into the output. Not including a template will put the cuts directly into a txt file.'
    )
optionalArgs.add_argument(
    '-g','--gui',
    help='Display the GUI version for inputting these arguments.',
    action='store_true')
optionalArgs.add_argument(
    '-h','--help',
    help='Show this help message and exit',
    action='help')

if len(sys.argv) < 2:
    parser.print_help()
    print("\n")

# To do: Call GUI here before we dive into converting to globals.

# Convert arguments into globals.

if len(sys.argv) > 3:
    args = parser.parse_args()
    imageFile = args.imageFile
    glyphSize = args.glyphSize
    kerningSize = args.kerningSize
    outputFile = args.outputFile
    templateFile = args.templateFile

# Do the things.
image = imageProcessor.loadImage(imageFile)