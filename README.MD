## Glyph Cutter 9000
This will cut glyphs from a provided bitmap font, and either dumped into a csv like file with tuples or any other text format file.

## Installation
1. Clone this repo.
2. `pip install requirements.txt`
3. Run the program using python


## Usage and help
```
usage: Glyph Cutter 9000 [-i IMAGEFILE] [-s GLYPHSIZE] [-k KERNINGSIZE] [-o OUTPUTFILE] [-sp SPACESIZE] [-lk] [-rk]
                         [-m MATCHPX] [-c COLORTHRESHOLD] [-to TOPOFFSET] [-bo BOTTOMOFFSET] [-sc SPACECOORD]
                         [-e EMPTYSIZE] [-gl GLYPHLIMIT] [-T] [-r] [-t TEMPLATEFILE] [-g] [-h]

Cuts bitmap glyphs to a template type of your choosing.

required arguments:
  -i IMAGEFILE, --imagefile IMAGEFILE
                        Path to an image with glyphs (fonts) to cut.
  -s GLYPHSIZE, --size GLYPHSIZE
                        Size (in px) of each glyph section to cut. If unsure, you'll need to check in your image
                        editor and setup a grid until everything is evenly sized.
  -k KERNINGSIZE, --kerning KERNINGSIZE
                        Amount of space (in px) between each glyph.
  -o OUTPUTFILE, --output OUTPUTFILE
                        Where to save the file once done. It can be in any text format.

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
                        How different does the pixel need to be from the background before we can count is as a match
  -to TOPOFFSET, --top-offset TOPOFFSET
                        How many pixels from the top before we can start looking for matches.
  -bo BOTTOMOFFSET, --bottom-offset BOTTOMOFFSET
                        How many pixels from the bottom until we stop looking for matches.
  -sc SPACECOORD, --space-coordinate SPACECOORD
                        Coordinates of a pixel in the space glyph. I'll do the math for you to find the glyph row and
                        column. Format: x,y
  -e EMPTYSIZE, --empty EMPTYSIZE
                        Amount of space (in px) for glyphs where a cut cannot be found.
  -gl GLYPHLIMIT, --glyph-limit GLYPHLIMIT
                        How many glyphs you want to process. Set this value to a negative to subtract from the total
                        glyph count.
  -T, --treat-solid-as-end
                        Treats any completely solid glyphs as the end of the glyph set.
  -r, --retry           Re-attempt to cut an unsuccessful glyph by ignoring the top and bottom offsets
  -t TEMPLATEFILE, --templatefile TEMPLATEFILE
                        Path to a template text file to tell this program how to build the cuts into the output. Not
                        including a template will put the cuts directly into a txt file. Please refer to the readme
                        for more info.
  -g, --gui             Display the GUI version for inputting these arguments.
  -h, --help            Show this help message and exit.
```

`python .\main.py -i .\FONT0.png -k 0 -s 32 -o .\FONT0.XML -t .\exampletemplate.xml -gl -6 -to 14 -sp 16 -sc 5,5`  

Keep in mind, the result won't be perfect but should be fairly close. You'll want to look over the font and make any other tweaks as needed.  

Use the gui by either running main.py directly, or by using -g when executing main.py.

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