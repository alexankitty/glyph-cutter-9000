import argparse
import sys
import imageProcessor
import gui
import strings
import random

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
    help=strings.imageFileHelp,
    dest='imageFile')
requiredArgs.add_argument(
    '-s','--size',
    type=int,
    help=strings.glyphSizeHelp,
    dest='glyphSize')
requiredArgs.add_argument(
    '-k','--kerning',
    type=int,
    help=strings.kerningSizeHelp,
    dest='kerningSize')
requiredArgs.add_argument(
    '-o','--output',
    help=strings.outputFileHelp,
    dest='outputFile')
optionalArgs.add_argument(
    '-sp','--space',
    type=int,
    help=strings.spaceSizeHelp,
    dest='spaceSize')
optionalArgs.add_argument(
    '-lk','--leftside-kerning',
    help=strings.leftKerningHelp,
    dest='leftKerning',
    action='store_true')
optionalArgs.add_argument(
    '-rk','--rightside-kerning',
    help=strings.rightKerningHelp,
    dest='rightKerning',
    action='store_true')
optionalArgs.add_argument(
    '-m','--match-threshold',
    type=int,
    help=strings.matchPxHelp,
    dest='matchPx')
optionalArgs.add_argument(
    '-c','--color-threshold',
    type=int,
    help=strings.colorThresholdHelp,
    dest='colorThreshold')
optionalArgs.add_argument(
    '-to','--top-offset',
    type=int,
    help=strings.topOffsetHelp,
    dest='topOffset')
optionalArgs.add_argument(
    '-bo','--bottom-offset',
    type=int,
    help=strings.bottomOffsetHelp,
    dest='bottomOffset')
optionalArgs.add_argument(
    '-sc','--space-coordinate',
    help=strings.spaceCoordHelp,
    dest='spaceCoord')
optionalArgs.add_argument(
    '-e','--empty',
    type=int,
    help=strings.emptySizeHelp,
    dest='emptySize')
optionalArgs.add_argument(
    '-gl','--glyph-limit',
    type=int,
    help=strings.glyphLimitHelp,
    dest='glyphLimit')
optionalArgs.add_argument(
    '-T','--treat-solid-as-end',
    help=strings.solidBehaviorHelp,
    dest='solidBehavior',
    action='store_true')
optionalArgs.add_argument(
    '-r','--retry',
    help=strings.retryHelp,
    dest='retry',
    action='store_true')
optionalArgs.add_argument(
    '-t','--templatefile',
    dest='templateFile',
    help=strings.templateFileHelp)
optionalArgs.add_argument(
    '-g','--gui',
    help=strings.guiHelp,
    dest='guiEnable',
    action='store_true')
optionalArgs.add_argument(
    '-h','--help',
    help=strings.help,
    action='help')


if len(sys.argv) < 2:
    gui.run()
args = parser.parse_args()
if args.guiEnable:
    gui.run()
# Convert arguments into globals.
elif len(sys.argv) > 3 and not args.guiEnable:
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
    glyphLimit = args.glyphLimit
    retry = args.retry
    font = imageProcessor.Font(imageFile, glyphSize, kerningSize, emptySize, space, spaceCoord, solidBehavior, leftKerning, rightKerning, matchPx, topOffset, bottomOffset, colorThreshold, glyphLimit, retry, templateFile)
    cuts = font.cutGlyphs()
    process = font.processCuts()
    output = open(outputFile, 'w')
    output.write(process)
    if not round(random.random() * 100) == 69:
        print("Finished cutting fonts. Thank you and have a wonderful day.")
    else:
        print("Finished cutting fonts, now get the hell off my property.")