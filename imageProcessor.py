from PIL import Image

class Font:
    def __init__(self, imagePath, size, kerning, empty, template):
        self.image = Image.open(imagePath)
        self.glyphSize = size
        self.kerning = kerning
        self.template = template
        self.width, self.height = self.image.size
        if self.width % self.glyphSize or self.height % self.glyphSize:
            raise Exception("""Image width and height must be equally divisible by the glyph size!\n
                            Image size: X:%s Y:%s Provided Glyph Size: %spx""" % (self.width, self.height, self.glyphSize))
        self.glyphColumns = self.width // self.glyphSize
        self.glyphRows = self.height // self.glyphSize
        self.refColor = self.image.getpixel((0,0))
        self.cuts = [[None for col in range(self.glyphColumns)] for row in range(self.glyphRows)]
        self.empty = empty // 2
      
        def cutGlyphs():
            for y in range(self.glyphRows):
                for x in range(self.glyphColumns):
                    #Variable clean up
                    if cutPosL:
                        del cutPosL
                    if cutPosR:
                        del cutPosR
                    segmentX = self.glyphSize * x
                    segmentY = self.glyphSize * y
                    for y2 in range(self.glyphSize):
                        pixelY = segmentY + y2
                        for x2 in range(self.glyphSize):
                            pixelX = segmentX + x2
                            pixelColor = self.image.getpixel(pixelX,pixelY)
                            if isinstance(pixelColor, tuple):
                                for z in range(len(pixelColor)):
                                    if pixelColor[z] > self.refColor[z]:
                                        cutPosL = (pixelX, pixelY)
                                        if cutPosL:
                                            cutPosR = (pixelX, pixelY)
                            elif pixelColor > self.refColor:
                                cutPosL = (pixelX, pixelY)
                                if cutPosL:
                                    cutPosR = (pixelX, pixelY)
                if not cutPosL or cutPosR:
                    center = self.glyphSize // 2
                    print("Couldn't find a cut for glyph segment: X:%s Y:%s. Using the empty value." % (x, y))
                    self.cuts[x][y] = (center - self.empty, center + self.empty)
                self.cuts[x][y] = (cutPosL - kerning - 1 , cutPosR + kerning + 1)
            return self.cuts

        def processCuts():
            processed = ""
            #Default processing if we don't have a template
            if not self.template:
                for row in range(len(self.cuts)):
                    for col in range(len(self.cuts[row])):
                        processed += "(%s,%s)" % self.cuts[row][col]

            return processed