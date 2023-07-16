import argparse
import sys
import imageProcessor

# Setup Argument Parsing
parser = argparse.ArgumentParser(
    prog='Glyph Cutter 9000',
    description='Cuts bitmap glyphs to a template type of your choosing.',
    epilog='Written by Alexankitty 2023.',
    add_help=False)

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
    '-o','--output',
    help='Where to save the file once done.',
    dest='outputFile',
    required=True)
optionalArgs.add_argument(
    '-sp','--space',
    type=int,
    help='Size (in px) of the space character.',
    dest='spaceSize')
optionalArgs.add_argument(
    '-c','--space-coordinate',
    help="Coordinates of a pixel in the space glyph. I'll do the math for you to find the glyph row and column. Format: x,y",
    dest='spaceCoord')
optionalArgs.add_argument(
    '-e','--empty',
    type=int,
    help='Amount of space (in px) for glyphs where a cut cannot be found.',
    dest='emptySize')
optionalArgs.add_argument(
    '-T','--treat-solid-as-end',
    help='Treats any completely solid glyphs as the end of the glyph set.',
    dest='solidBehavior',
    action='store_true')
optionalArgs.add_argument(
    '-t','--templatefile',
    dest='templateFile',
    help='Path to a template text file to tell this program how to build the cuts into the output. Not including a template will put the cuts directly into a txt file.')
optionalArgs.add_argument(
    '-g','--gui',
    help='Display the GUI version for inputting these arguments.',
    action='store_true')
optionalArgs.add_argument(
    '-h','--help',
    help='Show this help message and exit',
    action='help')

args = parser.parse_args()
if len(sys.argv) < 2:
    parser.print_help()

# To do: Call GUI here before we dive into converting to globals.

# Convert arguments into globals.
if len(sys.argv) > 3:
    imageFile = args.imageFile
    glyphSize = args.glyphSize
    kerningSize = args.kerningSize
    emptySize = args.emptySize
    outputFile = args.outputFile
    space = args.spaceSize
    spaceCoord = args.spaceCoord
    solidBehavior = args.solidBehavior
    templateFile = args.templateFile

font = imageProcessor.Font(imageFile, glyphSize, kerningSize, emptySize, space, spaceCoord, solidBehavior, templateFile)
cuts = font.cutGlyphs()
process = font.processCuts()
output = open(outputFile, 'w')
output.write(process)
