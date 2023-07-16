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
    '-lk','--leftside-kerning',
    help='Apply kerning to left side (by default we assume both sides).',
    dest='leftKerning',
    action='store_true')
optionalArgs.add_argument(
    '-rk','--rightside-kerning',
    help='Apply kerning to right side (by default we assume both sides).',
    dest='rightKerning',
    action='store_true')
optionalArgs.add_argument(
    '-m','--match-threshold',
    type=int,
    help='How many pixels need to be match before it can be considered a cut point. Defaults to 1.',
    dest='matchPx')
optionalArgs.add_argument(
    '-c','--color-threshold',
    type=int,
    help='How different does the pixel need to be from the background before we can match it',
    dest='colorThreshold')
optionalArgs.add_argument(
    '-to','--top-offset',
    type=int,
    help='How many pixels from the top before we can start looking for matches.',
    dest='topOffset')
optionalArgs.add_argument(
    '-bo','--bottom-offset',
    type=int,
    help='How many pixels from the bottom until we stop looking for matches.',
    dest='bottomOffset')
optionalArgs.add_argument(
    '-sc','--space-coordinate',
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


if len(sys.argv) < 2:
    parser.print_help()
args = parser.parse_args()
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
    leftKerning = args.leftKerning
    rightKerning = args.rightKerning
    matchPx = args.matchPx
    topOffset = args.topOffset
    bottomOffset = args.bottomOffset
    colorThreshold = args.colorThreshold

font = imageProcessor.Font(imageFile, glyphSize, kerningSize, emptySize, space, spaceCoord, solidBehavior, leftKerning, rightKerning, matchPx, topOffset, bottomOffset, colorThreshold, templateFile)
cuts = font.cutGlyphs()
process = font.processCuts()
output = open(outputFile, 'w')
output.write(process)
