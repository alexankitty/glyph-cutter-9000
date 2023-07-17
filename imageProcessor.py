from PIL import Image
from pathlib import Path
import regex

class Font:
    def __init__(self, imagePath, size, kerning, empty, space, spaceCoord, solidBehavior, leftKerning, rightKerning, matchPx, topOffset, bottomOffset, colorThreshold, glyphLimit, retry, template):
        # sourcery skip: raise-specific-error
        self.image = Image.open(imagePath)
        self.glyphSize = size
        self.kerning = kerning
        self.template = template
        self.leftKerning = leftKerning
        self.rightKerning = rightKerning
        self.width, self.height = self.image.size
        self.topOffset = topOffset or 0
        if not bottomOffset:
            self.bottomOffset = self.glyphSize
        else:
            self.bottomOffset = self.glyphSize - bottomOffset
        self.matchPx = matchPx or 1
        self.empty = empty // 2 if empty else 0
        self.spaceSize = space // 2 if space else 0
        if spaceCoord:
            string = spaceCoord.split(",")
            self.spaceX = int(string[0]) // self.glyphSize
            self.spaceY = int(string[1]) // self.glyphSize
            self.space = True
        else:
            self.space = False
        self.solidBehavior = bool(solidBehavior)
        if self.width % self.glyphSize or self.height % self.glyphSize:
            raise Exception(f"""Image width and height must be equally divisible by the glyph size!\n
                            Image size: X:{self.width} Y:{self.height} Provided Glyph Size: {self.glyphSize}px""")
        self.glyphColumns = self.width // self.glyphSize
        self.glyphRows = self.height // self.glyphSize
        if not glyphLimit:
            self.glyphLimit = self.glyphColumns * self.glyphRows
        elif glyphLimit < 0:
            self.glyphLimit = (self.glyphColumns * self.glyphRows) + glyphLimit
        elif glyphLimit > 0:
            self.glyphLimit = glyphLimit
        self.refColor = self.image.getpixel((0,0))
        if isinstance(self.refColor, tuple):
            for z in range(len(self.refColor)):
                if not colorThreshold:
                    self.colorThreshold[z] = 0
                else:
                    self.colorThreshold[z] = self.refColor[z] + colorThreshold
        elif not colorThreshold:
            self.colorThreshold = self.refColor
        else:
            self.colorThreshold = self.refColor + colorThreshold
        self.cuts = [
            [None for _ in range(self.glyphColumns)] for _ in range(self.glyphRows)
        ]
        self.retry = retry or False
    def cutGlyphs(self):
        glyphCount = 0
        for row in range(self.glyphRows):
            for col in range(self.glyphColumns):
                retrying = False
                if glyphCount >= self.glyphLimit:
                    return self.cuts
                #Variable clean up
                cutPosL = None
                cutPosR = None
                segmentX = self.glyphSize * col
                segmentY = self.glyphSize * row
                x = 0
                while x < self.glyphSize:
                    pixelX = segmentX + x
                    matching = 0
                    y = 0
                    while y < self.glyphSize:
                        if y <= self.topOffset and not retrying:
                            y +=1
                            continue
                        if y >= self.bottomOffset and not retrying:
                            y +=1
                            continue
                        pixelY = segmentY + y
                        pixelColor = self.image.getpixel((pixelX,pixelY))
                        if isinstance(pixelColor, tuple):
                            for z in range(len(pixelColor)):
                                if pixelColor[z] > self.colorThreshold[z]:
                                    matching += 1
                                    if matching >= self.matchPx:
                                        if cutPosL == None:
                                            cutPosL = x
                                        if cutPosL >= 0:
                                            cutPosR = x + 1
                        elif pixelColor > self.colorThreshold:
                            matching += 1
                            if matching >= self.matchPx:
                                if cutPosL == None:
                                    cutPosL = x
                                if cutPosL >= 0:
                                    cutPosR = x + 1
                        y +=1
                    x +=1
                    if x == self.glyphSize and cutPosL == None and cutPosR == None and not retrying:
                        x = 0
                        y = 0
                        retrying = True
                        print(F"Failed to find a cut for X:{row} Y:{col}. Retrying without offsets.")
                center = self.glyphSize // 2
                if self.space == True and row == self.spaceX and col == self.spaceY:
                    self.cuts[row][col] = (center - self.spaceSize, center + self.spaceSize)
                
                elif cutPosL == None and cutPosR == None:
                    if self.empty == 0:
                        print(f"Couldn't find a cut for glyph segment: X:{row} Y:{col}. Using 0.")
                        self.cuts[row][col] = (0,0)
                    else:
                        print(f"Couldn't find a cut for glyph segment: X:{row} Y:{col}. Using {self.empty} from center.")
                        self.cuts[row][col] = (center - self.empty, center + self.empty)
                elif cutPosL == 0 and cutPosR == self.glyphSize - 1:
                    if self.solidBehavior:
                        print("Reached end of glyphs, not processing more.")
                        return self.cuts
                    self.cuts[row][col] = (0,0)
                else:
                    if self.leftKerning:
                        cutPosL -= self.kerning
                    if self.rightKerning:
                        cutPosR += self.kerning
                    if not self.leftKerning and not self.rightKerning:
                        cutPosL -= self.kerning
                        cutPosR += self.kerning
                    ## checking if we go out of bounds.
                    if cutPosL < 0:
                        cutPosL = 0
                    if cutPosR < 0:
                        cutPosR = 0
                    if cutPosL > self.glyphSize - 1:
                        cutPosL = self.glyphSize - 1
                    if cutPosR > self.glyphSize - 1:
                        cutPosR = self.glyphSize - 1
                    self.cuts[row][col] = (cutPosL, cutPosR)
                glyphCount += 1
        return self.cuts
    
    def processCuts(self):
        # Safety protection
        if not self.template:
            return self.defaultProcessing()
        self.templateLeftover = Path(self.template).read_text(encoding='UTF-8')
        self.checkTemplateStrings()
        advancedFormat = self.checkAdvancedFormat()
        if advancedFormat:
            colDeepest = self.getDeepestItem("startcol", self.templateLeftover) > self.getDeepestItem("startrow", self.templateLeftover)
            if colDeepest and advancedFormat:
                templateColumn = self.getSectionTemplate("col", self.templateLeftover)
                templateRow = self.getSectionTemplate("row", self.templateLeftover)
            else:
                templateRow = self.getSectionTemplate("row", self.templateLeftover)
                templateColumn = self.getSectionTemplate("col", self.templateLeftover)
        processedColumn = ""
        processedRow = ""
        processedTemplate = ""
        if not advancedFormat:
            for row in range(len(self.cuts)):
                if self.cuts[row] is None:
                    break
                for col in range(len(self.cuts[row])):
                    if self.cuts[row][col] is None:
                        break
                    cuts = self.cuts[row][col]
                    processedTemplate += self.parseTemplate("row", self.templateLeftover, row)
                    processedTemplate += self.parseTemplate("col", self.templateLeftover, col)
                    processedTemplate += self.parseTemplate("leftcut", self.templateLeftover, cuts[0])
                    processedTemplate += self.parseTemplate("rightcut", self.templateLeftover, cuts[1])
        elif colDeepest:
            for row in range(len(self.cuts)):
                processedColumn = ""
                if self.cuts[row] is None:
                    break
                for col in range(len(self.cuts[row])):
                    if self.cuts[row][col] is None:
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
                if self.cuts[row] is None or self.cuts[row][col] is None:
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
            if search in ["replacerow", "replacecol"]:
                templateString = regex.sub(r"\s*\$" + search, replace, templateString)
            else:
                templateString = regex.sub(r"\$" + search, replace, templateString)
            return templateString
        for _ in range(len(regExList)):
            stringEval = regex.search(regExSearch,templateString)
            if not stringEval:
                return templateString
            stringEval = stringEval.group()
            stringEval = regex.sub(r"\$" + search, replace, stringEval)
            stringEval = str(eval(stringEval))
            templateString = regex.sub(regExSearch, stringEval, templateString, 1)
        return templateString
    
    def getSectionTemplate(self, search, templateString):
        # sourcery skip: raise-specific-error
        regExBase = r"(\$startSection)([\s\S]*)(\$endsection)"
        regExStart = r"\s*\$startSection"
        regExStart = regExStart.replace("Section", search)
        regExEnd = r"\s*\$endSection"
        regExEnd = regExEnd.replace("Section", search)
        regExSearch = regExBase.replace("Section", search)
        regExList = regex.findall(regExSearch, templateString)
        if len(regExList) > 1:
            raise Exception(f"Only one ${search} section allowed!")
        if len(regExList) == 0:
            return False
        templateSection = regex.search(regExSearch, templateString).group()
        templateSection = regex.sub(regExStart, "", templateSection, 1)
        templateSection = regex.sub(regExEnd, "", templateSection, 1)
        self.templateLeftover = regex.sub(
            regExSearch, f"$replace{search}", templateString
        )
        return templateSection
    
    def processTemplate(self, search, template, replace, cuts):
        template = self.parseTemplate(search, template, replace)
        template = self.parseTemplate("leftcut", template, cuts[0])
        template = self.parseTemplate("rightcut", template, cuts[1])
        return template
    
    def checkIfExist(self, search, template):
        regExList = regex.findall(r"\$" + search, template)
        return bool(len(regExList))
    
    def getDeepestItem(self, search, template):
        return regex.search(r"\$"+ search, template).span()[1]
    
    def checkTemplateStrings(self):  # sourcery skip: raise-specific-error
        missing = ""
        missingCount = 0
        print("checking template strings")
        if not self.checkIfExist("row", self.templateLeftover):
            missing += "$row"
            missingCount += 1
        if not self.checkIfExist("col", self.templateLeftover):
            missing += " $col"
            missingCount += 1
        if not self.checkIfExist("leftcut", self.templateLeftover):
            missing += " $leftcut"
            missingCount += 1
        if not self.checkIfExist("rightcut", self.templateLeftover):
            missing += " $rightcut"
            missingCount += 1
        if missingCount == 4:
            raise Exception(f"Template has no replaceable strings, verify one of {missing} are present.")
        elif missingCount:
            print(f"The following items are missing in the template, output may not be as expected: {missing}.")
    def checkAdvancedFormat(self):  # sourcery skip: raise-specific-error
        missing = ""
        missingCount = 0
        if not self.checkIfExist("startcol", self.templateLeftover):
            missing += "$startcol"
            missingCount += 1
        if not self.checkIfExist("startrow", self.templateLeftover):
            missing += " $startrow"
            missingCount += 1
        if not self.checkIfExist("endcol", self.templateLeftover):
            missing +=  " $endcol"
            missingCount += 1
        if not self.checkIfExist("endrow", self.templateLeftover):
            missing += " $endrow"
            missingCount += 1
        if missingCount == 0:
            return True
        elif missingCount == 4:
            return False
        else:
            raise Exception(
                f"Not all criteria of advanced formatting are met. The following are missing: {missing}."
            )
    def defaultProcessing(self):
        processed = ""
        #Default processing if we don't have a template
        for row in range(len(self.cuts)):
            if self.cuts[row] is None:
                return processed
            for col in range(len(self.cuts[row])):
                if self.cuts[row][col] is None:
                    return processed
                processed += "(%s,%s)," % self.cuts[row][col]
            processed += "\n"
        return processed