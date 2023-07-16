from PIL import Image
from pathlib import Path
import regex

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
        if self.template:
            self.templateLeftover = Path(self.template).read_text(encoding='UTF-8')
            colDeepest = self.getDeepestItem("startcol", self.templateLeftover) > self.getDeepestItem("startrow", self.templateLeftover)
            if colDeepest:
                templateColumn = self.getSectionTemplate("col", self.templateLeftover)
                templateRow = self.getSectionTemplate("row", self.templateLeftover)
            else:
                templateRow = self.getSectionTemplate("row", self.templateLeftover)
                templateColumn = self.getSectionTemplate("col", self.templateLeftover)
            processedColumn = ""
            processedRow = ""
            processedTemplate = ""
            if not templateColumn and not templateRow:
                for row in range(len(self.cuts)):
                    if self.cuts[row] == None:
                        break
                    for col in range(len(self.cuts[row])):
                        if self.cuts[row][col] == None:
                            break
                        cuts = self.cuts[row][col]
                        processedTemplate += self.parseTemplate("row", self.templateLeftover, row)
                        processedTemplate += self.parseTemplate("col", self.templateLeftover, col)
                        processedTemplate += self.parseTemplate("leftcut", self.templateLeftover, cuts[0])
                        processedTemplate += self.parseTemplate("rightcut", self.templateLeftover, cuts[1])
            elif colDeepest:
                for row in range(len(self.cuts)):
                    processedColumn = ""
                    if self.cuts[row] == None:
                        break
                    for col in range(len(self.cuts[row])):
                        if self.cuts[row][col] == None:
                            break
                        cuts = self.cuts[row][col]
                        currentColumn = self.processTemplate("col", templateColumn, col, cuts)
                        processedColumn += currentColumn
                    currentRow = self.parseTemplate("row", templateRow, row)
                    currentRow = self.parseTemplate("replacecol", currentRow, processedColumn)
                    processedRow += currentRow
                processedTemplate = self.parseTemplate("replacerow", self.templateLeftover, processedRow)

            else:
                row = 0
                for col in range(len(self.cuts[row])):
                    processedRow = ""
                    if self.cuts[row] == None or self.cuts[row][col] == None:
                        break
                    while row < len(self.cuts):
                        cuts = self.cuts[row][col]
                        currentRow = self.processTemplate("row", templateRow, row, cuts)
                        processedRow += currentRow
                        row += 1
                    row = 0
                    currentColumn = self.parseTemplate("col", templateColumn, col)
                    currentColumn = self.parseTemplate("replacerow",currentColumn,processedRow)
                    processedColumn += currentColumn
                processedTemplate = self.parseTemplate("replacecol", self.templateLeftover, processedColumn)
            return processedTemplate
            
    def parseTemplate(self, search, templateString, replace):
        replace = str(replace)
        regExBase = r"\(\$templateItem.+(.+?).+\)"
        regExSearch = regExBase.replace("templateItem", search)
        regExList = regex.findall(regExSearch, templateString)
        if len(regExList) == 0:
            regExList = regex.findall(search, templateString)
            if len(regExList) == 0:
                return templateString
            if search == "replacerow" or search == "replacecol":
                templateString = regex.sub(r"\s*\$" + search, replace, templateString)
            else:
                templateString = regex.sub(r"\$" + search, replace, templateString)
            return templateString
        for x in range(len(regExList)):
            stringEval = regex.search(regExSearch,templateString)
            if not stringEval:
                return templateString
            stringEval = stringEval.group()
            stringEval = regex.sub(r"\$" + search, replace, stringEval)
            stringEval = str(eval(stringEval))
            templateString = regex.sub(regExSearch, stringEval, templateString, 1)
        return templateString
    
    def getSectionTemplate(self, search, templateString):
        regExBase = r"(\$startsection)([\s\S]*)(\$endsection)"
        regExStart = r"\s*\$startsection"
        regExStart = regExStart.replace("section", search)
        regExEnd = r"\s*\$endsection"
        regExEnd = regExEnd.replace("section", search)
        regExSearch = regExBase.replace("section", search)
        regExList = regex.findall(regExSearch, templateString)
        if len(regExList) > 1:
            raise Exception("Only one %s section allowed!" % "$" + search)
        if len(regExList) == 0:
            return False
        templateSection = regex.search(regExSearch, templateString).group()
        templateSection = regex.sub(regExStart, "", templateSection, 1)
        templateSection = regex.sub(regExEnd, "", templateSection, 1)
        self.templateLeftover = regex.sub(regExSearch, "$replace" + search, templateString)
        return templateSection

    def processTemplate(self, search, template, replace, cuts):
        template = self.parseTemplate(search, template, replace)
        template = self.parseTemplate("leftcut", template, cuts[0])
        template = self.parseTemplate("rightcut", template, cuts[1])
        return template
    
    def getDeepestItem(self, search, template):
        deepest = regex.search(r"\$"+ search, template).span()[1]
        return deepest