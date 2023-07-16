## Glyph Cutter 9000
This will cut glyphs from a provided bitmap font, and either dumped into a csv like file with tuples or any other text format file.

## Installation
1. Clone this repo.
2. `pip install requirements.txt`
3. Run the program using python

Example usage:
`python .\main.py -i .\FONT0.BMP -s 32 -k 2 -e 4 -o "FONT0 WIDTH TABLE.XML" -T -sp 15 -sc 5,5 -m 2 -t exampletemplate.xml -c 10 -lk`

## Usage and help
```
usage: Glyph Cutter 9000 -i IMAGEFILE -s GLYPHSIZE -k KERNINGSIZE -o OUTPUTFILE [-sp SPACESIZE] [-lk] [-rk]
                         [-m MATCHPX] [-c COLORTHRESHOLD] [-to TOPOFFSET] [-bo BOTTOMOFFSET] [-sc SPACECOORD]
                         [-e EMPTYSIZE] [-T] [-t TEMPLATEFILE] [-g] [-h]

Cuts bitmap glyphs to a template type of your choosing.

required arguments:
  -i IMAGEFILE, --imagefile IMAGEFILE
                        Path to a bitmap image with glyphs to cut.
  -s GLYPHSIZE, --size GLYPHSIZE
                        Size (in px) of each glyph section to cut.
  -k KERNINGSIZE, --kerning KERNINGSIZE
                        Amount of space (in px) between each glyph.
  -o OUTPUTFILE, --output OUTPUTFILE
                        Where to save the file once done.

optional arguments:
  -sp SPACESIZE, --space SPACESIZE
                        Size (in px) of the space character.
  -lk, --leftside-kerning
                        Apply kerning to left side (by default we assume both sides).
  -rk, --rightside-kerning
                        Apply kerning to right side (by default we assume both sides).
  -m MATCHPX, --match-threshold MATCHPX
                        How many pixels need to be matched before it can be considered a cut point. Defaults to 1.
  -c COLORTHRESHOLD, --color-threshold COLORTHRESHOLD
                        How different does the pixel need to be from the background before we can match it
  -to TOPOFFSET, --top-offset TOPOFFSET
                        How many pixels from the top before we can start looking for matches.
  -bo BOTTOMOFFSET, --bottom-offset BOTTOMOFFSET
                        How many pixels from the bottom until we stop looking for matches.
  -sc SPACECOORD, --space-coordinate SPACECOORD
                        Coordinates of a pixel in the space glyph. I'll do the math for you to find the glyph row and
                        column. Format: x,y
  -e EMPTYSIZE, --empty EMPTYSIZE
                        Amount of space (in px) for glyphs where a cut cannot be found.
  -T, --treat-solid-as-end
                        Treats any completely solid glyphs as the end of the glyph set.
  -t TEMPLATEFILE, --templatefile TEMPLATEFILE
                        Path to a template text file to tell this program how to build the cuts into the output. Not
                        including a template will put the cuts directly into a txt file.
  -g, --gui             Display the GUI version for inputting these arguments.
  -h, --help            Show this help message and exit
```

## Template formating
An exampletemplate.xml is included, but you can really use any format as long as it's a text file.
### You're given a few template place holders to work with.
$row - row number of each glyph.  
$col - column number of each glyph  
$leftcut - number of pixels from the left side up to the first differing pixel minus kerning  
$rightcut - number of pixels from the left side to the right most differing pixel plus kerning
Any placeholders can be wrapped in parentheses to perform a mathematical calculation on them.  
Ex: ($row + 1) to make the row count start at one.
  
You must use both or neither of the below.  
$startcol - Section of your column format data.  
$startrow - section of your row format data  
The script will automagically determine whichever instance is deeper and act accordingly.