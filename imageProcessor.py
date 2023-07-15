from PIL import Image

class Font:
    def __init__(self, imagePath, size, kerning, empty, space, spaceCoord, solidBehavior, template):
        self.image = Image.open(imagePath)
        self.glyphSize = size
        self.kerning = kerning
        self.template = template
        self.width, self.height = self.image.size
        if not empty:
            self.empty = 0
        else:
            self.empty = self.glyphSize // 2
        if not space:
            self.spaceSize = 0
        else:
            self.spaceSize = space // 2
        if spaceCoord:
            string = spaceCoord.split(",")
            self.spaceX = int(string[0]) // self.glyphSize
            self.spaceY = int(string[1]) // self.glyphSize
            self.space = True
        if solidBehavior:
            self.solidBehavior = True
        else:
            self.solidBehavior = False
        if self.width % self.glyphSize or self.height % self.glyphSize:
            raise Exception("""Image width and height must be equally divisible by the glyph size!\n
                            Image size: X:%s Y:%s Provided Glyph Size: %spx""" % (self.width, self.height, self.glyphSize))
        self.glyphColumns = self.width // self.glyphSize
        self.glyphRows = self.height // self.glyphSize
        self.refColor = self.image.getpixel((0,0))
        self.cuts = [[None for cols in range(self.glyphColumns)] for rows in range(self.glyphRows)]

        print (len(self.cuts), len(self.cuts[0]))
    
    def cutGlyphs(self):
        for row in range(self.glyphRows):
            for col in range(self.glyphColumns):
                #Variable clean up
                cutPosL = None
                cutPosR = None
                segmentX = self.glyphSize * col
                segmentY = self.glyphSize * row
                for x in range(self.glyphSize):
                    pixelX = segmentX + x
                    for y in range(self.glyphSize):
                        pixelY = segmentY + y
                        pixelColor = self.image.getpixel((pixelX,pixelY))
                        if isinstance(pixelColor, tuple):
                            for z in range(len(pixelColor)):
                                if pixelColor[z] > self.refColor[z]:
                                    if cutPosL == None:
                                        cutPosL = x
                                    if cutPosL >= 0:
                                        cutPosR = self.glyphSize - 1 - x
                        elif pixelColor > self.refColor:
                            if cutPosL == None:
                                cutPosL = x
                            if cutPosL >= 0:
                                cutPosR = self.glyphSize - 1 - x
                center = self.glyphSize // 2
                if self.space == True and row == self.spaceX and col == self.spaceY:
                    self.cuts[row][col] = (center - self.spaceSize, center + self.spaceSize)
                elif cutPosL == None and cutPosR == None:
                    if center == self.empty:
                        print("Couldn't find a cut for glyph segment: X:%s Y:%s. Using %s." % (row, col, 0))
                        self.cuts[row][col] = (0,0)
                    else:
                        print("Couldn't find a cut for glyph segment: X:%s Y:%s. Using %s from center." % (row, col, self.empty))
                        self.cuts[row][col] = (center - self.empty, center + self.empty)
                elif cutPosL == 0 and cutPosR == 0:
                    if self.solidBehavior:
                        print("Reached end of glyphs, not processing more.")
                        return self.cuts
                    self.cuts[row][col] = (0,0)
                else:
                    self.cuts[row][col] = (cutPosL - self.kerning, cutPosR - self.kerning)
        return self.cuts
    
    def processCuts(self):
        processed = ""
        #Default processing if we don't have a template
        if not self.template:
            for row in range(len(self.cuts)):
                if self.cuts[row] == None:
                    return processed
                for col in range(len(self.cuts[row])):
                    if self.cuts[row][col] == None:
                        return processed
                    processed += "(%s,%s)," % self.cuts[row][col]
                processed += "\n"
        return processed
