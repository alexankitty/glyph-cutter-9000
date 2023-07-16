## Glyph Cutter 9000
This will cut glyphs from a provided bitmap font, and either dumped into a csv like file with tuples or any other text format file.

## Installation
1. Clone this repo.
2. `pip install requirements.txt`
3. Run the program using python

## Usage and help
```
usage: Glyph Cutter 9000 -i IMAGEFILE -s GLYPHSIZE -k KERNINGSIZE -o OUTPUTFILE [-sp SPACESIZE] [-c SPACECOORD]
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
  -c SPACECOORD, --space-coordinate SPACECOORD
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
$rightcut - number of pixels from the right side up to the first differing pixel plus kerning.  
  
You must use both or neither of the below.  
$startcol - Section of your column format data.  
$startrow - section of your row format data  
The script will automagically determine whichever instance is deeper and act accordingly.